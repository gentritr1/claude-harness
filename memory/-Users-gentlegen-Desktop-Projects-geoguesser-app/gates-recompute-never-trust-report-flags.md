---
name: gates-recompute-never-trust-report-flags
description: "C1a's coverage `check` passed a 240-probe report against a table needing 18,432 because it trusted the report's own `reconciled` flags (2026-09-16)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-16T23:28:53.779Z
---

The C1a coverage gate (`scripts/discover-coverage.mjs check`) read `run.reconciled` from the verify
report instead of recomputing seeds × n × runs against the table. Reproduced offline: runs rewritten to
80 probes each against the 768-seed table gave "true-360 share 0.988 (n=240)", PASS, exit 0. Its
"out-of-sample" label likewise used the summary date, not probe times, so re-summarizing old probes (or
re-running the seed that selected the table) could pass as the owed out-of-sample measurement.

**Why:** an acceptance gate that trusts fields written by the tool it checks verifies nothing. The
committed numbers were right; the gate could not tell.

**How to apply:** pattern → the gate reads self-reported flags or dates → detection rule: mutate the
report's counts or dates in a scratch copy and rerun the gate → future briefs: every gate recomputes
its identities from primary data (table, journal, probe timestamps) and fails safe when they are
unknown. Related: [[mapillary-single-shared-token]], [[shared-quota-lock-outside-checkout]].
