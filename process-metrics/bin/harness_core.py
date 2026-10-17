"""harness_core: stream-parse Claude Code transcripts into small, privacy-safe per-file digests.

Ported from arrows-game/scripts/process/agent_time_audit.py (v1, 2026-10-07): the Bash category
rules, wait targets, call pairing, exclusive time attribution (model / dormant / bg-wait), token
accounting and outcome heuristics are kept; this module extends them with error-cause
classification, call fingerprints for loop detection, tool-choice features, dispatch sketches,
skill invocations and per-minute activity for host-concurrency analysis.

Privacy: a digest never stores prompt text, file contents or command text. It keeps tool names,
categories, timings, hashes (fingerprints, sketches), a redacted command head (program names
only) and, for errors only, one redacted <=120-char signature line.

python3 stdlib only.
"""
import bisect
import collections
import hashlib
import json
import os
import re
from datetime import datetime

PARSER_VERSION = 'harness-audit/1.5'  # 1.4: workaround-detector features, timeout param, hook-predicate flag, bg status; 1.5: heredoc bodies are data


def ts(s):
    return datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()


def h10(s):
    return hashlib.blake2b(s.encode('utf-8', 'replace'), digest_size=5).hexdigest()


# ------------------------------------------------------------------ redaction
_R_USER = re.compile(r'/(Users|home)/[^/\s\'"]+')
_R_KV = re.compile(r'(?i)\b(api[_-]?key|access[_-]?token|token|secret|password|passwd|authorization|bearer|cookie)\b(\s*[:=]\s*|\s+)\S+')
_R_KEYS = re.compile(r'\b(sk-[A-Za-z0-9_\-]{8,}|gh[pousr]_[A-Za-z0-9]{10,}|xox[bapr]-[A-Za-z0-9\-]+|AKIA[0-9A-Z]{12,}|AIza[0-9A-Za-z_\-]{20,}|eyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-.]+)')
_R_LONG = re.compile(r'[A-Za-z0-9_\-+/=]{32,}')
_R_EMAIL = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')


def redact(s, n=120):
    s = str(s)
    s = _R_USER.sub('~', s)
    s = _R_KV.sub(lambda m: m.group(1) + '=<REDACTED>', s)
    s = _R_KEYS.sub('<REDACTED>', s)
    s = _R_LONG.sub('<REDACTED>', s)
    s = _R_EMAIL.sub('<EMAIL>', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:n]


# ------------------------------------------------------------------ project naming
def project_of(dirname):
    """'-Users-x-Desktop-Projects-arrows-game--claude-worktrees-foo' -> 'arrows-game'."""
    d = re.sub(r'--claude-worktrees-.*$', '', dirname)
    if 'Claude-scratch-workspaces' in d:
        return 'claude-scratch'
    m = re.match(r'^-(?:Users|home)-[^-]+-(?:Desktop|Documents|Projects|src|code|dev)-(?:Projects-)?(.+)$', d)
    if m:
        p = m.group(1)
        if p.startswith('Codex-'):
            return 'codex-' + re.sub(r'^\d{4}-\d{2}-\d{2}-', '', p[6:])[:40]
        return p
    return d.strip('-') or 'unknown'


# ------------------------------------------------------------------ Bash categories (v1 rules + extensions)
RX = lambda p: re.compile(p, re.I | re.S)
BASH_RULES = [
    ('build:gradle', RX(r'gradlew|assembleRelease|bundleRelease|assembleDebug|\bgradle\b')),
    ('build:prebuild', RX(r'expo\s+prebuild')),
    ('build:js-repack', RX(r'export:embed|hermesc|apksigner|zipalign|bundle-proof|repack')),
    ('build:xcode', RX(r'xcodebuild|\bpod\s+install|xcrun\s+simctl\s+install')),
    ('build:eas', RX(r'\beas\s+(build|update|submit)')),
    ('build:web', RX(r'(npm|pnpm|yarn|bun)\s+(run\s+)?build\b|\bvite\s+build|\bnext\s+build|expo\s+export(?!:embed)|\bastro\s+build|\bwebpack\b|\besbuild\b|\bcargo\s+build|\bgo\s+build')),
    ('build:script', RX(r'(artifacts/[^ ]*/build[^ ]*\.sh|build[-_a-z0-9]*\.sh\b|run-aab|build-test|build_apk)')),
    ('emulator:boot', RX(r'emulator\s+-avd|boot_completed|-no-snapshot|avdmanager|emu\s+kill|simctl\s+boot')),
    ('wait-loop', RX(r'(^|[;&|\n]\s*)(until|while|for)\b.*\bsleep\b|^\s*sleep\s+\d+\s*($|;|&&)|\bwait\s+\$|tail\s+-f')),
    ('test:jest', RX(r'\bjest\b|npm (run )?test|yarn test|pnpm test|bun test')),
    ('test:vitest', RX(r'\bvitest\b')),
    ('test:pytest', RX(r'\bpytest\b|python3? -m unittest')),
    ('test:e2e', RX(r'\bplaywright\b|\bmaestro\b|\bdetox\b|\bcypress\b')),
    ('test:tsc', RX(r'\btsc\b')),
    ('test:lint', RX(r'\beslint\b|\bprettier\b|\bruff\b|\bswiftlint\b|\bktlint\b|expo\s+lint|npm run lint')),
    ('adb:install', RX(r'adb\b[^\n]*\binstall|pm\s+install|install-multiple')),
    ('adb:backup-restore', RX(r'adb\b[^\n]*(\btar\b|backup|restore|run-as|pull\s+/data|push[^\n]*/data)')),
    ('adb:su-sqlite', RX(r'adb\b[^\n]*(\bsu\b|sqlite)')),
    ('adb:screen', RX(r'screencap|screenrecord|exec-out')),
    ('adb:uiautomator', RX(r'uiautomator')),
    ('adb:perf', RX(r'gfxinfo|dumpsys|perfetto|atrace|framestats|simpleperf|meminfo')),
    ('adb:input', RX(r'adb\b[^\n]*input\s+(tap|swipe|keyevent|text)')),
    ('adb:logcat', RX(r'logcat')),
    ('adb:other', RX(r'\badb\b')),
    ('capture-harness', RX(r'capture[-_a-z0-9]*\.(mjs|js|py|sh)|harness|puppeteer|chromium')),
    ('image:sharp-ffmpeg', RX(r'\bsharp\b|ffmpeg|ffprobe|magick|convert\s|pixelmatch|sips\b|\.png')),
    ('net:http', RX(r'^\s*(cd [^;&]+[;&]+\s*)?(curl|wget|http)\b|\bvercel\b|\bgh\s+')),
    ('analysis:python-node', RX(r'\bpython3?\b|\bnode\b|\bnpx\s+(tsx|ts-node)|\btsx\b')),
    ('git', RX(r'^\s*(cd [^;&]+[;&]+\s*)?git\b')),
    ('fs:read-search', RX(r'^\s*(cd [^;&]+[;&]+\s*)?(cat|head|tail|grep|rg|sed -n|ls|find|wc|stat|du|df|awk|diff|tree|file|nl)\b')),
    ('pkg:install', RX(r'(npm|pnpm|yarn|bun)\s+(i|install|add|ci)\b|expo\s+install|\bpip3?\s+install|\bbrew\s+install')),
]

