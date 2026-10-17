---
name: hud-integration-scars
description: "HUD redesign (2026-09-08/09) — where it lives, what the merge broke, and the review rules it produced"
metadata: 
  node_type: memory
  type: project
  originSessionId: 662a742d-ce8a-498d-8dae-4a833d439e98
  modified: 2026-09-09T11:54:36.266Z
---

HUD redesign landed on `work/ascension-pad` via merge `d903b25` (2026-09-09) from `work/hud-redesign` (worktree `/private/tmp/hud-redesign`, port 5310). Write-up: `docs/HUD-PASS.md`. Evidence: `art/evidence/hud/`. Settings `hudScale`/`menuScale` shipped as save schema v5 (identity migration, wipe risk none).

**Scar 1 — per-validator runs are not the suite.** The HUD pass ran ~12 validators individually and reported them; `npm run test:code` end to end was listed as "not run". The merge then failed `validate:tideline-runtime`: it drives `InputController` under a Node stub (bare `EventTarget` window, no global `Element`), and the new focus rule did `target instanceof Element` → ReferenceError.
- **Why:** the validators I picked were the ones touching files I edited; the failing one touched a file I edited only indirectly (input.ts is imported by every circuit runtime validator).
- **How to apply:** before calling any pass "verified", run `test:code` fully (≈4 min) and quote its exit code. Anything in `src/game/input.ts`, `action-gate.js`, `input-shaping.js` must be duck-typed (no `instanceof` on DOM globals) because `validate-tideline-runtime.mjs` and `validate-polarity-runtime.mjs` stub `window`/`document`/`navigator`.

**Scar 2 — the HUD scripts parse `--flag=value` only.** `--port 5200` silently falls back to 5310 and `--out` to `art/evidence/hud`, so a mistyped run hits the wrong server AND overwrites committed evidence. Always `--port=NNNN --out=DIR`; check `git status art/evidence/hud` after any run.

**Scar 3 — a live harness must wait on game state, never a fixed timeout.** `pause-quit.mjs` waited 9 s for the race; under a loaded dev server Polarity was still streaming, Escape paused an unstarted race, focus sat on RESUME and the hold "failed". Fixed to wait for `#time-value` to advance (as capture-hud already did). Also: never run two Playwright harnesses against one Vite dev server while judging timing-sensitive steps, and never edit `src/` while one runs (HMR full-reloads the page mid-scenario).

**Bundle ceilings:** validate-build.mjs pins raw/gzip/shell ceilings at measured + ~1.5 KiB by convention; Codex's phase E pinned gzip/shell at exactly measured, so any byte fails. HUD re-pinned 964/262/272 → 969/266/277 after making `ability-slots.ts` lazy (bought 3.6 raw / 1.2 gzip KiB).

**Layout margin to watch:** Tideline at 1280×720 with HUD SCALE L clears the standing block by 19.3 px. A third ability row on any circuit breaks it. Measured by `scripts/visual/hud/capture-hud.mjs` (`clearOfStanding`).

**Still unverified after merge:** no human eyeball at full size, no gamepad quit-hold, no contrast measurement, no perf before/after. See [[polarity-work-fork]] for the checkout and [[delegation-model-rule]] for who reviews.

- CONTROLS SCREEN EMPTY AT LAPTOP HEIGHT (found 2026-09-12 while auditing an external UI/HUD prompt; VERIFIED live at 1280x720 — `#controls-screen .controls-list` computes `display:none`, 10 rows / 0 visible). Cause: `@media (max-height: 800px) and (min-width: 701px) { .controls-list { display:none } }` in style.css (~line 1957) was written when the key legend lived on the intro panel; commit 7371a5f moved the legend into the dedicated CONTROLS view but the global rule followed the class, not the screen. The 2026-09-09 `followup-3-menus/controls.png` evidence IS 1280x720 and already shows the empty panel — `menu-paths.mjs` asserted only `controls: true` (screen visible), never that any row rendered, and the reviewer did not eyeball the PNG. Pattern → detection rule → brief update: a component that MOVES screens keeps every media rule targeting its class → when relocating a component, grep every `@media` block for its selector and assert the screen's CONTENT rows have height, not that the screen is visible → menu/screen briefs must name 1280x720 as a mandatory capture and the reviewer must open the PNG, not read the JSON.

- HUD FOLLOW-UP PASS (2026-09-12, branch work/hud-followup, Opus implementer): (1) BUILD CEILINGS SIT ON THE BASELINE — main @ eafe0b9 had 0.63 KiB raw and 6 BYTES shell headroom, so any UI byte fails validate:build; re-pinned measured+~1.5 KiB (974/267/279) per the M1 and 2026-09-09 precedent. Rule: a brief that adds first-paint code must quote the CURRENT headroom from validate-build.mjs, not the ceiling. (2) VITE SERVES THE PREVIOUS STYLESHEET for a moment after `git checkout -- file` — a baseline run became a mongrel tree (main ui.ts + branch style.css); caught only because a computed-style read disagreed with the file. Rule: baseline captures check out src/ and index.html together and settle before launching, and one computed-style probe per baseline. (3) A TWO-LINE H1 costs ~53 px: making the circuit the title pushed the launch button below the fold at 1920x1080 on 5/7 circuits (3 already were on main); fixed by raising the intro compaction media threshold 900->1100 px, not by hiding anything. Rule: any paddock copy change re-runs paddock-captures.mjs at 1280x720, 1366x768 AND 1920x1080 for all seven circuits. (4) Stress case parked: Tideline scale L with every runtime's longest ability phrase at once overlaps the standing block by 11.3 px (main: cleared by 0.6 px); live frames clear >= 7.4 px. Fix candidates: shorter runtime copy or a one-line clamp on .hud-ability__action.
