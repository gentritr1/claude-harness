---
name: admob-b-emulator-gotchas
description: ADMOB-B (2026-09-24) — reaching an interstitial on the emulator, solver-tap calibration limits, stray taps click through test ads, release has no ad logs
metadata:
  type: project
---
- Interstitial "due" on emulator: a loss counts toward pacing; clear a level by adb-tapping `Board.findHint()` order from `LevelGenerator.generate(i)` (boards 20x20/21x21: cell=1440*0.94/n, board centre y=1731 px, calibrated on the app's own hint arrow). The same calibration FAILED on level 3 (37x37 triangle): hearts ran out and blind taps clicked through a TEST rewarded ad (3 aclk lines). Rule: screenshot between tap batches; stop the moment state diverges.
- Release build prints only `[ads] AdMob initialize resolved; unitSet=…` + `I Ads: This request is sent from a test device` (one per unit) — no pacing/telemetry logs, app not debuggable → counter reset proven behaviourally (shown at due, not shown at count 1).
- `uiautomator dump` fails ("could not get idle state") while the board animates; use screenshots.
- Test-flag vs owner-ID proof: owner table guarded by `EXPO_PUBLIC_ADMOB_TEST_ADS==='1' ? null : {…}` folds out of the minified bundle; positive control = flag-unset export:embed --reset-cache + hermesc.
