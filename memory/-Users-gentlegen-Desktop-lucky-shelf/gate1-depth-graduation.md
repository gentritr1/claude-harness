---
name: gate1-depth-graduation
description: Gate 1 (RELEASE-PLAN) — goal-table retune vs TRUE graduating config done + validated; flip blocked on one-way env flag semantics; jingle = external asset
metadata: 
  node_type: memory
  type: project
  originSessionId: 3bb5b22f-cf63-495e-be5e-4f3f9b194708
---

Gate 1 of docs/RELEASE-PLAN.md (five-gate roadmap adopted 2026-07-10 from the impeccable
critique, 30/40). Session 2026-07-10/11.

**Done + verified:**
- **Threshold scar fired a 5TH time**: goal table tuned 07-08 vs `allDepth` (5 flags) measured
  0.95–0.99 hit under the real 8-flag graduating set (band 0.65–0.85) — `allDepth` lacks
  shelf-expansion (the d8→d9 yield jump 139→186 is the expansion tier), unlock ladder, day-2
  starter. **Detection rule now permanent:** `graduating` config exists in `BALANCE_FLAG_CONFIGS`
  (src/sim/balanceHarness.ts) — tune ONLY against it; `scripts/goal-tune.ts` is the named
  measurement script (pooled greedy+combo p25 day totals → candidate table + predicted rates).
- New 12-entry GOAL_LADDER_TARGETS [18,44,68,92,106,112,114,116,148,152,166,172] (smoothed
  monotone, extended 10→12 for the expansion tier). VERIFIED out-of-sample (fresh seed
  graduation-0710-v2, 400 runs): all days 0.71–0.82 both strategies, survival median 30d
  unchanged; reward feedback loop real (~20% fewer free rerolls) but stayed in band.
- B-M12 summary copy fix (Opus): "Closest rent payment: N coins to spare" — resolves the
  RENT MISSED contradiction. LOW RISK approved; 291/291 + tsc re-run by Fable.

**Flip DONE on branch `graduation-flip` (`49ad41c`), unmerged — merge gate = Gate 2 device pass.**
The scars this landed (transferable):
- One-way env flags (`CONST || env==='1'`) can't ship a flip: two-way ('0' forces OFF) landed
  on main first (`df1423b`), harness pins absent keys '0' so `baseline` still measures OFF.
- **Ambient flag reads in scoring/offer code = save corruption at graduation.** Synergy +
  signature scoring and the signature offer filter read env/const, not the run's `state.loopV2`
  snapshot — a v1 save would have changed scoring + shop contents at app update. Detection:
  the M0 golden `m0-wine-dine-combo` failed on the flip branch. Rule: every mechanic surface
  that touches an EXISTING state must gate on the run snapshot, never the ambient flag.
- Tests may not imply flags from compiled defaults: `testkit.withFlagWorld` pins all 9 keys;
  every flag-sensitive suite names its world. Determinism has TWO pins now: frozen v1
  `8d48e1c5a6ad14c9` (asserted under explicit all-OFF) + graduating `4d5b9f57ba63b916`.
- Branch proof: 292/292, no-env fuzz = exact graduating set, balance:assert numerically
  identical pre/post flip. Accepted quirk: day-1 pre-action v1 save sees supplier choice
  post-update (steering's createRun gate ambient by design).

**Jingle (Gate 1.5): external asset dependency** — session audio tools are speech-only (SFX
models pipeline-restricted). Spec + swap point (`DISCOVERY_JINGLE_SOURCE`, audio.ts) in
RELEASE-PLAN Gate 1.5.

Related: [[b-m11-discovery-moments]] [[loop-v2-phase3-goal-ladder]] [[balance-target-bands]]
