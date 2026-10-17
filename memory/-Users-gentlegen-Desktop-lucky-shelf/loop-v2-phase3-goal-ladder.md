---
name: loop-v2-phase3-goal-ladder
description: Phase 3 goal ladder — IMPLEMENTED + reviewed APPROVE, committed de12a3d (flag OFF, requires LOOP_V2).
metadata: 
  node_type: memory
  type: project
  originSessionId: 055e11c1-e558-4c66-b0dc-b4986591cb9e
---

Phase 3 = **daily coin target + reward** layered over rent (Balatro-blinds heartbeat). Brief written
2026-07-07 at `docs/lane-a/loop-redesign-phase3-goal-ladder-brief.md`, ready for a fresh Codex/Lane A
session. Not yet implemented. Flag `GOAL_LADDER_ENABLED` (default OFF).

**Traced the loop unit first** (honoring [[goal-horizon-vs-resource-cadence]]): per-day `dayTotal` at
openShop, 1000 runs greedy+combo under `LOOP_V2_ENABLED=1` (levers ON, sigs OFF). Greedy ≈ combo. Curve
rises fast d1–6 then **PLATEAUS at median ~89 / p25 ~77 from day ~8** (12-slot board saturates); ~5%
attrition by day 12 (rent doesn't kill competent play). Full table is embedded in the brief.

**Design:** target ≈ **0.7× greedy median** (≈p25–p30 → competent play beats it ~75% of days). Reward =
**one next-shop free reroll token** (0/1, spent before coins; doesn't inflate coins/undercut rent).

**IMPLEMENTED by Codex + reviewed APPROVE, committed `de12a3d`** (stand-in `A-M5d-fable-review.md`,
packet `A-M5d`). Codex **tuned the targets UP** from the brief's `[15..62]` to
`[16,24,34,39,49,59,62,68,72,74]` (cap 74) because the originals fuzzed to ~90% hit (too easy). I
re-verified: cap 74 < p25 ~77 < plateau ~89 (scar holds), and an **independent 800-run ON fuzz** gave
in-band late-day hit (greedy 0.746 / combo 0.769 days 9-12, overall 0.79/0.81, random 0.001, game-over
1.000). Additive contract fields (dailyTarget/dailyTargetResult/freeRerollTokens), no schema bump.
Graduation still gated on real Fable sign-off + device feel-gate.

**Scar baked into the brief as a HARD requirement:** the target must **cap below the ~89 yield plateau**
— a target that climbs past it is unfillable by construction (the exact prior scar). Acceptance forces
validating the **late-day (9–12) hit-rate**, not just the early ramp; band 65–85% across the whole
curve; rent must still bite (game-over within ±3pts of baseline). No `ContractSchemaVersion` bump
(additive optional fields). See [[loop-v2-phase1]], [[loop-v2-phase2a-tag-synergy]].
