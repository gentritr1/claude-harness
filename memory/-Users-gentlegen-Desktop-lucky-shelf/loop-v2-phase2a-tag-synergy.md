---
name: loop-v2-phase2a-tag-synergy
description: "Phase 2a tag-set synergy — IMPLEMENTED + reviewed APPROVE, committed 5e0797a (flag default OFF)."
metadata: 
  node_type: memory
  type: project
  originSessionId: 055e11c1-e558-4c66-b0dc-b4986591cb9e
---

Phase 2a of the loop redesign = **escalating tag-set synergies** (build identity). Brief at
`docs/lane-a/loop-redesign-phase2a-tag-synergy-brief.md`. **IMPLEMENTED by Codex + reviewed APPROVE,
committed `5e0797a`** (with 2b). Flag `TAG_SYNERGY_ENABLED` default OFF; packet `A-M5c`. Review evidence:
OFF byte-identical (pin held), best-tag-not-product proven by orchestrator's own scenario (a drink:4/
fancy:5 item took one 1.6 fire, not the 2.24 product), own mutation dropped 6 tests. Graduation still
gated on Fable sign-off (scoring-order CCR) + device feel-gate; p95 ceiling rises (flagged for Fable).

**Design (baked into the brief, my recommendations):**
- New flag `TAG_SYNERGY_ENABLED` (default OFF) in `src/sim/economy.ts`; ladder `<3→×1, 3→1.2, 4→1.4,
  5→1.6, 6+→1.8` over the eligible tag set (reuse `DEMAND_TAG_POOL`). All magnitudes provisional.
- Each item multiplies by its **single best qualifying tag** (max, NOT product) — legible + bounded +
  rewards committing to one archetype.
- **Supersedes** the [[todays-order-demand]] lever when ON (skip the `order` ×1.5 branch, no
  double-mult); featured-tag steering returns in Phase 2b. When OFF the `order` lever is untouched.
- **No contract/schema change** — derived from shelf tag counts at scoring time like `orderMet`; slots
  into scoring.ts exactly where the `order` mult sits (after ambient auras, before spotlight). Emits
  `ruleFire{ruleId:'synergy', delta:{mult}}`, reusing the existing multDelta shape — no new TraceEvent.

**Three taste-forks flagged for relay/Fable sign-off** (brief implements the recommended path):
best-tag vs product; supersede-vs-stack with Today's Order; floor at 3 (commitment) vs 2.

**Graduation gate** (same as every phase): OFF byte-identical (goldens + pin `8d48e1c5a6ad14c9`), fuzz
A/B must show distinct archetype runs AND that rent still bites (loss rate not ~0), then device
feel-gate. See [[loop-v2-phase1]], [[reviewer-workflow-opus-split]].

**Repo note:** all redesign work is committed **directly on `main`** (unpushed), not on a
`loop-redesign-and-ui` branch as some handoff text implies.
