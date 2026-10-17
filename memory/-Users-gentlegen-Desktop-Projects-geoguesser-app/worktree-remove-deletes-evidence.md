---
name: worktree-remove-deletes-evidence
description: "git worktree remove after a merge deleted every unit's gitignored docs/plan/evidence dir (C1b-1..C3-3); copy evidence out first"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-04T01:27:24.432Z
---

On feat/next-level the controller-made scratchpad worktrees held each unit's gitignored `docs/plan/evidence/<unit>/`. Running `git worktree remove --force` after each merge silently deleted all of it, from C1b-1 to C3-3. Noticed 2026-10-04. Only the committed reports kept the numbers.

**Why:** evidence is gitignored by rule R11, so the merge never carries it over, and `remove --force` doesn't warn about ignored files.

**How to apply:** before removing a unit's worktree, run `cp -R <wt>/docs/plan/evidence/<unit>* <main>/docs/plan/evidence/`, then check with `ls`. Related: [[agent-worktree-isolation-cuts-from-main]], [[gate-commits-on-the-exit-code]].
