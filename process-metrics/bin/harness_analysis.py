"""harness_analysis: aggregate harness_core digests into reliability, loop, tool-choice, skill and
condition tables, plus §10 ledger lines. python3 stdlib only. Never sees raw transcript text."""
import collections
import json
import math
import os
import re
import statistics
import time

import harness_core as H

GAP_CAP = 600.0          # reaction gap after a failure counts at most 10 min (longer = dormant/owner)
LOOP_WINDOW = 1800.0     # near-identical calls more than 30 min apart start a new cluster
LONG_CATS = ('build:', 'test:jest', 'test:vitest', 'test:e2e', 'test:pytest', 'wait-loop:', 'emulator:', 'adb:install', 'capture-harness')
EDIT_TOOLS = ('Edit', 'MultiEdit', 'Write', 'NotebookEdit')
OWNER_TIME_CLASSES = ('permission:user-rejected',)


def pct(xs, p):
    if not xs:
        return None
    xs = sorted(xs)
    k = (len(xs) - 1) * p
    f = int(k)
    c = min(f + 1, len(xs) - 1)
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - r) / d), min(1.0, (c + r) / d))


def mh_or(strata):
    """Mantel-Haenszel pooled odds ratio with Robins-Breslow-Greenland 95% CI.
    strata: list of (a, b, c, d) = (failA, okA, failB, okB)."""
    R = S = P_R = PS_QR = Q_S = 0.0
    for a, b, c, d in strata:
        n = a + b + c + d
        if n == 0:
            continue
        r = a * d / n
        s = b * c / n
        p = (a + d) / n
        q = (b + c) / n
        R += r
        S += s
        P_R += p * r
        PS_QR += p * s + q * r
        Q_S += q * s
    if R == 0 or S == 0:
        return None, None, None
    orr = R / S
    var = P_R / (2 * R * R) + PS_QR / (2 * R * S) + Q_S / (2 * S * S)
    se = math.sqrt(var)
    return orr, math.exp(math.log(orr) - 1.96 * se), math.exp(math.log(orr) + 1.96 * se)


def fmt_h(s):
    return '%.1f' % (s / 3600.0)


def fdate(t):
    return time.strftime('%Y-%m-%d', time.localtime(t)) if t else '?'


def is_fail(c):
    return bool(c.get('err') or c.get('to'))


