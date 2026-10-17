---
name: claude-platform-local-research
description: "Owner wants research and heavy runs billed to Claude Platform API credits locally, not Claude Code weekly usage; how that is wired (2026-10-10)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4c6ca233-30a5-409f-8b36-6a97f716a4b6
  modified: 2026-10-10T13:34:36.082Z
---

The owner does not want research or other heavy work to spend their Claude Code weekly usage. That work should run on Claude Platform API credits, from their own machine.

**Why:** the owner said so on 2026-10-10, after I had launched three web-research subagents inside the session. I stopped those agents and kept their partial reports.

**How to apply:**
- Before fanning out research subagents, offer the local runner instead: `npx tsx scripts/research.mts research/briefs/<name>.md` (on branch `feat/claude-platform`).
- The runner authenticates through the existing `ant auth login` OAuth profile in `~/.config/anthropic` (profile "default"). A token-free `models.retrieve` check confirmed that profile works on 2026-10-10. The `ant` CLI binary itself is not installed.
- Running a brief spends the owner's API credits, so get their go-ahead first.
- **Measured cost, 2026-10-10:**
  - competitors brief: 17 searches, $4.09, no prompt caching;
  - channels brief: 20 searches, $7.99, 0 cache reads (cause unknown, and that run saved no usage file);
  - trust brief: 10 searches, $0.92, with top-level `cache_control`, 979k tokens read from cache across 34 server-side iterations.
  - Each run's usage is saved to `research/out/<name>.usage.json`. If cache reads are 0, read that file before changing anything.
- Higgsfield is on the free plan: GPT Image 2.5 is blocked; `nano_banana_pro` at 2k costs 2 credits per image.

Related: [[appcare-landing-open-questions]].
