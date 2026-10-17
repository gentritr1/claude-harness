---
name: annex-review-scar-clamped-counters
description: "Review scar 2026-07-23: unifying UI counters by clamping made the display false past the threshold"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0b1a5b43-8b07-44a8-89d7-cc7036f27cf1
  modified: 2026-07-23T21:27:29.547Z
---

Pattern: delegate unified mismatched counters (0/2 SITES vs 0/4 filed) by clamping the display to `Math.min(count, 2)/2` — filing a 3rd/4th site then produced no visible change and "2/2" became factually false.

**Why:** a unification brief said "one pair of numbers"; the cheapest satisfying implementation silently discarded truthful state.

**How to apply:** any `Math.min`/`Math.max` inside a *displayed* counter is a red flag — check what happens past the bound before approving. Fix used: denominator = threshold until met, then true total (n/2 → n/4). Related: [[annex-investigation-inspector-always-mounted]].
