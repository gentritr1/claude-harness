---
name: game-design-truths-measured
description: "Measured truths about the Arrows game design that contradict PRODUCT.md: no order can brick a board, the difficulty curve is flat forever, and 4 shapes are 71% of content"
metadata: 
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-09-09T15:02:55.120Z
---

Measured 2026-09-09 by running the real generator/board code under `tsx` (scripts in the
session scratchpad; re-derivable in ~20 lines against `src/core/levelGenerator.ts` and
`src/core/boardLogic.ts`).

**1. No ordering can ever brick a board — the game is not a logic puzzle.**
50 random-greedy playthroughs across levels 1, 3, 6, 12, 24, 36, 60, 117, 162, 168 (incl. the
202-arrow SuperHard Cat): every run cleared in exactly `arrowCount` taps, zero dead ends.
Provable from the rules, not just empirical: removing an arrow only empties cells, so `canExit`
is monotone — a clear lane stays clear. PRODUCT.md's "The puzzle is finding the order" is FALSE
as implemented. The actual game is a **visual-search / attention task** repeated 60–209 times.
The only failure mode is a misread, never a bad plan.

**2. The difficulty curve is flat forever.**
Level 1 = 60 arrows, 100 = 85, 200 = 93, 500 = 119, 1000 = 97. Mean arrows levels 1–30 = 96.2 vs
levels 171–200 = 100.4. `Difficulties.config()` switches on the tier enum only and never reads
the level index, so level 200's Normal config is byte-identical to level 2's.

**3. Content is thin and ordered backwards.** Across levels 1–200:
Circle/Diamond/Square/Rectangle = **71%** of all levels; **33%** are a plain filled rectangle with
no picture at all (Square/Rectangle are `fillsGrid`); levels 1 AND 2 are both Circle; 29/199 levels
repeat the previous level's shape. First appearances: Crown@60 → **57-level drought** → Hexagon@117,
Butterfly@120, Flower@126, X@159, Heart@162, Cat@168. After 168 nothing new exists ever again
(26 shapes total). The most shareable silhouettes are buried behind 160+ levels.

**Why:** these three facts decide what "next level" means. If order never matters, depth cannot be
added by tuning the generator's existing knobs — only by more arrows on a bigger grid (which is
what the flat curve already proves), or by a NEW mechanic that makes plans fail.

**How to apply:** never repeat PRODUCT.md's "finding the order" framing in copy or a brief without
flagging it. Any difficulty/content change re-generates boards for existing players mid-progress
(levels are pure functions of the index and DESIGN.md makes that a hard contract) — it needs a
level-schema version + migration. See [[arrows-next-level-plan]] and
[[shipping-defects-found-2026-09-09]].
