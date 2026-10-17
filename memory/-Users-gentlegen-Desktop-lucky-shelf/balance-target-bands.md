---
name: balance-target-bands
description: "The §6 \"soft spot\" bands are now set (guardrail philosophy); how they're enforced and why build-swing can't live in the unit suite."
metadata: 
  node_type: memory
  type: project
  originSessionId: 523339a0-35c7-4643-bd36-369320df5b1d
---

2026-07-08 (Opus session): filled the balance-harness §6 target bands (STATUS #3 "next code task").
Human chose **guardrail philosophy** (bracket current reality → `pnpm balance:assert` stays green, catches
future DRIFT; does NOT itself tighten the economy). In `src/sim/balanceHarness.ts`:

- **Active (asserted):** `ceilingMedianRunLengthDays {24,36}` (ceilings median 27/30d), `buildSwingTotalCoinsRatio {1.3,2.0}` (current 1.33/1.53/1.66×).
- **Deferred to Fable (null):** surplus ratio + consecutive-days (a guardrail there would *bless* the known loose 5–7× economy), and `nearDeathRunRate` (tension = taste).
- **Aspirational, NON-blocking:** `ASPIRATIONAL_TARGET_BANDS.floorFirstRentSurvivalRate {0.4,0.7}` — human wanted a softer beginner floor, but reality is ~16–21%, so it's reported (not asserted) and needs Fable to ease the opening economy. Kept out of the asserted set so `pnpm test` stays green.

**SCAR → detection rule → enforcement placement:** build swing is only stable at the calibrated
80-run/seed `balance` report. At 12 runs floor swing = 2.21× (out of [1.3,2.0]); greedy = 1.23×. So a
reduced-run unit test would false-fail/flake. Rule: **a band calibrated on a full report is enforced via
the script gate (`pnpm balance:assert`, wired into `m1`), never a reduced-run unit test.** The unit test
(`balanceHarness.test.ts`) asserts run-length (stable at any count) on a small real report + exercises the
build-swing band *logic* against controlled values. Run-length medians are integer-stable (27/30) at all
counts.

**BUG fixed (report-only, no assertion/engine impact):** `nearDeath()` was degenerate — it counted the
opening broke-before-rent-1 state, so it read a flat **100% for every config/policy** (measured nothing).
Fixed to ignore the opening tier (`sample.rentAmount > openingRent`). Now discriminates: floor 10–25%,
ceilings ~92–100%. The band stays null, so this only makes the printed report honest.

Verified: typecheck clean; full suite **117 passed** (the old `it.skip` TODO(fable) test is now active,
+~2.5s); `pnpm balance:assert` exit 0; git diff touches only package.json, scripts/balance.ts,
balanceHarness.ts + .test.ts — no engine/economy/items/rng, so determinism pin `8d48e1c5a6ad14c9` + M0
goldens stay byte-identical. See [[goal-horizon-vs-resource-cadence]], [[device-feel-gate-round2]].
