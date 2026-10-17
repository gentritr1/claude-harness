---
name: lane-b-web-verification
description: "How to verify Lane B UI on Expo web — Skia wasm not served, GH ignores synthetic drags"
metadata: 
  node_type: memory
  type: project
  originSessionId: 85382d6a-d358-472c-865f-39a2e4ea8336
---

Lane B web-preview verification playbook for Lucky Shelf (learned B-M1, 2026-07-06):

- **Skia-on-web wasm is NOT served in this dev env.** CanvasKit's emscripten
  `abort()` escapes try/catch as an uncaught error and redboxes web. The scene is
  built so the Skia canvas is a swappable layer: `WEB_SKIA_ENABLED=false` in
  `src/juice/skiaWeb.ts` gates it, and `SkiaShelfFrame` is required native-only in
  `ShelfScene.tsx` (never re-export it from the juice barrel or the skia module
  auto-inits on web). Web uses the RN `FallbackFrame`. **Skia visuals are
  device-verify-only** until the wasm is served.

- **react-native-gesture-handler ignores synthetic PointerEvents.** You cannot
  drive a Pan drag from `preview_eval` — grab won't activate (zIndex stays 1).
  What DOES work: `preview_click` (trusted CDP input) fires grab→release cleanly;
  use it to prove the gesture pipeline has no worklet error. Full pan/drop **feel**
  is verified by the human-relay device recording, by design.

- **Verify idle motion by sampling transforms**, not screenshots: walk up from a
  glyph to the ancestor whose computed `transform !== 'none'`, sample twice ~700ms
  apart. Breathing oscillates scale within 1.5%; reduced-motion freezes it to
  `matrix(1,0,0,1,0,0)`. Reduced-motion persists only across **client-side** nav
  (zustand store), not `location.href` hard reloads.

- **`preview_console_logs` buffer persists across `location.href` reloads** — it
  shows stale deprecation warnings (`props.pointerEvents`, `shadow*`) even after a
  fix bundles in, so the count never drops and looks like the fix failed. To verify
  a warning is actually gone: on the loaded page, monkey-patch `console.warn` to
  count matching messages, then trigger the re-render **without navigating** (a full
  nav resets the JS context and loses the patch). Fresh count 0 = clean. (Learned
  B-M2 fixing R-25 web shadows + the cascade `pointerEvents` props.)

- **Cascade timing on web:** goldens are ~6–13 events × 260 ms, so transient visuals
  (ruleFire arrows ~180 ms, count-ups) can't be frozen by `preview_screenshot` — the
  round-trip outruns them. Persistent state (row aura + `×mult` label, final tags,
  dayTotal slam, combo banner) screenshots fine; arrows/haptics are device-recording
  material. Pure cascade semantics (R-6 beneficiary etc.) are locked in
  `src/juice/cascade/cascadeState.test.ts` instead — verify the trace math there, the
  motion on device.

- **The tray drop can't be driven on web at all** (M3, 2026-07-07). The delivery
  tray uses the same `Gesture.Pan`; a trusted `preview_click` on the tray item's
  `data-testid` fires grab→release but the Pan never activates a placing `onEnd`,
  and synthetic PointerEvents are ignored. Consequence: you cannot place the
  drafted item on web, so anything gated behind placement — notably the **run.tsx
  cascade overlay end-to-end** (scrim over arrange HUD, snapshot header, Collect
  routes) — is **device-verify-only**. Verify the overlay CONTENT instead via the
  cascade-harness (identical `CascadeLayer`), which auto-plays to done.
- **Verify visuals with computed values, not screenshots** (worked well M3):
  aura gold band = `rgb(255,217,160)` @ opacity 0.30 (0 teal elements left);
  combo dock = `transform matrix(0.58,…,+102,-4)` @ opacity 1; vanish puff =
  sample the coupon wrapper opacity 1→0 while scale 1→1.35 over ~300 ms.

- Ports 8090/8091 are often held by parallel sessions; added an `expo-web-b3`
  config on **8092** to `.claude/launch.json`. See [[lucky-shelf-env]] for the
  Node/pnpm quirks.
