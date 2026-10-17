# Slice Ledger port (2026-08-21)

Replaced the photoreal pie + `renderPizzaToppings` count system with the designer's
**Slice Ledger** in full cartoon: one wedge per player, a topping per card played,
the lit wedge = whose turn, a Flip sweeps the glow the long way round.
Files: `public/index.html`, `public/styles.css`, `public/js/app.js` (client only).

## Geometry facts worth keeping
- Wedge centres = `90 + offset * 360/n` screen degrees (0 = right, +ve = clockwise).
  You are always 90 (bottom). n=4 → 180/270/0 = left/top/right exactly; n=2 → 270;
  n=3 → 90/210/330 (the concept's own layout — 90/180/0 cannot tile a circle).
- conic-gradient angle = screen angle + 90. Wedge boundaries start at `180 - span/2`.
- `left: X%` inside a circle is X% of the **diameter**, so the concept's "radius 27–42"
  and "seat tags at 46" are 0.54–0.84 and 0.92 of the RADIUS. Don't read them as radii.
- Measured at this app: sauce r = .397 x `--table-d`, crust r = .478, `.center` column
  half-height .225, plaque worst-case width 273px (matches the 272px in the styles.css
  `--min-orbit` comment — good cross-check that a worst-case measurement is right).

## Scars → detection rules
- **Ray clearance ≠ shape clearance.** Placing a piece's CENTRE past a keep-out box
  along the ray still lets its bounding square poke over the box's CORNER (2 of 32 did,
  on a 375px phone). → Inflate the box by the shape's half-diagonal first (Minkowski),
  then ray-test. Any "keep X clear of Y" geometry must be asserted at the corners.
- **A keep-out measured from a TEXT box breathes.** "Topping ● Cheese" vs
  "Match ↻ ● Pepperoni or Flip" differ ~25px, so pieces placed against the short plaque
  ended up under the long one (11 clipped frames in 47 plays). → Measure the worst case
  once on a hidden CLONE inside the same stage. Include the **rotated bbox HEIGHT**, not
  just width: `.plaque` is rotate(-2deg), so wider = taller, which still drifted ~1px.
- **Order inside a render function is load-bearing.** `layoutLedger` ran at the TOP of
  `renderCenter`, i.e. against the PREVIOUS turn's plaque. → Anything that measures the
  centre column must run last, after the column is repainted.
- **An easing `--table-d` changes the ratio of fixed-px furniture to the pie every
  frame.** Laying out once at the start of the ease places pieces for a pie about to stop
  existing. → keep re-spacing via rAF while `stage.getAnimations()` has a `--table-d`
  transition.
- **The probe contaminated the measurement.** The harness called `layoutLedger(g, true)`
  to time it, which re-fixed the positions it was about to check — `moved` was garbage
  until the probe went read-only. → A verification probe must never call the code path
  it is measuring for side effects.
- **`getAnimations()` is empty inside a MutationObserver** for a just-inserted node
  (styles unresolved). Sample keyframes off an already-settled node instead.
- **Hidden tab freezes CSS animations at frame 0**, so `getBoundingClientRect()` returns
  the 0% keyframe — here `scale(2.1)`, which manufactured phantom card overlaps.
  → `getAnimations().finish()` on the SUBTREE you are measuring before asserting, and
  never `finish()` the stage's own transitions if you also want the live size.
- **Porting an "on the pie" annotation needs the seat furniture measured first.** The
  concept's seat tags at .92 of the radius are impossible here: our side-seat plates
  reach in to **.558 of the ring radius**, straight over the wedge centres. Dropped the
  tags (and with them the optional "N ON THE PIE" tally); a faint per-wedge wash of the
  owner's seat tone carries ownership instead.

## Numbers to reuse
- Cap: `~30 topping nodes total`, `Math.max(5, round(30/n))` per wedge → 15/10/8 for
  2/3/4 players. Derived from annulus area per wedge (~44,000px² vs ~2,500px² a piece
  at a 825px table, ~45% coverage), NOT guessed.
- `--tp-u` = `max(.62px, --table-fit * .002334)` — one unit; every topping is the
  concept's own px number times it (pep 26, bas 28, chz 26x22, anc 31x14). 1/428 of the
  table, not the concept's 1/320, because our discard card eats the annulus.
- Verified: 4p 109 plays / 3p 44 / 2p 24 — 0 card overlaps, 0 plaque overlaps,
  0 wedge misattributions (checked against the server's own `PLAYED` log), node count
  flat at the cap, 0 drift at constant table size.
