---
name: perf-gates-need-jitter-and-resolution-tolerance
description: A p95-vs-16.67ms gate fails every healthy 60fps thread; budget comparisons need a vsync-jitter and measurement-resolution allowance
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:32:51.658Z
---

Comparing a frame-time **p95 against exactly 16.667 ms** flags threads that are perfectly healthy.
A vsync-locked 60 fps thread reports `p50 = 16.67` and a p95 slightly *above* it, because frame
deltas scatter symmetrically around the period.

Two false failures in the first real run of the merge-kit spike harness:
- ramp @40 bodies: js p95 16.97, **zero** dropped frames → reported as "gate failed at 40 bodies",
  when the true cliff was ~100. That would have aimed the engine decision at the wrong body count.
- UI thread: every frame in histogram bucket [16.5, 17.0) → midpoint 16.75, i.e. "0.08 ms over
  budget" — a shortfall **smaller than the 0.5 ms measurement resolution**.

**How to apply.** Judge a perf gate with: `p95 ≤ budget + jitterAllowance + measurementResolution`
**and** `droppedFrames / samples ≤ 1%`. In merge-kit: `withinBudget()` in
`packages/merge-shell/src/metrics/frameStats.ts`, allowance 1.5 ms (9% of budget — far below any
real failure, which were 4-6× over). Carry a `resolutionMs` field on any stat block so quantised
sources declare their own precision; never report a difference smaller than it as a finding.

Corollary: always report the raw percentiles alongside the verdict so a reviewer can apply a
stricter threshold, and regression-test the gate with the **real observed numbers**, not synthetic
ones.

Related: [[v02-spike-outcome-matter-js-fails-120]]
