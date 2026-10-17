---
name: perf-audit-2026-10-05
description: "Measured performance facts (prod build, M1 Pro) — shaders never precompiled, light-count toggles recompile scenes, garage snap camera, load bytes; harness location"
metadata:
  node_type: memory
  type: project
  originSessionId: bc22fd48-292b-4c01-8557-bda18d130dff
  modified: 2026-10-05T20:58:19.987Z
---

Audit 2026-10-05 on main b93ff29 (Opus investigator; orchestrator spot-checked the code claims). Prod build via vite preview, Chrome 154 headless=new on ANGLE Metal (real GPU), frame counts reconciled vs window×60 Hz.

- "ASSEMBLING TOTEM" = the initial loading screen (index.html:270), not the garage. Circuit switch is a full page reload (launch-menu.ts → location.assign), so players see it on every circuit change.
- NO `compile`/`compileAsync` outside src/review/ (grep-verified). First frame blocks 354–768 ms compiling 47–91 programs (link-status waits). Cold vs warm differs hugely (macOS Metal program cache): garage open 1254 ms link wait cold → 68 ms warm. Always state cold/warm when quoting.
- Light-count changes force scene-wide recompiles: hangar lamps `visible` toggle (atmosphere.ts:835) → Greenwater 52 programs mid-race (4.55 s cold / ~300 ms warm frame); garage `serviceLight.visible` (garage-scene.ts:158). Fix pattern: keep lights visible at intensity 0. A/B (via __THREE_DEVTOOLS__, no repo edits): constant lights + compileAsync + warm render → mid-race programs 52→0–1, worst frame 300→117 ms (residual unexplained).
- Greenwater `relocateCorridorObstacles` (course-repair.ts:263) blocks ~900 ms right after the menu shows (course.project per vertex).
- Garage camera = `1-exp(-delta*13)` ease (garage-scene.ts:152): 19.5% of the move on frame 0, 90% in 183 ms → reads as a snap. Garage open cold 1483 ms (Fog + light change recompiles TOTEM; 2nd AudioContext in garage-sound.ts:49).
- Bytes per circuit 14.8–17.9 MB cold; no Draco/meshopt/KTX2; gzip alone ~5× on env GLBs; `_headers` has no Cache-Control.
- Steady driving fine: p95 16.7–16.8 ms all circuits.
- Harness + results: /private/tmp/claude-501/perf-audit/ (load.mjs, garage.mjs, cam.mjs, warm.mjs, profile.mjs; raw CDP via `node --experimental-websocket`, since Playwright is not installed). Temp dir — may vanish.
- Scar: two agents' headless Chromes on the same debug port contaminated a run — give each agent its own port and verify ownership by PID. Same for Vite: a "free-looking" port (5198) was held by a background agent's server, so a review audit would have measured the wrong tree — `lsof -nP -iTCP:<port> -sTCP:LISTEN` before choosing, and use `--strictPort`.
- Frostline grounding review 2026-10-05 (work/frostline-grounding 9552fb9): orchestrator re-ran scripts/frostline/grounding-audit.mjs on pre-fix b93ff29 → 1,397 props >0.5 m (max 53.62 m), on the branch → 0 (max 0). Audit samples the real ground mesh triangles, not the placement function, so it is not self-confirming. Buried props 12→33, terrain max slope 35°, env tris +1.6%.

- Owner rule 2026-10-06: headless Chrome (`--headless=new`) PLAYS game audio through the speakers — every harness Chrome launch must carry `--mute-audio` (AudioContext still created, so measurements are unchanged). Put it in every brief that drives a browser.
- Reviews 2026-10-06 (orchestrator re-ran each harness on prod builds of b93ff29 vs branch, muted):
  - work/garage-smooth APPROVE (eyeball pending): open 283→33 ms, first part 67→16.8, links 10→0, camera first step 19–48 %→2.6 %, t90 ~150→~295 ms, retarget turn 129°→36°. validate:garage-b2 fails on old scene for the camera (19.5 %), not only the lights rule. Trade: menu gets one 150 ms headless long task (AudioContext prewarm) — real Chrome on this Mac creates an AudioContext in 8.8 ms, so likely headless-only (UNVERIFIED in-game).
  - work/perf-warmup APPROVE: mid-race programs 51/14/10/11→0 on all 4 circuits; Greenwater menu freeze 1133/1217→33/17 ms, mid-race worst 383/350→16.8/49.9. One Night Shift 283 ms frame (0 programs) did NOT replicate in 3 interleaved re-runs at load 16–50 (branch 16.8/16.8/33.4 vs base 67/50/50) → noise.
  - Owner said "merge them all" 2026-10-06 → local main fast-forwarded b93ff29→1c19441 (= work/integrate-2026-10-06: phone-pass-2 + frostline-grounding + perf-warmup + garage-smooth); test:code exit 0 (134 steps) on that exact commit. Pushed to origin/main 2026-10-06 with owner OK (ls-remote confirmed 1c19441).
- Scar: a single-run outlier with no compile/GL cause → interleave ≥3 A/B re-runs before blaming or clearing the branch.

Related: [[phone-controller]], [[consolidation-2026-10-04]].
