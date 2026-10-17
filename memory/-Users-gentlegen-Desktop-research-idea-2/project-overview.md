---
name: project-overview
description: "Fuseline — draw-a-fuse path-order roguelite; concept Fable-APPROVED 2026-07-18; Opus executes, Fable reviews, loop until agreement."
metadata: 
  node_type: memory
  type: project
  originSessionId: 34efc46f-cf4b-48ec-91db-1c0e87da9387
---

**Fuseline** (research-idea-2): web game — draw one wire through a seeded 5x5 grid; tiles
fire in drawn order (Spark +5, Amp x2, Coil +4/fired, Twin x3-after-multiplier, Static
-25% tax); 3 pulses/round, 8 rounds, per-board-per-BUILD par with clearability certificate;
charm draft between rounds. Concept approved 2026-07-18 after a 2-round adversarial loop
(round 1: REQUEST CHANGES — name collision with Steam game "Filament", invented numbers;
round 2: all numbers solver-derived, reviewer reproduced them).

Workflow (user-mandated): **Opus 4.8 is the executor, Fable orchestrates/reviews/owns git;
loop every deliverable until Fable can genuinely agree.** Rubric frozen in docs/RUBRIC.md.

Key docs: docs/CONCEPT-SPEC.md (the build bible), docs/concepts/FABLE-REVIEW-round{1,2}.md,
docs/research/*.md (3 research reports + synthesis). Solver: tools/fuseline-solver.ts
(dependency-free TS; commands: check/metrics/calibrate/sim/timing/examples; Node 24 native
type-stripping). Baseline commit d8fdc20.

Honest-contract pillars (product identity, from negative-review research): no ads/energy/
dark patterns; visible seed; provable beatability (certificate); local-first additive-schema
save + export; bounded 4-8 min sessions; daily = shared seed, streak not load-bearing.

**STATUS 2026-07-18 end of build day: M1+M2+M3 ALL SHIPPED & Fable-approved** (commits
f738465, cddd3fd, 60a054a; whipsaw ruling 177a027). 88 tests. Game is feature-complete
for v1: playable 8-round loop, certificate replay, points ledger (100xcharge/B0 cap
1000), full juice pass (flame front, weld flash, static crack, shatter, procedural
audio), honest daily + spoiler-safe share, stats/settings/export-import. Reviews in
docs/reviews/. Dev server: preview_start "fuseline" port 8090.

**THE open gate: HUMAN EYEBALL/FEEL PASS** (spec §16 protocol: flame pace, shake, audio,
drafting-feels-fair, 5-session playtest with pre-registered delta par-discount fallback).
Device-gated: real touch drag, literal getFrameStats, phone worker par timing. Watch
items: UTC daily rollover, stats counts replays (deliberate), targets can drop between
rounds (honest), session length unobserved.

Related: [[node-and-ports]], [[loop-discipline]].
