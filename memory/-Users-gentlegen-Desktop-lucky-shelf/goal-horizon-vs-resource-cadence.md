---
name: goal-horizon-vs-resource-cadence
description: Design-review scar — I shipped a daily-rerolling goal that a 1-item/day loop could never fill; check goal horizon against resource cadence.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b64ec080-bda3-4267-9ae4-93fecb2d7c5b
---

While prototyping the "Today's Order" demand ([[todays-order-demand]]) I designed a goal that re-rolled its target **every day** and required accumulating **3 of a tag**, in a loop that only hands the player **one draft per day**. The target moved faster than the player could ever satisfy it, so the goal was structurally unfillable on purpose — and I only caught it during the tuning pass, when the fuzz numbers looked flat and I asked *why*.

**What I ignored:** I specced the mechanic's *reward* (the mult) without simulating one player turn against the *resource rate*. I checked "is the bonus big enough?" before "can the player physically reach the condition given how fast the inputs arrive?" I also over-trusted the flat fuzz numbers as "weak lever" instead of "unreachable lever" — the bots weren't under-motivated, the goal was impossible to aim at.

**Why it matters:** an unfillable (or trivially-fillable) goal is worthless at *any* magnitude. Tuning numbers on a broken cadence is wasted motion. This is the kind of invisible-design miss my harness already warns about for feel work — it applies to goal/economy design too.

**How to apply:** before tuning a goal's reward, trace ONE unit of the loop by hand: how many qualifying inputs arrive per period, how long the goal's window stays open, and whether accumulation across periods is even possible. Align the goal's horizon with the resource cadence (I fixed it by keying the order to the 3-day rent cycle, not the day, and dropping the count 3→2). Detection rule for briefs/reviews: **any goal that needs multi-period accumulation against a slower input rate is a red flag — state the arithmetic (inputs/period × periods-open ≥ required?) explicitly.** If this pattern recurs in another project, promote it to the §6 red-flags list in the global harness.
