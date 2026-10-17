---
name: deadline-radar-project
description: "deadline-radar (Oct 2026) — RN/Expo upgrade + store-deadline tool; repo, bench, positioning rule (complement Expo tools, never compete), v0.2 queued"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bb56d09-6e53-4a9f-87a4-708273fd5c90
  modified: 2026-10-17T19:05:12.393Z
---

**Repo:** `~/Desktop/Projects/deadline-radar`, local only; nothing pushed without the owner's yes. Its `LEDGER.md` is the recovery map.

**Bench:**
- `bench/`: 3 test apps, an independent oracle, `PREREG.md` (amendments 1–2), frozen arm prompts in `ARMS.md`, and the run log `RUNS.md`.
- Phase 5: 8 A/B runs (Claude Code alone vs with radar, Sonnet 5.5, ABBA order).
- The standalone copy for arm B is at `~/tools/deadline-radar`.

**Owner's positioning rule (2026-10-17):** radar complements expo-doctor, expo install, react-native doctor and Upgrade Helper. Never compete with them or copy their depth.
- **Why:** they're earlier in the market and have far more work behind them. Radar earns its place by helping them, not dividing the market.
- **How to apply:** new radar code is sequencing and gap-filling only. It calls those tools, never re-implements them, and offers upstream fixes to Expo instead of out-competing them.

**Gaps radar owns:**
- missing required peers;
- non-Expo native libraries (version choice from `tested_rn`, read from each library version's own devDependencies);
- dated store rules across vendors;
- 16 KB failures traced to an npm package;
- `--to safest` SDK choice;
- an evidence receipt.

**Key evidence:**
- Mechanical `expo install --fix` failed the build 6 of 6: reanimated 4 without `react-native-worklets`, while `expo install --check` passed.
- expo-doctor's store check is hard-coded to Aug 2024 (API 34, SDK 50).

**Queued:** v0.2 orchestrator, after the 8 runs, with a smaller re-test. Then the Fable whole-project review and a results artifact.

Related: [[play-deadline-kit]] (vendored into radar), [[proof-runner-project]] (the receipt).