WAIT_TARGETS = [
    ('build', RX(r'build|gradle|\.aab|\.apk|assemble|prebuild|repack|xcodebuild|eas')),
    ('perf-series', RX(r'series|chain|perf|pace|soak|gate|fps|gfxinfo|trace|A/?B|run-log')),
    ('test', RX(r'jest|tsc|tdd|vitest|pytest')),
    ('capture', RX(r'capture|shot|screen|record|png|mp4|frames?')),
    ('device', RX(r'adb|emulator|boot|simctl')),
    ('server', RX(r'curl|localhost|:\d{4}|metro|expo start|dev server|vite|next dev')),
]


def classify_bash(cmd):
    for name, rx in BASH_RULES:
        if rx.search(cmd):
            if name == 'wait-loop':
                for sub, rx2 in WAIT_TARGETS:
                    if rx2.search(cmd):
                        return 'wait-loop:' + sub
                return 'wait-loop:other'
            return name
    return 'bash:other'


BROWSER_PREFIXES = ('mcp__Claude_Browser', 'mcp__claude-in-chrome', 'mcp__computer-use', 'mcp__remote-devices')


def tool_norm(name):
    """Tool name used in the reliability tables."""
    if name in ('Task',):
        return 'Agent'
    if name in ('MultiEdit',):
        return 'Edit'
    if name in ('BashOutput', 'TaskOutput'):
        return 'TaskOutput'
    if name in ('KillShell', 'KillBash'):
        return 'TaskStop'
    if name.startswith('mcp__'):
        parts = name.split('__')
        srv = parts[1] if len(parts) > 1 else '?'
        if re.match(r'^[0-9a-f]{8}-', srv):
            srv = 'connector'
        return 'mcp:' + srv
    return name


def classify(name, inp):
    """Call category (v1 semantics)."""
    if name == 'Bash':
        return classify_bash(inp.get('command', '') or '')
    if name == 'Read':
        return 'tool:Read'
    if name in ('Edit', 'Write', 'MultiEdit', 'NotebookEdit'):
        return 'tool:Edit/Write'
    if name in ('Grep', 'Glob'):
        return 'tool:Grep/Glob'
    if name.startswith(BROWSER_PREFIXES):
        return 'tool:browser'
    if name in ('Agent', 'Task', 'SendMessage'):
        return 'tool:agent'
    if name in ('Monitor', 'TaskOutput', 'BashOutput'):
        return 'wait-loop:tool'
    return 'tool:' + name.split('__')[-1]


# ------------------------------------------------------------------ command features (tool-choice comparisons)
_CD = r'^\s*(?:cd\s+[^;&|]+(?:&&|;)\s*)*'
_PREFIX = re.compile(_CD + r'(?:(?:[A-Z_][A-Z0-9_]*=\S*|nice(?:\s+-n\s*-?\d+)?|timeout\s+\d+\S*|time|command|env)\s+)*')
R_READCMD = re.compile(r'^(cat|head|tail|nl|less|sed\s+-n)\b(?![^\n]*(<<|\|\s*(sh|bash|python)))')
R_SHELL_EDIT = re.compile(r'\bsed\s+(-[a-zA-Z]*\s+)*-i\b|\bsed\s+-i|\bperl\s+-[a-z]*p[a-z]*i|\bperl\s+-[a-z]*i|write_text\(|open\([^)]*[\'"](w|a|r\+)[\'"]|\.writeFileSync\(|fs\.writeFile')
R_HEREDOC_WRITE = re.compile(r'\b(cat|tee)\b[^\n|]*(>{1,2}\s*[^\s&|;]+[^\n]*<<|<<[^\n]*>{1,2}\s*[^\s&|;]+)|\btee\s+[^\n]*<<')
R_GREPCMD = re.compile(r'^(grep|egrep|rg|ag|ack)\b|^git\s+grep\b')
R_FINDCMD = re.compile(r'^(find|fd|bfs)\b')
R_SH_C = re.compile(r'\b(ba|z)?sh\s+-c\b|\bbash\s+[^\s-]|\bsh\s+[^\s-][^\s]*\.sh\b|\bbash\s+-[a-z]*\s+\S+\.sh\b')
R_ABS = re.compile(r'(^|[\s=\'"(])(/(Users|private|tmp|var|opt|usr|home|Volumes)/|~/|\$HOME/)')
R_REL = re.compile(r'(^|[\s=\'"(])(\.{1,2}/[\w.-]|(?!-)[\w.-]+/[\w./-]*\.\w{1,6}\b|(src|app|lib|scripts|docs|artifacts|android|ios|test|tests|__tests__|components|public|assets)/)')
R_MUTATE = re.compile(r'\bsed\s+(-[a-zA-Z]*\s+)*-i|\bperl\s+-[a-z]*i|\bgit\s+(checkout|apply|cherry-pick|merge|reset|stash|pull|rebase|switch|restore|am|commit)\b|\bpatch\s|(npm|pnpm|yarn|bun)\s+(i|install|add|ci)\b|expo\s+(install|prebuild)|\b(cp|mv|rm|rsync|unzip|tar\s+-?x)\s|\btee\s|write_text\(|open\([^)]*[\'"]w|writeFileSync|>\s*[\w./-]*\.(ts|tsx|js|jsx|mjs|cjs|kt|java|swift|py|json|xml|gradle|properties|plist|m|mm|h|c|cc|cpp|css|scss|html|md|yml|yaml|toml)\b')
R_TESTFOCUS = re.compile(r'--findRelatedTests|\brelated\b|-t\s|--testNamePattern|--testPathPattern|\.(test|spec)\.\w+|__tests__/|\btests?/\S+\.(py|ts|js)|::|\s-k\s|--grep\b|--watch')


