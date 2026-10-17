---
name: perf-architecture-and-evidence
description: "Dense-board perf architecture (retained native view + bounded feedback) and where its evidence actually comes from (API 31 emulator only, iOS unmeasured)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 64b158b4-b89c-4265-98a1-f540d8346275
  modified: 2026-09-16T15:15:20.050Z
---

Perf commit 0a1df94 (2026-09-01) moved the static arrow field into a retained
native view (`modules/arrows-board`, Kotlin onDraw + Swift draw(_:)), fed once
per level with a text geometry payload plus an O(n) `visibleMask` string;
pan/zoom is a Reanimated transform on the parent; feedback (hint/shake/2 exit
slots, 180 ms) lives on a Skia overlay. Full ledger: `docs/performance-optimization-knowledge-base.html`.

**Evidence provenance:** every frame/memory number (11.45 ms p95, 0.19% jank,
5.62 MB tail growth) came from `npm run perf:android` on an **API 31 AVD with
host GPU**, release build, level 3827 (39x39, 250 arrows). No physical Android
device run and no iOS soak exist as of 2026-09-01; the doc itself lists these
as open gaps.

**Why:** the emulator's GPU is the Mac's; a low-end phone can miss the same
gate. iOS `draw(_:)` on a board-sized view allocates bounds x scale backing
store (39x39 board = 1560 pt -> 4680 px @3x ~= 88 MB), the exact failure mode
the SVG path was fixed for on Android.

**How to apply:** treat "perf fixed" claims as emulator-only until a phone
number exists; any review of `ArrowsBoardView.swift` must check layer backing
size, not just draw code. See [[review-scars]].

**iOS plan:** `docs/IOS_BOARD_PLAN.md` (written 2026-09-01) — swap `draw(_:)`
for two CAShapeLayers, acceptance gates A1–A5, needs ≥20 GB free disk to build.

**2026-09-01 follow-up:** exit feedback unified to a native slither at every
density (Android Canvas DashPathEffect driven from onDraw + frame clock; iOS
CAShapeLayer lineDashPhase, uncompiled). Duration scales with on-screen travel
(180–320 ms, `exitTrailDurationMs`), pinned to 180 in benchmark builds.
Harness gotchas: it sets all three animation scales to 0. `animator_duration_scale 0`
(a) made the old ValueAnimator launch finish instantly (the old "exit" number
measured nothing); separately (b) Reanimated 4.5.1 reads reduced motion from
`Settings.Global.TRANSITION_ANIMATION_SCALE == 0` (NativeProxy.kt:324-329),
once at app start — so harness exit runs measure the fade-only variant. To
capture real motion, set all three scales to 1, force-stop, relaunch, read back. `adb shell input tap` cell mapping must use
bottom = max(a11y bottom, 3120) like `findBoardBounds`. Shell needs
`ANDROID_HOME=~/Library/Android/sdk` for gradle. Exit phase after change:
p95 13.3 ms / p99 15.1 / 0% jank, 120 frames = 10 runs × 12 (reconciled).

**2026-09-02 feedback tuning:** the Unity whoosh measured peak -20.6 dBFS,
centroid 445 Hz, 99 ms to peak: 14 dB under the fail thud and mostly below
what a phone speaker reproduces. Replaced by an 8-step pentatonic pop ladder
(`pop0..7.wav`, -6 dBFS, 1.6 ms attack) driven by `src/ui/exitCombo.ts`
(1.2 s window). Android exit haptic was CLOCK_TICK = EFFECT_TEXTURE_TICK
(weakest, per AOSP HapticFeedbackVibrationProvider); now CONTEXT_CLICK =
EFFECT_TICK. iOS: selection -> UIImpactFeedbackGenerator(.light) with
intensity 0.6..1.0 by step. Emulator proof of haptic dispatch: logcat
`android.hardware.vibrator-service.example: Vibrator perform` once per tap.
Audible output and feel remain device-only checks. Listening demos live in
the scratchpad only; regenerate with `node scripts/generate-sfx.js`.

**2026-10-01:** the owner's "Arrows Performance Field Guide" now lives in the repo: docs/performance/field-guide.md (Markdown) + field-guide.html (original). AGENTS.md and docs/engineering-lessons.md point to it — read it before any rendering/perf work.
