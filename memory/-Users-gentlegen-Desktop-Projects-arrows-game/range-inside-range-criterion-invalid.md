---
name: range-inside-range-criterion-invalid
description: "Every ON run inside the OFF run range" is not a valid perf gate at small n — identical builds fail it most of the time
metadata:
  type: feedback
---

A perf acceptance written as "every run of arm B lies inside arm A's per-run range" fails by chance: with 8 vs 8 runs of the SAME build, it failed on 4 of 5 metrics (W4-07 fix round, 2026-09-25; the chance one sample's range sits inside another's is ~23% per metric at n=8).

**Why:** I wrote that criterion into the W4-07 fix-round brief; the implementer showed it rejects identical builds, and I had to accept on statistics instead.

**How to apply:** gate perf with (a) a same-APK null run giving the minimum detectable effect, then (b) a difference in medians beyond that spread that replicates with non-overlapping ranges across alternating runs, or a permutation test. Never "range inside range". Related: [[detector-needs-positive-control]].
