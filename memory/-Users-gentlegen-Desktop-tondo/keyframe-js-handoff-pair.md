---
name: keyframe-js-handoff-pair
description: Tondo — `top-card-land` 0% keyframe and `LAND_RISE`/`s * 1.07` in app.js are one contract; v0.2 edited the CSS side only and rewrote the comment to claim they match
metadata:
  type: project
---

The flight ghost's last WAAPI keyframe (`app.js` ~line 662: `translateY(dy - LAND_RISE)
scale(s * 1.07) rotate(-3deg)`) must equal the first frame of `@keyframes top-card-land`
(`styles.css`): the ghost is swapped for the real pile card on that frame.

Fired 2026-08-22: the polish pass changed the keyframe to `scale(1.04)` and edited the CSS
comment to say "4% oversized — see LAND_RISE in app.js", but app.js still says 1.07 → a 3%
(~3px on a 98px card) size snap at the hand-off, and a comment that now lies.

FIXED 2026-08-22: app.js now owns `LAND_RISE`/`LAND_SCALE` and writes `--land-rise`/`--land-scale`
onto `#top-card`; the keyframe reads `var(--land-scale, 1.04)`. Measured in headless Chrome (real
bot game): ghost final bbox 122.85×170.21 == landing 0% bbox 122.85×170.21, centres within 0.5px.

**Why:** the contract is split across two files and two languages; a reviewer reading only the
CSS diff sees a self-consistent comment.

**How to apply:** when either side of a ghost→real hand-off is edited, grep the other
(`LAND_RISE`, `1.07`, `top-card-land`) and quote both values in the report. Same rule for
deal ghosts / `travel-ghost`. Related: [[2026-08-animation-pass]].
