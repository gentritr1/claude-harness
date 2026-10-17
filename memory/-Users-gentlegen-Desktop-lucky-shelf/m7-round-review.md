---
name: m7-round-review
description: "2026-07-08 round 3 reviewed — A-M7 unlock ladder APPROVED (daily-canonical-pool graduation gate ruled), B-M5 streak APPROVED, B-M6 spectacle logic APPROVED (apex ruled rare-and-special); threshold scar promoted to global CLAUDE.md"
metadata: 
  node_type: memory
  type: project
  originSessionId: d2f754bd-8615-4d94-82b0-739f8ebff536
---

Round-3 (pre-test content) reviewed by Fable, all three from ONE shared dirty checkout —
untangled into per-lane commits (verdicts in `docs/review-packets/*-fable-review.md`):

- **A-M7 unlock ladder APPROVED** (Codex): 16 always / 15 runsPlayed / 5 discovery-combo;
  replay-integrity via `GameState.unlockedItemIds?` snapshot; ten tests incl.
  replay-after-catalog-mutation + locked-never-offered fuzz. **HARD GRADUATION GATE ruled:
  daily-seeded runs must pin a canonical pool before UNLOCK_LADDER ships ON** — personal unlocks
  otherwise break "same shelf worldwide" (and the P3 ghost/leaderboard moat). **Gate CLOSED
  (`ef1efae`)**: dailies snapshot `allUnlockableItemIds()` explicitly — the engine defaults an
  ABSENT option to the starter set (caught when the first regression-test cut failed), so the
  canonical pool must be passed, never omitted. Two-catalogs-same-daily test in store.test.ts.

**Jury verdict adopted (PRODUCT.md, `8d6a742`):** depth-not-breadth; gate order changes, not the
codebase; quiet streak stays with a no-pressure-mechanics rule. Round-4 briefs delegated:
B-M7 accessibility floor + B-M8 receipt cascade (headless cores now, device shots batched
later); Velvet Snap waits for the human's device window.
- **B-M5 Part 1 daily streak APPROVED** (Opus): additive `streak?` on the daily schema; the
  cold-relaunch streak-reset was caught BY the recorded catalog-wipe scar (3rd firing) —
  load-guard + rollover carry + regression test. Parts 2–3 (silhouettes, next-unlock teaser)
  now UNBLOCKED by A-M7. Screenshots = human gate (seed recipe in packet).
- **B-M6 cascade spectacle logic APPROVED** (Opus): pure `cascadeTier` (2.8×/4.2×/40/50 —
  retuned from my brief's 1.5×/2.5×/12 which caught 84% of days, scar's 4th firing).
  **Ruling on the escalated dual-target conflict: rare-and-special stands** (~apex once per 2
  runs; %-of-runs phrasing retired). Feel = human recording gate via /cascade-harness one-tap
  APEX/BIG demos.

**Scar PROMOTED to global `~/.claude/CLAUDE.md` §6 red flags** (4th firing): no numeric
threshold enters a brief without a measurement script run against live data; the brief names
the script.

Workflow precedent: implementers sharing one checkout correctly refused to commit (would sweep
the other lane's in-flight work) and refused native builds on an unstable tree — reviewer
(Fable) owns the untangling and the commits.
