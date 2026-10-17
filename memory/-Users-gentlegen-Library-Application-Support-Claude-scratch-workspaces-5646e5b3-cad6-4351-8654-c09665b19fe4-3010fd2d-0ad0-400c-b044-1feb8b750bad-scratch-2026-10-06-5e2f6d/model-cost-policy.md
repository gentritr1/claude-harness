---
name: model-cost-policy
description: LOMN on Console API credits — Fable only for plan reviews + milestone-end reviews; Opus 5.5 medium / Sonnet 5.5 implement; fresh session per sub-milestone
metadata:
  node_type: memory
  type: feedback
  originSessionId: c8633adf-6274-4881-8605-b50b189e7417
  modified: 2026-10-08T21:58:22.404Z
---

Owner direction 2026-10-08, when switching LOMN work to platform.claude.com API credits ($200 prepaid, $500/month tier limit): Fable 5.1 is expensive, so use it less often.
- **Fable 5.1:**
  - one precise review of each sub-milestone's spec and plan before implementation, so the cheaper models can implement it as written;
  - the final review at the end of each *milestone* (M2, M3…).
  - This replaces "consult Fable before every spec and plan" plus a Fable final review per sub-milestone.
- **Opus 5.5 at medium effort:**
  - the controller session;
  - design-heavy or integration implementation;
  - task reviews of risky code;
  - sub-milestone final reviews.
- **Sonnet 5.5:**
  - well-specified implementation (E2 found no quality gap vs Opus-medium);
  - corpus authoring;
  - mechanical fixes;
  - scoped re-reviews.

**Why:** the prices per MTok (in / out / 1 h cache write / cache hit), read 2026-10-08 on the pricing page:
- Fable 5.1: $10 / $50 / $20 / $0.25
- Opus 5.5: $4 / $20 / $8 / $0.20
- Sonnet 5.5: $2 / $10 / $4 / $0.10

**How to apply:**
- Start a fresh session per sub-milestone, resuming from docs/ROADMAP.md, so the controller's context stays small. Re-sent context dominates agentic cost.
- Fast mode stays off (it costs 2×).
- After the first sub-milestone on credits, read the dashboard spend and record $ per sub-milestone in the ledger. Re-plan from that measured number, not from estimates.

Related: [[claude-only-implementers]], [[lomn-process-experiments]].

Haiku 5.5 (`claude-haiku-5-5`; on the API Claude Code's `haiku` alias resolves to it; subagent frontmatter accepts the full ID):
- Price per MTok: $0.10 in / $0.50 out / $0.01 cache hit, for prompts up to 100k tokens; above that the rates are 5×.
- Proposed for bounded, checkable jobs only: searches, log triage, bookkeeping, mechanical edits, hygiene scans. Never for reviews or design.
- Its main value is keeping big outputs out of the Opus controller's re-sent context.
- Gated on experiment E3: Haiku vs Sonnet on the same inputs, ABAB, 3 runs each (see docs/ROADMAP.md §6).
