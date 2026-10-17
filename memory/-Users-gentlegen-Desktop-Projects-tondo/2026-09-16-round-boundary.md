---
name: 2026-09-16-round-boundary
description: Tondo Task 5 (commit 8e28e6f) — round deal ghosts must be re-aimed (the deal snapshot moves the table 116-146px), banner overlap probes must wait for the 200ms tray swap, card ids repeat across rounds
metadata:
  type: project
---

Report: .superpowers/sdd/2026-09-16-tondo-tier2-tier3/task-5-report.md.

1. **The snapshot that deals also swaps scoreboard→hand**, so for --t-swap (200ms) the tray, stage and
   --table-d all move. Ghosts aimed at the snapshot frame missed by 116px (1440x900) / 146px (390x844).
   Fix: create ghosts in the snapshot task (keeps WAAPI delays locked to renderHand entries) and re-aim
   waiting ones per rAF with `effect.setKeyframes` (followDeal). Same trap applies to ANY travel fired on
   a snapshot that toggles `.is-compressed` or swaps a tray panel.
2. **Layout measured right after a snapshot is mid-transition.** A live banner-overlap probe read "no
   overlap" at 390x844 at 0ms into the tray's @starting-style growth (stage 47-716 vs settled 47-481).
   Wait until no `--table-d`/height/margin/padding CSSTransition is running before measuring.
3. **Card ids (c0..c67) name deck cards, not hands**: keyed hand nodes can survive into a new round.
   Rebuild the hand row on a round deal.
4. Banner now `bottom: 8px`: clears seats at 390x844/1280x800/1440x900; NOT seat-free on 760-768px-tall
   desktops at round over (3-9px corner overlap) — no stage position exists there. Old `top: 8px` covered
   87-100% of the plaque there.
5. Brief-probe vacuity: `valid: ... toppingsBefore >= 0` and "any non-CSS anim on .tp" both passed with
   nothing happening (controls in task-5-probes). Count WAAPI by `id`, validate by the step's own signal.
**Fix round 1 (commit 9c6261c):**
6. **A ghost must follow its target until it LANDS, not until it leaves.** The lobby deal has no sweep to
   wait behind, so its first cards fly while the game screen is still growing: 117.7px miss at 390x844.
   Flying ghosts keep their launch point and tilt (a tilt flipping sign mid-flight snaps) and re-aim only
   the destination.
7. **Under reduced motion, `display` (allow-discrete) is the ONLY sign a tray swap is still running** —
   height/--table-d do not transition at all. A probe that waits on "layout moving" without it reads the
   stage 29px short at 5ms and reports a banner over the top card that is clear by 190ms.
8. **`AudioBufferSourceNode` declares its own `start()`** — wrapping `AudioScheduledSourceNode.prototype`
   alone misses every noise-based card sound. Audio-clock reads need ~10ms tolerance (128-sample quanta).
9. **A probe whose tap actually plays destroys the rest of its own run** (the turn moves, the banner
   goes). Record what the app sends, do not deliver it.
10. Invisible-but-live controls: a hand card at opacity 0 was focusable and playable. `inert` until its
   own rise animation starts, released off that animation, plus a guard in tapCardId.
Open: none from the fix round; the YOUR TURN high placement is conservative by ~20px of viewport height
(375x812 goes high although the low banner would clear the card by 3-4px).

## "Never overlaps" needs a per-frame sweep, not a settled read (2026-09-26)

The Task 5 probe asserted "YOUR TURN never intersects #top-card" with ONE read
taken after the layout stopped moving. A reviewer argued that a probe change
(adding `display` to the set of transitions that mean "layout still moving")
was masking a transient overlap during the tray swap. Measuring settled it,
and both sides were wrong about where it lived:

- reduced motion, 1280x800 — the reviewer's specific case — has **zero**
  overlap frames;
- **normal** motion on desktop widths does overlap: 1280x800 six frames,
  9-88ms, up to **28.4%** of the top card; 1440x900 five frames, 18-85ms,
  12.2%. Phones: zero.
- The same sweep at the pre-fix commit measures it identically, so it
  predates the task — ruled a deferred minor, not a blocker.

**Pattern → detection rule → brief update.** A geometry assertion of the form
"A must never overlap B" that is read once after settle cannot fail during the
transition, which is exactly when layout is most likely to violate it. Any such
assertion has to sample EVERY frame across the transition and print the frame
count reconciled against `window / 16.67`. Briefs must say "per-frame across
the transition", never just "assert they do not overlap".

Related: [[cdp-capture-harness]], [[2026-08-21-a11y-geometry-pass]]
