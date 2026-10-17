---
name: loop-v2-phase2b-build-steering
description: Phase 2b build-steering — IMPLEMENTED + reviewed APPROVE, committed 5e0797a (flag default OFF).
metadata: 
  node_type: memory
  type: project
  originSessionId: 055e11c1-e558-4c66-b0dc-b4986591cb9e
---

Phase 2b = **build-steering / supplier lean** (research mechanic #3, "plan from turn 1"). Brief at
`docs/lane-a/loop-redesign-phase2b-build-steering-brief.md`. **IMPLEMENTED by Codex + reviewed APPROVE,
committed `5e0797a`** (with 2a); packet `A-M5e`. Flag `BUILD_STEERING_ENABLED` default OFF. **Pairs with
2a** — you lean the tag whose synergy ladder you then climb.

**Chose path B** (additive `chooseSupplier{tag}` action + `GameState.supplierTag`, no schema bump).
**Deviation from brief (accepted, flag for Fable/feel-gate):** Codex made the supplier pick **MANDATORY**
at opening delivery (draft blocks until chosen), a stronger "commit turn 1" than the brief's "legal once."
**Lane B dependency:** flag-on requires a supplier-picker UI or opening delivery is stuck. Review
evidence: OFF byte-identical (pin held, createRun omits supplierTag when off); own scenario confirmed
mandatory gate + bias ×2.5 exact + pool not locked (food offers 148→277/300 seeds, 623/900 still
non-food); own mutation (neutralize bias) dropped Codex's weight test + my checks. Graduation gated on
Fable sign-off (CCR: supplierTag + chooseSupplier) + device feel-gate.

**Design:** additive optional `GameState.supplierTag`; `generateOffers` multiplies `offerWeight` of the
leaned tag by `BUILD_STEER_BIAS` (~2.5, must NOT lock the pool). Eligible leans = the synergy/
`DEMAND_TAG_POOL` tags. Choice mechanism — recommended **(B) a new `chooseSupplier{tag}` action** (a
new additive variant of the strict `ActionSchema` union, legal once in the opening delivery phase, NO
new `GamePhase`, NO schema-version bump — but it's a contract change ⇒ CCR); lighter fallback **(A)**
seeded lean + targeted reroll (no new action). Codex picks with rationale.

**Acceptance = the spec bar "fuzz shows distinct archetype runs":** a steering bot ends with a higher
dominant-tag count than unsteered (runs visibly separate into archetypes), and game-over rate +
bestDayTotal stay within ~±3pts of baseline (steering shapes runs, doesn't inflate them). OFF path
byte-identical (goldens + pin `8d48e1c5a6ad14c9`), no new legal action surfaces. See
[[loop-v2-phase2a-tag-synergy]], [[loop-v2-phase1]].
