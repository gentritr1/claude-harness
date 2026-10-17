---
name: stale-design-docs-trap
description: DESIGN-TWEAK-PROMPT.md and the DESIGN-UPGRADE-BRIEF files are stale; VENUE-QUESTIONS.md is the authoritative source of venue facts
metadata:
  type: project
---

The repo root holds several design documents that read as authoritative but are **superseded**:
`DESIGN-TWEAK-PROMPT.md`, `DESIGN-UPGRADE-BRIEF.md`, `-2.md`, `-3.md`. `DESIGN-TWEAK-PROMPT.md`
still says the venue is "near Fier, Albania" and describes an "engraved Adriatic coastline".
Both are wrong — see [[venue-ground-truth]].

**Why:** on 2026-09-09 I copied "near Fier, Albania" and "one event at a time" straight out of
`DESIGN-TWEAK-PROMPT.md` into the context block of a 17-agent research workflow. A mapper agent
caught it by reading `VENUE-QUESTIONS.md`, but only after the whole Map phase had run on a false
premise, and the "signature ideas" brief had been explicitly pointed at Adriatic light and the
archaeological park. Cost: a stop-patch-resume cycle.

**How to apply:** `VENUE-QUESTIONS.md` (the owner's own answers, in Albanian) beats every design
doc in this repo. Before writing any brief that states a venue fact, read it first and quote it.
The design docs are useful for the *token/typography system* only — treat their business and
geography claims as unverified. Related: [[gallery-is-one-art-exhibition]].
