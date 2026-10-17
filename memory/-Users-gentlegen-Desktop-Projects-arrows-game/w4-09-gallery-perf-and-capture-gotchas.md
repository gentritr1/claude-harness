---
name: w4-09-gallery-perf-and-capture-gotchas
description: W4-09 (2026-09-25) - emulator buffer-wait mode fakes "missed deadlines"; unequal-protocol A/B/A gave a non-replicating +28 ms; level-300 fold = 26/26; capture-diag markers
metadata:
  type: project
---
- framestats on emulator-5556 is bimodal: whole windows where DequeueBufferDuration ~14 ms, frames end ~20 ms after vsync, every frame "missed" but no vsync skipped. Report app work (UI HandleInput/AnimationStart->SyncQueued + render SyncStart->SwapBuffers) beside duration; never quote "missed" alone.
- A/B/A blocks where only the ON runs also did extra steps (gallery open, scroll, screencap) before the next force-stop produced mount max +28 ms p=0.001 that did not replicate under an equal protocol (alternating 3-run blocks, 24 v 24). Keep arm protocols identical; measure extra flows in separate runs.
- Collection: levels 1-168 already cover all 26 catalogue shapes, so any fold >= 168 levels is 26/26 (use level 50 = 17/26 for a mixed wall).
- EXPO_PUBLIC_CAPTURE_DIAG=1 logs `[capture-diag] ... screen=<name>` on every screen change: free logcat markers aligned with framestats (no instrumentation patch). Driver: artifacts/W4-09/scripts/galleryshot.mjs (seed via su sqlite3 between force-stop and launch).
- zsh does not word-split `$G args` or `set -- $x` (again): write multi-step device scripts as bash files.
- Fix round 1 (2026-09-25): react-native-svg Android SvgView rasterises EACH Svg into its own bitmap in onDraw (SvgView.java drawOutput) -> many small Svgs = slow first frame; one Svg with translated Paths cut the gallery mount frame 69 -> 41 ms (n=24). Moving Paths into one Svg shifts edges at fractional densities unless origins are snapped like Yoga (round each relative offset half-up): 0 px at 3.0, 14k px at 3.5 until snapped.
- Leaving the MENU logs Reanimated `synchronouslyUpdateUIProps failed for tag N` (RetryableMountingLayerException, ~90-line stack trace each, on the UI thread in the next screen's mount frame) in ~2/3 of exits (Play->game too; seen since W0-02). It inflates the next screen's first frame (29 -> 48 ms). Split perf by its presence before blaming the new screen.
- Mount frame: identify from framestats (first frame with DrawStart->SyncQueued >= 1 ms after the tap), not from a useEffect marker (can land one frame late).
