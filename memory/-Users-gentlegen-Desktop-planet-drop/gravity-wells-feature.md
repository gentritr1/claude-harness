---
name: gravity-wells-feature
description: Post-MVP
metadata: 
  node_type: memory
  type: project
  originSessionId: 2f83faef-f3fc-4cd6-85b7-1dcbadcd9448
---

Chosen differentiating feature (2026-07-03, from ideation vs. a research report on ahead-of-time mechanics): **Gravity Wells** — bodies at tier ≥ 9 exert a gentle deterministic radial pull (inverse-square, hard accel cap ~9 vs world gravity 42, range 3 attractor-radii, smooth fade). Beat "PB ghost run" (blocked: determinism deferred) and "Egg legacy seeding" (just prestige) on an 11/12 novelty-playability-resonance-feasibility gate.

**Why:** mechanic-deep novelty (all Suika-likes have static gravity; here the player builds the field), thematically inevitable, and it directly attacks the harness finding that tier 12 is unreachable — heavy bodies attract each other, raising late same-tier contact rates. Deliberately NOT a violation of the "benevolent randomness" principle that rejected gravity flips (brief #3): wells are deterministic and player-authored.

**Status 2026-07-03:** Phase 1 MERGED to main via PR #32 (squash `8e16bad`), default OFF. Review fix 4e039d1 = per-FixedUpdate attractor snapshot refresh so high-timescale bot A/Bs don't measure stale-position pull; 231/231 EditMode via Unity MCP. **The in-editor feel acceptance was DEFERRED at user's request — it is step zero of Phase 2**, brief at `docs/briefs/2026-07-03-gravity-wells-phase2.md` (main `436e1e3`). Chunks D+E (decision metrics merges_t10/11/12 + awake_mean_fraction in bot CSVs, A/B runbook at ConfigureGravityWellsForBatch) MERGED via PR #33 (squash `d8b61a9`, 234/234 EditMode). Decision-gate table pre-committed (kill after two failed retunes, flag stays OFF, delete nothing). **What remains before any Phase 3 work: user runs step-zero feel check, then two ≥30-run GreedyMatch batches (wells off/on) and we evaluate the gate.** Phase 3 (bent aim line, lensing ring, haptic, default ON) locked until the gate passes.

**Plan:** Phase 1 brief at `docs/briefs/2026-07-03-gravity-wells-phase1.md` (branch `post-mvp/5-gravity-wells`): Chunk A pure `GravityWellMath` + EditMode tests; Chunk B `GravityWellController` (kinship-controller pattern, FixedUpdate AddForce, never wakes sleeping bodies, skips non-simulated/Consumed so it can't fight merge convergence, default OFF behind `game.gravity_wells.*` config + DEV drawer toggle); Chunk C bot-harness A/B hookup. Phase 2 = harness kill/keep gate (kill if piles jitter/never sleep, fail-line variance explodes, or no tier-11/12 merge-rate gain). Phase 3 (only after data): bent aim line, lensing visuals, haptics.

Related: [[agent-playtest-harness]], [[merge-feel-convergence-gap]], [[retention-addictiveness-plan]].
