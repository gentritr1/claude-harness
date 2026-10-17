---
name: stacked-pr-merging
description: Merging stacked PRs — never `gh pr merge --delete-branch` on a PR that another open PR uses as its base
metadata:
  type: feedback
---

On 2026-10-04, `gh pr merge 18 --delete-branch` deleted the branch that stacked PR #19 targeted; GitHub **closed** #19 instead of retargeting it. Recovered by re-pushing the base branch at its old commit, `gh pr reopen 19`, `gh pr edit 19 --base main`, then deleting the branch.

**Why:** GitHub only auto-retargets in some setups; a deleted base closes dependent PRs, and a closed PR with a deleted base cannot be reopened.

**How to apply:** for a stack A←B←C, merge A *without* `--delete-branch`, `gh pr edit B --base main`, merge B, retarget C, and delete branches only after nothing targets them. Related: [[competitive-and-security-findings-2026-10]].
