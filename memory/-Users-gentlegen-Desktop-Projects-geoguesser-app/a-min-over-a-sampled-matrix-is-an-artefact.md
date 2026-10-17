---
name: a-min-over-a-sampled-matrix-is-an-artefact
description: "A worst-case taken over sampled widths/scales is a sampling artefact when the threshold slides with the sampled variable — quote sensitivity, not a minimum"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-01T00:41:27.789Z
---

B1-4 quoted "the tightest slack is 9.7 dp" from a sweep over 4 widths. The same question answered
**9.3** at a finer step, **1.5** over 6 widths, and **0.000** over all 161 integer widths 320-480.
Every answer was correct for its sample and useless as a bound.

The reason is structural: `hudLayout`'s threshold is `width − constants`, so it slides **1:1 with
width** while the glyph advance does not. A minimum of (threshold − fixed) over a continuous range
therefore tends to zero by construction. No amount of care in computing the minimum fixes it.

**Why:** three agents in a row — implementer, reviewer, re-reviewer — each checked whether the number
was *derived correctly* and none asked whether the set it was derived over was *complete*. The
controller (me) then propagated the artefact into a findings document and nearly into a ruling.

**How to apply:**
- Before quoting a worst case over a sampled matrix, ask whether the quantity slides with the sampled
  variable. If it does, the minimum is an artefact — state the **sensitivity** instead ("a measurement
  N dp wider costs a band of widths exactly N wide"), which is sampling-independent.
- Prefer removing the delta to bounding it. B1-4 ended by measuring the same glyph run the base build
  measures, so the delta is 0 by construction and needs no matrix at all.
- A sweep's step size is part of its answer: a 0.5 dp sweep can only ever return a multiple of 0.5.
  Binary-search a threshold, or state the resolution next to the number.
- **A number quoted from an earlier report must be re-read in that report before it drives a decision.**
  I repeated "the box is ~10 dp wider than the glyph" as a measurement; it was a *budget* the
  implementer had computed, and the box-vs-glyph difference had never been measured on any device.

Related: [[gates-recompute-never-trust-report-flags]], [[device-and-web-qa-harness-traps]].

Also (C2-1, 2026-10-03): a single-sample SE on a MEDIAN can badly under-report — the country-rung median distance was
bimodal across seeds (~420.3 vs 423.15 km), so one run's SE looked tight while a replicate moved a committed band
(5250 -> 5260). For order statistics, pool independent batches (SE = SD/sqrt(batches)) and decide a value that sits
on a rounding edge by the pooled estimate across replicate runs, never by whichever seed ran first.
CORRECTION (same day, reviewer): the mean of batch MEDIANS is itself wrong when the distribution has a gap at the
median — it drifts with the batch count. Point estimate = the whole-sample median; batches only give the uncertainty.
And check the PRNG: per-stream seeds of one 2^32 generator overlapped (17 of 77 stream pairs) — independence assumed
by every SE must be designed, not hoped for.
