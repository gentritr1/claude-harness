# 2026-08-21 — accessibility + Slice Ledger geometry pass

Fixes applied from `.impeccable/critique/2026-08-21T14-32-17Z__slice-ledger-redesign.md`
(P0-2/3/4/5, P1-2/3/5/6). Only `public/styles.css` and `public/js/app.js` touched.

## Scars worth keeping

- **`padding: 2.2%` on `.ring` resolved against the STAGE, not the table.** Padding
  percentages always resolve against the containing block's *inline size*. Measured: the
  same declaration was 8.25px at 375px wide and **39.59px at 1800px wide**, so the stone
  rim ate 17.8% of a desktop table and left the sauce 304px across on a 445.68px board.
  Now `calc(var(--table-d) * .022)`. **Detection rule: any `%` padding/margin inside the
  stage is suspect — check it at 375 and 1800 wide before trusting it.**
- **A `hidden` surface froze an `fx-panel` height transition and I nearly "fixed" a
  non-bug.** The pane reported `.tray` at 150.9px (hand-wrap 0px) against a `--chrome-h`
  model of 393.5px, which looked like a 190px modelling error worth reclaiming. With
  `*{transition:none;animation:none}` injected first, the tray measured 339.5px and the
  model was accurate to 1px. **Rule: inject a motion-killing stylesheet into the frame
  BEFORE any layout measurement, not just before animation claims.** (Extends
  `2026-08-wide-two-column.md`.)
- **WCAG luminance ratio is the wrong instrument for hue-separated fills.** The four seat
  tones over the sauce sit within .03 of each other in luminance, so adjacent wedges
  measure 1.03–1.30:1 at *any* alpha (.13 → 1.004–1.118; .50 → 1.111–1.357). Chasing 3:1
  with the wash would have meant painting the pie in flat primaries. Report ΔE alongside
  (11.3–17.7 → 32.7–49.4) and put the required contrast on the BOUNDARY, which has no
  such ceiling: the cut measures 3.27–5.52:1 and the lit-wedge outline 3.31–7.07:1.
- **No flat ink reaches AA on a mid-tone gradient.** Cream measured 1.45:1 on cheese's
  light stop; pure black only reaches 3.43:1 on pepperoni's dark stop. A card digit on a
  saturated card needs its own ground (`--*-ink` chip), not a darker ink.
- **Banner clearance is fixed px, not a fraction of the table.** A first attempt at
  `top: calc(50% - var(--table-fit) * .34)` still covered 27.8% of the plaque at 1024×768
  — the clearance needed is plaque-half-height + banner height, which does not shrink when
  the window does. Anchored to the stage top (`top: 8px`) instead: 0% at every size.
- **Keyframes that hard-code an element's base transform break when its anchor moves.**
  `tondo-slam`/`tondo-leave` both wrote `translate(-50%,-50%)`; changing `.banner` to a
  top anchor required editing both or the banner jumps for the length of the slam.
- **`ledgerGeom` HOLDS stale geometry while any centre part animates, and `layoutLedger`'s
  signature early-out then decides nothing moved.** A resize landing during a landing
  discard left every topping placed for the previous pie. Fixed with an `app.geomHeld`
  flag + a rAF retry placed BEFORE the early-out.

## Numbers this pass was tuned against (measured, real Chrome + same-origin iframes)

- `--table-d` @1800×900: 445.68 → 476.06; sauce diameter 304.2 → 377.8 (+24%).
- Ledger ring (worst wedge, best bearing in it) went negative at most desktop sizes
  (−75.6px @1800×900 at 4 players) → **+30 to +80px at every size and player count**,
  always ≥ one pepperoni diameter. Toppings may now spill onto the crust band
  (`.ledger { overflow: visible }`, ceiling = crust radius) rather than vanish.
- Live 4-player bot game, 24–27 toppings: 0 inside the centre column, 0 outside the crust,
  including a mid-game resize 1024×768 → 1800×747 (the audit's failing viewport).
