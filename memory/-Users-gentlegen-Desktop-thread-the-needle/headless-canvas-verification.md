---
name: headless-canvas-verification
description: How to verify this Canvas game in the Browser pane where rAF is frozen and the compositor is flaky
metadata: 
  node_type: memory
  type: project
  originSessionId: c8dea768-0576-4c80-a808-455bfec9c3e0
---

The Browser pane loads the game with `document.visibilityState === "hidden"`, so `requestAnimationFrame` NEVER fires — the game loop does not advance on its own. Verification recipe (built 2026-07-13):

- Open `http://localhost:3000/?debug=1` → `window.__ttn` exposes `state`, `player`, `metrics`, `step(dt, skipRender)`, `render()`, `setInput(held)`, `start()`, `setNowDate(iso)`.
- Drive runs with `step(1/60, true)` (skipRender — software rendering every step is >30s slow and times out javascript_tool), then `t.render()` once before a screenshot.
- `?debug=1` also creates the 2D context with `willReadFrequently: true` — software raster works while hidden; the default GPU context draws nothing (canvas stays black) when hidden.
- Compositor for CDP screenshots: works on a tab freshly opened by `preview_start`; sometimes survives `navigate`, sometimes goes permanently black (then `preview_stop` + `preview_start` for a fresh tab). If viewport reads 0x0, call `resize_window` then `dispatchEvent(new Event("resize"))`.
- Autopilot pattern that plays well: nearest unchecked obstacle ahead; expansion gate → release; needle → hold when center distance < 420px. Reaches 30+ gates.
- `localhost` and `127.0.0.1` are DIFFERENT localStorage origins — persisted state does not carry across.

Related: [[retention-v1-status]]
