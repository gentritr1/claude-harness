---
name: agency-beats-choreography
description: "Feels like art, not a game" was an agency problem — autonomous per-actor controllers plus player click-to-move fixed what better staging and motion specs could not.
metadata:
  type: feedback
---

Across four review rounds on Secret Dictator, the user kept saying the world felt
like "floating art". Rounds 2–3 answered with better *presentation* — spec-accurate
walk speeds, depth scaling, painted plates — and the verdict stayed the same. What
fixed it (round 4) was a model change: bot citizens got autonomous roam controllers
(idle→stroll→errand, desynchronized, personal space, density cap), phase
choreography shrank to summons for story roles only, and the player got
click-to-move on the ground. The user accepted immediately.

**Why:** "game feel" for an inhabited world = perceived agency. Deterministic,
synchronized, whole-crowd arrangements read as authored art no matter how good the
motion curves are. Autonomy (self-initiated, desynchronized movement) plus player
control is the vibe; polish multiplies it but cannot substitute for it.

**How to apply:** when a client compares to a "world" game (Town of Salem, Among
Us) and calls the build static/deterministic, do not reach for more motion polish —
ask whether any entity moves *without being told to* and whether the player can
move *themselves*. Detection rule for reviews: instrument the choreography entry
point and count movements that happen with zero choreography calls in flight; if
the answer is none, the world is staged, not alive.

Related: [[secret-dictator-project]]
