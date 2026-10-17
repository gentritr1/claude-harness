---
name: grid-center-degrades-to-start-on-overflow
description: "place-items:center silently becomes start-alignment on whichever axis the item overflows, which parks a scaled fixed-size stage off-centre."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9d90e3f0-7698-483d-a615-b31b363ed1c5
  modified: 2026-08-07T22:53:35.019Z
---

Secret Dictator uses a fixed 1240×800 stage scaled with `transform: scale()` to fit
the window. `transform` does not change the layout box, so in a narrower window the
box overflows horizontally — and `place-items: center` then aligned it to **start**
on that axis (browsers do this to keep overflow reachable). The board rendered
off-centre and clipped, while the vertical axis, which did not overflow, stayed
correctly centred. That asymmetry is the tell.

**How to apply:** centre a scaled fixed-size stage with absolute positioning
(`left:50%; top:50%; transform: translate(-50%,-50%) scale(var(--scale))`), never
with flex/grid alignment. Also: measure with `getBoundingClientRect()` rather than
trusting a screenshot — the first screenshots here were stale and sent me chasing
the wrong cause twice.

Related: [[css-var-url-resolves-against-stylesheet]]
