# A cross-check derived from the same fields is not a cross-check

**2026-08-09, Gate 3.** `test/ambience.test.js` counts the ambience's public
edges (gavel / tally / tile sting) against "facts the rules confirm". The first
version computed those facts the same way the module under test does — watching
`view.nominee` go null→id, and hashing `lastVote`'s fields. It agreed perfectly
with a real bug.

Rewriting the independent count to come from the **engine's own public prose**
(`view.log` matched on `/ nominated /`, `/^Government elected /`,
`/^The motion fails /`) surfaced it immediately: `tally stings 510 vs elections
held 512`.

The bug: **two consecutive elections can produce a byte-identical tally.** Seed
3210 at five citizens — the same Speaker nominates the same citizen on two
successive days and it fails 1–4 both times. An edge keyed on "`lastVote`
changed" silently misses the second one. Fixed by firing on entering
`vote_result`, with the content test kept as the second half of an `OR`.

- **Detection rule:** when a test asserts "module X noticed N things", the count
  of N must come from a *different representation* — the engine's log, a
  recorded action list, a final board state — never from the same view fields X
  reads.
- **Brief/test update:** any future "the presentation noticed the right events"
  gate names its independent source explicitly in the test header.

Second thing this gate taught about its own suite: the tally mutant **survives
at 12 games and dies at the default 36** (the colliding seed is game 30). The
default game count is load-bearing; lowering it for speed would disarm the
check. Written into `docs/step-07.md` so nobody does it.
