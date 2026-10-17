---
name: pending-m1-fun-gate-review
description: WaveDNA M1 fun-gate recordings review was deferred — must happen before/with M2 acceptance
metadata: 
  node_type: memory
  type: project
  originSessionId: 480e5785-95e4-4d09-8545-b11343b8efa4
---

As of 2026-07-05, WaveDNA M1 (commits `a53964d`, `4daed6d`) was accepted on code evidence only. The §5 fun-gate review — matching the 4 requested screen recordings (20s calm + 20s choppy with sound, one summary-screen run, one fixture-switch clip) to their DNA blind — was deferred at the user's request so M2 could start.

**Why:** The kickoff brief says M1 is the stop-and-fix gate; if calm/choppy aren't distinguishable by thumb rhythm alone, tuning must happen even if M2 rendering has landed.

**Update 2026-07-05 (web preview live):** Expo Web preview now works — `.claude/launch.json` config `wavedna-web` (port 8091, needs Homebrew Node via PATH prefix; shell default Node 14 breaks everything). `src/app/index.tsx` has a web-only WithSkiaWeb shim (CanvasKit from jsdelivr CDN) — do not "simplify" it into a static import, Skia must not evaluate before WASM loads. Fable can now verify visual passes directly on web. M1.5 (`e83919d`) fixed the zero-input scoring (now exactly 0; pumped runs score thousands with correct calm/choppy asymmetry) and cleaned haze/silhouettes. Remaining before gate close: device recordings must confirm shore finale (not verifiable on throttled web tab), shell reachability feel (naive pumping collects only 1-2 shells), foam-dash polish still deferred. Note: unfocused preview tabs throttle rAF to ~1fps — use headless `runReplay` via tsx for sim checks instead of waiting on live runs.

**Model split (2026-07-05, user-approved experiment succeeded):** Codex implements sim/generation/perception logic; Claude Opus 4.8 does design passes (M2.1 UI chrome pass `572a1b1` was high quality, perfect scope discipline). M2.2 scene beauty pass landed (`2c145d1`, accepted): foam dashes → crest patches + edge line, shore beauty, shell halos, wind-tile key fix, PathBuilder migration. Open tuning directive: foam caps too dominant on high-amplitude beaches — halve the `wave.primaryAmplitude * 0.12` size term in buildFoamCrestPath and flatten cap profile (wider than tall, trailing taper). Remaining deprecations (pointerEvents/textShadow*) live in game-screen.tsx, owed to a future UI pass. Codex approved to start M3 perception (boundaries: /src/perception + screens only; render files were Opus's). Preview port 8092 (8091 held by another session).

**Update 2026-07-05 (screenshots reviewed):** Visual distinctness PASSES (4 fixtures instantly distinguishable). Surfer-at-origin transform bug found and fixed. Open fun-gate finding from the user: input agency isn't legible — surfer auto-rides and holding barely changes the picture. Feel sprint directed before M3: visible hold (tuck+dip+spray), launch pop, felt speed (wake/camera), no-input runs ~60-70% speed of pumped runs. Gate closes on: 15s video where thumb timing is readable + four fixture videos (sound on, note jank).

**Update 2026-07-06:** M3 perception landed (`aabc62e`), code-approved. Entry route is now the scan screen; game moved to `/play` (web shim preserved there). Outstanding M3 acceptance: user must supply 4-6 real sea clips + 1 pool/indoor clip and set `EXPO_PUBLIC_ANTHROPIC_API_KEY`, then verify end-to-end scans (calm vs rough clips → different games; pool clip → Mystery Waters). Security: EXPO_PUBLIC key is bundled into the client — M6 blocker: store builds must use the proxy path, never a direct key. Cost note: ~1-2¢/scan on Sonnet 5; after M3, eval Haiku 4.5 against fixture clips as config-only downgrade.

**How to apply:** When the user shares recordings, run the deferred M1 feel ruling first. M2 code landed as `8d3be8b` (approved 2026-07-05); M2 acceptance still needs from recordings: M1 fun ruling, per-fixture visual distinctness, motion never freezing, observed 60fps on mid-range Android. Remaining polish owed before/with M4: palette-tinted silhouette ink, real foam crest patches (replace DashPathEffect look), run-summary panel breathing, real type pairing via expo-font (no system fonts past M4 — postcard is a beauty-blocker). Frontend-design skill standards apply to M4/M6 reviews.
