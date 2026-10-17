# 2026-08-22 — message fade, deck reach, 60fps audit

Three tasks in one pass (v0.2 working tree, not committed by me — orchestrator owns git).

## Message line (`#message`, `setText`)
- `instant` in `setText()` was a rule about text→TEXT only (hover flicker). It was also flattening
  empty→text and text→empty. New contract, both halves must stay in sync:
  - `.txt-fade:empty { opacity: 0 }` in styles.css is the RESTING state; `setText` writes arriving
    words immediately (the node stops matching `:empty` and CSS fades it in).
  - Clearing can NOT be left to CSS — the words must still be in the DOM while they fade, so the
    `.is-swapping` out-fade runs first and the clear happens after `--t-text-out`.
- `#message` lives in `.action-row`, NOT in `.foot` (a brief said otherwise). The reflow it caused:
  17px on desktop (hint + Leave dropped), 29px on phones (the bottom-anchored tray pushed the HAND up).
- Fix: `min-height: 1lh` on `.message`, plus `flex: 0 0 100%` in the phone band (whether the sentence
  wraps depends on the sentence, so a width tweak can't be the fix). The two-column band overrides it
  back to `flex: 0 1 auto` because it matches the phone media query at 1800x700 but has no draw button.
- Accepted cost: reserving the line makes the tray permanently the height it already had whenever a
  message was showing. At 320x568 only, that leaves the pie ~1.6px clipped top/bottom (the stage hits
  its 180px min-height). Compensating `--chrome-h` instead would have cost ~25px of pie — worse.
- Reduced motion: `.txt-fade` is in the RM damper list, which strips `transform` from the transition
  property list, so the 3px settle needs `.message, .hint { transform: none !important }` in that block
  or it arrives as a step.

## Deck reach (Task 3)
- Measured reach (deck centre → nearest edge of nearest hand card) BEFORE: 7.19 card-widths at
  1280x720, 3.95 at 1440x900, 4.77 at 1920x1080, 3.85 at 2000x1290, 9.30 at 1800x700.
- Anything in the STAGE fails: a small hand is centred, so a control at the stage's edge is ~250-500px
  from the nearest card, and the pie occupies the middle. Anything in flow BELOW the hand in the
  single-column bands steals stage height (`--chrome-h` is a hardcoded constant → the pie overflows or
  must shrink). The only free placement is BESIDE the fan: `.hand-dock` flex row, deck `flex: 0 0 auto`,
  `.hand-wrap { flex: 0 1 auto; max-width: calc(100% - var(--dock-deck)) }`. AFTER: 0.59-0.82 card-widths.
- **A var used by an element you relocate has to be re-homed**: `--deck-w` was declared on `.stage`
  (derived from `--table-fit`), so moving `#deck` into the tray would have silently dropped it to the
  `@property` initial 70px. Re-derived as `.7 * --card-w` on `:root`.
- **`.hand-wrap[hidden] + .deck { display: none }` broke the draw flight**: a drawn card arrives in the
  same snapshot that swaps the hand for the decision bar, so `pileRect()` saw `offsetParent === null`
  and fell back to the discard — the card flew out of the pile it was about to be played onto.
  `pileRect()` now caches the last on-screen deck rect. (Phone band, where the deck never shows, still
  falls through to the discard as designed.)
- Whether a fan of N cards leaves room for the deck must not decide the layout, or the deck hops
  between "beside" and "below" as the hand shrinks: the two-column band pins `.hand-wrap { flex-basis: 100% }`.

## 60fps audit (Task 2)
- **Headless Chrome ticks rAF at ~120Hz (median 8.3ms), not 60.** Calibrated on an idle page: 241
  samples / 2000.1ms reconciles 1:1 with window/8.33. So "frames >16.7ms" there means "the main thread
  missed ≥2 ticks", and expected-frame counts must use 8.33, not 16.67.
- **Best tool by far: instrument the READS.** `Page.addScriptToEvaluateOnNewDocument` wrapping
  `getBoundingClientRect`, the `offsetWidth`/`scrollWidth`/`clientWidth`/`scrollLeft` getters and
  `getComputedStyle` with a timer + `new Error().stack` gives exact per-call-site attribution of forced
  synchronous layout. Traces did not (no stacks without the `.stack` category, and tracing overhead
  inflated the same task from 25ms to 125ms across runs).
- The whole deal window's forced layout was TWO reads: `scrollWidth @ updateFades` 18.9ms and
  `offsetWidth @ showBanner` 7.1ms. `ledgerGeom`/`centreWorst` never fired (empty ledger at deal time).
- **Removing a forced layout can just move it to the next reader**: after deferring `updateFades` to a
  rAF, `moveToken`'s `getBoundingClientRect` inherited the 23.8ms. Total in-task reads 26.4 → 23.9ms.
- `void el.offsetWidth` to restart an animation is unnecessary when the element is coming out of
  `hidden`: display:none→block starts the animation at 0 by itself. Only restart when it was showing.
- Shuffled A/B (old/new/old/new/old/new, deal window) is what settled it: `over16.7` did NOT improve
  (old 2,2,2 vs new 3,3,2 — noise), but `RecalcStyleDuration` (old 16.8-21.2 vs new 14.3-15.2) and
  `TaskDuration` (old 155.6-182.3 vs new 148.6-152.7) were non-overlapping. Report the honest split.
- Claims from the static audit that the measurements did NOT support: the `--table-d` ease (0 frames
  over budget at 1280x720), and `updateFades` on the un-throttled scroll handler (LayoutCount 0 at
  desktop — a `classList.toggle` that doesn't flip dirties nothing). The phone confetti window's
  p95 15.8ms is GPU/raster bound in headless (GPUTask 274ms), not main-thread.
