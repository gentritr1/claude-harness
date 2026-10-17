---
name: b-m6-cascade-spectacle
description: B-M6 cascade spectacle tiering (pure cascadeTier + tier-gated overlay); brief thresholds failed the live curves again; apex-frequency dual-target conflict escalated
metadata: 
  node_type: memory
  type: project
  originSessionId: 0d698d1d-51eb-448a-9532-ddfa7c13cd82
---

B-M6 (P4 "spectacle without swing") implemented 2026-07-09, headlessly green (12 tier tests, full
suite 191), NOT committed. Deliverable: `docs/review-packets/B-M6-cascade-spectacle-review.md`.
Pure `cascadeTier(trace, dailyTarget?)` in `src/juice/cascade/cascadeTier.ts` (exported
`CASCADE_TIER_THRESHOLDS`); tier-gated overlay `CascadeSpectacle.tsx` (edge glow / slam wash / spark
burst) + oversized apex day-total + warmer pops + `apexSlam` haptic, all in `CascadeLayer.tsx`.
Zero sim/scoring/trace/economy changes.

**Scar (4th firing of "sanity-check brief constants against live curves" — see [[m6-round-review]]):**
the brief's provisional thresholds (big 1.5×, apex 2.5× target OR ≥12 ruleFires) caught **84% of
days**. Measured full-stack curve: a MEDIAN day scores 1.88× its goal with 27 ruleFires (the bots
overshoot the low goal target massively even though coin build-swing stays gentle 1.3–2.0×). Retuned
to live percentiles: big 2.8× (~p88), apex 4.2× (~p98), apexRuleFires 50 (~p99). Detection rule
already known — this reconfirms it: **any brief threshold expressed against a game quantity must be
re-derived from a fuzz percentile dump before shipping; never trust the brief's number.** The
measurement pattern that works: set economy env flags in a script, `playRun` to get actions, replay
them through exported `dispatch` to read each day's `lastScoringTrace`+`dailyTarget` (no sim edit).

**Escalated to Fable (unresolved):** the brief's two apex targets conflict — "once per 2–3 runs" AND
"30–60% of runs" can't both hold because apex days CLUSTER in high-scoring runs. Shipped rare
(0.52 apex-days/run, 10.8% of runs); widening to 30–60% of runs forces ~1.5 apex-days/run ("once a
day," which the brief forbids). One exported constant to flip if Fable prefers the other reading.

Byte-identical normal = code-path short-circuit (no RN render-test harness exists): `spectacle` flag
gates the overlay to null, `POP_SCALE_BOOST.normal===1`, apex typography/haptic on `tier==='apex'`
branch only. Recording of apex+big is the HUMAN device gate (can't record headlessly); harness demos
added (`/cascade-harness` → "APEX/BIG (demo)") force the tier via a small `dailyTarget` on the
richest golden. Still can't `git commit` — shared tree churned by Lane A. See [[b-m5-daily-streak]].