def strip_prefix(cmd):
    first = re.split(r'\n', cmd.strip(), 1)[0]
    return _PREFIX.sub('', first, count=1).strip()


def cmd_head(cmd):
    """Program name(s) only, never arguments: 'npx jest', 'adb shell', 'python3'."""
    s = strip_prefix(cmd)
    toks = s.split()
    if not toks:
        return ''
    out = []
    for t in toks[:2]:
        t = t.strip('\'"()')
        if '/' in t:
            t = os.path.basename(t.rstrip('/')) or t
        if not re.match(r'^[\w.:+-]{1,24}$', t) or t.startswith('-'):
            break
        out.append(t)
        if toks[0] not in ('npx', 'npm', 'pnpm', 'yarn', 'bun', 'adb', 'git', 'xcrun', 'expo', 'eas', 'python3', 'python', 'node', 'gh', 'brew', 'docker', 'cargo', 'go', 'uv'):
            break
    return ' '.join(out)[:30]


def bash_features(cmd):
    f = []
    s = strip_prefix(cmd)
    if R_READCMD.match(s) and '>' not in s.split('|')[0]:
        f.append('read-cmd')
    if R_SHELL_EDIT.search(cmd):
        f.append('shell-edit')
    if R_HEREDOC_WRITE.search(cmd):
        f.append('heredoc-write')
    if R_GREPCMD.match(s):
        f.append('grep-cmd')
    if R_FINDCMD.match(s):
        f.append('find-cmd')
    if R_SH_C.search(cmd):
        f.append('sh-c')
    a = bool(R_ABS.search(cmd))
    r = bool(R_REL.search(cmd))
    f.append('paths:' + ('mixed' if a and r else 'abs' if a else 'rel' if r else 'none'))
    if R_MUTATE.search(cmd):
        f.append('mutate')
    if re.search(r'\bcd\s', cmd):
        f.append('cd')
    if '\n' in cmd.strip() or cmd.count('&&') + cmd.count(';') >= 3:
        f.append('compound')
    return f


# ------------------------------------------------------------------ fg-wait-guard experiment instruments (1.4)
# The hook (agent-playbooks tools/hooks/fg-wait-guard.sh) denies foreground until/while+sleep calls with timeout
# >= 300000. These features detect the ways an agent could keep waiting in the foreground without that form.
# They are counted per 1,000 Bash calls in a frozen baseline and must stay flat after the hook starts.
R_HEREDOC = re.compile(r'<<-?\s*([\'"]?)(\w+)\1[^\n]*\n(.*?)(?:\n[ \t]*\2[ \t]*(?=\n|$)|\Z)', re.S)
R_PY_HEREDOC = re.compile(r'\bpython3?\s+-\s*<<-?\s*([\'"]?)(\w+)\1[^\n]*\n(.*?)(?:\n[ \t]*\2[ \t]*(?=\n|$)|\Z)', re.S)
R_FILE_WRITE = re.compile(r'write_text\(|\.write\(|open\([^)]*[\'"][wa]|\.replace\(')
# Rules run on the command with heredoc bodies removed (a heredoc is data: an edit script that mentions `sleep(`
# or `wait-for.sh` is not a wait). The python-heredoc rule reads the body of a `python - <<EOF` only.
WORKAROUND_RULES = [
    ('wa:py-sleep', re.compile(r'\bpython3?\s+-c\s+[\'"][^\n]*?\bsleep\s*\(')),
    ('wa:node-sleep', re.compile(r'\b(?:node|bun|deno)\s+(?:--\S+\s+)*(?:-e|--eval|-p)\s[\s\S]*?\b(?:setTimeout|setInterval|sleep)\s*\(')),
    ('wa:read-t', re.compile(r'\bread\s+(?:-[a-zA-Z]+\s+)*-[a-zA-Z]*t\s*\d')),
    ('wa:timeout-tail', re.compile(r'\bg?timeout\s+(?:-\S+\s+)*\d+[smhd]?\s+tail\s+(?:-\S+\s+)*-[a-zA-Z]*[fF]')),
    ('wa:wait-script', re.compile(r'(?:^|[;&|(\n]\s*|\b(?:sh|bash|zsh|python3?|node|bun|npx|exec)\s+)(?:\S*/)?(?:[\w.]*[-_])?wait(?:[-_.]?[\w-]*)?\.(?:sh|py|mjs|cjs|js|ts)\b|\bnpx\s+wait-on\b|\bwait-for-it\b')),
]


def strip_heredocs(cmd):
    return R_HEREDOC.sub('<<HEREDOC\n', cmd)


# Forms the hook leaves legal on purpose (tools/hooks/README.md "Known gaps"); reported, never judged.
R_HOOK_LOOP = re.compile(r'(until|while)\b')
R_GAP_FOR = re.compile(r'^for\b')
R_GAP_CD = re.compile(r'^cd\s[^\n]*?(?:&&|;)\s*(?:until|while)\b')


def hook_loop(cmd):
    """The hook's own loop predicate, copied verbatim: first statement until/while, `sleep` anywhere."""
    first = cmd.lstrip()
    return R_HOOK_LOOP.match(first) is not None and re.search(r'\bsleep\b', first) is not None


def workaround_features(cmd):
    bare = strip_heredocs(cmd)
    f = [name for name, rx in WORKAROUND_RULES if rx.search(bare)]
    if 'wa:py-sleep' not in f:
        for m in R_PY_HEREDOC.finditer(cmd):
            body = m.group(3)
            if re.search(r'\bwhile\b[\s\S]*?\bsleep\s*\(', body) and not R_FILE_WRITE.search(body):
                f.insert(0, 'wa:py-sleep')
                break
    s = cmd.lstrip()
    if re.search(r'\bsleep\b', s):
        if R_GAP_FOR.match(s):
            f.append('gap:for')
        if R_GAP_CD.match(s):
            f.append('gap:cd')
    if hook_loop(cmd):
        f.append('hook-loop')
    return f


def norm_cmd(c):
    return re.sub(r'\s+', ' ', c).strip()[:2000]


def skeleton(c):
    s = norm_cmd(c)
    s = re.sub(r'\d+', 'N', s)
    s = re.sub(r'[0-9a-f]{7,}', 'H', s)
    return s


