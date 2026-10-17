---
name: polish-t11-gate-gotchas
description: "POLISH-T11 (2026-09-25) whole-round perf gate - libhwui aborts from gfxinfo/SF resets, stray taps after a crash, idle-gap \"dropped\" artefact, device-clock dumps, duplicate detached chains, PRE-native scratch build recipe"
metadata:
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-09-25T11:22:48.856Z
---

- API 31 emulator libhwui JankTracker aborts ("Impossible totalDuration ... gpuComplete=-1", "Impossible dequeue
  duration") hit the app 3x in ~170 runs when `dumpsys gfxinfo reset` / `SurfaceFlinger --latency-clear` ran during
  continuous drawing (2 of 6 runs with SF clears). After the crash, scripted taps landed on the launcher (opened Google
  Photos). Rule: check `mCurrentFocus` is the app before every injected input (t11lib guard()); keep SF capture opt-in.
- T10Input app_process exits ~0.85 s after its UP: a host sleep after it dumps late and HWUI's 120-row history can drop
  a window's first frames. Time dumps on the device clock (read /proc/uptime, sleep the remainder).
- POLISH-T12's reconciliation ("gaps < 100 ms = dropped") counts idle pauses at animation boundaries (entrance end ->
  first star ~100 ms; gesture ends) as dropped frames: it produced a false REGRESSES (13/s) on the win entrance. Report
  1-2-refresh gaps separately; check gap context before calling a drop.
- Loaded host (load 4-7) -> emulator buffer-stuffed mode: every continuous animation reads RT ~16 ms / total 20-30 ms
  while SF still presents every refresh. ">16.7 ms" then counts latency, not drops; use late-episode starts, 1-2 gap
  skips and >33 ms frames.
- A nohup/& waiter started from a Bash tool call can survive although `ps | grep` missed it -> two chains drove the
  device at once. Use run_in_background only, and check for duplicates by PID tree before starting a chain.
- PRE-native build without checkout: `git archive <sha>` to scratch, `cp -cR node_modules` (APFS clone) then delete
  node_modules/*/android/{build,.cxx} in the clone (CMake absolute paths), symlink credentials/, `expo prebuild
  --clean --no-install` (android/ identical to repo's), full gradle 3 min, ~2 GB new blocks. Native .text identical to
  the original except librnskia __FILE__ paths.
- Result: no scenario regressed; META_LEVEL_TRANSITION Next exposure (6/30 vs 0/30 transitions with a >33 ms frame,
  host stalls) and META_PRESS_SPRING ~78-frame tail left as owner calls. Report: docs/next-level/reports/POLISH-T11.md.
