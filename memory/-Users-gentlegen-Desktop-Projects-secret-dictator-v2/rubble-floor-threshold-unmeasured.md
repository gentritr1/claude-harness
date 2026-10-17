---
name: rubble-floor-threshold-unmeasured
description: "The rubble brief's Gate 3 floor (1,11,20) was already failed at the branch point; the darkest-pixel statistic is not a ground measure and must be replaced by a ground-masked percentile delta vs baseline"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df4dd4c1-38f3-4c2b-8e0b-c496f217dd8b
  modified: 2026-09-05T22:36:32.069Z
---

On 2026-09-06 the phase-1 review of the rubble art pass found that the brief's phase-5 criterion "trial darkest pixel not below (1,11,20)" was unreachable before any art changed: the phase-0 baseline capture (design/reviews/baseline-v2/measurements.json) already recorded the trial frame's darkest scene pixel as (0,0,1), and the same pixel position (130,173) is darkest in both baseline and phase 1, so it belongs to an unchanged object, not the ground. Codex's ground-masked variant also failed at baseline with (0,1,4).

**Why:** the (1,11,20) number came from docs/step-07 at Gate 3 with an older scene. A single-pixel minimum is an extreme-value statistic that any dark texel or shadow edge breaks. Pattern → detection rule → brief update: threshold copied from memory into a brief → run the named measurement script on the frozen baseline BEFORE the number is written → briefs pin "delta vs baseline, same script, ground-masked percentile (p1/p5)" not an absolute darkest pixel. This is the §6 "numeric threshold never computed from live data" red flag firing again; the reviewer (me) should have caught it at phase 0 when the baseline measurements were committed.

**How to apply:** for phase 5 of [[rubble-square-art-pass]], define the floor as ground-only p1 and p5 luma from a VIS ground ID mask (scripts/measure-rubble-ground-floor.mjs is the mask method), compared against the same script on /private/tmp/rubble-square-baseline, and require no darker p1/p5 than baseline plus the "blue not black" hue check on those percentiles. See also [[rubble-vite-ipv6-localhost]].
