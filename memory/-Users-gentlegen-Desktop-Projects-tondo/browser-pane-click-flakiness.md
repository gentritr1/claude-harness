---
name: browser-pane-click-flakiness
description: Browser-pane physical clicks can time out / dispatch late while the pane is hidden — verify interactions via JS dispatch
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 98212e7f-52fe-4101-89d2-52f2f68ae4e0
  modified: 2026-08-14T22:32:12.859Z
---

During 2026-08-15 verification, `computer left_click` calls on the Browser pane twice timed out ("pane currently hidden") and the clicks dispatched late or not at all, which briefly looked like an app bug (armed card that never committed).

**Why:** the pane defers input dispatch while hidden; a silent timeout is not proof the event fired, and a late dispatch can land between screenshots.

**How to apply:** when a pane click times out, do not debug the app from that evidence. Re-verify the interaction deterministically with `javascript_tool` (`element.click()`) and read DOM state in the same evaluation; use physical clicks only for coordinate/hit-target verification when the pane is responsive.

**2026-08-20 extension — the pane can also PAINT wrong, not just click wrong.** During the
Stone Oven review the pane rendered the live game's top card as an anchovy-blue flip while
inline style + getComputedStyle both said pepperoni red; no filters, blends, pseudos,
animations, duplicate nodes, or overlays existed (all checked). Moving the element 220px
repainted it red; moving it back repainted it blue. The identical outerHTML + stylesheet in
REAL Chrome rendered red, matching computed style. Verdict: pane compositor artifact, zero
app bug. **Rule: a "wrong color/paint" seen only in the pane, where computed style disagrees
with pixels, must be re-checked in real Chrome (claude-in-chrome) before blaming the app.**

**2026-08-21 — a HIDDEN or unfocused surface silently stops animations.** Chasing an
apparent flight-ghost regression I measured 0 travel-card ghosts over two 12s windows in a
real bot game, while the game state advanced normally (ribbon showed bot plays, hand count
dropped). Cause: `document.visibilityState === "hidden"` on the pane tab — background tabs
throttle rAF, so animation code never runs even though sockets and rendering state do.
Fronting the tab gave 2 bot flights at 1.6s and 3.9s immediately.
**Rules:** (1) assert `document.hidden === false` before concluding ANY animation is missing;
(2) flight ghosts are appended to `document.body`, NOT `#stage` — a MutationObserver on the
stage sees nothing; (3) an unfocused surface also freezes CSS transitions/WAAPI mid-flight,
so call `getAnimations().finish()` before asserting settled sizes; (4) `resize_window` sets
the OUTER window in real Chrome — 1800x876 outer was 1800x699 inner, which silently drops
into the phone media band.

