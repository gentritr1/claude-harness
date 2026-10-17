---
name: phantom-pan-responder-releases
description: The greybox self-dropped ~100 bodies with zero touch input; a PanResponder release must not be trusted as a player action on its own
metadata: 
  node_type: memory
  type: project
  originSessionId: 4350671c-b674-4bdd-be6d-75edc0aad3af
  modified: 2026-07-25T14:33:28.496Z
---

merge-kit's greybox, Release build on the iOS simulator: the game **dropped continuously with no
input at all** — 23 drops within seconds of the screen mounting, 101 thirty seconds later, paced at
almost exactly the 0.4 s rules cooldown (i.e. a drop was queued essentially every frame). The only
touch in the whole session was the tap on the menu button that mounted the screen.

Cause class: `onPanResponderRelease → requestDrop` trusts that a release was preceded by a real
touch. Whatever produces stray/synthesised releases (responder churn on a view that re-renders at
60 fps, a touch delivered across a mount boundary, the simulator's input injection), the handler
fires and the game acts.

**How to apply.** A discrete action must require the *pair*: gesture logic lives in
`packages/merge-shell/src/react/aimGesture.ts` as a plain state machine —
- `grant` sets `dragging`; `release` only acts if `dragging`, otherwise it increments
  `unpairedReleases` and is discarded;
- `terminate` clears the drag without acting;
- counters (`grants/releases/drops/unpairedReleases`) render in the greybox HUD, so a recurrence is
  visible in a screen recording rather than buried in a log.

Detection rules learned:
- A gesture wired straight into a runtime is not unit-testable; extract the decision logic so
  "release without grant produces no action" can be a test (`test/aimGesture.test.ts`).
- **Cross-check counters against your own input.** The bug was only obvious because the HUD showed
  `drops 23` after one tap. Any screen that acts on input should display how many actions it thinks
  it received.
