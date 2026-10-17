---
name: delegate-on-the-newest-opus
description: "Implementers and full reviews on Opus 5.5, scoped re-reviews on Sonnet 5.5 — model enum verified 2026-10-02"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-01T23:28:18.823Z
---

**Verified 2026-10-02** by asking three throwaway agents to report their own model:
`model: "sonnet"` → **Sonnet 5.5** (`claude-sonnet-5-5`); `model: "opus"` → **Opus 5.5** (`claude-opus-5-5`); `model`
omitted → **Opus 5.5** (inherits the session). The enum resolves to the newest version of each tier, so naming the tier
is safe. (An earlier version of this note assumed `"opus"` might pin an older Opus and said to omit the field; that was
an untested assumption and it was wrong.)

**The owner's rule:** use Sonnet where the difference is not noticeable, Opus 5.5 where the drop would be large.

**Applied:**
- **Implementers and full task reviews → Opus 5.5.** These need breadth and design judgment across many files, and the
  task reviews on this branch are where the structural findings came from (R104/R105's wrong reasoning, the deleted-test
  mapping, the round-start crash's root cause).
- **Scoped re-reviews of a fix round → Sonnet 5.5.** Evidence from feat/next-level: every Sonnet re-review found a real
  defect, several the Opus task review had missed, and two overturned the controller's own rulings — B1-5's reader holes
  (duplicate lines, `--allow-silent == --rounds`), B1-4's unpinned `AnimatedNumber` wiring, B2-1's sibling ceiling hole,
  B2-2's two "redundant" guards that were load-bearing. No noticeable drop for that job.

**Why:** the owner switched the session to Opus 5.5 and wants that quality where it matters, without paying for it where
it does not.

**How to apply:** name the tier explicitly (`"opus"` / `"sonnet"`). If a Sonnet re-review ever passes a fix that a later
review then breaks, that is the signal to move re-reviews back to Opus — record it here when it happens.

Related: [[next-level-execution-paused]], [[every-gate-we-write-ships-a-silent-pass]].
