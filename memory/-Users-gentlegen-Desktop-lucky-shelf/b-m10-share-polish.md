---
name: b-m10-share-polish
description: B-M10 friendly seed labels + receipt card done; ScoringTrace-total + node-version gotchas
metadata: 
  node_type: memory
  type: project
  originSessionId: b59c3a99-3fc0-4bbd-b164-b8d8d52fb7ad
---

B-M10 (share polish) implemented + packet delivered (`docs/review-packets/B-M10-share-polish-review.md`),
awaiting Fable. Suite 251/251, tsc + boundary/token greps clean. NOT committed (Lane A held the tree).

- **Seed codec** `src/state/seedLabel.ts`: pure FNV-1a 32-bit → `WORD-NNN`, 64-word cozy pool, no
  gambling words. Stable-forever (spoken between players) so a hand-rolled fixed hash, not an engine
  one; frozen test pins (`daily-2026-07-09 → ACORN-770`). Collisions OK — nickname, not a key.
- **Receipt card**: store view-model `receiptCardView(gameState)` (keeps screen off `@/items`);
  imports `../juice/receipt` submodule (pure, no Skia, no cycle), NOT the `@/juice` barrel. Uses
  `lastScoringTrace` = closing day, labeled honestly; no trace persistence (best-day = Fable follow-up).
- Added `fonts.mono` + `typeScale.receipt` to tokens.ts so the dot-leader body aligns.

**Gotcha 1 (scar):** `ScoringTrace` has **no top-level `dayTotal`** — the total is the trace's
terminal `dayTotal` *event* (`{kind:'dayTotal', coins}`), surfaced by the receipt model's `total`
line. Assumed `trace.dayTotal`, got `undefined`; the receipt snapshot test caught it on first run.
Read the day total from the receipt's total line (or the last event), never `trace.dayTotal`. See
[[b-m8-receipt-cascade]].

**Gotcha 2 (env):** shell default node here is **v14** — too old for vite 8 / vitest 4. Run tests
with `export PATH="$HOME/.nvm/versions/node/v20.19.4/bin:$PATH"` (v20.18 also fails the ERR_REQUIRE_ESM;
need ≥20.19). tsc + vitest both fine on 20.19.4.
