---
name: agent-worktree-isolation-cuts-from-main
description: "Agent isolation:\"worktree\" branched from main (305d2d7), not feat/next-level — make the worktree yourself and have the dispatch verify HEAD"
metadata:
  type: feedback
---

On 2026-10-02 a fix-round implementer dispatched with `isolation: "worktree"` landed on `main`'s tip (305d2d7, release
1.5.0) instead of feat/next-level's a506e34. It only noticed because the dispatch said "verify HEAD is a506e34, else stop".
Had it not checked, it would have "fixed" B2-5 code that did not exist on its base.

**Why:** the tool cuts from the default branch, not the session's current branch.

**How to apply:** on a feature branch, create the worktree yourself (`git worktree add -b <name> <scratchpad path>
<sha>`, symlink node_modules) and pass the path; every dispatch states the expected HEAD sha and says to stop if it
differs. The symlinked node_modules shows as untracked — tell the agent to stage paths explicitly.
