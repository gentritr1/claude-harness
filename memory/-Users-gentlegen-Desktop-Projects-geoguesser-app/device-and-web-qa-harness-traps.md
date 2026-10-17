---
name: device-and-web-qa-harness-traps
description: "Four QA-harness traps hit in E1b-3 (2026-09-17): flag override persists in the CDP Chrome profile, a timed-out adb install kills the launched app, reduced motion is read at app start, test-ad height moves the summary"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-30T20:32:03.228Z
---

Each of these made evidence look valid when it was not, during E1b-3's result/summary QA.

1. **Web: the art_v2 override survives between CDP runs.** The E1b-2/E1b-3 harness (`cdp.mjs`) reuses
   `--user-data-dir=<plan dir>/chrome-profile`; flag overrides live in localStorage, so a plan that never sets
   art_v2 inherited ON from the previous ON run. The "OFF" capture was ON and still "differed" as expected of a
   sensitivity check. Fix: `rm -rf chrome-profile` before every run, and print `__flags.getFlagSnapshot().art_v2`
   in every plan and check the log.
2. **Device: `timeout 30 adb install -r` cut the install off.** The package manager finished ~5 s later, after
   `am start`, and the package update killed the freshly launched app (focus back on the launcher, no crash log).
   Fix: long install timeout, then prove the installed APK: `pm path` + `sha256sum` on device equals the local file.
3. **Reanimated reads reduced motion when the app starts.** Setting animator_duration_scale back to 1 while the app
   runs does not bring count-ups or bursts back; a recording needs a cold start with animations on (and no
   uiautomator dumps on animated screens — tap known coordinates, prove each state by a log line).
4. **Test banners change height between mounts** (320x50, 468x60, adaptive creatives), which moves GameSummary's
   vertically centred content. For pixel diffs capture the summary with Wi-Fi and data off (no fill; check the dump
   has no android.webkit.WebView), and take one online capture separately for the layout with an ad.

5. **The AVD's clock runs behind the host's** — ~19.9 s on 2026-09-30, and it drifts, so the offset is not a constant
   you can hard-code. Any duration computed as `host_stamp − app_stamp` (the app logs device time in `mount=` / `at=`)
   is wrong by that offset, which silently corrupted two intermediate results in B1-3's device pass before it was
   caught. Fix: take BOTH ends from device time — `adb shell date +%s%3N`, or logcat's own timestamps — and never
   subtract a `date` run on the Mac from a number printed by the app. Measure the offset once per session and print
   it beside any timing table. **Any earlier B1/E2 device timing that mixed the two clocks should be re-checked.**
6. **A logcat line can vanish.** One QA probe line in ~20 never reached logcat although the reveal ran and was
   dumped (B1-3 device pass, batch 13). Reconcile the number of captured lines against the number of runs and report
   the shortfall; never treat "n lines" as "n runs".

**How to apply:** any before/after pixel proof on web or device: fresh profile + logged flag value per run, hash-verified
installs, cold start for motion, offline for screens with an AdBanner. For any TIMING claim: both stamps from the same
clock, and a line count reconciled against the run count. E1b-3's scripts are in
docs/plan/evidence/e1b-3/device/scripts and web/harness; B1-3's in docs/plan/evidence/b1-3.
Related: [[pixel-exact-before-after-screenshots]], [[seed-store-from-browser-for-visual-qa]], [[avd-stale-global-proxy]].

2026-10-07: an unscoped `grep "FATAL EXCEPTION"` over logcat failed a clean trip. The FATAL was `app_process`
(the `uiautomator dump` CLI, thread UiAutomation, "Bad file descriptor"), not the app. Scope crash checks to
`Process: com.snaxxtech.geoguesser` plus ` E ReactNativeJS` plus an unchanged app pid. Prove the scoped check catches
injected lines before trusting a 0 ([[every-gate-we-write-ships-a-silent-pass]]).

2026-10-07/08, three more traps that each gave a false result:
- **uiautomator clips nodes to their ScrollView:** a node below the fold reports its bottom AT the viewport edge
  (Modes [1723..1680], a negative height), so "row bottom <= banner top" passed the known failure. Require positive
  normal heights (scripts/home_metrics.py) and run the gate on the pre-fix dump first.
- **The IME is a separate window, absent from the dump.** Gboard's "Try out your stylus" onboarding and stylus
  toolbar (after adb input) both passed a dump-based keyboard check, and the app logged keyboard height=-24. Judge
  the keyboard from the screenshot (kb_top.py), and set `secure stylus_handwriting_enabled 0` for the run, then
  delete it.
- **Never edit a zsh script while it runs:** zsh reads it incrementally, and the shifted bytes broke the rest of a
  sound run. Also: `$0` inside a zsh function is the function name, so capture SD=${0:A:h} at the top; use
  `grep -F` for "[mode]"-style log lines (the brackets are a regex class); on API 36 get the uid from
  `pm list packages -U`, since `dumpsys package` has no userId=.
- **A buffered QA log line is not a trigger** (ART-4b, 2026-10-08). The `[globe] spin start` line used netLog with
  flush=false, so it printed at settle, 37-40 ms before the settle line. Harness steps that waited on it to tap Menu or
  HOME "mid-spin" acted AFTER the spin: the results were void, and so were gfxinfo windows built from those logcat times.
  Before using a log line as a trigger or a window edge, confirm it is flushed at once (or carries its own UI
  timestamp), and check its spacing against the event's duration.
- **QA panel rows whose label carries a value** ("Spin deadline (QA only): default (100 ms)") need a prefix match.
  Fast 600 ms swipes fling past a 3-row block between dumps; use slow, short swipes (70%->45%, 400 ms) and scroll to the
  top first. The panel shows art_v2-gated rows only after art_v2 was read at a start, so restart before looking for them.
- **Recording the AVD (2026-10-08):** `adb emu screenrecord start` (host side) FROZE on the QA-panel frame for 6 s while
  the logged spin ran underneath, in both takes. Unusable. On-device `screenrecord` shows the motion but its encoder
  costs frames (a 44/44 spin read 32/44 while recording). Judge smoothness from the frame counters, judge the look from
  on-device recordings, and have the owner judge feel on a phone.

- **2026-10-08 test-runner collision:** `scripts/test.cjs` deletes `.check/test` when it starts. So two runs in one worktree corrupt each other (10 bogus ENOENT failures came from my flake loop overlapping a reviewer's run). Check `pgrep -fl scripts/test.cjs` first, and give each reviewer or flake loop its own worktree, or serialise.