# ------------------------------------------------------------------ error classification
# (class, bucket). Buckets: ENV = host, shell, sandbox, permissions, services; TOOL = a different tool
# or shell form would have avoided it; BEHAVIOUR = the agent's own step was wrong (didn't read first,
# guessed a path, wrong params, buggy script); SIGNAL = the command worked and reported a real
# failure of the thing under test (failing test, tsc error) or a benign non-zero (grep no match).
CLASS_BUCKET = {
    'permission:user-rejected': 'BEHAVIOUR',
    'permission:classifier-denied': 'ENV',
    'permission:classifier-unavailable': 'ENV',
    'permission:hook-blocked': 'ENV',
    'sandbox:worktree-guard': 'TOOL',
    'sandbox:not-permitted': 'ENV',
    'wait:sleep-blocked': 'TOOL',
    'edit:not-read-first': 'BEHAVIOUR',
    'edit:stale-read': 'ENV',
    'edit:string-not-found': 'BEHAVIOUR',
    'edit:not-unique': 'BEHAVIOUR',
    'edit:no-op': 'BEHAVIOUR',
    'file:too-large': 'TOOL',
    'file:not-found': 'BEHAVIOUR',
    'file:is-directory': 'BEHAVIOUR',
    'timeout:foreground-wait': 'BEHAVIOUR',
    'timeout:command': 'BEHAVIOUR',  # only 8 of 269 non-wait timeouts passed on rerun; 202 hit the limit and were moved to background
    'timeout:host-load-passed-on-rerun': 'ENV',
    'env:command-not-found': 'ENV',
    'env:disk-full': 'ENV',
    'env:port-in-use': 'ENV',
    'env:service-limit': 'ENV',
    'shell:zsh-equals-expansion': 'TOOL',
    'shell:zsh-glob-nomatch': 'TOOL',
    'shell:zsh-no-word-split': 'TOOL',
    'shell:zsh-other': 'TOOL',
    'shell:bsd-vs-gnu-flags': 'TOOL',
    'shell:find-is-bfs': 'ENV',
    'shell:syntax': 'BEHAVIOUR',
    'git:conflict-or-dirty': 'ENV',
    'git:other': 'BEHAVIOUR',
    'network': 'ENV',
    'device:adb-offline': 'ENV',
    'device:install-failed': 'ENV',
    'build:gradle-xcode-failed': 'SIGNAL',
    'build:metro-bundler': 'SIGNAL',
    'test:failures': 'SIGNAL',
    'test:tsc-errors': 'SIGNAL',
    'nonzero:benign-no-match': 'SIGNAL',
    'nonzero:check-failed': 'SIGNAL',
    'script:python-traceback': 'BEHAVIOUR',
    'script:node-error': 'BEHAVIOUR',
    'browser:precondition': 'BEHAVIOUR',
    'browser:pane-timeout': 'ENV',
    'browser:navigation-denied': 'ENV',
    'browser:js-error': 'BEHAVIOUR',
    'browser:no-preview': 'BEHAVIOUR',
    'browser:other': 'ENV',
    'tool:misuse-params': 'BEHAVIOUR',
    'tool:unknown-tool': 'BEHAVIOUR',
    'tool:subagent-wrote-report': 'BEHAVIOUR',
    'mcp:service-error': 'ENV',
    'interrupted': 'ENV',
    'other:nonzero-exit': 'BEHAVIOUR',
    'other': 'BEHAVIOUR',
}

TIMEOUT_RX = re.compile(r'timed out|Exceeded|timeout after|Command timed out|did not complete within', re.I)
# harness-emitted markers only (output text of a command may legitimately say 'timed out')
HARNESS_TO_RX = re.compile(r'Command timed out after|did not complete within its|^\s*(Exit code \d+\s*)?(Timed out|Timeout)\b|timed out waiting for (the )?(task|command|condition)', re.I | re.M)
_ERR_KW = re.compile(r'error|not found|No such|denied|failed|fatal|cannot|unable|zsh:|sh:|Traceback|refused|offline|timed out|killed|ENOENT|EACCES|not permitted|no matches|FAIL|exception', re.I)


def sig_line(text):
    lines = [x for x in text.splitlines() if x.strip()]
    if not lines:
        return ''
    if re.match(r'Exit code \d+', lines[0]):
        rest = lines[1:]
        s = next((x for x in rest if _ERR_KW.search(x)), rest[-1] if rest else '')
        return lines[0] + ': ' + s
    return lines[0]


