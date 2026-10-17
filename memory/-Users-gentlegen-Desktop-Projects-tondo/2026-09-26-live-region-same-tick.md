---
name: 2026-09-26-live-region-same-tick
description: Announcements and focus moves that a later write in the SAME repaint undoes — three instances on one task; also the scroll-container trap that fooled two agents
metadata:
  type: project
---

Tondo repaints the whole screen from every snapshot, which makes "I set it,
therefore the user got it" false for anything a later line in the same tick can
overwrite. Task 8 (a11y) hit this **three times**:

1. `setScreen`'s orientation line was overwritten by `renderGame` in the same
   repaint — the brief's requirement would have shipped as pure decoration,
   passing a DOM check while announcing nothing. Fixed with a one-repaint guard.
2. An auto-opened help dialog stayed over a dealt table because nothing tied it
   to the screen it belonged to. Fixed by closing it with the screen.
3. The one a same-region guard cannot catch: `#live-polite` gets
   `"Game started."` while `#live-now` (`role="alert"`, `aria-live="assertive"`)
   gets `"Your turn. N playable."` — **both fired at t=103ms, the same tick**,
   measured with MutationObservers on both regions. An assertive region preempts
   a polite one, so the mandated polite line is the one that loses.

**Pattern → detection rule → brief update.**
- A brief that adds a live-region line must name every OTHER region written in
  that same snapshot, and the probe must observe them with MutationObservers —
  reading one `textContent` after the fact cannot see a clobber.
- Keying a list fixes focus DURING updates but not AFTER the user presses the
  control: any brief that keys a list must also say where focus lands when the
  pressed control's own container is hidden, and when the focused row is the row
  that left.

## The scroll-container trap (same day, two agents, independently)

`#screen-home` and `#screen-lobby` are `overflow: auto` with `margin: auto` on
the card (the fix from [[flex-centre-overflow-clip]]). The DOCUMENT never
scrolls. Measuring `document.scrollingElement.scrollHeight - clientHeight`
returns 0 and looks exactly like "content is trapped off-screen" — I made this
call once and a subagent made it again hours later. Measure the screen element,
and decide "unreachable" only from the set hidden at BOTH scroll extremes.

Related: [[2026-09-16-round-boundary]], [[2026-08-21-a11y-geometry-pass]]
