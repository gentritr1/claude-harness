---
name: delegation-review-loop
description: "The four-round Opus-delegate / Fable-review loop that shipped Secret Dictator's living world — what made it work, and the operational gotchas."
metadata: 
  node_type: memory
  type: project
  originSessionId: 9d90e3f0-7698-483d-a615-b31b363ed1c5
  modified: 2026-08-08T20:31:28.231Z
---

Pattern that worked (2026-08-08, four rounds to user acceptance):

1. Self-contained brief per round (context, hard constraints, per-item verification
   duties, report format). Delegates ran verification themselves; my review then
   **re-ran the scenarios independently** rather than trusting reports — and every
   round it caught something the report missed (round 3: reveal pieces standing on
   the painted rooftops; round 2: 7s walks needed duration-over-speed adjudication).
2. Each round's brief folded in: the previous round's disclosed deviations, my
   review findings, and any new user feedback. Reviewer applied small fixes
   directly (WALK_CEIL, chat seams) instead of spinning another round.
3. Commit + push per approved round as checkpoints with honest "known issue" notes
   in the message.

Operational gotchas:
- **Delegate transcripts expire** — a SendMessage follow-up to a finished agent
  failed ("No transcript found"); round 2 had to relaunch as a fresh agent with a
  fully self-contained brief. Never plan on resuming a completed delegate; always
  write briefs that stand alone.
- Stray test-rig intervals in a reused browser tab clobbered a later rig (an old
  watcher cleared the new autoplayer's handle). Hard-reload between rigs, or
  `for(i=1;i<9999;i++)clearInterval(i)`.
- Delegates' quality jumped when the brief demanded DOM-measured evidence (position
  ladders, sample reconciliation) instead of screenshots alone — round 4 even
  runtime-verified reduced motion via a matchMedia stub page on its own initiative.

Related: [[agency-beats-choreography]], [[secret-dictator-project]]
