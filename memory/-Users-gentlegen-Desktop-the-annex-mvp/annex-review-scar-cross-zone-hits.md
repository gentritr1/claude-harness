---
name: annex-review-scar-cross-zone-hits
description: "Review scar 2026-07-25: two latent pilot bugs — overlapping caption boxes stole hit-tests / dual captions collided — invisible to per-zone verification"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0b1a5b43-8b07-44a8-89d7-cc7036f27cf1
  modified: 2026-07-25T16:38:38.596Z
---

Pattern: the shipped Care Ward pilot carried two latent bugs my review approved past: (1) two scene zones' caption boxes overlapped, so the later element in DOM order won the hit test and clicking one ring's centre ARMED THE OTHER METHOD at 375px; (2) with focus on one zone and pointer on the other, both captions printed over each other. Both were found only when the rooms round ran cross-zone interaction sweeps (fixed in df7f15e: pointer-transparent captions + ring-sized hit region; armed > hover > focus caption precedence with a one-open-caption harness assertion).

**Why:** the pilot's verification drove each zone's path individually (arm/commit per zone, keyboard per zone) — correct per-control, blind to control-pair interference. Overlap bugs live BETWEEN controls.

**How to apply:** any surface with ≥2 positioned interactive elements gets a cross-element sweep in review: click each control's visual centre and assert the INTENDED control armed (not just "a" control); drive split focus/pointer states; assert at most one caption/tooltip open. Per-element verification passing is not evidence the pair works. Related: [[annex-prototype-qa-scars]], [[annex-review-scar-clamped-counters]].
