"""fg_wait: frozen baseline and judgement for the fg-wait-guard hook experiment (~/.claude/CLAUDE.md §11).

The hook (agent-playbooks tools/hooks/fg-wait-guard.sh) denies foreground Bash calls whose first statement is an
until/while loop containing `sleep`, with timeout >= 300000. Its log records decisions, not outcomes, so the
experiment is judged from transcripts by harness-audit:

  A    foreground Bash calls that ran >= 300 s, per 1,000 Bash calls          (success: down >= 50 % in both strata)
  B    foreground Bash call-hours on calls >= 120 s (absolute and per 1,000)  (reported, not judged)
  WA   workaround detector, foreground forms per 1,000 Bash calls             (must stay flat)
  NULL zsh `=` expansion failures per 1,000 Bash calls                        (must stay flat; the hook cannot touch it)

Strata: arrows-game and geoguesser-app (the projects with the cap hits); `all` is reported beside them.
The rule below is pre-registered in the frozen baseline file; judge() reads it from there, not from this module.

python3 stdlib only.
"""
import collections
import datetime as dt
import hashlib
import json
import math
import os
import time

STRATA = ('arrows-game', 'geoguesser-app')
SCOPES = STRATA + ('all',)
WA_KEYS = ('wa:py-sleep', 'wa:node-sleep', 'wa:read-t', 'wa:timeout-tail', 'wa:wait-script', 'wa:bg-wait-timeout')
GAP_KEYS = ('gap:for', 'gap:cd')
NULL_CLASS = 'shell:zsh-equals-expansion'
SCHEMA = 'fg-wait-baseline/1'

RULE = {
    'id': 'FG-WAIT-R1',
    'registered': '2026-10-07',
    'success': ('A per 1,000 Bash calls is down >= 50 % vs the baseline in BOTH strata, and in each stratum the post '
                'count is below the 5th percentile of Poisson(baseline rate x post Bash calls), i.e. the drop beats '
                'count noise'),
    'workaround_flat': ('in each stratum the post workaround count (sum of WA_KEYS) is at or below the 95th percentile '
                        'of Poisson(baseline rate x post Bash calls); above it in either stratum = ROSE'),
    'null_flat': ('in each stratum the post zsh `=` failure count lies inside the central 95 % Poisson interval of '
                  'baseline rate x post Bash calls; outside it in either stratum = the population moved'),
    'min_post_bash_calls': 1000,
    'verdicts': {
        'INSUFFICIENT': 'a stratum has fewer than min_post_bash_calls post Bash calls, or a zero baseline A count',
        'REMOVE-HOOK': 'the workaround detector ROSE (§11: remove the hook if workarounds rise)',
        'INCONCLUSIVE': 'the null moved, so a change in A cannot be attributed to the hook',
        'SUCCESS': 'success condition met, workarounds flat, null flat',
        'NO-EFFECT': 'anything else',
    },
    'not_judged': 'B (call-hours) and gap forms (for loops, cd && prefixes) are reported only; they are legal by design',
}


# ------------------------------------------------------------------ Poisson helpers (exact, log-space)
def _pmf_terms(lam):
    k = 0
    while True:
        if lam == 0:
            yield k, (1.0 if k == 0 else 0.0)
        else:
            yield k, math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))
        k += 1


def poisson_quantile(lam, q):
    """Smallest k with P(X <= k) >= q."""
    c = 0.0
    for k, p in _pmf_terms(lam):
        c += p
        if c >= q - 1e-12:
            return k
        if k > 10 * lam + 100:
            return k


# ------------------------------------------------------------------ metrics
def parse_local(s):
    """'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM[:SS][+HH:MM]' -> epoch seconds; naive values are local time."""
    if 'T' not in s:
        s += 'T00:00'
    d = dt.datetime.fromisoformat(s)
    if d.tzinfo is None:
        d = d.astimezone()  # attach the host's local offset
    return d.timestamp()


def iso_local(t):
    return dt.datetime.fromtimestamp(t).astimezone().isoformat(timespec='minutes')


def bash_rows(digests_by_proj, since, until):
    """{scope: [Bash call dicts]} for calls that STARTED in [since, until)."""
    out = collections.defaultdict(list)
    for proj, calls in digests_by_proj:
        for c in calls:
            if c.get('tool') != 'Bash' or not (since <= c['t'] < until):
                continue
            out['all'].append(c)
            if proj in STRATA:
                out[proj].append(c)
    return out


