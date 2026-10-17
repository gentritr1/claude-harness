---
name: annex-reviewer-pinned-thresholds
description: "Reviewer scar (2026-07-31): I pinned a heap threshold in a brief without computing it from live data — the exact red flag I enforce on others"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c843d244-2d69-48ae-a3e1-cb8492e43154
  modified: 2026-07-31T08:39:08.198Z
---

**I wrote an unmeasurable acceptance criterion into the in-world conversion plan and shipped it to an implementer.** R2's gate said "heap after the five-phase walk within 12% of heap after briefing." I carried that number from the architect's draft without asking what script produced it. It is unmeetable by *any* implementation that keeps one renderer alive across phases, because the residue being measured is other surfaces' **first mount**, not a leak — there is no point in a five-phase walk where every surface has already mounted once.

**Why:** this is verbatim the red flag in my own harness — "a numeric threshold/target in a brief or spec that was never computed from live data; a brief that pins a number must name the measurement script that produced it." Enforcing it on delegates while breaking it myself is the reviewer's version of the same failure.

**How to apply:** before writing any numeric acceptance criterion into a brief, either (a) name the existing script that produces the number and state the measured baseline, or (b) mark it explicitly `PROVISIONAL — implementer must measure and propose the real gate in round N`. Never state a bare number as a gate. Corollary that worked: the implementer's correct response was to measure a **pre-fix control** (+80.04% on the prior commit, whose investigation→reconstruction step was −15.06% — that negative step *is* the old teardown) and then construct the criterion that isolates the real question (repeated phase cycles with the first-mount confound removed: +1.71%). **Demanding a pre-fix control turned an unmeetable gate into a real one** — ask for that control whenever a delegate reports a threshold miss, before accepting either the miss or a widened cap.

Related: [[annex-prototype-qa-scars]], [[annex-campaign-decisions]].
