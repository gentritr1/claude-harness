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

**Measured 2026-10-09** (Console billing; the JSON cost matches the Console log):
- small fix: Sonnet $0.19, Haiku $0.02, with the same quality;
- medium fix: Sonnet $0.40;
- thorough review: Opus-medium $0.86.

Estimate: $45–90 per sub-milestone; $200 covers about 2–4 sub-milestones; the first playable area needs about $400–900. Details in docs/ROADMAP.md §4.1. Re-measure after the first full sub-milestone on credits.

**Billing split (owner, 2026-10-09):**
- Fable reviews and the controller run on the owner's Max 20x plan: Agent-tool subagents from the desktop session bill to the plan.
- Implementation also runs on the plan by default.
- The $200 Console credits are for overflow when plan limits are hit, for parallel bursts, and for exact-$ measurement. Headless `claude -p` bills to whatever account the terminal CLI is logged into, currently the Console.
- **E3 verdict, 2026-10-09:** ADOPT Haiku 5.5 for bounded, checkable mechanical jobs. It was correct 3 of 3, the same as Sonnet, at 8.5–16× lower cost. The controller still verifies each job. Haiku's edge-case design choices get one extra read: in rep 3 it chose a -1 sentinel where Sonnet's 0 is sturdier.
- 2026-10-09 Haiku miss (M2a-2 integ fix): asked to write the text 
- 2026-10-09 Haiku miss (M2a-2 integ fix): asked to write the text \u00ff in a doc, it wrote the literal character (U+00FF). A precision slip on an edge case, caught by the controller's extra read; harmless (doc only). Keep the extra read on Haiku output.
- 2026-10-09 Haiku miss #2 (docs batch 3a3a6eb): appended the Co-Authored-By trailer to the commit SUBJECT line instead of a separate trailer line. Cosmetic, left in history (rewrites are owner-gated). Pattern: Haiku slips on format details; give it the exact `git commit -m "subject" -m "trailer"` command.
- **2026-10-09 owner: the Max plan's weekly usage is at 80%, so NO more plan usage for LOMN.** All further work runs from a terminal `claude` logged into the Console account (credits), in a fresh session. Do not dispatch from the desktop session.

- 2026-10-09: owner approved ~/.claude/agents/Explore.md (Haiku 5.5, medium, Read/Grep/Glob) replacing the built-in Explore (which follows the main model). Trial: compare the next headless run cost vs ctl-p89 (started before the change). Researcher agent and main-session high effort were NOT adopted (low use / raises credit cost).
- 2026-10-09 Explore A/B (6 read-only runs, ABBAAB, frozen 5353e97, 6 Qs / 15-pt key from grep incl. a decoy): Haiku 15/15 x3 at $0.012/$0.068/$0.013 (22-75 s); Opus 15/15 x3 at $0.38/$0.36/$0.22 (38-49 s). ~10x cheaper, same accuracy, time within spread. CEILING: the questions did not separate the models; re-test with harder cross-file questions if a Haiku Explore miss is ever seen. Adopted.
- 2026-10-09 ctl-p89 headless controller (Opus medium, Console): pairs 8+9 merged at 2b84505, $35.94 (Opus 25.45, Sonnet 10.49), 49 min. A $45 cap made it skip 2 scoped re-reviews.
- 2026-10-09 ctl-f7t10 run: only F7 done (merged a794f04, ROADMAP 1ba99cc), $34.91 (Opus 22.32, Sonnet 12.58, Haiku 0.01); the F7a C++ Opus implementer alone ~$15 (360k-token context). Controller stopped at its $38 line before Task 10. Lesson: "small" multi-item batches on Opus are not small; estimate per implementer context, not per item. Verified by me: trace 541/541, osi-a9 4/4, 974 passed, 69 natives tier1 35/tier2 34/stub 0, taint 0 sinks.
