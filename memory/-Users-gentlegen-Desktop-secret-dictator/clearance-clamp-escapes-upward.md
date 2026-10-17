---
name: clearance-clamp-escapes-upward
description: "Secret Dictator's clampToClearance can push a piece ABOVE an obstacle, which on a painted plate means standing on a roof — any autonomous destination needs a band re-check after clamping."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9d90e3f0-7698-483d-a615-b31b363ed1c5
  modified: 2026-08-08T20:20:15.061Z
---

`clampToClearance` in `js/ui.js` scores four escapes (above / below / left / right)
by how many boxes each clears, then by distance. "Above the top edge" is often the
cheapest escape — and on the painted plaza that means the citizen's feet land at the
prop's top edge, i.e. **on the roof of the hay cart, above the horizon**. Round 3
never noticed because choreographed layouts never aimed at a prop. Round 4's roaming
controller deliberately sends citizens to loiter at the notice board and the cart,
and the first measured stroll put a piece at local y 47 (stage y 357, sky).

**Two fixes, both needed:**
1. `inBand()` re-check *after* the clamp — a destination that leaves the walkable
   band (local y 110–300) is rejected and re-picked. The pre-clamp band clamp is not
   enough because the clamp runs after it.
2. Offer prop loiter spots at the prop's **left and right shoulders**, not its
   centre-front: a standee is taller than either prop, so a centre aim always makes
   "up" the cheapest escape, while a shoulder aim makes "sideways" cheapest.

**Detection rule:** any code that generates destinations autonomously (not from a
hand-placed layout) must assert the post-clamp point is still inside the walkable
band, and the test must sample **style.left/top of every piece over a window**, not
just eyeball one frame — this only showed up in 1 of 7 pieces after ~60s.

Related: [[grid-center-degrades-to-start-on-overflow]]
