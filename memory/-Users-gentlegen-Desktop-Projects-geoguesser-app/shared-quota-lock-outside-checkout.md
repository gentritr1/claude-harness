---
name: shared-quota-lock-outside-checkout
description: "A process lock guarding the shared Mapillary quota was per checkout, so parallel agent worktrees could double the request rate (C1a re-review, 2026-09-17)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-16T23:28:58.850Z
---

C1a's fix put a `wx` network lock in `<stateDir>/network.lock`, and the state dir resolves inside the
checkout. The re-reviewer ran two scratch checkouts: while checkout A held its lock, a pass in checkout
B got straight past it. This repo runs implementers in parallel worktrees, so that is the normal case,
not an edge case. The brief's own wording ("a lock in the state directory") caused it.

**Why:** the quota being protected (one Mapillary token shared with live players) is machine-wide and
beyond; a lock scoped to one checkout protects nothing when agents work side by side.

**How to apply:** a lock or budget that guards an external shared resource lives outside any checkout
(`COVERAGE_LOCK_DIR` or `~/.cache/geoguesser-coverage`), names its holder, and states what it still
cannot see (other users, machines, CI). Test it with two different roots sharing one lock dir. Briefs
must not say "in the state directory" for such locks. Related: [[mapillary-single-shared-token]],
[[gates-recompute-never-trust-report-flags]].
