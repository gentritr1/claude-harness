---
name: orchestrator-codex-workflow
description: User runs Claude as orchestrator/reviewer/merger; GPT Codex is the implementer
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a71f4219-b9d9-49d5-a27b-473b18d5814d
---

For Future Debt, the user wants Claude to act as orchestrator: produce precise implementation
specs, hand them to GPT Codex (outside this session), then independently review Codex's diff and
be the only one who commits/merges. See [[debt-comes-due-roadmap]].

**Why:** the user stated "u are an orchestrator and the gpt codex is the implementation, u will
give plan and review its changes and then only u can merge these" (2026-07-03).

**How to apply:** don't implement features directly unless asked; write specs grounded in the real
code (exact type/field names), verify Codex's claims by running tests and reading diffs myself,
and commit only after the spec's definition-of-done gate passes.