# ------------------------------------------------------------------ main aggregation
class Audit:
    def __init__(self, digests, now=None):
        self.raw = [d for d in digests if d.get('first')]
        self.D, self.dedup = dedupe(self.raw)
        self.now = now or time.time()
        self.calls = []        # (digest_idx, call)
        for i, d in enumerate(self.D):
            for c in d['calls']:
                self.calls.append((i, c))
        self._host_load_reclass()
        self._concurrency()

    # timeouts that later pass on rerun of the same skeleton in the same agent -> host load
    def _host_load_reclass(self):
        n = 0
        for d in self.D:
            seen_ok = collections.defaultdict(list)
            for c in d['calls']:
                if not is_fail(c) and c.get('sk'):
                    seen_ok[c['sk']].append(c['t'])
            for c in d['calls']:
                if c.get('ec') == 'timeout:command' and c.get('sk'):
                    if any(t > c['t'] for t in seen_ok.get(c['sk'], [])):
                        c['ec'] = 'timeout:host-load-passed-on-rerun'
                        n += 1
        self.host_reclass = n

    def _concurrency(self):
        mp = collections.defaultdict(set)
        ma = collections.Counter()
        for i, d in enumerate(self.D):
            for m in d['minutes']:
                mp[m].add(d['project'])
                ma[m] += 1
        self.min_proj = mp
        self.min_agents = ma

    # ---------------------------------------------------------- reconciliation
    def reconciliation(self):
        D = self.D
        RAW = self.raw
        uses = sum(d['n_uses'] for d in RAW)
        results = sum(d['n_results'] for d in RAW)
        paired_raw = sum(len(d['calls']) for d in RAW)
        paired = len(self.calls)
        orphan = sum(d['orphan_uses'] for d in RAW)
        errs = sum(1 for _, c in self.calls if c.get('err'))
        tos = sum(1 for _, c in self.calls if c.get('to') and not c.get('err'))
        fails = errs + tos
        cls = collections.Counter(c.get('ec') for _, c in self.calls if is_fail(c))
        other = cls.get('other', 0)
        other_nz = cls.get('other:nonzero-exit', 0)
        return dict(files=len(D), main=sum(1 for d in D if d['kind'] == 'main'), sub=sum(1 for d in D if d['kind'] == 'sub'),
                    lines=sum(d['n_lines'] for d in D), bad_lines=sum(d['n_bad'] for d in D),
                    tool_use_blocks=uses, tool_results=results, paired_calls=paired, orphan_uses=orphan,
                    results_without_use=results - paired_raw, paired_raw=paired_raw, dedup=self.dedup, raw_files=len(RAW), errors=errs, timeouts_not_error=tos, failures=fails,
                    classified=fails - other - other_nz, other=other, other_nonzero=other_nz,
                    other_share=(other + other_nz) / fails if fails else 0,
                    first=min(d['first'] for d in D) if D else None, last=max(d['last'] for d in D) if D else None,
                    agent_wall_h=sum(d['wall'] for d in D) / 3600, host_reclass=self.host_reclass)

    # ---------------------------------------------------------- per-tool table
    def tool_table(self, key=lambda d, c: c['tn']):
        g = collections.defaultdict(list)
        for i, c in self.calls:
            g[key(self.D[i], c)].append(c)
        rows = []
        for k, cs in g.items():
            fg = [c['d'] for c in cs if not c.get('bg')]
            fgw = [c['d'] for c in cs if not c.get('bg') and c['tool'] != 'AskUserQuestion']
            rows.append(dict(key=k, n=len(cs), err=sum(c['err'] for c in cs), fail=sum(1 for c in cs if is_fail(c)),
                             med=pct(fg, .5), p90=pct(fg, .9), hours=sum(fgw) / 3600))
        rows.sort(key=lambda r: -r['n'])
        return rows

    # ---------------------------------------------------------- error classes
    def error_classes(self):
        g = collections.defaultdict(list)
        for i, c in self.calls:
            if is_fail(c):
                g[c.get('ec') or 'other'].append((i, c))
        rows = []
        for k, lst in g.items():
            # owner decision time is not agent time: a rejected permission prompt waits on the owner
            call_s = 0.0 if k in OWNER_TIME_CLASSES else sum(c['d'] for _, c in lst if not c.get('bg'))
            owner_s = sum(c['d'] for _, c in lst) if k in OWNER_TIME_CLASSES else 0.0
            gap_s = sum(min(c['gap'], GAP_CAP) for _, c in lst if c.get('gap') is not None)
            projs = collections.Counter(self.D[i]['project'] for i, _ in lst)
            snips = collections.Counter(re.sub(r'\d+', 'N', c.get('es', ''))[:120] for _, c in lst if c.get('es'))
            tools = collections.Counter(c['tn'] for _, c in lst)
            rows.append(dict(cls=k, bucket=H.CLASS_BUCKET.get(k, 'BEHAVIOUR'), n=len(lst), call_h=call_s / 3600, lost_h=(call_s + gap_s) / 3600,
                             projects=projs.most_common(3), tools=tools.most_common(3), example=(snips.most_common(1)[0][0] if snips else ''),
                             sigs=snips.most_common(6), owner_h=owner_s / 3600))
        rows.sort(key=lambda r: -r['lost_h'])
        return rows

    # ---------------------------------------------------------- loops and double work
    def loops(self):
        out = {}
        D = self.D
        # 1. identical-skeleton retry loops with >=2 failures
        ex = []
        for i, d in enumerate(D):
            grp = collections.defaultdict(list)
            for c in d['calls']:
                if c.get('sk') and c['tool'] not in ('Read', 'TaskOutput', 'BashOutput', 'Monitor') and not c['cat'].startswith('wait-loop'):
                    grp[c['sk']].append(c)
            for sk, cs in grp.items():
                cl = [cs[0]]
                for c in cs[1:] + [None]:
                    if c is not None and c['t'] - (cl[-1]['t'] + cl[-1]['d']) <= LOOP_WINDOW:
                        cl.append(c)
                        continue
                    nf = sum(1 for x in cl if is_fail(x))
                    if len(cl) >= 3 and is_fail(cl[0]) and nf >= 2:
                        last_ok = not is_fail(cl[-1])
                        ex.append(dict(i=i, n=len(cl), nf=nf, lo=sum(x['d'] for x in cl[1:]), hi=(cl[-1]['t'] + cl[-1]['d'] - cl[0]['t']),
                                       tool=cl[0]['tn'], head=cl[0].get('head', ''), ec=cl[0].get('ec'), t=cl[0]['t'],
                                       ended=('succeeded on attempt %d' % len(cl)) if last_ok else 'still failing; approach abandoned or changed'))
                    if c is not None:
                        cl = [c]
        out['retry_loops'] = ex
        # 2. consecutive failure streaks of one tool (any input), >=3
        st = []
        for i, d in enumerate(D):
            run = []
            for c in d['calls'] + [None]:
                if c is not None and is_fail(c) and (not run or run[-1]['tn'] == c['tn']):
                    run.append(c)
                    continue
                if len(run) >= 3:
                    nxt = c
                    st.append(dict(i=i, n=len(run), tool=run[0]['tn'], t=run[0]['t'], span=run[-1]['t'] + run[-1]['d'] - run[0]['t'],
                                   lo=sum(x['d'] for x in run), ecs=collections.Counter(x.get('ec') for x in run).most_common(2),
                                   ended=('next call of same tool succeeded' if nxt is not None and nxt['tn'] == run[0]['tn'] else 'switched tool/approach' if nxt is not None else 'agent ended')))
                run = [c] if (c is not None and is_fail(c)) else []
        out['fail_streaks'] = st
        # 3. edit-fail-re-edit cycles per file
        cyc = []
        for i, d in enumerate(D):
            byf = collections.defaultdict(list)
            for c in d['calls']:
                if c['tool'] in EDIT_TOOLS and c.get('fh'):
                    byf[c['fh']].append(c)
            for fh, cs in byf.items():
                fails = [c for c in cs if c.get('err')]
                if not fails:
                    continue
                rec = 0.0
                for f in fails:
                    nxt = next((c for c in cs if c['t'] > f['t'] and not c.get('err')), None)
                    if nxt:
                        rec += nxt['t'] - (f['t'] + f['d'])
                cyc.append(dict(i=i, fails=len(fails), edits=len(cs), rec=rec, t=fails[0]['t'], ecs=collections.Counter(c.get('ec') for c in fails).most_common(2)))
        out['edit_cycles'] = cyc
        # 4. duplicate dispatch (near-identical Agent prompts)
        out['dups'] = self._dups()
        # 5/6. builds of an unchanged tree, repeated full test runs with no change
        rb, rt = [], []
        for i, d in enumerate(D):
            bgdur = {round(b['t'], 3): b.get('dur') for b in d.get('bg', [])}
            last_b, last_t = {}, {}
            for c in d['calls']:
                if (c['tool'] in EDIT_TOOLS and not c.get('err')) or ('mutate' in (c.get('feat') or [])):
                    last_b.clear()
                    last_t.clear()
                    continue
                cat = c['cat']
                dur = bgdur.get(round(c['t'], 3)) if c.get('bg') else c['d']
                dur = dur or 0.0
                if c.get('head', '').split(' ')[0] in ('until', 'while', 'for', 'sleep', 'tail', 'cat', 'ls', 'grep'):
                    continue
                if cat.startswith('build:') and cat != 'build:prebuild':
                    k = c.get('sk')
                    if k in last_b:
                        rb.append(dict(i=i, t=c['t'], dur=dur, prev_fail=last_b[k], head=c.get('head', ''), cat=cat))
                    last_b[k] = is_fail(c)
                elif cat.startswith('test:') and 'fulltest' in (c.get('feat') or []):
                    k = c.get('sk')
                    if k in last_t:
                        rt.append(dict(i=i, t=c['t'], dur=dur, prev_fail=last_t[k], head=c.get('head', ''), cat=cat))
                    last_t[k] = is_fail(c)
        out['rebuilds'] = rb
        out['retests'] = rt
        # 7. waits that end in timeout
        wt = []
        for i, d in enumerate(D):
            for c in d['calls']:
                if (c['cat'].startswith('wait-loop') or c['tool'] in ('Monitor', 'TaskOutput', 'BashOutput')) and (c.get('to') or (c.get('ec') or '').startswith('timeout')):
                    wt.append(dict(i=i, t=c['t'], dur=c['d'], tool=c['tn'], cat=c['cat'], head=c.get('head', '')))
            for b in d.get('bg', []):
                if b['cat'].startswith('wait-loop') and b.get('status') in ('killed', 'failed', 'timeout', 'timed_out'):
                    wt.append(dict(i=i, t=b['t'], dur=b.get('dur') or 0, tool='Bash(bg)', cat=b['cat'], head=b.get('head', ''), bg=1))
        out['wait_timeouts'] = wt
        out['sleep_blocked'] = [dict(i=i, t=c['t']) for i, c in self.calls if c.get('ec') == 'wait:sleep-blocked']
        # 8. agents parked waiting on the coordinator
        pk = []
        for i, d in enumerate(D):
            if d['kind'] != 'sub':
                continue
            co = d['excl'].get('dormant:resume-coordinator', 0)
            bgw = d['excl'].get('dormant:resume-bg-notification', 0)
            if co or bgw:
                pk.append(dict(i=i, coord=co, bgwake=bgw))
        out['parked'] = pk
        # 9. manual polling: >=5 identical successful calls within a 30-min window
        pl = []
        for i, d in enumerate(D):
            grp = collections.defaultdict(list)
            for c in d['calls']:
                if c['tool'] == 'Bash' and not is_fail(c) and not c.get('bg') and c.get('fp'):
                    grp[c['fp']].append(c)
            for fp, cs in grp.items():
                cl = [cs[0]]
                for c in cs[1:] + [None]:
                    if c is not None and c['t'] - cl[-1]['t'] <= LOOP_WINDOW:
                        cl.append(c)
                        continue
                    if len(cl) >= 5:
                        pl.append(dict(i=i, n=len(cl), lo=sum(x['d'] for x in cl), hi=cl[-1]['t'] + cl[-1]['d'] - cl[0]['t'], head=cl[0].get('head', ''), cat=cl[0]['cat'], t=cl[0]['t']))
                    if c is not None:
                        cl = [c]
        out['polls'] = pl
        return out

    def _dups(self):
        by_tid = {d.get('tool_use_id'): d for d in self.D if d['kind'] == 'sub' and d.get('tool_use_id')}
        byproj = collections.defaultdict(list)
        for i, d in enumerate(self.D):
            for x in d.get('dispatches', []):
                byproj[d['project']].append((i, x))
        pairs = []
        for proj, lst in byproj.items():
            lst.sort(key=lambda z: z[1]['t'])
            sets = [set(x['sk']) for _, x in lst]
            for b in range(len(lst)):
                ib, xb = lst[b]
                for a in range(b):
                    ia, xa = lst[a]
                    if xa['plen'] and xb['plen'] and min(xa['plen'], xb['plen']) / max(xa['plen'], xb['plen']) < 0.7:
                        continue
                    sa, sb = sets[a], sets[b]
                    if not sa or not sb:
                        continue
                    k = 128
                    union = sorted(sa | sb)[:k]
                    j = sum(1 for v in union if v in sa and v in sb) / len(union)
                    if j < 0.8:
                        continue
                    da, db = by_tid.get(xa['id']), by_tid.get(xb['id'])
                    a_done = None if da is None else bool(da['last'] < xb['t'])
                    b_active = ((db['wall'] - sum(v for kk, v in db['excl'].items() if kk.startswith('dormant:'))) if db else 0)
                    pairs.append(dict(project=proj, j=j, same_prompt=xa['ph'] == xb['ph'], fx=xb.get('fx', 0), same_desc=xa['dh'] == xb['dh'] and bool(xa['desc']),
                                      a_done=a_done, a_err=xa['err'], a_outcome=(da or {}).get('outcome'), b_active=b_active,
                                      gap=xb['t'] - xa['t'], t=xb['t'], desc_a=xa['desc'], desc_b=xb['desc'], sess_same=self.D[ia]['session'] == self.D[ib]['session']))
        # keep only the best earlier match per later dispatch
        best = {}
        for p in pairs:
            k = (p['project'], p['t'])
            if k not in best or p['j'] > best[k]['j']:
                best[k] = p
        return list(best.values())

    # ---------------------------------------------------------- tool-choice comparisons
    def comparisons(self):
        def arm_rows(name, A, B, failfn=is_fail, note=''):
            # A, B: predicates on (d, c) -> bool
            ga = collections.defaultdict(lambda: [0, 0])
            gb = collections.defaultdict(lambda: [0, 0])
            ta = [0, 0]
            tb = [0, 0]
            for i, c in self.calls:
                d = self.D[i]
                if A(d, c):
                    f = failfn(c)
                    ga[i][0 if f else 1] += 1
                    ta[0 if f else 1] += 1
                elif B(d, c):
                    f = failfn(c)
                    gb[i][0 if f else 1] += 1
                    tb[0 if f else 1] += 1
            strata = [(ga[i][0], ga[i][1], gb[i][0], gb[i][1]) for i in set(ga) & set(gb)]
            orr, lo, hi = mh_or(strata)
            na, nb = sum(ta), sum(tb)
            wa = sum(a + b for a, b, _, _ in strata)
            wb = sum(c + d for _, _, c, d in strata)
            wfa = sum(a for a, _, _, _ in strata)
            wfb = sum(c for _, _, c, _ in strata)
            if na == 0 or nb == 0:
                verdict = 'arm %s never used (tool not exposed in these sessions?): no comparison possible' % ('A' if na == 0 else 'B')
            elif min(na, nb) < 30 or len(strata) < 5:
                verdict = 'small n: cannot separate from task mix'
            elif lo is None:
                verdict = 'no failures in one arm within shared agents: cannot estimate'
            elif hi < 1:
                verdict = 'A lower, holds within agent'
            elif lo > 1:
                verdict = 'A higher, holds within agent'
            else:
                verdict = 'no within-agent difference (raw gap is task mix)'
            return dict(name=name, na=na, fa=ta[0], nb=nb, fb=tb[0], ra=ta[0] / na if na else None, rb=tb[0] / nb if nb else None,
                        cia=wilson(ta[0], na), cib=wilson(tb[0], nb), strata=len(strata), wa=wa, wfa=wfa, wb=wb, wfb=wfb,
                        orr=orr, lo=lo, hi=hi, verdict=verdict, note=note)

        F = lambda c, f: f in (c.get('feat') or [])
        not_benign = lambda c: is_fail(c) and c.get('ec') != 'nonzero:benign-no-match'
        rows = [
            arm_rows('Read tool (A) vs Bash cat/head/tail/sed -n (B)', lambda d, c: c['tool'] == 'Read', lambda d, c: c['tool'] == 'Bash' and F(c, 'read-cmd')),
            arm_rows('Edit tool (A) vs sed -i / perl -i / script rewrite (B)', lambda d, c: c['tool'] in ('Edit', 'MultiEdit'), lambda d, c: c['tool'] == 'Bash' and F(c, 'shell-edit'),
                     note='sed -i exits 0 when nothing matched, so B under-reports silent misses'),
            arm_rows('Grep tool (A) vs Bash grep/rg (B), benign exit-1 excluded', lambda d, c: c['tool'] == 'Grep', lambda d, c: c['tool'] == 'Bash' and F(c, 'grep-cmd'), failfn=not_benign),
            arm_rows('Grep tool (A) vs Bash grep/rg (B), any non-zero', lambda d, c: c['tool'] == 'Grep', lambda d, c: c['tool'] == 'Bash' and F(c, 'grep-cmd')),
            arm_rows('Glob tool (A) vs Bash find (B)', lambda d, c: c['tool'] == 'Glob', lambda d, c: c['tool'] == 'Bash' and F(c, 'find-cmd'), failfn=not_benign),
            arm_rows('Write tool (A) vs heredoc/tee write (B)', lambda d, c: c['tool'] == 'Write', lambda d, c: c['tool'] == 'Bash' and F(c, 'heredoc-write')),
            arm_rows('Long command in background (A) vs foreground (B): timeout or error', lambda d, c: c['tool'] == 'Bash' and c['cat'].startswith(LONG_CATS) and c.get('bg'),
                     lambda d, c: c['tool'] == 'Bash' and c['cat'].startswith(LONG_CATS) and not c.get('bg'),
                     note='A counts the launch only; a background job that later fails shows in its notification, not here'),
            arm_rows('Monitor tool (A) vs Bash until/while+sleep loop (B): timeout or error', lambda d, c: c['tool'] == 'Monitor',
                     lambda d, c: c['tool'] == 'Bash' and c['cat'].startswith('wait-loop') and not c.get('bg')),
            arm_rows('sh -c / bash script (A) vs plain zsh command (B)', lambda d, c: c['tool'] == 'Bash' and F(c, 'sh-c'), lambda d, c: c['tool'] == 'Bash' and not F(c, 'sh-c') and not c.get('bg'), failfn=not_benign),
            arm_rows('sh -c / bash script (A) vs plain zsh (B): zsh-class errors only', lambda d, c: c['tool'] == 'Bash' and F(c, 'sh-c'), lambda d, c: c['tool'] == 'Bash' and not F(c, 'sh-c') and not c.get('bg'),
                     failfn=lambda c: (c.get('ec') or '').startswith('shell:zsh')),
            arm_rows('Bash with absolute paths only (A) vs relative paths only (B)', lambda d, c: c['tool'] == 'Bash' and F(c, 'paths:abs'), lambda d, c: c['tool'] == 'Bash' and F(c, 'paths:rel'), failfn=not_benign),
            arm_rows('Bash absolute (A) vs relative (B): file-not-found only', lambda d, c: c['tool'] == 'Bash' and F(c, 'paths:abs'), lambda d, c: c['tool'] == 'Bash' and F(c, 'paths:rel'),
                     failfn=lambda c: c.get('ec') in ('file:not-found',)),
            arm_rows('Bash compound (multi-line or 3+ chained) (A) vs simple (B)', lambda d, c: c['tool'] == 'Bash' and F(c, 'compound'), lambda d, c: c['tool'] == 'Bash' and not F(c, 'compound') and not c.get('bg'), failfn=not_benign),
            arm_rows('Read with offset/limit (A) vs whole-file Read (B)', lambda d, c: c['tool'] == 'Read' and c.get('ranged'), lambda d, c: c['tool'] == 'Read' and not c.get('ranged')),
        ]
        return rows

    # ---------------------------------------------------------- skills
    def skills(self):
        D = self.D
        inv = []
        for i, d in enumerate(D):
            for s in d.get('skills', []):
                inv.append((i, s))
        rows = collections.defaultdict(lambda: dict(n=0, projects=collections.Counter(), ep=[]))
        for i, s in inv:
            d = D[i]
            # episode: until next owner prompt (main) or agent end (sub)
            end = d['last']
            if d['kind'] == 'main':
                nxt = [t for t in d.get('up_t', []) if t > s['t']]
                if nxt:
                    end = nxt[0]
            cs = [c for c in d['calls'] if s['t'] < c['t'] <= end]
            nf = sum(1 for c in cs if is_fail(c))
            ep = dict(i=i, wall=end - s['t'], calls=len(cs), fails=nf, edits=sum(1 for c in cs if c['tool'] in EDIT_TOOLS),
                      agents=sum(1 for c in cs if c['tool'] in ('Agent', 'Task')), tests=sum(1 for c in cs if c['cat'].startswith('test:')),
                      outcome=d.get('outcome'), contra=self._contradiction(s['skill'], cs))
            r = rows[s['skill']]
            r['n'] += 1
            r['projects'][d['project']] += 1
            r['ep'].append(ep)
        # baseline: episodes without any skill (main turns, sub agents)
        base = []
        for i, d in enumerate(D):
            if d.get('skills'):
                continue
            if d['kind'] == 'sub':
                base.append(dict(wall=d['wall'], calls=len(d['calls']), fails=sum(1 for c in d['calls'] if is_fail(c))))
        out = []
        for k, r in rows.items():
            eps = r['ep']
            walls = [e['wall'] for e in eps]
            out.append(dict(skill=k, n=r['n'], projects=r['projects'].most_common(3), med_wall_min=(pct(walls, .5) or 0) / 60,
                            med_calls=pct([e['calls'] for e in eps], .5), fail_rate=(sum(e['fails'] for e in eps) / max(1, sum(e['calls'] for e in eps))),
                            agents=sum(e['agents'] for e in eps), tests=sum(e['tests'] for e in eps), edits=sum(e['edits'] for e in eps),
                            contra=collections.Counter(c for e in eps for c in e['contra']),
                            outcomes=collections.Counter(e['outcome'] for e in eps if e['outcome'])))
        out.sort(key=lambda r: -r['n'])
        bfr = sum(b['fails'] for b in base) / max(1, sum(b['calls'] for b in base))
        user_cmds = collections.Counter(u['cmd'] for d in D for u in d.get('user_cmds', []))
        return out, dict(n=len(base), fail_rate=bfr, med_wall_min=(pct([b['wall'] for b in base], .5) or 0) / 60, med_calls=pct([b['calls'] for b in base], .5)), user_cmds

    @staticmethod
    def _contradiction(skill, cs):
        """Heuristics only. Returns a list of labels."""
        s = skill.lower()
        out = []
        code_edit = [c for c in cs if c['tool'] in EDIT_TOOLS and not c.get('err') and c.get('ext') in ('.ts', '.tsx', '.js', '.jsx', '.py', '.kt', '.swift', '.java', '.mjs', '.cjs', '.go', '.rs')]
        if 'test-driven' in s:
            impl = next((c for c in code_edit if not c.get('testfile')), None)
            test = next((c for c in code_edit if c.get('testfile')), None)
            if impl and (test is None or impl['t'] < test['t']):
                out.append('impl edited before any test file')
        if 'systematic-debugging' in s:
            run = next((c for c in cs if c['tool'] == 'Bash' and (c['cat'].startswith(('test:', 'analysis:', 'adb:', 'build:')))), None)
            early = [c for c in code_edit if run is None or c['t'] < run['t']]
            if len(early) >= 2:
                out.append('2+ code edits before any reproduce/run')
            loops = collections.Counter(c.get('sk') for c in cs if is_fail(c) and c.get('sk'))
            if any(v >= 3 for v in loops.values()):
                out.append('same failing call 3+ times after invoking')
        if 'verification-before-completion' in s:
            if not any(c['tool'] == 'Bash' and c['cat'].startswith(('test:', 'build:', 'analysis:', 'adb:', 'capture')) for c in cs):
                out.append('no verification command after invoking')
        if 'subagent-driven' in s or 'dispatching-parallel' in s:
            ag = [c for c in cs if c['tool'] in ('Agent', 'Task')]
            if not ag:
                out.append('no agent dispatched after invoking')
            elif 'dispatching-parallel' in s and len(set(c.get('mid') for c in ag)) == len(ag) and not any(c.get('bg') for c in ag):
                out.append('agents dispatched one at a time, foreground')
            if 'subagent-driven' in s and len(code_edit) >= 3:
                out.append('controller edited code itself (3+ edits)')
        if 'brainstorming' in s:
            ask = next((c for c in cs if c['tool'] == 'AskUserQuestion'), None)
            if code_edit and (ask is None or code_edit[0]['t'] < ask['t']):
                out.append('code edited in the same turn, before any owner question')
        if 'writing-plans' in s:
            if not any(c['tool'] == 'Write' and c.get('planfile') for c in cs):
                out.append('no plan file written')
        if 'using-git-worktrees' in s:
            if not any(c['tool'] == 'Bash' and 'git' in (c.get('head') or '') for c in cs):
                out.append('no git command after invoking')
        return out

    # ---------------------------------------------------------- conditions
    def conditions(self):
        def pb(n):
            return '1' if n <= 1 else '2' if n == 2 else '3' if n == 3 else '4+'

        def ab(n):
            return '1-2' if n <= 2 else '3-5' if n <= 5 else '6-10' if n <= 10 else '11+'
        g = collections.defaultdict(lambda: dict(n=0, f=0, to=0, read=[], git=[], fs=[], jest=[], tsc=[], hl=0))
        g2 = collections.defaultdict(lambda: dict(n=0, f=0, to=0, read=[], git=[], fs=[], jest=[], tsc=[], hl=0))
        for i, c in self.calls:
            m = int(c['t'] // 60)
            for key, G in ((pb(len(self.min_proj.get(m, ()))), g), (ab(self.min_agents.get(m, 0)), g2)):
                r = G[key]
                r['n'] += 1
                r['f'] += int(is_fail(c) and c.get('ec') not in ('nonzero:benign-no-match',) and not (c.get('ec') or '').startswith(('test:', 'nonzero:', 'build:')))
                r['to'] += int(bool(c.get('to')) or (c.get('ec') or '').startswith('timeout'))
                r['hl'] += int(c.get('ec') == 'timeout:host-load-passed-on-rerun')
                if c['tool'] == 'Read' and not is_fail(c):
                    r['read'].append(c['d'])
                elif c['cat'] == 'git' and not is_fail(c):
                    r['git'].append(c['d'])
                elif c['cat'] == 'fs:read-search' and not is_fail(c):
                    r['fs'].append(c['d'])
                elif c['cat'] == 'test:jest' and not c.get('bg') and 'fulltest' in (c.get('feat') or []):
                    r['jest'].append(c['d'])
                elif c['cat'] == 'test:tsc' and not c.get('bg'):
                    r['tsc'].append(c['d'])
        # share of active minutes with >1 project
        tot = len(self.min_proj)
        multi = sum(1 for v in self.min_proj.values() if len(v) > 1)
        return g, g2, dict(active_minutes=tot, multi_project_minutes=multi)

    # ---------------------------------------------------------- per project
    def per_project(self, loops):
        P = collections.defaultdict(lambda: dict(main=0, sub=0, calls=0, fails=0, errs=0, wall=0.0, active=0.0, to_s=0.0, ec=collections.Counter(), loops_s=0.0, skills=0, dup=0, dup_s=0.0, first=None, last=None))
        for d in self.D:
            p = P[d['project']]
            p[d['kind']] += 1
            p['calls'] += len(d['calls'])
            p['errs'] += sum(c['err'] for c in d['calls'])
            p['fails'] += sum(1 for c in d['calls'] if is_fail(c))
            p['wall'] += d['wall']
            p['active'] += d['wall'] - sum(v for k, v in d['excl'].items() if k.startswith('dormant:'))
            p['to_s'] += sum(c['d'] for c in d['calls'] if (c.get('to') or (c.get('ec') or '').startswith('timeout')) and not c.get('bg'))
            p['ec'].update(c.get('ec') for c in d['calls'] if is_fail(c))
            p['skills'] += len(d.get('skills', []))
            p['first'] = d['first'] if p['first'] is None else min(p['first'], d['first'])
            p['last'] = d['last'] if p['last'] is None else max(p['last'], d['last'])
        for k in ('retry_loops',):
            for x in loops[k]:
                P[self.D[x['i']]['project']]['loops_s'] += x['lo']
        for x in loops['dups']:
            if x['j'] >= 0.9 and x['a_done']:
                P[x['project']]['dup'] += 1
                P[x['project']]['dup_s'] += x['b_active']
        return P

    # ---------------------------------------------------------- §10 ledger lines
    def ledger_lines(self, min_idle_min=30.0):
        out = collections.defaultdict(list)
        for d in self.D:
            if d['last'] is None or self.now - d['last'] < min_idle_min * 60:
                continue
            cs = d['calls']
            cm = collections.Counter()
            for k, v in d['excl'].items():
                cm[metric_cat(k)] += v / 60
            reads = collections.Counter(c['fh'] for c in cs if c['tool'] == 'Read' and c.get('fh'))
            builds = [c for c in cs if c['cat'].startswith('build:')]
            tests = [c for c in cs if c['cat'].startswith('test:')]
            tos = [c for c in cs if c.get('to') or (c.get('ec') or '').startswith('timeout')]
            reps = collections.Counter(c['fp'] for c in cs if c['tool'] == 'Bash' and c.get('fp') and not c['cat'].startswith('wait-loop'))
            buckets = collections.Counter(H.CLASS_BUCKET.get(c.get('ec') or 'other', 'BEHAVIOUR') for c in cs if is_fail(c))
            ms = [int(m) for m in d['minutes']]
            cp = [len(self.min_proj.get(m, ())) for m in ms]
            ca = [self.min_agents.get(m, 0) for m in ms]
            dormant = sum(v for k, v in d['excl'].items() if k.startswith('dormant:'))
            rec = dict(
                schema='process-metrics/2',
                task_id=d['agent'] if d['kind'] == 'sub' else d['session'],
                parent_id=d['session'] if d['kind'] == 'sub' else None,
                kind=d['kind'], project=d['project'],
                **{'class': infer_class(d.get('desc') or '')},
                date=fdate(d['first']), purpose=(d.get('desc') or '')[:80],
                wall_min=round(d['wall'] / 60, 1), active_min=round((d['wall'] - dormant) / 60, 1),
                tool_calls=len(cs), tokens=(d['tokens'] or {}).get('output') if d.get('tokens') else None,
                tokens_detail=d.get('tokens'),
                cat_min={k: round(cm.get(k, 0), 1) for k in METRIC_KEYS},
                builds=dict(n=len(builds), min=round(sum(c['d'] for c in builds if not c.get('bg')) / 60, 1), full_vs_incremental=None),
                tests=dict(n=len(tests), full_n=sum(1 for c in tests if 'fulltest' in (c.get('feat') or [])), min=round(sum(c['d'] for c in tests if not c.get('bg')) / 60, 1)),
                device_min=round(sum(v for k, v in cm.items() if k in ('adb_capture', 'adb_install', 'emulator_boot')), 1),
                timeouts=dict(n=len(tos), min=round(sum(c['d'] for c in tos if not c.get('bg')) / 60, 1)),
                retries=dict(n=sum(k - 1 for k in reps.values() if k > 1)),
                rereads=dict(n=sum(k - 1 for k in reads.values() if k > 1)),
                errors=dict(n=sum(1 for c in cs if is_fail(c)), by_bucket=dict(buckets)),
                conditions=dict(loadavg_start=None, loadavg_end=None, shared_emulator=None, disk_free_gb=None,
                                concurrent_projects_max=max(cp) if cp else None, concurrent_agents_median=pct(ca, .5)),
                owner=dict(round_trips=d.get('user_prompts') if d['kind'] == 'main' else None,
                           blocked_min=round(d.get('owner_wait_s', 0) / 60, 1) if d['kind'] == 'main' else None),
                outcome=d.get('outcome'), route_version=None,
                source=H.PARSER_VERSION + ' (transcript-derived; null = unknown, never estimated)',
            )
            s = json.dumps(rec, separators=(',', ':'))
            if len(s) > 4000:
                rec.pop('tokens_detail', None)
            out[d['project']].append(rec)
        return out


def dedupe(D):
    """Forked/resumed sessions copy transcripts: the same subagent file appears under two session dirs and a
    forked main session repeats its parent's records. Keep the fullest copy of each subagent, drop calls whose
    tool_use id was already seen, and drop a transcript that is >= 90% copied calls."""
    info = dict(sub_copies=0, calls_dropped=0, transcripts_dropped=0)
    best = {}
    for d in D:
        if d['kind'] == 'sub' and d.get('agent'):
            k = d['agent']
            if k not in best or d['n_lines'] > best[k]['n_lines']:
                if k in best:
                    info['sub_copies'] += 1
                best[k] = d
            else:
                info['sub_copies'] += 1
    keep = [d for d in D if not (d['kind'] == 'sub' and d.get('agent') and best.get(d['agent']) is not d)]
    keep.sort(key=lambda d: (-d['n_lines'], d['first']))
    seen = set()
    out = []
    for d in keep:
        cs = d['calls']
        new = [c for c in cs if c.get('u') is None or c['u'] not in seen]
        if len(cs) >= 5 and len(new) <= 0.1 * len(cs):
            info['transcripts_dropped'] += 1
            info['calls_dropped'] += len(cs)
            continue
        info['calls_dropped'] += len(cs) - len(new)
        for c in cs:
            if c.get('u'):
                seen.add(c['u'])
        if len(new) != len(cs):
            ids = set(c.get('u') for c in new)
            d = dict(d)
            d['calls'] = new
            d['dispatches'] = [x for x in d.get('dispatches', []) if H.h10(str(x['id'])) in ids]
            d['skills'] = [x for x in d.get('skills', []) if x.get('u') in ids]
        out.append(d)
    out.sort(key=lambda d: d['first'])
    return out, info


METRIC_KEYS = ['builds', 'prebuild', 'tests', 'adb_capture', 'adb_install', 'emulator_boot', 'waits', 'analysis_scripts', 'image_work', 'git', 'browser', 'agents', 'other', 'model', 'dormant']


def metric_cat(c):
    if c == 'model':
        return 'model'
    if c.startswith('dormant:'):
        return 'dormant'
    if c.startswith('build:'):
        return 'prebuild' if c == 'build:prebuild' else 'builds'
    if c.startswith('test:'):
        return 'tests'
    if c == 'adb:install':
        return 'adb_install'
    if c.startswith('adb:') or c == 'capture-harness':
        return 'adb_capture'
    if c == 'emulator:boot':
        return 'emulator_boot'
    if c.startswith('wait-loop') or c.startswith('bg-wait:'):
        return 'waits'
    if c == 'analysis:python-node':
        return 'analysis_scripts'
    if c == 'image:sharp-ffmpeg':
        return 'image_work'
    if c == 'git':
        return 'git'
    if c == 'tool:browser':
        return 'browser'
    if c == 'tool:agent':
        return 'agents'
    return 'other'


def infer_class(desc):
    s = desc.lower()
    for k, rx in (('review', r'review|re-review|verify|audit of'), ('capture', r'captur|screenshot|shots?\b|record'), ('perf', r'perf|fps|bench|jank|frame'),
                  ('build-fix', r'fix|bug|crash|broken|repair'), ('research', r'research|investigat|explor|survey|audit|analy|study|find'),
                  ('docs', r'doc|report|write-?up|readme|summary'), ('build', r'\bbuild\b|apk|aab|release|deploy'),
                  ('feature', r'implement|add|feature|create|make|design|art|skin|ui')):
        if re.search(rx, s):
            return k
    return 'other' if s else None


def append_ledger(lines_by_project, ledger_dir, dry=False):
    """Append-only, idempotent on task_id. Returns {project: added}."""
    added = {}
    os.makedirs(ledger_dir, exist_ok=True)
    for proj, recs in lines_by_project.items():
        safe = re.sub(r'[^\w.-]+', '_', proj)
        p = os.path.join(ledger_dir, safe + '.jsonl')
        have = set()
        if os.path.exists(p):
            with open(p) as fh:
                for line in fh:
                    try:
                        have.add(json.loads(line).get('task_id'))
                    except Exception:
                        pass
        new = [r for r in recs if r['task_id'] not in have]
        if new and not dry:
            with open(p, 'a') as fh:
                for r in sorted(new, key=lambda r: (r['date'], r['task_id'] or '')):
                    fh.write(json.dumps(r, separators=(',', ':')) + '\n')
        added[proj] = len(new)
    return added
