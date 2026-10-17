---
name: text-that-leaves-the-app
description: Share/export text built from a frozen id list plus a live-recomputed list can assert a falsehood; pin the unresolvable-reference case
metadata:
  type: project
---

Tondo's share text (Task 10) is built from `match.championIds`, **frozen** when
the pie completes, and `match.standings`, **recomputed live** and deliberately
dropping seats that left. The winner tapping "Leave table" — one tap, by the
person most likely to take it — makes the champion id unresolvable, and the
headline degrades to `🍕 TONDO — Nobody took the pie` while the screen beside
it still reads `Carmela takes the pie`. A shared pie degrades worse: it hands
one player a win they shared.

The bug is the conflation of **"nobody won"** with **"I cannot name the
winner."** `Nobody took the pie` is correct copy for a genuinely unwon pie
(`leaders()` returns `[]` at 0 points and 0 round wins), which is exactly why
the false case is invisible in review.

**Pattern → detection rule → brief update.** Any text assembled from a frozen
id list joined against a live-recomputed list must assert that every id
resolves *before* phrasing anything negative. Any brief producing text that
LEAVES the app — a share string, an export, a paste — must pin the
unresolvable-reference case as a test, because the artifact cannot be
corrected after it is sent and the happy-path suite stays green on the lie.

Two more from the same review, worth keeping:
- The origin line (`location.origin + location.pathname.replace(...)`) is the
  highest-consequence expression in the feature — a regression to
  `location.href` would paste a room code that is dead in 60 seconds — and no
  test touched it. Guard the shape of an outgoing URL, not just its text.
- A denylist test (`reward`, `unlock`, `bonus`, …) is a tripwire for
  regressions someone already imagined, not a guarantee that the copy "asks
  the reader for nothing". Say so in the brief instead of implying coverage.

Related: [[2026-09-26-live-region-same-tick]]
