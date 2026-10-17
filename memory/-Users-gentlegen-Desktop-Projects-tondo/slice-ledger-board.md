---
name: slice-ledger-board
description: Tondo — the pizza is the board (Slice Ledger): per-player wedges, toppings record ownership; geometry rules and why the seat tags were dropped
metadata:
  type: project
---

Chosen 2026-08-21 from the user's concept doc ("Pizza State Directions", direction 1a) over Sauce
Spiral and the rules-panel variant, in **full cartoon** (flat CSS/SVG, no photoreal). The photoreal
`pizza-*.webp` pies from earlier the same day are **unwired but kept on disk**.

**The idea:** the pie records OWNERSHIP. Each player owns a wedge; their played card drops a topping
into their wedge; the lit wedge is whose turn it is; a FLIP spins the turn glow the LONG way round.

**Geometry:** `wedgeAngle(offset, n) = 90 + offset * 360/n` in screen degrees (0 = right, +ve
clockwise). You are always 90deg (bottom) because you sit in the tray, not on the ring. n=4 lands on
our real `SLOTS` (left 180 / top 270 / right 0); n=2 puts the opponent at 270; **n=3 uses 90/210/330**
— our slots can't tile a circle in thirds, so it follows the concept's own 3-player layout.
Placement per the concept: `ang = seatAngle + (rand-.5)*(HALF*1.55)`, `rad = 27 + rand*15` percent.

**Cap: ~30 nodes, `max(5, round(30/n))` per wedge.** Derived from area, not guessed: at an 825px table
a 4-player wedge is ~44,000px² against a ~2,500px² piece, so ~8 pieces is the readable density.
Oldest 3 per wedge shrink and dim out.

**Two geometry traps that produced real bugs:**
- Clearing the centre card along the *ray* is not enough — a rotated square still pokes over the
  card's *corner*. Inflate each box by the piece's half-diagonal (Minkowski) before the ray test.
- The MATCH plaque's keep-out **breathes with its wording** ("Topping ● Cheese" vs "Match ↻ ●
  Pepperoni or Flip" differ ~25px). Measure the worst-case string on a hidden clone — it comes out
  at 273px, matching the 272px already noted in the `--min-orbit` comment. See [[2026-08-wide-two-column]].
- `layoutLedger` must run at the END of `renderCenter`, or it lays out against the previous turn's plaque.

**Dropped deliberately:** the concept's in-pie seat name tags and the "N ON THE PIE" tally. Our side
seat plates reach to 0.558 of the ring radius and sit ON the wedge centres, where the concept's seats
float above its pie. Each wedge instead carries a faint wash of its owner's seat tone. A tally would
have to live in the seat status pill, which touches the measured `--pill-max`/`--min-orbit` geometry.

**Known deviation from the motion standards:** the glow sweep is 550ms (800ms for a flip's long arc),
over the 300ms UI rule, kept because the sweep *is* the information. See [[2026-08-animation-pass]].
