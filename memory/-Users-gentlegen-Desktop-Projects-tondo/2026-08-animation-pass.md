# Animation polish pass (2026-08-20) — Emil/STANDARDS applied to the client

Scope: `public/styles.css` + `public/js/app.js` only. 44 tests still green.

## Scars / detection rules

- **CSSOM audit walkers give false negatives in Chrome.** `CSSStyleRule` now
  exposes an empty `.cssRules` (CSS nesting support), so a walker written as
  `if (r.cssRules) { recurse; continue; }` skips **every style rule** and
  happily reports "0 violations". First run reported `transition:all` = none,
  `ease-in` = none, ungated hover = none — all fake. → **Detection rule:** test
  `r.type === 1` FIRST and never recurse into it; always print a
  `styleRulesInspected` count and sanity-check it against the real rule count
  (412 here). A zero-findings audit with no denominator is not a finding.

- **Browser pane cannot produce `:hover`.** Neither synthetic `MouseEvent`
  dispatch nor `computer{action:"hover"}` set `:hover` — `document
  .querySelectorAll(':hover')` came back empty with the cursor provably over the
  element (`elementFromPoint` confirmed the hit). Extends the existing
  browser-pane flakiness note. → Verify hover *rules* via CSSOM + media-query
  scoping; verify *interruptibility* by scripting the underlying custom property
  and reading `getComputedStyle().transform` across frames.

- **`prefers-reduced-motion` cannot be emulated in the pane.** Workaround that
  actually executes the rules: locate the `@media (prefers-reduced-motion)`
  `CSSMediaRule`, re-inject its `cssRules` unwrapped into a probe `<style>`, then
  measure. Proved transform jumps instantly while `rm-fade` opacity still runs.
  The media-query *gating* itself stays inferred.

- **WAAPI entry animations must composite, not replace.** A hand-card entry
  ending at `transform: 'none'` snapped the card into its CSS fan rotation on
  finish. Fix: `composite: 'add'` for the transform effect. Opacity needs a
  SEPARATE effect — additive opacity resolves `1 + 0 = 1` and cancels the fade.
  Also `fill: 'backwards'`, or staggered cards sit at full opacity during their
  delay and then pop.

- **Flight→landing hand-off needs a shared constant.** The ghost's final frame
  and `@keyframes top-card-land`'s first frame must match exactly (offset,
  scale, rotation, opacity) or there is a visible jump. `LAND_RISE` in app.js is
  the contract; changing one side alone regresses it silently.

- **Animation classes driven from re-rendered markup replay spuriously.**
  `renderSeats` rewrites all seats via `innerHTML` on any change, so
  `.plate.is-acting { animation }` re-fired on every unrelated snapshot. Seat
  pops are now fired from JS on an actual turn change (`popSeat`). Same reason
  `.seat { transition: opacity }` is dead code — the nodes are never reused.

## Invariants confirmed still held
`--table-d`, `[hidden]` guard, keyed `renderHand`, `.hand-row` 20/18px inline
padding, all ids. Measured at 375×812 with 12 cards: first card fully reachable
at `scrollLeft=0` (gap −0.07px, i.e. exactly flush), last at max (gap 4.02px).

## Enter/exit + reflow pass (2026-08-20, later same day)

- **A `*/` inside a CSS comment silently ate the next rule.** The comment
  `.ring/.seat-*/.oven-mark` closed at `.seat-*` + `/`, and error recovery
  swallowed the `@property --table-d` block that followed. Everything else
  parsed, `.fx-panel` was present, so the file looked fine — the only symptom
  was `getComputedStyle(stage).getPropertyValue('--table-d')` returning the raw
  `min(...)` token stream instead of a px length. → **Detection rule:** after
  adding `@property`, assert the custom property computes to an absolute value;
  never write a selector containing `*/` in a comment.

- **`[hidden] { display: none !important }` does NOT block
  `transition: display … allow-discrete`.** Transition declarations outrank
  important author declarations in the cascade. Verified live: display stayed
  `flex` at 50ms and 200ms of a 300ms exit, `none` at 450ms. The guard stays.

- **`--e-out` is the wrong curve for a REFLOW.** cubic-bezier(.23,1,.32,1) has
  covered ~35% of the distance by the end of frame one, so an eased 118px tray
  change still opened with a 44.5px step. Split the channels: content entering
  = `--e-out` (opacity/transform), layout resolving = `--e-in-out`
  (height/margin/padding/`--table-d`). First frame then moves 0px, peak 22.9px.

- **CLS is not the metric for this work, and bot-game runs are not comparable**
  (their action mix, hence bar-toggle count, varies with the shuffle). Use a
  DETERMINISTIC scripted N-cycle swap and compare against the same page with
  `transition: none` forced on the fx classes: 10 cycles gave 2.201 (instant)
  vs 1.131 (eased) — easing halves CLS while producing 15x more entries.

- **Background tabs pause transitions.** A measurement in a background tab
  showed every transition `running` with `currentTime: 0` and the bar stuck at
  its `@starting-style` height. Not an app bug — always measure motion in the
  foreground tab.

- **`.label-row`'s shift was `#you-status`, not the labels.** dy was always 0,
  dx always ±30.9px = "your turn" (49.5px) − "you" (18.6px). The pill is
  content-sized and sits before `.label-row` in the flex row. Fixed by
  reserving `width: 12ch` on the status (measured max 11.13ch). Reserving space
  ELIMINATES a shift; easing only spreads it.
