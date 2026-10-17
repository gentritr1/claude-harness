---
name: consolidation-2026-10-06
description: Repo state after the 2026-10-06 merge — main 1c19441 everywhere, only main locally, GitHub = main + 3 backup/* branches
metadata:
  type: project
---

State on 2026-10-06 after merging phone-pass-2, frostline-grounding, perf-warmup and garage-smooth:
- Main folder and origin/main both at 1c19441; `main` is the only local branch; GitHub holds main + backup/{craft-art-review,handoff,polarity-work}-2026-10-04 (the only copies of deleted folders — keep).
- `.claude/worktrees/integrate` sits detached at 1c19441 and runs `npm run dev:phone` (its .cert is the one the iPhone accepted). Detached on purpose: a worktree on `main` blocks the main folder from checking out main.
- Old uncommitted phone prototype from the main folder is in local tag `backup/phone-prototype-2026-10-04` (superseded by main).
- `.claude/launch.json` in the main folder carries the owner's local edits — never commit or overwrite it.

**Why:** next session starts from a clean single-branch repo; earlier sessions found stale folders and branches.
**How to apply:** branch new work from main; don't put `main` on a worktree. Related: [[consolidation-2026-10-04]], [[perf-audit-2026-10-05]].
