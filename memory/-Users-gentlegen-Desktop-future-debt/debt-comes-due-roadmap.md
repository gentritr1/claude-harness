---
name: debt-comes-due-roadmap
description: "Future Debt flagship feature \"Debt Comes Due\" — 4-phase plan, Phase 1 done (commit 346c7ec), Phase 2 (content) next"
metadata: 
  node_type: memory
  type: project
  originSessionId: a71f4219-b9d9-49d5-a27b-473b18d5814d
---

Future Debt's differentiating feature is "Debt Comes Due": confirming a forecast schedules the
corruption's repayment on a player-chosen due beat from an authored `dueWindow`. Spec lives at
`docs/debt-comes-due/PHASE1_DOMAIN_SPEC.md`. Deferral interest/severity was explicitly deferred
beyond Phase 1.

Plan (agreed 2026-07-03): Phase 1 domain (DONE, 346c7ec) → Phase 2a solver-per-k +
ContentAnalysisRunner (DONE, 597e817) → Phase 2b content pack (DONE, 653241e: D_DueChoice free-beat = same-beat kill cancellation,
HP table 2→1/3→1/4→3; E blind 3 HP, all confirms cost 1; gates v3 per f00b4a2 — v2 was
unsatisfiable, one debt costs ≤2 HP) → Phase 3 Unity UI (DONE, a13db18: due-beat selector,
replan DueBeat fix, DEBT markers, playback callout, D/E registered in selector; commit also
carries the mobile fight UI refactor WIP) → Phase 4 spec written (ba9902e, docs/debt-comes-due/PHASE4_PLAYTEST_SPEC.md): Part A = Codex
instrumentation (JSONL playtest event log behind IPlaytestEventSink, session_summary line,
EnablePlaytestLog config flag), Part B = human protocol (5 testers, fight order B/A/C/D/E, D exam
questions, keep/pivot/kill thresholds). Part A DONE (b984c30) — all Codex phases complete;
roadmap code work is finished, remaining items are human-only.
Still user-manual: Unity Test Runner EditMode run + portrait device checklist
(MOBILE_PLAYTEST_QUICK_PASS.md) — CLI compile proxies passed but in-editor runs pending.
After playtests: PRODUCT.md wording update (forecast-required → human-required) on Keep.
Second-pass Higgsfield art landed (cc55c36); regen pipeline notes in MOBILE_ART_DIRECTION.md
(strip SVG bg path + rsvg-convert, never AI background removal).
Branch codex/mobile-focused-fight-ui pushed to origin (SnaxxTech/future-debt) 2026-07-04.

Design theorem (locked 2026-07-03, spec §0): forecast confirmation is strictly non-beneficial at
resolution — any plan that wins with forecasts wins without them at ≥ HP. So "forecast-required"
content can only mean human-required (information), never solver-required;
ForecastEffect.RequiredForWin/ImprovesOutcome are unreachable under current mechanics. Any future
mechanic granting player-side benefits from confirmation must update the monotonicity test.

Accepted deviation in Phase 1: a confirmed Duplicate's source action now logs AppliedCorruption
None (tag moved to the generated echo, with DebtSourceBeat); goldens were re-baselined and v1
replays verify through ReplayResult.WithV1CompatibilityFields(). Replay format is now v2.

**Why:** the workflow is user-as-relay: [[orchestrator-codex-workflow]] — I plan and review/merge,
GPT Codex implements.

**How to apply:** when the user reports Codex work is done, review the diff against the phase spec
gate before committing; keep Phase commits scoped away from the parallel mobile-UI work on the same
branch (watch for pre-staged index entries sneaking into commits).
