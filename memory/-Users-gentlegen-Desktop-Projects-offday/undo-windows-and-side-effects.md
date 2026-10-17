---
name: undo-windows-and-side-effects
description: Review lessons from request emails (2026-10-04) — client undo windows must be bounded by the server delay; cancel side effects only after the action succeeds
metadata:
  type: feedback
---
Two bugs in the request-emails feature (PR #26) passed TDD per task and were only caught by the final whole-branch review:
1. The undo toast paused on hover/focus with no limit, but the server sent the decline email after a fixed 8 s, so an undo could arrive after the email had gone. Fix: `lib/undo.ts` holds UNDO_LIMIT (7 s) and DECLINE_DELAY = UNDO_LIMIT + 1 s, one shared source.
2. `reopenRequest` cancelled the pending decline email before its checks ran, so a reopen that failed silently lost the email.

**Why:** each task's tests only covered the happy path ("an immediate reopen").

**How to apply:**
- Any client-side window (undo, grace period) paired with a server timer must share one constant, with the client strictly shorter. Test the hovered/focused case.
- A side effect that undoes something (cancelling a timer or a send) goes after the action has committed, never before its validation.
- Write a failure-path test, e.g. "the reopen fails, so the email still goes".

Related: [[stacked-pr-merging]]
