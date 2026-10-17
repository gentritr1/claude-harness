---
name: shared-tree-agent-collision
description: Two implementer agents in one checkout corrupt each other's verification; the worktree + git apply --cached recovery, and the scheduling rule that prevents it
metadata:
  type: feedback
---

2026-09-26, Tondo Tier 2/3: I dispatched the Task 10 implementer while the
Task 9 implementer was still live in the **same working tree**. Task 9's
verification matrix started failing with `ReferenceError: hideShareBtn is not
defined` — code it had never touched — because Task 10 was mid-write.

**Why it is worse than a merge conflict.** A half-written file from agent A is
indistinguishable, in agent B's verification output, from a regression B just
caused. B can spend a round chasing a phantom, or worse, "fix" it. And either
agent can `git add` a file holding the other's unfinished work and commit it.

**The recovery that worked** (Task 9's agent found it unprompted): move the
whole round into an isolated `git worktree` at your own base commit, verify
there, then stage only your own hunk with `git apply --cached` instead of
`git add <file>` when the file also holds the other agent's edits. Verify
afterwards that the other agent's files are still modified and still untracked.
Then check the knockout-style question: does the WORKING file still contain
your change, or only the index? `git apply --cached` stages without touching
the working tree, so a later commit by the other agent can silently revert you.

**Rule going forward:** never have two implementer agents live in one checkout.
Reviewers are fine in parallel (read-only). If two implementers must overlap,
give each its own `git worktree` in the dispatch brief, not as a recovery.
Before dispatching, check whether the previous agent has actually reported —
"it committed" is not the same as "it is done", because a fix round resumes it.

Related: [[2026-09-26-live-region-same-tick]]
