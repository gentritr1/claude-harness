"""Self-test for harness-audit on a tiny synthetic transcript fixture.

Covers: error classifier, redaction, loop/double-work detection, report generation and idempotent
ledger append. Run:  harness-audit --self-test   (or python3 selftest.py [--keep])
Exit code 0 = all checks passed.
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import harness_core as H  # noqa: E402
import harness_analysis as A  # noqa: E402
import fg_wait as FW  # noqa: E402

CLASSIFIER_CASES = [
    ('Edit', 'tool:Edit/Write', '<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>', '', 'edit:not-read-first'),
    ('Edit', 'tool:Edit/Write', '<tool_use_error>String to replace not found in file.\nString: foo</tool_use_error>', '', 'edit:string-not-found'),
    ('Edit', 'tool:Edit/Write', '<tool_use_error>Found 3 matches of the string to replace, but replace_all is false.</tool_use_error>', '', 'edit:not-unique'),
    ('Read', 'tool:Read', 'File content (40000 tokens) exceeds maximum allowed tokens (25000). Use offset and limit', '', 'file:too-large'),
    ('Read', 'tool:Read', 'File does not exist. Note: your current working directory is /Users/x/p', '', 'file:not-found'),
    ('Bash', 'bash:other', 'Exit code 1\n(eval):1: == not found', 'echo == done ==', 'shell:zsh-equals-expansion'),
    ('Bash', 'fs:read-search', 'Exit code 1\n(eval):1: no matches found: --include=*.ts', 'grep -r foo --include=*.ts .', 'shell:zsh-glob-nomatch'),
    ('Bash', 'adb:other', 'Exit code 127\n(eval):1: no such file or directory: /opt/sdk/adb -s emulator-5556', '$ADB devices', 'shell:zsh-no-word-split'),
    ('Bash', 'bash:other', 'Exit code 1\nsed: 1: "src/a.ts": invalid command code s', "sed -i 's/a/b/' src/a.ts", 'shell:bsd-vs-gnu-flags'),
    ('Bash', 'fs:read-search', 'Exit code 1\n', 'grep -n foo src/a.ts', 'nonzero:benign-no-match'),
    ('Bash', 'test:jest', 'Exit code 1\nTests:       2 failed, 30 passed, 32 total', 'npx jest', 'test:failures'),
    ('Bash', 'test:tsc', 'Exit code 2\nsrc/a.ts(3,1): error TS2322: Type string is not assignable', 'npx tsc --noEmit', 'test:tsc-errors'),
    ('Bash', 'wait-loop:build', 'Command timed out after 10m 0s', 'until [ -f out.apk ]; do sleep 5; done', 'timeout:foreground-wait'),
    ('Bash', 'bash:other', '<tool_use_error>Blocked: sleep 30 followed by: cat log. To wait for a condition, use Monitor', 'sleep 30; cat log', 'wait:sleep-blocked'),
    ('Bash', 'bash:other', 'This agent is isolated in the worktree /x but this command is too complex to verify', 'a | b', 'sandbox:worktree-guard'),
    ('Bash', 'adb:other', 'Exit code 1\nadb: device offline', 'adb shell ls', 'device:adb-offline'),
    ('Bash', 'git', 'Exit code 1\nerror: Your local changes to the following files would be overwritten by checkout', 'git checkout main', 'git:conflict-or-dirty'),
    ('Bash', 'bash:other', 'Exit code 1\nENOSPC: no space left on device', 'cp a b', 'env:disk-full'),
    ('Bash', 'bash:other', 'Exit code 127\nzsh: command not found: magick', 'magick a.png b.png', 'env:command-not-found'),
    ('Bash', 'bash:other', 'Permission for this action was denied by the Claude Code auto mode classifier. Reason: x', 'rm -rf x', 'permission:classifier-denied'),
    ('Bash', 'bash:other', "The user doesn't want to proceed with this tool use.", 'ls', 'permission:user-rejected'),
    ('Bash', 'bash:other', 'Exit code 1\nbfs: error: Unknown argument', 'find -Users-x -name a', 'shell:find-is-bfs'),
    ('mcp__Claude_Browser__computer', 'tool:browser', 'left_click with `coordinate` requires a prior computer{action:"screenshot"}', '', 'browser:precondition'),
    ('mcp__Claude_Browser__javascript_tool', 'tool:browser', 'javascript_tool timed out after 30s. The Browser pane is currently hidden.', '', 'browser:pane-timeout'),
    ('Monitor', 'wait-loop:tool', '<tool_use_error>InputValidationError: Monitor failed due to the following issue:', '', 'tool:misuse-params'),
]

T0 = 1767261600.0  # 2026-01-01 10:00 UTC, far older than the 30-min idle guard


def iso(t):
    import datetime
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')


class Fx:
    def __init__(self, tag='m'):
        self.lines = []
        self.t = T0
        self.tag = tag

    def user(self, text, dt=1):
        self.t += dt
        self.lines.append(dict(type='user', timestamp=iso(self.t), message=dict(role='user', content=text)))

    def call(self, name, inp, result, err=False, dt=2, dur=1.0, uid=None, extra=None):
        self.t += dt
        uid = uid or 'toolu_%s%06d' % (self.tag, len(self.lines))
        self.lines.append(dict(type='assistant', timestamp=iso(self.t), requestId='req_%d' % len(self.lines),
                               message=dict(id='msg_%d' % len(self.lines), role='assistant', usage=dict(output_tokens=10, input_tokens=5),
                                            content=[dict(type='tool_use', id=uid, name=name, input=inp)])))
        self.t += dur
        rec = dict(type='user', timestamp=iso(self.t), message=dict(role='user', content=[dict(type='tool_result', tool_use_id=uid, content=result, is_error=err)]))
        if extra:
            rec['toolUseResult'] = extra
        self.lines.append(rec)
        return uid

    def write(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as fh:
            for l in self.lines:
                fh.write(json.dumps(l) + '\n')
            fh.write('{"type":"user", "message": truncated-not-json\n')


def build_fixture(root):
    proj = os.path.join(root, '-Users-test-Desktop-Projects-demo')
    m = Fx()
    m.user('please fix the thing')
    m.call('Skill', dict(skill='superpowers:systematic-debugging'), 'Launching skill')
    m.call('Edit', dict(file_path='/Users/test/p/src/a.ts', old_string='x', new_string='y'), '<tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>', err=True)
    m.call('Read', dict(file_path='/Users/test/p/src/a.ts'), '1\tconst x = 1')
    m.call('Edit', dict(file_path='/Users/test/p/src/a.ts', old_string='z', new_string='y'), '<tool_use_error>String to replace not found in file.</tool_use_error>', err=True)
    m.call('Edit', dict(file_path='/Users/test/p/src/a.ts', old_string='x', new_string='y'), 'The file has been updated.')
    m.call('Bash', dict(command='echo === header ==='), 'Exit code 1\n(eval):1: == not found', err=True)
    for _ in range(3):
        m.call('Bash', dict(command='npx jest src/a.test.ts'), 'Exit code 1\nTests:       1 failed, 3 passed, 4 total\napi_key=sk-abcdefghijklmnop1234 at /Users/test/p', err=True, dur=5)
    m.call('Bash', dict(command='sleep 30; cat /tmp/log'), '<tool_use_error>Blocked: sleep 30 followed by: cat /tmp/log. To wait for a condition, use Monitor</tool_use_error>', err=True)
    m.call('Bash', dict(command='grep -rn foo src'), 'Exit code 1\n', err=True)
    m.call('Agent', dict(description='Fix thing', prompt=('Fix the parser bug in src/a.ts and add a failing test first. ' * 20), run_in_background=True), 'Async agent launched', uid='toolu_dispatch1')
    m.t += 4000  # the subagent runs and finishes in between
    m.call('Agent', dict(description='Fix thing again', prompt=('Fix the parser bug in src/a.ts and add a failing test first. ' * 20), run_in_background=True), 'Async agent launched', uid='toolu_dispatch2')
    m.write(os.path.join(proj, 'sess1.jsonl'))

    s = Fx('s')
    s.t = T0 + 600
    s.user('brief text')
    s.call('Bash', dict(command='cd /Users/test/p/android && ./gradlew assembleDebug'), 'BUILD SUCCESSFUL', dur=60)
    s.call('Bash', dict(command='cd /Users/test/p/android && ./gradlew assembleDebug'), 'BUILD SUCCESSFUL', dur=30)
    s.call('Bash', dict(command='until [ -f /tmp/done ]; do sleep 5; done'), 'Command timed out after 10m 0s', err=True, dur=600)
    sub = os.path.join(proj, 'sess1', 'subagents', 'agent-aaa.jsonl')
    s.write(sub)
    with open(sub[:-6] + '.meta.json', 'w') as fh:
        json.dump(dict(agentType='general-purpose', description='Fix thing', toolUseId='toolu_dispatch1', model='opus'), fh)
    # a resumed session copies the subagent transcript under a second session dir: must be counted once
    cp = os.path.join(proj, 'sess2', 'subagents', 'agent-aaa.jsonl')
    os.makedirs(os.path.dirname(cp), exist_ok=True)
    shutil.copy(sub, cp)
    shutil.copy(sub[:-6] + '.meta.json', cp[:-6] + '.meta.json')
    return root



# ------------------------------------------------------------------ fg-wait-guard instruments
WA_POSITIVE = [
    ('python3 -c "import time; time.sleep(30)"', 'wa:py-sleep'),
    ("python3 - <<'PY'\nimport time\nwhile not done():\n    time.sleep(5)\nPY", 'wa:py-sleep'),
    ("node -e 'setTimeout(() => {}, 60000)'", 'wa:node-sleep'),
    ('read -t 120 line < fifo', 'wa:read-t'),
    ('timeout 300 tail -f build.log', 'wa:timeout-tail'),
    ('./scripts/wait-for-metro.sh', 'wa:wait-script'),
    ('npx wait-on http://localhost:8081', 'wa:wait-script'),
    ('for i in $(seq 60); do sleep 5; done', 'gap:for'),
    ('cd app && until [ -f DONE ]; do sleep 2; done', 'gap:cd'),
    ('until grep -q Ready log; do sleep 1; done', 'hook-loop'),
]
WA_NEGATIVE = ["python3 - <<'EOF'\np='a.py'; s=open(p).read(); s=s.replace('x','time.sleep(1); ./wait-for.sh; read -t 5; node -e setTimeout(')\nopen(p,'w').write(s)\nEOF",
               'cp tools/hooks/fg-wait-guard.sh /tmp/x.sh', 'python3 analyze.py', 'node build.mjs', 'tail -f build.log', 'grep -rn await src/await.js',
               'timeout 30 npx jest', 'echo "read the file"', 'cat thread-t1.txt', 'sleep 5', 'git log -n 5']


def _rows(n, a=0, wa=0, null=0, bgwait=0, t0=100.0):
    rows = []
    for i in range(n):
        c = dict(tool='Bash', t=t0 + i, d=1.0, bg=0, cat='bash:other', feat=[])
        if i < a:
            c['d'] = 400.0
        elif i < a + wa:
            c['feat'] = ['wa:py-sleep']
        elif i < a + wa + null:
            c['ec'] = FW.NULL_CLASS
        elif i < a + wa + null + bgwait:
            c.update(bg=1, cat='wait-loop:build', bgs='killed')
        rows.append(c)
    return rows


def _scoped(arrows, geo):
    return {'arrows-game': FW.metrics(arrows), 'geoguesser-app': FW.metrics(geo), 'all': FW.metrics(arrows + geo)}


def fg_wait_checks(check):
    for cmd, want in WA_POSITIVE:
        got = H.workaround_features(cmd)
        check('workaround detector fires %-16s' % want, want in got, (cmd, got))
    for cmd in WA_NEGATIVE:
        got = H.workaround_features(cmd)
        check('workaround detector silent on %-24s' % cmd[:24].replace('\n', ' '), got == [], got)
    m = FW.metrics(_rows(1000, a=10, wa=4, null=3, bgwait=2) + [dict(tool='Bash', t=1, d=150.0, bg=0, cat='x', feat=[])])
    check('metrics: A counts foreground >= 300 s only', m['A_fg_ge300_count'] == 10, m)
    check('metrics: B sums foreground calls >= 120 s', abs(m['B_fg_ge120_hours'] - round((10 * 400 + 150) / 3600.0, 2)) < 1e-9, m['B_fg_ge120_hours'])
    check('metrics: WA = foreground forms + killed background waits', m['workaround']['total'] == 6 and m['workaround']['by_form']['wa:bg-wait-timeout'] == 2, m['workaround'])
    check('metrics: null counted', m['null_zsh_equals_count'] == 3, m)
    check('poisson quantile sane', FW.poisson_quantile(40, 0.05) in (29, 30) and FW.poisson_quantile(0, 0.95) == 0, FW.poisson_quantile(40, 0.05))
    base = dict(rule=FW.RULE, metrics=_scoped(_rows(2000, a=40, wa=10, null=8), _rows(2000, a=40, wa=10, null=8)))
    cases = [
        ('SUCCESS', _scoped(_rows(2000, a=5, wa=10, null=8), _rows(2000, a=6, wa=9, null=8))),
        ('NO-EFFECT', _scoped(_rows(2000, a=5, wa=10, null=8), _rows(2000, a=30, wa=10, null=8))),
        ('REMOVE-HOOK', _scoped(_rows(2000, a=5, wa=40, null=8), _rows(2000, a=5, wa=10, null=8))),
        ('INCONCLUSIVE', _scoped(_rows(2000, a=5, wa=10, null=40), _rows(2000, a=5, wa=10, null=8))),
        ('INSUFFICIENT', _scoped(_rows(500, a=0, wa=2, null=2), _rows(2000, a=5, wa=10, null=8))),
    ]
    for want, post in cases:
        got, det = FW.judge(base, post)
        check('judge synthetic -> %s' % want, got == want, (got, det))
    small = dict(rule=FW.RULE, metrics=_scoped(_rows(2000, a=6, wa=10, null=8), _rows(2000, a=6, wa=10, null=8)))
    got, det = FW.judge(small, _scoped(_rows(2000, a=2, wa=10, null=8), _rows(2000, a=2, wa=10, null=8)))
    check('judge: a 67 %% drop inside count noise is not SUCCESS', got == 'NO-EFFECT' and det['arrows-game']['A']['down_50'], (got, det.get('arrows-game')))


def run(keep=False):
    fails = []

    def check(name, cond, detail=''):
        print(('PASS ' if cond else 'FAIL ') + name + (('  [' + str(detail) + ']') if not cond and detail != '' else ''))
        if not cond:
            fails.append(name)

    # 1. classifier
    for tool, cat, text, cmd, want in CLASSIFIER_CASES:
        got = H.classify_error(tool, cat, text, cmd)
        check('classify %-28s' % want, got == want, got)
    # 2. redaction
    r = H.redact('open /Users/alice/secret.txt token=ghp_abcdefghijklmnopqrstuv mail bob@example.com key sk-abcdefghijklmn12345')
    check('redact strips user path, token, email, key', '/Users/alice' not in r and 'ghp_' not in r and 'bob@' not in r and 'sk-abc' not in r, r)
    check('redact caps at 120 chars', len(H.redact('x ' * 500)) <= 120)
    fg_wait_checks(check)
    check('project_of merges moved and worktree dirs', H.project_of('-Users-x-Desktop-Projects-arrows-game--claude-worktrees-foo') == 'arrows-game' == H.project_of('-Users-x-Desktop-arrows-game'))

    tmp = tempfile.mkdtemp(prefix='harness-selftest-')
    try:
        root = build_fixture(os.path.join(tmp, 'projects'))
        out = os.path.join(tmp, 'out')
        import importlib.machinery
        import importlib.util
        loader = importlib.machinery.SourceFileLoader('harness_audit_cli', os.path.join(HERE, 'harness-audit'))
        spec = importlib.util.spec_from_loader('harness_audit_cli', loader)
        cli = importlib.util.module_from_spec(spec)
        loader.exec_module(cli)
        ds = cli.load_digests(root, os.path.join(out, 'cache'), quiet=True)
        check('three transcript files digested (one is a copy)', len(ds) == 3, len(ds))
        check('copied subagent dropped by dedupe', len(A.Audit(ds).D) == 2 and A.Audit(ds).dedup['sub_copies'] == 1, A.Audit(ds).dedup)
        main = next(d for d in ds if d['kind'] == 'main')
        sub = next(d for d in ds if d['kind'] == 'sub')
        check('main calls paired', len(main['calls']) == 13, len(main['calls']))
        check('bad JSON line counted, not fatal', main['n_bad'] == 1, main['n_bad'])
        dig = json.dumps(ds)
        check('digest holds no prompt text', 'parser bug' not in dig and 'please fix' not in dig)
        check('digest holds no secret', 'sk-abcdefghijklmnop' not in dig and '/Users/test' not in dig)
        au = A.Audit(ds)
        L = au.loops()
        rl = L['retry_loops']
        check('retry loop detected once (jest x3)', len(rl) == 1 and rl[0]['n'] == 3, [(x['n'], x['head']) for x in rl])
        check('edit fail -> re-edit cycle on one file', len(L['edit_cycles']) == 1 and L['edit_cycles'][0]['fails'] == 2, L['edit_cycles'])
        check('unchanged-tree rebuild detected', len(L['rebuilds']) == 1, L['rebuilds'])
        dd = [x for x in L['dups'] if x['j'] >= 0.9 and x['a_done']]
        check('re-dispatch of finished work detected', len(dd) == 1 and dd[0]['same_prompt'] is True, L['dups'])
        check('foreground wait timeout detected', len(L['wait_timeouts']) == 1, L['wait_timeouts'])
        check('sleep-blocked counted', len(L['sleep_blocked']) == 1)
        ec = {r['cls']: r['n'] for r in au.error_classes()}
        check('classes in fixture', ec.get('edit:not-read-first') == 1 and ec.get('test:failures') == 3 and ec.get('nonzero:benign-no-match') == 1 and ec.get('shell:zsh-equals-expansion') == 1, ec)
        sk, base, _ = au.skills()
        check('skill invocation found', sk and sk[0]['skill'] == 'superpowers:systematic-debugging', sk)
        check('skill contradiction heuristic fires (same failing call 3+ times)', sk and sk[0]['contra'].get('same failing call 3+ times after invoking') == 1, sk and sk[0]['contra'])
        body, J = cli.render(au, 'fixture')
        check('report renders all sections', all(('## %d.' % k) in body for k in range(1, 10)))
        check('report has no user path or secret', '/Users/test' not in body and 'sk-abcdefghijklmnop' not in body)
        # 3. idempotent ledger append
        led = os.path.join(out, 'ledger')
        a1 = A.append_ledger(au.ledger_lines(30), led)
        a2 = A.append_ledger(au.ledger_lines(30), led)
        check('ledger first run adds 2 lines', a1 == {'demo': 2}, a1)
        check('ledger second run adds 0 lines', a2 == {'demo': 0}, a2)
        lines = open(os.path.join(led, 'demo.jsonl')).read().splitlines()
        check('ledger has 2 lines, each < 4 KB with schema', len(lines) == 2 and all(len(l) < 4096 and json.loads(l).get('schema') == 'process-metrics/2' for l in lines), [len(l) for l in lines])
        check('ledger never stores prompt text', all('parser bug' not in l for l in lines))
        # 4. cache: second load is all hits and identical
        ds2 = cli.load_digests(root, os.path.join(out, 'cache'), quiet=True)
        key = lambda d: (d['kind'], d['session'])
        check('cache reload identical', json.dumps(sorted(ds2, key=key), sort_keys=True) == json.dumps(sorted(ds, key=key), sort_keys=True))
        # 5. cache invalidation: touching a file changes its key
        p = os.path.join(root, '-Users-test-Desktop-Projects-demo', 'sess1.jsonl')
        with open(p, 'a') as fh:
            fh.write('\n')
        _d, cached = H.cached_digest(p, 'demo', 'main', 'sess1', None, os.path.join(out, 'cache'))
        check('cache invalidates on file change', cached is False)
        # 6. frozen baseline: written once, refuses overwrite, tamper detected by the judge
        bj, bm = os.path.join(out, 'fgb.json'), os.path.join(out, 'fgb.md')
        FW.freeze(au, 0, 4e9, bj, bm, H.PARSER_VERSION)
        try:
            FW.freeze(au, 0, 4e9, bj, bm, H.PARSER_VERSION)
            refused = False
        except SystemExit:
            refused = True
        check('frozen baseline refuses overwrite', refused)
        doc = json.load(open(bj))
        check('frozen baseline sha matches its metrics', FW._digest(doc['metrics']) == doc['metrics_sha'])
        doc['metrics']['all']['A_fg_ge300_count'] += 1
        check('edited baseline fails the sha check', FW._digest(doc['metrics']) != doc['metrics_sha'])
        check('baseline md carries the pre-registered rule', 'FG-WAIT-R1' in open(bm).read())
    finally:
        if keep:
            print('fixture kept at', tmp)
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    print('\nSELF-TEST %s: %d checks failed' % ('PASSED' if not fails else 'FAILED', len(fails)))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(run(keep='--keep' in sys.argv))
