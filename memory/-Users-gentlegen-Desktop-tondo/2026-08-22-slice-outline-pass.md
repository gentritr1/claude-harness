---
name: 2026-08-22-slice-outline-pass
description: Tondo lit-slice outline rebuilt as an SVG sector path; cheese mark centroid fix; stress perf — and four reviewer premises the delegate refuted with measurement
metadata:
  type: project
---

Delegated to Opus 5 on 2026-08-22 after the user asked for the "whose turn" slice to be more
accurate and the cheese icon to be centred.

**What shipped**
- `.wedge-glow` no longer uses conic gradients + a masked radial ring. `#wedge-sector` is an
  inline SVG path (viewBox 100, radius 49.535 = 49.85 − stroke/2, `--wedge-stroke: .63` =
  1.26% of the sauce radius ≈ 2.75px at a 437px pie) written by `sectorPath(360/players)` in
  app.js next to `--wedge-span`. Stroke equal on all three sides (spread 0.10px), edges on the
  cut centreline (≤0.63px), arc ≤1px inside the sauce edge, corners closed. `.wedge-edge::after`
  `top: 2.6%` (a % of the rail HEIGHT = sauce radius) keeps the marker 2–3px clear of the arc.
- `.mk-wedge { transform: translateY(calc(var(--m) * -.115)) }` — h/6 centroid correction
  (10.67%) + 0.83% optical lift; measured −0.3…−1.6% in six contexts (was +9.3…+10.7% low).
- `dealGhosts` guard timeout (hidden tab: 12 ghosts stayed forever → 0 by 2s);
  `app.confettiTimer` stored (a second burst inside 1.5s was swept at 1.1s).
- Rejected after shuffled A/B: removing `moveToken`'s rect reads — overlapping ranges, inverted
  half the time. A forced layout relocates work the frame owes anyway; only a DOUBLED layout costs.

**Loudness change (taste, user's call):** old outline had a 13.6px blurry rim band; new one is
a uniform 2.75px line — ~4× less gold area. One var (`--wedge-stroke`) tunes it.

**Reviewer premises that were WRONG (write specs from measurements, not from rect reads):**
1. "`.wedge-glow` box 617px vs 437px sauce" — `getBoundingClientRect` of a 135°-rotated square
   = 437 × (|cos|+|sin|). The arc was 6.3px short, not 41%.
2. "edges run into the crust" — `.sauce` is `overflow:hidden; border-radius:50%`; 0 gold samples
   outside. The visible defect was the edge overshooting its own short arc.
3. "open corners" — gap 0.00px; 4. "aliased conic stops" — 0.23px residual, Chrome AA's them.
Rule: a rotated element's bounding rect is not its size; derive from the unrotated parent.
Related: [[2026-08-22-message-deck-perf-pass]], [[slice-ledger-board]].
