---
name: delegate-overrode-my-ruling
description: Two cases where an implementer declined my instruction with evidence and was right — what made that possible, and the shape of my error both times
metadata:
  type: feedback
---

Twice in the Tondo Tier 2/3 pass a delegate refused to execute my ruling
literally, came back with the measurement instead, and was right.

1. **The casing guard.** I ruled "leave a word alone when it already contains an
   interior capital" and said to apply it to both copies of `nicely()`. That
   helper is also used on hardcoded suit labels, so under my guard
   `nicely('PEPPERONI')` returns `PEPPERONI` unchanged and "Doesn't match — need
   Pepperoni" would have shipped as "need PEPPERONI". The implementer checked
   each of the 26 call sites' context before converting, split the helper, and
   said why. I verified: my rule did exactly that.
2. **The knockout.** I ruled that both strip toggles should get the same
   treatment. The implementer built it, looked, and found a 1px ring severs a
   1.6px *outline* glyph into brackets (1158 → 1089 ink px), while the filled
   cone needs exactly that treatment. It shipped the knockout on one and not the
   other, and recorded that the grammar I actually cared about was preserved.

**My error was the same shape both times:** I generalised a rule from the case
in front of me to "apply it everywhere this function/class is used" without
checking the other call sites. The instruction was right for its case and wrong
as a blanket.

**How to apply.** When ruling on a shared helper or a shared class, either name
the call sites the ruling covers, or say explicitly "check every call site
before applying; report if any context differs". And keep saying out loud that
a delegate reporting "your instruction would cause harm, here is the
measurement" is the outcome I want — both of these arrived because the brief
asked for reasoning rather than compliance.

Related: [[2026-09-27-tier23-shipped]]