def classify_error(tool, cat, text, cmd=''):
    t = text or ''
    head = t[:3000]
    low = head.lower()
    tail = t[-3000:]
    both = head + '\n' + tail
    # harness / permission layer
    if "doesn't want to proceed" in head or "doesn't want to take this action" in head or 'Request interrupted by user' in head:
        return 'permission:user-rejected'
    if 'temporarily unavailable' in head and 'auto mode' in head:
        return 'permission:classifier-unavailable'
    if 'auto mode classifier' in head or 'built-in Claude Code safety check' in head or re.search(r'Permission (to use|for this) .* (has been |was )?denied', head) or 'This command requires approval' in head:
        return 'permission:classifier-denied'
    if 'This agent is isolated in the worktree' in head:
        return 'sandbox:worktree-guard'
    if re.search(r'Blocked: (sleep|standalone sleep)', head):
        return 'wait:sleep-blocked'
    if 'Subagents should return findings as text' in head:
        return 'tool:subagent-wrote-report'
    if re.search(r'<tool_use_error>Blocked:|hook (blocked|denied|error|returned)|PreToolUse|blocked by (a )?hook', head):
        return 'permission:hook-blocked'
    if 'File has not been read yet' in head:
        return 'edit:not-read-first'
    if 'modified since read' in head:
        return 'edit:stale-read'
    if 'String to replace not found' in head:
        return 'edit:string-not-found'
    if re.search(r'Found \d+ matches of the string to replace', head):
        return 'edit:not-unique'
    if 'No changes to make' in head:
        return 'edit:no-op'
    if 'exceeds maximum allowed' in head or re.search(r'File content \(\d+ tokens\)', head) or 'too large' in low[:300]:
        return 'file:too-large'
    if 'InputValidationError' in head or 'Input validation error' in head or 'Invalid arguments for tool' in head or 'could not be parsed' in head or 'does not match required schema' in head:
        return 'tool:misuse-params'
    if 'No such tool available' in head:
        return 'tool:unknown-tool'
    if "hit your session limit" in head or 'rate limit' in low[:300] or 'Overloaded' in head or 'Out of credits' in head or re.search(r'\b(429|529)\b', head[:200]) or 'API Error' in head[:100]:
        return 'env:service-limit'
    if 'ENOSPC' in both or 'No space left on device' in both:
        return 'env:disk-full'
    # browser / computer-use
    if tool.startswith(BROWSER_PREFIXES) or tool.startswith('mcp__Claude_Browser'):
        if re.search(r'requires a prior|no read_page tree cached|ref map not initialized|call read_page first|Use `navigate` first|No site is open|not a valid file path|is no longer open|Tab cap reached|preview_stop takes|No server named|local file, not a web page|pinned to a local file|outside the viewport', head):
            return 'browser:precondition'
        if re.search(r'No preview is open|Preview not found|Preview tab', head):
            return 'browser:no-preview'
        if 'timed out' in low[:400]:
            return 'browser:pane-timeout'
        if re.search(r'denied or failed|Policy check in progress|ERR_|not accessible', head):
            return 'browser:navigation-denied'
        if re.search(r'javascript_tool failed|Failed to execute JavaScript|SyntaxError|TypeError|ReferenceError', head):
            return 'browser:js-error'
        if 'Port' in head and 'in use' in head:
            return 'env:port-in-use'
        if 'dev server exited' in head:
            return 'build:metro-bundler'
        return 'browser:other'
    if tool.startswith('mcp__'):
        if TIMEOUT_RX.search(head[:400]):
            return 'timeout:command'
        if re.search(r'ENOTFOUND|ECONNREFUSED|certificate|SSL|fetch failed|net::ERR', head):
            return 'network'
        return 'mcp:service-error'
    if 'Port' in head and 'in use' in head or 'EADDRINUSE' in both:
        return 'env:port-in-use'
    if HARNESS_TO_RX.search(head[:300]) and (tool == 'Bash' or tool in ('Monitor', 'TaskOutput', 'BashOutput')):
        return 'timeout:foreground-wait' if cat.startswith('wait-loop') else 'timeout:command'
    if 'File does not exist' in head or 'Path does not exist' in head or 'does not exist' in head[:200] and tool in ('Read', 'Edit', 'Write', 'Glob', 'Grep', 'NotebookEdit'):
        return 'file:not-found'
    if 'EISDIR' in head or 'Is a directory' in head[:300] or 'is a directory' in low[:300]:
        return 'file:is-directory'
    if tool in ('WebFetch', 'WebSearch'):
        return 'network'
    if tool == 'Bash':
        m = re.match(r'Exit code (\d+)', head)
        code = int(m.group(1)) if m else None
        body = '\n'.join(head.splitlines()[1:]) if m else head
        bl = body.lower()
        if 'bfs: error' in both:
            return 'shell:find-is-bfs'
        if re.search(r'(\(eval\)|zsh):(\d+:)? =\S* not found', both):
            return 'shell:zsh-equals-expansion'
        if re.search(r'(\(eval\)|zsh):(\d+:)? no matches found', both):
            return 'shell:zsh-glob-nomatch'
        if re.search(r'(\(eval\)|zsh):(\d+:)? (no such file or directory|command not found|permission denied): \S+ -?\S', both):
            return 'shell:zsh-no-word-split'
        if re.search(r'(\(eval\)|zsh):(\d+:)? (bad substitution|parse error|bad pattern|unmatched|event not found|unknown file attribute|bad math|number expected|no such user|bad option)', both):
            return 'shell:zsh-other'
        if re.search(r'invalid command code|illegal line count|illegal option|sed: -[eI]? ?\S*: No such file|sed: \d+: ".*": (unknown|extra|undefined)|unrecognized option|stat: illegal|date: illegal|xargs: illegal|grep: invalid option', both):
            return 'shell:bsd-vs-gnu-flags'
        if 'Operation not permitted' in both or 'sandbox' in bl[:500] and 'denied' in bl[:500]:
            return 'sandbox:not-permitted'
        if re.search(r'command not found|: not found\b|is not installed|No module named|Cannot find module|ERR_MODULE_NOT_FOUND|Unsupported engine|requires Node|node: bad option|env: \S+: No such file|not recognized as', both):
            return 'env:command-not-found'
        if re.search(r'device offline|no devices/emulators found|device \S* ?not found|more than one device|error: closed|adb: device|emulator-\d+\s+offline|Can\'t find service', both):
            return 'device:adb-offline'
        if re.search(r'INSTALL_FAILED|INSTALL_PARSE_FAILED|Failure \[', both):
            return 'device:install-failed'
        if re.search(r'CONFLICT \(|Merge conflict|would be overwritten|Your local changes|untracked working tree files|not possible to fast-forward|Not possible to fast-forward|non-fast-forward|needs merge|unmerged|index\.lock|working tree (is )?(dirty|not clean)|is already checked out|already exists and is not an empty', both):
            return 'git:conflict-or-dirty'
        if re.search(r'Could not resolve host|ENOTFOUND|ECONNREFUSED|ECONNRESET|ETIMEDOUT|Connection refused|Failed to connect|SSL|certificate|fetch failed|getaddrinfo|Network is unreachable|curl: \(\d+\)', both):
            return 'network'
        if re.search(r'BUILD FAILED|FAILURE: Build failed|Execution failed for task|\*\* BUILD FAILED \*\*|xcodebuild: error|Gradle build daemon disappeared|error: linker', both):
            return 'build:gradle-xcode-failed'
        if re.search(r'Unable to resolve module|bundling failed|Metro|Error: Cannot resolve|Transform error|Build failed with \d+ error|vite.*error|\[vite\]|next build', both, re.I):
            return 'build:metro-bundler'
        if re.search(r'Tests?:\s+\d+ failed|Test Suites?:.*failed|\bFAIL\b\s+\S+|AssertionError|\d+ failed|failed, \d+ passed|✕|FAILED \(|Error: expect\(', both):
            return 'test:failures'
        if re.search(r'error TS\d+', both):
            return 'test:tsc-errors'
        if re.search(r'Traceback \(most recent call last\)', both):
            return 'script:python-traceback'
        if re.search(r'^\s*(Syntax|Type|Reference|Range)Error\b|Uncaught|node:internal|at Object\.<anonymous>|UnhandledPromiseRejection', both, re.M):
            return 'script:node-error'
        if re.search(r'syntax error|unexpected (token|end of file|EOF)|unterminated|parse error', both, re.I):
            return 'shell:syntax'
        if re.search(r'No such file or directory|cannot access|can\'t open|cannot open|does not exist|not a directory|ENOENT', both):
            return 'file:not-found'
        if re.search(r'Permission denied|EACCES|EPERM', both):
            return 'sandbox:not-permitted'
        if re.search(r'^fatal: |^error: ', both, re.M) and re.search(r'\bgit\b', cmd):
            return 'git:other'
        if code in (124, 137, 143) or 'Killed' in both[:200]:
            return 'timeout:command'
        if code == 1 and len(body.strip()) < 3:
            return 'nonzero:benign-no-match'
        if code == 1 and re.match(r'^\s*(grep|rg|egrep|diff|cmp|test|\[|pgrep|git diff|ls)\b', strip_prefix(cmd)):
            return 'nonzero:benign-no-match'
        if re.search(r'\b(FAIL|failed|mismatch|regression|exceeds|over budget|not ok|assert(ion)?)\b', body[-600:], re.I):
            return 'nonzero:check-failed'
        if code is not None:
            return 'other:nonzero-exit'
    if '<tool_use_error>' in head and re.search(r'does not exist|not found', head):
        return 'file:not-found'
    if re.search(r'interrupted', low[:200]):
        return 'interrupted'
    return 'other'