def metrics(rows):
    n = len(rows)
    fg = [c for c in rows if not c.get('bg')]
    per = lambda k: round(1000.0 * k / n, 3) if n else None
    a = sum(1 for c in fg if c['d'] >= 300)
    b_s = sum(c['d'] for c in fg if c['d'] >= 120)
    null = sum(1 for c in rows if c.get('ec') == NULL_CLASS)
    wa = collections.Counter()
    gaps = collections.Counter()
    would_deny = 0
    for c in fg:
        feat = c.get('feat') or []
        for k in feat:
            if k.startswith('wa:'):
                wa[k] += 1
            elif k.startswith('gap:'):
                gaps[k] += 1
        if 'hook-loop' in feat and (c.get('tmo') or 0) >= 300000:
            would_deny += 1
    for c in rows:
        if c.get('bg') and str(c.get('cat', '')).startswith('wait-loop') and c.get('bgs') in ('failed', 'killed'):
            wa['wa:bg-wait-timeout'] += 1
    wa_total = sum(wa.values())
    return dict(
        bash_calls=n, fg_bash_calls=len(fg),
        A_fg_ge300_count=a, A_per_1000=per(a),
        B_fg_ge120_hours=round(b_s / 3600.0, 2), B_hours_per_1000=(round(1000.0 * b_s / 3600.0 / n, 3) if n else None),
        null_zsh_equals_count=null, null_per_1000=per(null),
        workaround=dict(total=wa_total, per_1000=per(wa_total), by_form={k: wa.get(k, 0) for k in WA_KEYS}),
        gap_forms_not_judged={k: gaps.get(k, 0) for k in GAP_KEYS},
        hook_predicate_would_deny=would_deny,
    )


def compute(audit, since, until):
    pairs = [(d['project'], d['calls']) for d in audit.D]
    rows = bash_rows(pairs, since, until)
    return {s: metrics(rows.get(s, [])) for s in SCOPES}


def _digest(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]


def freeze(audit, since, until, json_path, md_path, parser_version, force=False, reason=None):
    if not force and (os.path.exists(json_path) or os.path.exists(md_path)):
        raise SystemExit('refusing to overwrite a frozen baseline: %s (pass --force only to rebuild it on purpose)' % json_path)
    m = compute(audit, since, until)
    doc = dict(schema=SCHEMA, frozen_at=iso_local(time.time()), parser=parser_version,
               window=dict(since=iso_local(since), until=iso_local(until), basis='call start time, local host clock'),
               scopes=list(SCOPES), rule=RULE, metrics=m, rebuild_reason=reason if force else None)
    doc['metrics_sha'] = _digest(m)
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w') as fh:
        json.dump(doc, fh, indent=1)
    with open(md_path, 'w') as fh:
        fh.write(render_baseline_md(doc))
    return doc


