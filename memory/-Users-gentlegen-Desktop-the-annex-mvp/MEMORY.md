# Memory index

- [UX audit 2026-08](annex-ux-audit-2026-08.md) — Opus audit reviewed; dead first-run rule behind `!scene.world`; dead number-key ordinals; F2 missing-copy scar

- [CSS + contrast measurement scars](annex-css-and-contrast-scars.md) — CSS syntax errors pass tsc/eslint/vitest (run `vite build`); composited-contrast probe pitfalls; "too much text" is a hierarchy measurement, not an area one; where the type scale lives

- [Investigation inspector always mounted](annex-investigation-inspector-always-mounted.md) — site methods/room aren't gated behind world-view closeup; base CTAs on room phase; set-state-in-effect lint scar

- [Shelf Zero room](annex-shelf-zero-room.md) — Small Archive classification room shipped 4df4da0; rAF-focus-after-unmount scar; headless keyboard-evidence recipe

- [Annex MVP verified state](annex-mvp-verified-state.md) — what the 2026-07-19 review confirmed vs. what the build session overstated (untested save wrappers, zero git commits)
- [Annex MVP next features](annex-mvp-next-features.md) — ranked backlog; #1 Counterfactual Memory panel, #2 reconstruction↔decision tension line
- [Browser pane stale screenshot](browser-pane-stale-screenshot.md) — frozen capture frame while DOM healthy; verify via read_page/JS, reload fixes
- [Annex MVP design review](annex-mvp-design-review.md) — both-worlds verdict; all 6 violations since FIXED + review-approved; oklch contrast-probe gotcha
- [Annex MVP shipping backlog](annex-mvp-shipping-backlog.md) — website-shipping gaps: 1.9MB PNG in deploy, no Vite base, no OG meta, preload, browser matrix, save-migration note
- [Annex campaign decisions](annex-campaign-decisions.md) — user-ratified: 2.5D diorama (no WebGL), latest-verdict-is-canon, build order through Case 84; content-id-leak grep as review step
- [Annex preview pane quirks](annex-preview-pane-quirks.md) — synthetic clicks dont reach React (use el.click()), vite serves on 4174 not the assigned port, reload snaps to dead URL
- [Annex transition-clock measurement](annex-transition-clock-measurement.md) — pane getComputedStyle reads the START frame of transitioned props; disable transition before probing bg-color/opacity
- [Review scar: clamped counters](annex-review-scar-clamped-counters.md) — Math.min in a displayed counter hides state past the bound; check the >threshold branch
- [Scene plate opacity strand](annex-scene-opacity-strand.md) — diorama went black on site re-entry; opacity-ramp + fill:both stranded at 0%; carry reveals via clip-path
- [Prototype QA scars](annex-prototype-qa-scars.md) — class-collision invisible to text asserts; reduced-motion advance-paced; test the user's real play width; pumped-rAF rigs prove logic not liveness (walkable r1 WASD dead); loop predicates need input state
- [Review scar: cross-zone hit-tests](annex-review-scar-cross-zone-hits.md) — per-zone verification is blind to control-pair interference; sweep every positioned-control pair
- [Reviewer scar: pinned thresholds](annex-reviewer-pinned-thresholds.md) — I wrote a 12% heap gate with no measurement script; unmeetable by design. Demand a pre-fix control before accepting a threshold miss
- [Worktree stale-server scar](annex-worktree-stale-server-scar.md) — harnesses default to :3000, which can be a main-checkout server; verify served CSS contains the edit, pass worktree URL as argv
- [R3 conversation scars](annex-r3-conversation-scars.md) — save schema 3→4 (no new field); data-persona selector collision; a spike generator that never dispatched the new action; node:fs unusable in src tests