# ------------------------------------------------------------------ prompt sketches (near-duplicate dispatch)
def sketch(text, k=128, w=5):
    words = re.findall(r'\w+', (text or '').lower())
    if len(words) < w:
        words = words + [''] * (w - len(words))
    hs = set()
    for i in range(0, max(1, len(words) - w + 1)):
        hs.add(int.from_bytes(hashlib.blake2b(' '.join(words[i:i + w]).encode(), digest_size=8).digest(), 'big'))
    return sorted(hs)[:k]


def jaccard_sketch(a, b, k=128):
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    union = sorted(sa | sb)[:k]
    inter = sum(1 for x in union if x in sa and x in sb)
    return inter / len(union) if union else 0.0


# ------------------------------------------------------------------ content helpers
NOTIF_RX = re.compile(r'<tool-use-id>(toolu_[A-Za-z0-9]+)</tool-use-id>')
STATUS_RX = re.compile(r'<status>(\w+)</status>')
CMDNAME_RX = re.compile(r'<command-name>/?([\w:.\-]+)</command-name>')
TS_RX = re.compile(r'"timestamp":"([^"]+)"')


def content_text(c):
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        out = []
        for b in c:
            if isinstance(b, dict):
                if b.get('type') == 'text':
                    out.append(b.get('text', ''))
                elif b.get('type') == 'image':
                    out.append('[image]')
                else:
                    out.append(str(b.get('content', '')))
        return '\n'.join(out)
    return str(c)


def outcome_of(wake_texts):
    """v1 heuristic: only when obvious from the coordinator's follow-up messages."""
    txt = '\n'.join(wake_texts or [])
    if re.search(r'\brevert(ed)?\b', txt, re.I) and re.search(r'\b(we|controller|coordinator)\b[^\n]{0,40}revert', txt, re.I):
        return 'reverted'
    if re.search(r'REQUEST CHANGES|fix round \d|Controller review[^\n]{0,80}fix', txt):
        return 'changes'
    if re.search(r'\bAPPROVE(D)?\b', txt):
        return 'approved'
    return None


TEST_PATH_RX = re.compile(r'(__tests__|\.test\.|\.spec\.|/tests?/|_test\.)')


