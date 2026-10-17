---
name: minimap-directions-design
description: "2026-09-27 minimap A/B/C study on a Claude Design canvas — facts found, the Design-runtime SVG-text scar, how to render a canvas headlessly, open gaps"
metadata:
  node_type: memory
  type: project
  originSessionId: bc22fd48-292b-4c01-8557-bda18d130dff
  modified: 2026-09-26T23:04:55.033Z
---

Canvas: https://claude.ai/artifact/GCLuM8TWWadJ2UmREDUJpP (private). Directions: A Circuit Signature (whole-lap ribbon), B Corner Radar (heading-up local), C Arcade Sector Board (replaces the NEXT GATE strip). Build scripts live in the session scratchpad only (build/lib.js sim, vm.js, tpl/*.html, build-dc.mjs); nothing was changed in src/.

Facts found (VERIFIED by capture/grep):
- Shipped minimap is `display:none` on every landscape phone (style.css `@media (max-height: 520px) .minimap`) and at max-width 700px. Phone players currently get no map at all.
- HUD "NEXT GATE xx / yy NAME" uses `sectorLabelAt(player progress)` — the sector you are IN, not the gate's name (ui.ts ~841). Finish gate reads "LAP GATE ARMED" / "FINISH VECTOR ARMED".
- Night Shift turn table = nightshift-course.ts constructor (|curvature| ≥ .003, peak radius); resampled geometry underestimates curvature badly — use the source station curvature.
- Existing phone HUD bug: NEXT GATE strip overlaps the P#/4 plate and lap block at 844×390.
- Rendered on-screen positions: race-time block starts ~x1060 CSS at 1280×720; the gate strip spans ~x390–890 (frames are 2x DPR — scale screenshots by 1.28 then /2, I misread this once).

Scar — Claude Design (.dc.html) runtime wraps EVERY `{{hole}}` in `<span class="sc-interp">`; inside SVG `<text>` that span never renders. Dynamic labels must be HTML overlays; static SVG text is fine. A string-substitution harness cannot catch this.
- **How to apply:** render with the real runtime headlessly: `artifact-type/dc-runtime.js` is the self-contained `support.js` (bundles React). Playwright `page.route` serving project files + `/_blob/<id>` from disk, no sign-in needed (the built-in browser is not signed in to claude.ai).

Open gaps (updated 2026-09-27): A+ is in-game behind the dev flag and recorded, but final sign-off is the user's moving-game judgement (not given yet); recordings are headless ~22 fps, not a real device; phone strip overlap is pre-existing (spawned task). Related: [[hud-integration-scars]], [[futurisma-architecture-facts]].

**2026-09-27 A+ implementation (branch work/minimap-aplus, uncommitted):** `src/game/minimap-aplus.ts` (new) + a dev-only delegate in `minimap.ts`; `?minimap=aplus` on the dev server. Prod bundle verified byte-identical per file (3,161,032 B, 91 js/css) and test:code exit 0 (57 validators).
- **Gate indexing scar:** `checkpointProgress(0)` is the lap line; intermediate gates are 1..checkpointCount, so a lap has count+1 sectors. Looping `i < checkpointCount` silently drops the LAST gate (both canvas data and first A+ build did; caught only because a plate read "S8/7").
- **Seam budget scar:** `validate:seams` pins game.ts at exactly its current length (2577/2577) — zero headroom. Integrate new systems via an existing module's call site (minimap.ts already gets everything per tick), never by line-stuffing game.ts.
- **`import.meta.env.DEV` crashes `validate:polarity-minimap`** (it transpiles minimap.ts via oxc into a data: module with no env). Use `import.meta.env?.DEV` — still folds out of the Vite build (verified byte-identical).
- **Recorder naming scar:** a reduced-motion run reused the full run's file name and overwrote its video + JSON; the first NS comparison was built from the wrong clip. Name every run by every varying parameter; count announcements from the plate's own `animate()` calls, not a 0.5 s DOM sampler (it missed one 0.9 s plate) nor the diagnostics counter (lags its ~1 s report).
- Pre-existing, not mine: `validate:dreamisland-painted` rewrites `art/evidence/dreamisland-v1/phase-c/validators/painted-validation.json` with a different painted.glb sha256 (6027368… vs committed 7bb24e…) — evidence is stale vs the served GLB. Restore it after any test:code run.

**2026-09-27 commits on work/minimap-aplus (not pushed):** e47a601 A+ dev-only checkpoint; 0aebf7e phone gate-strip fix (two-row strip bottom-right on max-height 520, top 264 on max-width 700). Evidence + pre-existing overlaps: art/evidence/minimap-aplus/README.md. User decision: A+ is the chosen direction; default-on waits for a real-device driving check.
- **Harness scars:** the dev server listens on `[::1]:5173` only, and `capture-hud.mjs` hard-codes 127.0.0.1 and bundled Chromium (not installed). Ran it via a `node --import` shim (`chromium.launch` → `channel:"chrome"`) plus a throwaway 127.0.0.1→[::1] TCP relay; never edit the harness for this.
- **Design-runtime scars (beyond SVG holes):** bare boolean attrs (`controls`, `muted`, `loop`) are stripped (React reads "" as false) — use `attr="{{yes}}"`; the hidden `<x-dc>` source is live DOM, so its `<video>` copies load and fire inline `on*` media handlers (`{{x}}` → ReferenceError) — poll media state instead; a `ref` attribute is evaluated as code — find elements by id. Playwright `getByRole({name})` is substring-matching: "Play" hit "PLAY ALL" — use `exact: true`.
- **Audit rule that paid:** worst-case audits (force transient banners/alerts on) found the portrait strip under the banner slot; a count claimed in a README (228) was wrong vs the JSON (212) — generate counts from data.
- Pre-existing (not fixed): Dream Island 1280x720 lap block overlaps the strip 27.5 px (identical on HEAD CSS); Dream Island portrait HUD skin broken; portrait RACE TIME overlaps lap block; Tideline 844x390 ability column pushes drive block over standing.
