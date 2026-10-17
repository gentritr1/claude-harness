---
name: m6-round-review
description: 2026-07-08 late — M6a/M6b/B-M4 delegate round reviewed; catalog-wipe P0 found in review; two new scars (load-guard persisted merges; sanity-check brief constants against live curves)
metadata: 
  node_type: memory
  type: project
  originSessionId: d2f754bd-8615-4d94-82b0-739f8ebff536
---

**Round 3 delegated (2026-07-08, pre-test content push, `29909fe`):** A-M7 unlock ladder
(Codex — predicates over existing catalog stats, zero wipe risk; replay integrity via additive
`GameState.unlockedItemIds?` snapshot), B-M5 retention surfaces (Opus — daily streak needs an
additive persisted field, NOT derivable from dailyStore; silhouettes/teaser after A-M7), B-M6
cascade spectacle (Opus, parallel — `cascadeTier` headless logic; apex ~1 per 2–3 runs;
recording-gated). Human's state-of-game review + moat promotion committed same commit.

Round-2 delegation reviewed by Fable with independent re-runs (verdicts in
`docs/review-packets/*-fable-review.md`; queue + STATUS updated):

- **A-M6a shelf expansion APPROVED** (sink: day-12 surplus 7.3×→3.2× on my seed; uptake ~0.9).
  Graduation gates: goal-table retune vs FINAL flag set (16 slots → days-9–12 hit ~0.85, band
  top — third firing of the [[fable-signoff-pass]] tune-vs-stack scar), equal-n signature
  re-probe with expansion ON, Lane B 4-row rendering.
- **B-M4 summary v2 APPROVED** (bests/near-miss/build recap; device-polished; `closestRentMargin`
  + `longestRun` contract adds approved, no bumps).
- **A-M6b warm opening landed, floor acceptance NOT met** — offer composition lifts the beginner
  floor only ~1.25× (loopV2 10→12.5%, allDepth 16.3→20%); gap escalated. Ruled day-aware ceiling
  (4 day 1 / 10 day 2) + cheapest-first replacement (most-expensive-first dented ceilings −6–7%).
  **Human chose option 1: free day-2 starter delivery → A-M6c implemented + APPROVED, and the
  beginner-floor mechanism chase is CLOSED** (verdict in `A-M6c-fable-review.md`): combined floor
  ~20–27.5% by seed (~2× baseline), reliably below 0.30 — the bottleneck is the floor-bot proxy
  (never rearranges/synergizes), not the economy. The [40,70]% aspiration re-anchors to the P2
  real-playtest milestone; **welcome-week rent = the one unpulled lever**, only if real humans
  bounce off rent 1. Packet's combo −5.49% A/B miss did NOT reproduce on my seed (noise).

**Scar 1 — persisted-store merges must load-guard (P0 found in review).** `recordRunEnd` merged
the finished run into the in-memory catalog and saved it; nothing at boot loaded the catalog
(only the album screen did), so every run finished without visiting the album **overwrote the
persisted catalog with just that run** — silent data loss since the M4 merge point.
**Why missed:** the implementer's migration test checked schema parsing, not load-before-merge
ordering; every dev/test flow happened to load the catalog first.
**How to apply:** any `record*`/merge-and-save on a lazily-loaded store needs (a) a load-guard in
the method itself, not just at call sites, and (b) a regression test that records WITHOUT loading
first (`src/state/catalogStore.test.ts` is the template). Check this on every new persisted store.

**Scar 2 — brief constants must be sanity-checked against the live curves they bind.** My M6b
brief demanded "≥2 offers costing ≤4 on days 1–2" while the day-2 price floor is 8 — an
unsatisfiable spec the implementer (correctly) degraded on instead of fabricating discounts.
**How to apply:** when a brief pins a threshold, compute the actual reachable range from the live
table/curve in the brief itself (one script line) — never quote a constant from memory of day-1
values.