# ------------------------------------------------------------------ digest
def digest_file(path, project, kind, meta=None, session=None):
    """Stream one transcript file; return a privacy-safe digest dict."""
    meta = meta or {}
    first = last = None
    events = []
    usage = {}
    wake_texts = []
    minutes = set()
    user_prompts = []      # timestamps of genuine owner prompts (main sessions)
    user_cmds = []
    last_assist_t = None
    owner_wait = 0.0
    title = None
    n_lines = n_bad = 0
    with open(path, errors='replace') as fh:
        for line in fh:
            n_lines += 1
            # cheap pre-filter; the parsed record's type is checked again below
            if not ('"assistant"' in line or '"user"' in line or 'queued_command' in line or 'custom-title' in line):
                continue
            try:
                o = json.loads(line)
            except Exception:
                n_bad += 1
                continue
            typ = o.get('type')
            if typ == 'custom-title':
                title = o.get('customTitle') or title
                continue
            if typ not in ('user', 'assistant', 'attachment'):
                continue
            if typ == 'attachment' and 'queued_command' not in line:
                continue
            t = o.get('timestamp')
            if not t:
                continue
            try:
                t = ts(t)
            except Exception:
                continue
            first = t if first is None else min(first, t)
            last = t if last is None else max(last, t)
            minutes.add(int(t // 60))
            if typ == 'attachment':
                a = o.get('attachment', {}) or {}
                if a.get('type') == 'queued_command':
                    p = str(a.get('prompt', ''))
                    m = NOTIF_RX.search(p)
                    if m:
                        st = STATUS_RX.search(p)
                        events.append((t, 'notif', (m.group(1), st.group(1) if st else None)))
                continue
            msg = o.get('message', {}) or {}
            c = msg.get('content')
            if typ == 'user':
                if isinstance(c, str):
                    if '<task-notification>' in c:
                        m = NOTIF_RX.search(c)
                        if m:
                            st = STATUS_RX.search(c)
                            events.append((t, 'notif', (m.group(1), st.group(1) if st else None)))
                    if kind == 'sub':
                        if not events and not wake_texts and 'prompt_seen' not in meta:
                            meta['prompt_seen'] = True
                        else:
                            k2 = 'resume-session-ended' if 'session ended' in c else ('resume-coordinator' if 'coordinator sent a message' in c else ('resume-bg-notification' if ('SYSTEM NOTIFICATION' in c or '<task-notification>' in c) else 'resume-other'))
                            if 'cut off mid-stream' in c:
                                k2 = 'api-cutoff'
                            events.append((t, 'wake', k2))
                            wake_texts.append(c[:3000])
                    else:
                        mc = CMDNAME_RX.search(c)
                        if mc:
                            user_cmds.append((t, mc.group(1)))
                        genuine = not (o.get('isMeta') or '<task-notification>' in c or 'SYSTEM NOTIFICATION' in c or c.startswith('<local-command') or c.startswith('<command-') or 'Caveat:' in c[:40])
                        if genuine or mc:
                            user_prompts.append(t)
                            events.append((t, 'wake', 'owner-prompt'))
                            if last_assist_t is not None and t > last_assist_t:
                                owner_wait += t - last_assist_t
                elif isinstance(c, list):
                    has_result = False
                    for b in c:
                        if not isinstance(b, dict):
                            continue
                        if b.get('type') == 'text':
                            tx = b.get('text', '')
                            if '<task-notification>' in tx:
                                m = NOTIF_RX.search(tx)
                                if m:
                                    st = STATUS_RX.search(tx)
                                    events.append((t, 'notif', (m.group(1), st.group(1) if st else None)))
                            elif kind == 'main':
                                mc = CMDNAME_RX.search(tx)
                                if mc:
                                    user_cmds.append((t, mc.group(1)))
                        if b.get('type') == 'tool_result':
                            has_result = True
                            tu = o.get('toolUseResult')
                            extra = {}
                            if isinstance(tu, dict):
                                if tu.get('interrupted'):
                                    extra['interrupted'] = True
                                if tu.get('timedOutAfterMs'):
                                    extra['timed_out'] = True
                                if tu.get('backgroundTaskId'):
                                    extra['bg_task'] = True
                            events.append((t, 'result', (b.get('tool_use_id'), content_text(b.get('content')), bool(b.get('is_error')), extra)))
                    if kind == 'main' and not has_result and not o.get('isMeta'):
                        txt = content_text(c)
                        if txt.strip() and '<task-notification>' not in txt and 'SYSTEM NOTIFICATION' not in txt and not txt.startswith('[Request interrupted'):
                            user_prompts.append(t)
                            events.append((t, 'wake', 'owner-prompt'))
                            if last_assist_t is not None and t > last_assist_t:
                                owner_wait += t - last_assist_t
            elif typ == 'assistant':
                last_assist_t = t
                u = msg.get('usage') or {}
                rid = o.get('requestId') or msg.get('id')
                if u and rid:
                    r = usage.setdefault(rid, dict(output=0, input=0, cache_read=0, cache_creation=0))
                    r['output'] = max(r['output'], u.get('output_tokens') or 0)
                    r['input'] = max(r['input'], u.get('input_tokens') or 0)
                    r['cache_read'] = max(r['cache_read'], u.get('cache_read_input_tokens') or 0)
                    r['cache_creation'] = max(r['cache_creation'], u.get('cache_creation_input_tokens') or 0)
                if isinstance(c, list):
                    for b in c:
                        if not isinstance(b, dict):
                            continue
                        if b.get('type') == 'tool_use':
                            events.append((t, 'use', (b, msg.get('id') or rid)))
                        elif b.get('type') in ('text', 'thinking'):
                            events.append((t, 'assist', None))
    events.sort(key=lambda e: e[0])
    uses = {}
    notif = {}
    for t, k, p in events:
        if k == 'use':
            uses[p[0].get('id')] = (t, p[0], p[1])
        elif k == 'notif':
            notif.setdefault(p[0], (t, p[1]))
    n_uses = len(uses)
    calls = []
    intervals = []
    dispatches = []
    skills = []
    bg = []
    bg_ids = {}
    n_results = 0
    for t, k, p in events:
        if k != 'result':
            continue
        n_results += 1
        tid, txt, iserr, extra = p
        if tid not in uses:
            continue
        t0, b, mid = uses.pop(tid)
        name = b.get('name', '?')
        inp = b.get('input', {}) or {}
        if not isinstance(inp, dict):
            inp = {}
        cat = classify(name, inp)
        cmd = inp.get('command') if name == 'Bash' else ''
        cmd = cmd if isinstance(cmd, str) else ''
        timeout = (bool(HARNESS_TO_RX.search(txt[:300])) and name in ('Bash', 'Monitor', 'TaskOutput', 'BashOutput')) or bool(extra.get('timed_out'))
        moved_bg = 'moved to the background' in txt[:600]
        rec = dict(u=h10(str(tid)), t=round(t0, 3), d=round(t - t0, 3), tool=name, tn=tool_norm(name), cat=cat, err=int(iserr),
                   to=int(bool(timeout or moved_bg)), bg=int(bool(inp.get('run_in_background'))), rlen=len(txt), mid=h10(str(mid)))
        if name == 'Bash':
            rec['fp'] = h10(norm_cmd(cmd))
            rec['sk'] = h10(skeleton(cmd))
            rec['head'] = cmd_head(cmd)
            rec['feat'] = bash_features(cmd)
            if rec['cat'].startswith('test:') and not R_TESTFOCUS.search(cmd):
                rec['feat'].append('fulltest')
            rec['tok'] = sorted(set(h10(x)[:6] for x in re.findall(r'[\w./-]+', cmd)[:60]))
            if moved_bg:
                rec['feat'].append('moved-bg')
            rec['feat'].extend(workaround_features(cmd))
            tmo = inp.get('timeout')
            rec['tmo'] = int(tmo) if isinstance(tmo, (int, float)) else None
            if rec['bg']:
                nt0 = notif.get(b.get('id'))
                rec['bgs'] = nt0[1] if nt0 else None
        elif name in ('Read', 'Edit', 'Write', 'MultiEdit', 'NotebookEdit'):
            fpth = str(inp.get('file_path') or inp.get('notebook_path') or '')
            rec['fh'] = h10(fpth)
            rec['fp'] = h10(fpth + '|' + str(inp.get('old_string', ''))[:500] + '|' + str(inp.get('offset')) + '|' + str(inp.get('limit')))
            rec['sk'] = rec['fp']
            rec['ext'] = os.path.splitext(fpth)[1][:8]
            rec['testfile'] = int(bool(TEST_PATH_RX.search(fpth)))
            rec['planfile'] = int(bool(re.search(r'plan|spec|design|brief', fpth, re.I)) and fpth.endswith('.md'))
            rec['abs'] = int(fpth.startswith('/'))
            if name == 'Read':
                rec['ranged'] = int(inp.get('offset') is not None or inp.get('limit') is not None)
        else:
            rec['head'] = name.split('__')[-1][:30]
            try:
                s = json.dumps(inp, sort_keys=True)[:3000]
            except Exception:
                s = str(inp)[:3000]
            rec['fp'] = h10(name + s)
            rec['sk'] = h10(name + re.sub(r'\d+', 'N', s))
        if name in ('Grep', 'Glob'):
            rec['feat'] = ['grep-tool' if name == 'Grep' else 'glob-tool']
        if iserr or rec['to']:
            ec = classify_error(name, cat, txt, cmd) if iserr else ('timeout:foreground-wait' if cat.startswith('wait-loop') else 'timeout:command')
            rec['ec'] = ec
            rec['es'] = redact(sig_line(txt), 120)
            if extra.get('interrupted'):
                rec['intr'] = 1
        if name in ('Agent', 'Task'):
            pr = str(inp.get('prompt') or '')
            dispatches.append(dict(t=rec['t'], id=b.get('id'), desc=redact(inp.get('description') or '', 60), dh=h10((inp.get('description') or '').strip().lower()),
                                   sk=sketch(pr), plen=len(pr), ph=h10(pr), type=inp.get('subagent_type'), bg=int(bool(inp.get('run_in_background'))), err=int(iserr),
                                   fx=int(bool(re.search(r'fix round|re-?review|request(ed)? changes|round \d|\bretry\b|\bresume\b|continue where|second attempt|try again|previous (agent|attempt|run)', pr, re.I))),
                                   wt=int(inp.get('isolation') == 'worktree')))
        if name == 'Skill':
            skills.append(dict(u=rec['u'], t=rec['t'], skill=str(inp.get('skill') or '?')[:60], idx=len(calls), err=int(iserr)))
        if rec['bg'] and name == 'Bash':
            nt = notif.get(b.get('id'))
            bg.append(dict(t=rec['t'], cat=cat, head=rec.get('head', ''), dur=(round(nt[0] - t0, 1) if nt else None), status=(nt[1] if nt else None)))
            bg_ids[b.get('id')] = cat
        calls.append(rec)
        intervals.append((t0, t, rec))
    orphan = len(uses)
    # reaction gaps (time from a call's result to the next tool_use in this file)
    use_times = sorted(e[0] for e in events if e[1] == 'use')
    for r in calls:
        end = r['t'] + r['d']
        i = bisect.bisect_right(use_times, end)
        r['gap'] = round(use_times[i] - end, 1) if i < len(use_times) else None
    # exclusive attribution (v1)
    excl = collections.Counter()
    if first is not None:
        notif_set = {}
        for nid, (nt, _st) in notif.items():
            if nid in bg_ids:
                notif_set[nt] = bg_ids[nid]
        wakes = {e[0]: e[2] for e in events if e[1] == 'wake'}
        cuts = sorted(set([first, last] + [i[0] for i in intervals] + [i[1] for i in intervals] + [n for n in notif_set if first <= n <= last] + list(wakes)))
        acts = sorted(set(e[0] for e in events if e[1] in ('use', 'assist', 'result')))
        iv = sorted(intervals, key=lambda x: x[0])
        starts = [x[0] for x in iv]
        for a, b2 in zip(cuts, cuts[1:]):
            if b2 <= a:
                continue
            mid = (a + b2) / 2
            j = bisect.bisect_right(starts, mid)
            active = [r for (s, e, r) in iv[max(0, j - 400):j] if s <= mid < e]
            L = b2 - a
            if active:
                for r in active:
                    excl[r['cat']] += L / len(active)
            else:
                i = bisect.bisect_left(acts, b2) - 1
                lastact = acts[i] if i >= 0 and acts[i] > a else a
                excl['model'] += lastact - a
                idle = b2 - lastact
                if b2 in wakes:
                    excl['dormant:' + wakes[b2]] += idle
                elif b2 in notif_set:
                    excl['bg-wait:' + notif_set[b2]] += idle
                else:
                    excl['model'] += idle
    tokens = {k: sum(r[k] for r in usage.values()) for k in ('output', 'input', 'cache_read', 'cache_creation')} if usage else None
    return dict(
        v=PARSER_VERSION, project=project, kind=kind, session=session, agent=meta.get('agent_id'),
        desc=redact(meta.get('description') or (title if kind == 'main' else '') or '', 80),
        agent_type=meta.get('agentType'), model=meta.get('model'), tool_use_id=meta.get('toolUseId'),
        first=first, last=last, wall=(last - first) if first else 0, excl={k: round(v, 2) for k, v in excl.items()},
        tokens=tokens, n_requests=len(usage), n_lines=n_lines, n_bad=n_bad, n_uses=n_uses, n_results=n_results,
        orphan_uses=orphan, calls=calls, dispatches=dispatches, skills=skills, bg=bg,
        minutes=sorted(minutes), user_prompts=len(user_prompts), up_t=[round(x, 1) for x in sorted(user_prompts)], owner_wait_s=round(owner_wait, 1),
        user_cmds=[dict(t=round(t, 1), cmd=c[:60]) for t, c in user_cmds],
        outcome=outcome_of(wake_texts) if kind == 'sub' else None,
    )


# ------------------------------------------------------------------ discovery + cache
def discover(root):
    """Yield (path, project, kind, session, meta_path) for every transcript under root."""
    for d in sorted(os.listdir(root)):
        pd = os.path.join(root, d)
        if not os.path.isdir(pd):
            continue
        proj = project_of(d)
        for dirpath, _dirs, files in os.walk(pd):
            for f in files:
                if not f.endswith('.jsonl'):
                    continue
                p = os.path.join(dirpath, f)
                if os.sep + 'subagents' in dirpath:
                    sess = os.path.basename(os.path.dirname(dirpath))
                    mp = p[:-6] + '.meta.json'
                    yield p, proj, 'sub', sess, (mp if os.path.exists(mp) else None)
                elif dirpath == pd:
                    yield p, proj, 'main', f[:-6], None
                else:
                    # other nested transcripts (e.g. workflows) are counted as subagents without meta
                    yield p, proj, 'sub', os.path.basename(dirpath), None


def cached_digest(path, project, kind, session, meta_path, cache_dir):
    st = os.stat(path)
    key = '%s|%d|%d|%s' % (path, st.st_size, int(st.st_mtime), PARSER_VERSION)
    cp = os.path.join(cache_dir, h10(path) + hashlib.blake2b(path.encode(), digest_size=6).hexdigest() + '.json')
    if os.path.exists(cp):
        try:
            with open(cp) as fh:
                d = json.load(fh)
            if d.get('_key') == key:
                return d, True
        except Exception:
            pass
    meta = {}
    if meta_path:
        try:
            with open(meta_path) as fh:
                meta = json.load(fh)
        except Exception:
            meta = {}
    meta['agent_id'] = os.path.basename(path)[:-6]
    d = digest_file(path, project, kind, meta, session)
    d['_key'] = key
    d['mtime'] = st.st_mtime
    tmp = cp + '.tmp'
    with open(tmp, 'w') as fh:
        json.dump(d, fh, separators=(',', ':'))
    os.replace(tmp, cp)
    return d, False
