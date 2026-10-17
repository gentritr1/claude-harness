---
name: hint-attempt-design
description: "Hint-costs-one-attempt round (2026-07-19) — legacy grace, clue-leak findings, open gaps"
metadata: 
  node_type: memory
  type: project
  originSessionId: 65a98170-6072-4511-a581-c285d9d4d9cc
  modified: 2026-07-19T17:37:44.570Z
---

Reviewed 2026-07-19 (Codex round, uncommitted at review time): hint reveals only part-of-speech + syllable *count* + clue, costs one attempt (`state.hintRow` ∈ {3,4}), spent row rendered on board, share grid gets a 💡 row, attemptCount flows into distribution/dailyResults.

Non-obvious decisions verified as deliberate:
- **Legacy grace:** old in-progress saves with `usedHint:true` but no `hintRow` hydrate as a FREE hint (no retroactive attempt charge — charging could instantly flip a save to lost). Don't "fix" this.
- `hydrateGame` forces `besa=false` when `usedHint` and drops hintRow after a win-row; profile layer gates `besaWins` on `besa && !usedHint` (tested).
- Cross-tab `gameProgress` re-weighted to attempts×100 — fixes old comparator bug where a full current row + flags (12) outranked a submitted guess (10).

**Clue-leak audit (script: check clue for word or ≥4-char stem):** FJALË (idx 26, IN daily pool) clue contains "fjali"; ROSAK (idx 112, practice-only) clue starts "Rosa" — both hand over 4/5 letters. The daily-v1 SHA pin hashes ONLY `word` strings (tests/words.test.js `publishedWords.join("\n")`), so clue edits are safe without an epoch. Needs native-authored replacement clues.

Open verification gaps: native Albanian pass on the ~15 new hint strings (scar: [[review-scars]]); cross-tab hint announce (code-reviewed only); iOS Safari untested (in-app Chromium only).
