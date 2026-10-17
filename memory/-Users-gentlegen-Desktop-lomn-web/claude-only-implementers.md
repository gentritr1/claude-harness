---
name: claude-only-implementers
description: "For the LOMN web port, all coding is done by Claude (main session + Claude subagents) — never Codex"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c8633adf-6274-4881-8605-b50b189e7417
  modified: 2026-10-06T22:39:33.230Z
---

All implementation work goes to Claude subagents (superpowers subagent-driven development), not Codex.

**Why:** user said 2026-10-07 "we only code in claude not codex" when choosing option A (Claude specs, splits work across parallel subagents, reviews each piece).

**How to apply:** plans and briefs target Claude subagents; Claude main session specs, reviews (re-running the failure scenario per CLAUDE.md §6) and owns git. Related: [[lomn-web-port-probes]].