def render_baseline_md(doc):
    m = doc['metrics']
    L = ['# fg-wait-guard baseline (frozen %s)\n' % doc['frozen_at'],
         'Window %s .. %s (%s). Parser `%s`. Metrics sha `%s`. Written by `harness-audit --fg-wait-baseline`; '
         'do not edit, rebuild only with `--force` and a recorded reason.\n' % (doc['window']['since'], doc['window']['until'], doc['window']['basis'], doc['parser'], doc['metrics_sha']),
         ('Rebuilt with --force: %s\n' % doc['rebuild_reason']) if doc.get('rebuild_reason') else '',
         '| metric | ' + ' | '.join(SCOPES) + ' |', '|---|' + '---|' * len(SCOPES)]
    rows = [
        ('Bash calls (denominator)', 'bash_calls'), ('foreground Bash calls', 'fg_bash_calls'),
        ('A: foreground calls >= 300 s', 'A_fg_ge300_count'), ('A per 1,000 Bash calls', 'A_per_1000'),
        ('B: foreground call-hours on calls >= 120 s', 'B_fg_ge120_hours'), ('B hours per 1,000 Bash calls', 'B_hours_per_1000'),
        ('NULL: zsh `=` failures', 'null_zsh_equals_count'), ('NULL per 1,000', 'null_per_1000'),
        ('WA: workaround forms (total)', ('workaround', 'total')), ('WA per 1,000', ('workaround', 'per_1000')),
    ] + [('WA %s' % k, ('workaround', 'by_form', k)) for k in WA_KEYS] + [
        ('gap form %s (not judged)' % k, ('gap_forms_not_judged', k)) for k in GAP_KEYS] + [
        ('calls the hook predicate would deny', 'hook_predicate_would_deny')]
    for name, key in rows:
        vals = []
        for s in SCOPES:
            v = m[s]
            for part in (key if isinstance(key, tuple) else (key,)):
                v = v[part]
            vals.append(str(v))
        L.append('| %s | %s |' % (name, ' | '.join(vals)))
    L.append('\nReconciliation: A <= foreground calls <= Bash calls in every column; `all` >= the sum of the two strata.')
    L.append('\nWorkaround forms (foreground only, except the last): inline python sleeps (`python -c`/heredoc with `sleep(`), '
             'inline node/bun/deno `setTimeout`/`setInterval`/`sleep(`, `read -t N`, `timeout N tail -f`, scripts or tools named '
             '`*wait*` (`wait-for-it`, `wait-on`, `wait_ready.py`), and background wait loops whose task ended `failed` or `killed` '
             '(the digest has no exit code, so this is the proxy for "ended by its timeout").')
    L.append('\n## Pre-registered rule %s (registered %s)\n' % (doc['rule']['id'], doc['rule']['registered']))
    for k in ('success', 'workaround_flat', 'null_flat', 'not_judged'):
        L.append('- **%s:** %s' % (k, doc['rule'][k]))
    L.append('- **min post Bash calls per stratum:** %d' % doc['rule']['min_post_bash_calls'])
    for k, v in doc['rule']['verdicts'].items():
        L.append('- **%s:** %s' % (k, v))
    L.append('\nJudge: `harness-audit --judge-fg-wait` (post window = baseline end .. now, same parser features).')
    return '\n'.join(L) + '\n'


def judge(base_doc, post):
    """Apply the frozen rule to post metrics {scope: metrics}. Returns (verdict, details)."""
    rule = base_doc['rule']
    base = base_doc['metrics']
    det = {}
    insufficient = rose = moved = False
    success = True
    for s in STRATA:
        b, p = base[s], post[s]
        n = p['bash_calls']
        d = dict(post_bash_calls=n)
        if n < rule['min_post_bash_calls'] or not b['bash_calls'] or not b['A_fg_ge300_count']:
            insufficient = True
            d['status'] = 'INSUFFICIENT'
            det[s] = d
            continue
        scale = float(n) / b['bash_calls']
        expA = b['A_fg_ge300_count'] * scale
        dropA = 1 - (p['A_fg_ge300_count'] / float(n)) / (b['A_fg_ge300_count'] / float(b['bash_calls']))
        lowA = poisson_quantile(expA, 0.05)
        d['A'] = dict(base_per_1000=b['A_per_1000'], post_per_1000=p['A_per_1000'], drop=round(dropA, 3),
                      expected_if_unchanged=round(expA, 1), post_count=p['A_fg_ge300_count'], noise_p05=lowA,
                      down_50=dropA >= 0.5, beats_noise=p['A_fg_ge300_count'] < lowA)
        success = success and d['A']['down_50'] and d['A']['beats_noise']
        expW = b['workaround']['total'] * scale
        hiW = poisson_quantile(expW, 0.95)
        d['WA'] = dict(base_per_1000=b['workaround']['per_1000'], post_per_1000=p['workaround']['per_1000'],
                       expected=round(expW, 1), post_count=p['workaround']['total'], p95=hiW, rose=p['workaround']['total'] > hiW)
        rose = rose or d['WA']['rose']
        expN = b['null_zsh_equals_count'] * scale
        lo, hi = poisson_quantile(expN, 0.025), poisson_quantile(expN, 0.975)
        d['NULL'] = dict(base_per_1000=b['null_per_1000'], post_per_1000=p['null_per_1000'], expected=round(expN, 1),
                         post_count=p['null_zsh_equals_count'], interval95=[lo, hi],
                         flat=lo <= p['null_zsh_equals_count'] <= hi)
        moved = moved or not d['NULL']['flat']
        det[s] = d
    if insufficient:
        v = 'INSUFFICIENT'
    elif rose:
        v = 'REMOVE-HOOK'
    elif moved:
        v = 'INCONCLUSIVE'
    elif success:
        v = 'SUCCESS'
    else:
        v = 'NO-EFFECT'
    return v, det
