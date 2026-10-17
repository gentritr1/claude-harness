---
name: annex-scene-opacity-strand
description: "Scene plate went black on site re-entry: entry-animation opacity ramp + fill:both stranded at 0% frame"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0b1a5b43-8b07-44a8-89d7-cc7036f27cf1
  modified: 2026-07-24T17:05:25.808Z
---

Bug (fixed 2026-07-24, commit 422e952): the Small Archive (and every) diorama rendered solid black when the player re-entered a site — reported live via screenshot, 4th site after moving around.

Root cause: `@keyframes site-closeup-enter` ramped `.site-closeup-stage` **opacity 0.25 → 1** with `animation-fill-mode: both`. On re-entry the plate image is already cached, the stage remounts fast, and the animation stranded at its 0% frame → whole (dark) plate held at 0.25 opacity = black. First entry fired the animation normally; re-entry did not. The `img` itself was always fine (naturalWidth 1600x900, opacity 1) — the ancestor stage was the dimmer.

Fix: removed opacity from the entry keyframes entirely. The reveal is carried by the clip-path aperture + scale settle, which never gate visibility. Opacity now 1 on every frame.

**Detection rule:** any entry/reveal animation that ramps `opacity` from a low value with `fill: both` can strand the element invisible if the animation is cancelled/throttled/re-triggered (cached re-mounts, backgrounded tab). Carry reveals via clip-path/transform, keep opacity 1 — or the base rule must set the visible opacity so a stalled animation can't hide content. Verify by RE-ENTERING (not just first-entering) the view. Related: [[annex-preview-pane-quirks]], [[browser-pane-stale-screenshot]].
