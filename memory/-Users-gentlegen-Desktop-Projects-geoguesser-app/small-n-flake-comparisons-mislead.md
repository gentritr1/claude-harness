---
name: small-n-flake-comparisons-mislead
description: 0/16 vs 4/14 looked like a regression; at a ~4% base rate it was noise plus a test-precision bug present at base
metadata:
  type: feedback
---
On 2026-10-08 I compared runs of the art-4b "warm cap" test, interleaved at the same load:
- art-4c: 4/14 failed.
- base: 0/16 failed.

I declared a regression. The implementer then ran 100 runs per arm on a focused harness: base 4/100, art-4c 1/100. The real cause was the test's regex matching a legitimate retry warmer that mounted in the same act(), and that cause exists at base.

**Why:** at a base rate of ~4%, 0/16 has about a 52% chance of happening. Small samples cannot separate a 4% flake from a regression.

**How to apply:**
- Before calling a flake a regression, size the run count to the base rate: at least 50-100 runs per arm, or a focused repeat harness.
- Find the mechanism, using a per-instance assertion and a print at the failing assertion.
- State the confidence interval, not the raw counts.
- Related: [[timer-floor-assertions-need-slack]] and [[gate-commits-on-the-exit-code]].
