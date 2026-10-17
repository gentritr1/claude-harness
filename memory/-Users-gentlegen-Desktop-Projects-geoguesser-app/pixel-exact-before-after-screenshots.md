---
name: pixel-exact-before-after-screenshots
description: How E1b-1 got pixel-identical flag-OFF before/after screenshots on the AVD and on expo web (instrument self-checked with repeat runs)
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-16T19:43:00.280Z
---

Proving "flag OFF is unchanged" by pixel diff works if the instrument is deterministic first:

- **Device:** build the BEFORE QA APK from the clean tree, keep a copy. `settings put global
  animator_duration_scale 0` (+ transition/window) freezes the hero loops and entering animations;
  SystemUI demo mode fixes the clock. Capture only when two screencaps 1.5 s apart are identical.
  Two BEFORE runs were 0 px apart. Mask the status bar (rows < 100 at 3x): each demo-mode `network`
  broadcast adds another icon. Restore the settings after (animator_duration_scale was unset → `settings delete`).
- **Web:** headless Chrome over CDP (node --experimental-websocket on Node 20) with
  `Emulation.setEmulatedMedia prefers-reduced-motion: reduce` and `--disable-gpu
  --disable-gpu-compositing --run-all-compositor-stages-before-draw --disable-threaded-animation
  --disable-checker-imaging --disable-partial-raster --disable-lcd-text`. Without those flags two
  identical runs differed (±2 on scaled images, up to 50 in blurred shadows); with them, 0 px.
  RN-web's ActivityIndicator is a CSS animation reduced motion does not stop — its phase can differ.
  Stores are reachable without a source harness: `__r.getModules()` → find the module whose
  exports have `useGameStore`.
- **Taps:** prove hit-testing with real input (CDP `Input.dispatchMouseEvent` / adb taps) plus a UI
  dump before and after, and a negative control (taps elsewhere must not open the QA panel).
- A cold-booted AVD on a loaded host showed "Process system isn't responding" every few seconds;
  `adb reboot` cleared it.
