---
name: fable-signoff-pass
description: "2026-07-08 Fable pass done — all 6 phases ruled, goal-ladder table out of band under full stack, economy-tightening brief issued; scar: tune against the graduating stack, not a single flag"
metadata: 
  node_type: memory
  type: project
  originSessionId: d2f754bd-8615-4d94-82b0-739f8ebff536
---

**2026-07-08: the real Fable sign-off pass ran in-session** (Fable 5 available at last) —
authoritative rulings in `docs/review-packets/FABLE-RULINGS-2026-07-08.md`, superseding the Opus
stand-in verdicts ([[reviewer-workflow-opus-split]]).

Outcomes:
- Levers, LOOP_V2 P1, 2a, 2b, 2c: **APPROVED** — every open CCR question answered (best-tag max,
  supersession, blocked-slot counting, mandatory supplier pick, 5 signature rule kinds, additive
  contract fields, no version bump). 2b's Lane B picker dependency was already closed (draft.tsx).
- Goal ladder (P3): CCR approved, **target table REQUEST CHANGES** — see scar below.
- Balance ruled: sell-back **v2-gated floor of 1** (19/41 items sell for 0 — broader than the
  "tier-1" framing); loose economy ([[device-feel-gate-round2]]) gets one coherent v2-gated
  tightening pass (rent steepening/coin sink + goal-table retune + sell floor + beginner-opening
  ease, then re-set [[balance-target-bands]]). **Economy pass IMPLEMENTED + verified later the
  same day** (v2 rent 1.75@c4 → 27d ceiling; sell floor 1; goal table `[18..90]` in-band on a
  400-run fuzz 0.67–0.82/day; run-length band min re-set 24→20; assert green; OFF path
  byte-identical). Also fixed the [[buyout-reroll-duplicate-bug]] found by the pass. **Tried &
  reverted (don't re-try):** day-2 shop discount (build swing collapsed to 1.13 — guardrail
  caught it), rent-late from cycle 3 (21d runs, out of band), starting coins 10 (broke the
  day-one two-buys path). **Design briefs WRITTEN + pushed (`9147672`):**
  `docs/lane-a/coin-sink-shelf-expansion-brief.md` (A-M6a, Codex — 3×4→4×4 row, zero schema
  edits), `docs/lane-a/opening-warmup-brief.md` (A-M6b, Codex, AFTER M6a — guaranteed ≥2 cheap
  offers days 1–2, never a price discount), `docs/lane-b/summary-v2-retention-brief.md` (B-M4,
  Opus 4.8, parallel-safe). Each ends in a review packet Fable re-runs; implementers never
  self-sign-off. Final acceptance = the human device feel-gate.

**Scar (promote if seen again): a table tuned against one flag is not tuned against the stack.**
The goal-ladder targets were verified in-band (65–85% late hit) against LOOP_V2-only yield; under
all five flags my 120-run fuzz (seed `fable-signoff-0708`) measured **0.892/0.926** days-9–12 —
out of band on the easy side. Multipliers compound; targets don't.
**Why:** each phase's fuzz-tuning implicitly froze the other flags OFF.
**How to apply:** any balance table/band verification must run with the *exact flag set that will
graduate together*; a brief that tunes numbers must name that flag set in its verification method.

Also: natural-pickup fuzz showed consignment-sign 2.076× dominance — that is the small-n trap the
[[loop-v2-phase2c-signature-items]] gate doc warns about; the equal-n=3000 probe (1.13×) stays
authoritative. Don't re-open the closed gate from natural-pickup noise.
