---
name: preview-demo-id-remap
description: Signed-out preview ids ("e1"…) change when ensureDemo starts a demo — any action that carries an employee id from the preview must re-find the person by email
metadata:
  type: feedback
---
Time to rest, SnaxxTech/offday#30 (2026-10-04): the card's "Plan" passed a preview employee id into `openForm`. `ensureDemo()` then created a demo with new UUIDs, so the form opened for the first person ("Alex Morgan (you)") instead of the one clicked. Tests signed in first, so they never took the preview path. There was already a comment about this in `inDemo` ("matched by email"), and it was still missed. The final reviewer caught it.

**Why:** the preview is the public page every visitor sees, and it is the one path signed-in tests never cover.

**How to apply:**
- Any new button that carries an employee id and can be clicked signed out goes through the email remap after `ensureDemo`.
- Add one signed-out UI test for it.
- Pick a row that isn't the first person. A wrong id falls back to the first option, which hides the bug.

Related: [[typed-date-intermediate-values]]
