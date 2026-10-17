# Tondo — project memory index

## Current
- [2026-09-09 next-level pass](2026-09-09-next-level-pass.md) — the pie match layer, sound, events.js, delivery; the zero-match CSS selector and five other bugs; what was rejected and why
- [Snapshot-delta events](snapshot-delta-events.md) — events.js derives what happened from two snapshots; the audio-must-land-on-the-impact-frame rule
- [Action-legibility fx (Task 3)](2026-09-16-action-legibility-fx.md) — animation-name fallback replays a pop after a one-shot; timer-vs-WAAPI-ready drift (chain `finished`); mock `transition` probes contaminated by BEFORE
- [Round boundary (Task 5)](2026-09-16-round-boundary.md) — deal ghosts re-aimed while the table swaps; measure overlaps after the 200ms tray swap; card ids repeat across rounds; banner at stage bottom
- [CDP capture harness](cdp-capture-harness.md) — scripts/shoot.js and the three traps that made it lie (zombie Chrome on a fixed port, wrong-banner detection, breakpoint-dependent affordances)

## Layout, geometry & scaling
- [Fluid board scaling](2026-08-fluid-board-scaling.md) — length/length `--cs` works (unitless rule obsolete); 3rd selector-order clobber (`.top-card`); derive furniture from an UNREGISTERED var; fan overhang = .371 × card
- [Wide two-column layout](2026-08-wide-two-column.md) — aspect-ratio (not size) picks the layout; clearances vs TEXT must use the longest real string; **unfocused surfaces freeze transitions/WAAPI → finish animations before measuring**; `resize_window` sets OUTER size
- [Slice Ledger port](2026-08-slice-ledger-port.md) — wedge angles per player count; ray-clearance ≠ shape clearance; the probe contaminated its own measurement
- [Slice Ledger board](slice-ledger-board.md) — the pizza IS the board; wedge angles, the ~30-node cap, Minkowski + plaque keep-outs
- [Stone Oven port](2026-08-stone-oven-port.md) — unitless `--cs` trap (**superseded**), selector-order clobbers, global `[hidden]` guard, seat/plaque geometry invariant
- [Flex-centre overflow clip](flex-centre-overflow-clip.md) — the v0.2 welcome card's top became unreachable at 320×568 (FIXED with margin:auto)

## Motion & rendering
- [Animation polish pass](2026-08-animation-pass.md) — motion tokens, flight→landing hand-off (`LAND_RISE`); CSSOM-walker false negatives; the pane can't do `:hover` or reduced-motion
- [Keyframe/JS hand-off pair](keyframe-js-handoff-pair.md) — `top-card-land` 0% and the flight ghost are ONE contract; grep both sides when either moves
- [Message, deck reach & perf](2026-08-22-message-deck-perf.md) — `:empty` as the resting state for text fades; headless rAF ticks at 120Hz; instrumenting layout READS beats tracing
- [Message/deck/perf pass 2](2026-08-22-message-deck-perf-pass.md) — deck docked beside the hand (508→78px reach); same-tick-as-goto rects are pre-layout
- [Slice outline pass](2026-08-22-slice-outline-pass.md) — the lit wedge is an SVG sector path; rotated-element bounding rects fooled the reviewer's spec

## A11y & colour
- [A11y + ledger geometry pass](2026-08-21-a11y-geometry-pass.md) — `%` padding resolves against the STAGE; kill motion BEFORE measuring layout; WCAG ratio is the wrong tool for hue-separated fills (use ΔE + a boundary)

## Verification environment
- [Browser-pane click flakiness](browser-pane-click-flakiness.md) — pane click timeouts AND wrong-paint artifacts aren't app bugs; re-verify via JS dispatch / real Chrome; a hidden surface silently stops animations
- [Headless CDP media emulation](headless-cdp-media-emulation.md) — the pane can't flip reduced-motion or run rAF while hidden; headless Chrome over CDP does both
- [`hidden` defeated by `display`](hidden-attr-defeated-by-display.md) — any new `display` rule on a `hidden`-toggled class needs a `[hidden]` guard

## Assets & history
- [Pizza suit photos](pizza-suit-photos.md) — photoreal pie per topping; suit keys are full words, not PEP/BAS codes
- [2026-08 polish pass](2026-08-polish-pass.md) — 4-agent review outcome, keyed-render + `--table-d` invariants
- [Design skills for UI work](design-skills-for-ui-work.md) — the user wants emil-design-eng / frontend-design / ui-ux-pro-max folded into briefs that touch visible UI
- [Live-region same-tick clobber](2026-09-26-live-region-same-tick.md) — three ways a later write in the same repaint undoes an announcement or focus move; plus the scroll-container trap that fooled two agents
- [Shared-tree agent collision](shared-tree-agent-collision.md) — never run two implementer agents in one checkout; the worktree + `git apply --cached` recovery when it happens
- [Text that leaves the app](text-that-leaves-the-app.md) — frozen ids + live standings can assert a falsehood in a pasted message; pin the unresolvable-reference case
- [Tier 2/3 shipped](2026-09-27-tier23-shipped.md) — what landed on next-level/PR #1, what only a human can close, and the defects deliberately left in
- [When a delegate overrode my ruling](delegate-overrode-my-ruling.md) — twice right; my error was generalising a rule across call sites I had not checked
- [Shoot gate load flake](shoot-gate-load-flake.md) — banner-clear valid=false under load; the frame-count floors have no jitter allowance; re-run clean before concluding
- [Easing eats duration](animation-easing-eats-duration.md) — a front-loaded timing function shows a flourish for ~1/5 of its declared time; per-keyframe easing cannot fix it; measure before tuning alpha
- [Sampled-viewport gate blind spot](sampled-viewport-gate-blind-spot.md) — a 3-point geometry gate passed while 1366×768 overlapped; sweep the band when clearance is single-digit
- [Measured the component, not the container](measured-the-component-not-the-container.md) — the chip fit; the help button it pushed off-screen did not. Assert the last siblings edge against the container
- [Hosting free-tier facts](hosting-free-tier-facts.md) — Fly has no free tier for new orgs (2026-10-10); Neon is a DB, not a WS host; Render free sleeps
- [Predicted RED is a hypothesis](brief-predicted-red-is-a-hypothesis.md) — plan predicted the wrong pre-fix failure; TEST-001 mutants (incl. a surviving ±1) are the real proof
- [Crew-retention shipped to PR](2026-10-10-crew-retention-shipped.md) — branch crew-retention / PR #2 open; what is verified locally; Task 10 (deploy) still owner-gated
- [legacy-peer-deps breaks host npm ci](npmrc-legacy-peer-deps-lockfile.md) — ~/.npmrc legacy-peer-deps=true drops peers from lockfiles; regenerate with --legacy-peer-deps=false before deploys
