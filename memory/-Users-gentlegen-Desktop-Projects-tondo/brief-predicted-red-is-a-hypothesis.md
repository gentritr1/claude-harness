---
name: brief-predicted-red-is-a-hypothesis
description: "A plan's predicted pre-fix failure message was wrong (an older, tighter cap tripped first); TEST-001 mutants, not the red run, proved the test guards the hole"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3fb08f38-07c3-4529-b2e2-21cde8419a74
  modified: 2026-10-10T00:01:11.852Z
---

**What happened (2026-10-10, crew-retention Task 2):** my plan predicted the pre-fix run of the wrong-code test would fail with "11th after reconnect: No table has that code." It actually failed at "attempt 6: Too many wrong table codes". The OLD per-socket cap was 5, so the first socket never reached the reconnect. So the red run went red for a reason other than the hole it was meant to show.

**What proved the test anyway:** the reviewer's mutants, agent-playbooks TEST-001. The decisive one kept burst 10 but keyed the budget per socket again; it failed exactly at "11th after reconnect". The same run showed a connect-burst +1 mutant SURVIVING, because of a `Math.ceil(elapsed)` slack that is always ≥ 1.

**Why:** a red run only proves the test can fail. It does not show the test fails at the guarded line, and a predicted failure message in a brief is a number like any other (TEST-006).

**How to apply:**
- Never write the expected RED output into a brief as fact. Write the mutant that must be caught instead: "a budget a reconnect refills must fail assertion X".
- Every brief that adds a guard test asks the implementer for a TEST-001 mutant table with `cmp` restore.
- Any slack term in an assertion is checked against a ±1 mutant.

Related: [[shoot-gate-load-flake]] (jitter allowance done right), [[delegate-overrode-my-ruling]].
