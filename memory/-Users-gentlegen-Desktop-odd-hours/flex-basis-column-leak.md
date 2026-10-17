---
name: flex-basis-column-leak
description: flex-basis set for row direction becomes height when a media query flips to column
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c0bff7d7-4d12-4eb5-addf-8dea9a66ddb9
  modified: 2026-08-16T12:38:11.589Z
---

Two independent phone-layout bugs in one review came from the same CSS pattern:
`flex: 1 1 130px` (width basis) inside a row that a phone media query flips to
`flex-direction: column` — the basis becomes *height* (a 133px-tall text
field; a 240px empty band), and one pushed the primary CTA below the fold.

**Why:** flex-basis is axis-relative, not width-relative.

**How to apply:** review rule — whenever a media query flips flex-direction,
grep that container's children for `flex: N N <px>` and pin them to
`flex: 0 0 auto` in the flipped block. Fired 2× on Odd Hours (2026-08-16);
promote to global red-flag list if seen again elsewhere.
