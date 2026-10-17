---
name: lane-wip-lives-in-main-checkout
description: "Cross-lane reconciliation edits must happen in the main checkout, not a lane worktree"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9a1bffae-24fd-4e33-8cdf-065ce5d3b000
  modified: 2026-08-16T20:43:16.491Z
---

Lane worktrees under `.claude/worktrees/` share committed history but never see other lanes' *uncommitted* files. As of 2026-08-16 the home rework (HomeScreen.tsx/css, HomeMailroomHero) and the strict-matching e2e edits sat uncommitted in `/Users/gentlegen/Desktop/odd-hours` on `main`, while lane branches were all at the same HEAD (bdea5ca).

**Why:** an edit made in a worktree against a screen that only exists as WIP elsewhere can't be run or verified, and will conflict textually when the WIP commits.

**How to apply:** before touching cross-lane files (e2e/helpers.ts is the usual suspect), run `git -C /Users/gentlegen/Desktop/odd-hours status --short` — if the files you depend on are modified there, edit and verify in the main checkout directly.
