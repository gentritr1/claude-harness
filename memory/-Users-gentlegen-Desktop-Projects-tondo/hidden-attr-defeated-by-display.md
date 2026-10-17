---
name: hidden-attr-defeated-by-display
description: Tondo — `el.hidden = true` silently does nothing when an author CSS rule sets `display` on that element's class; two live instances found 2026-08-20
metadata:
  type: project
---

Tondo's client hides UI by setting `node.hidden = true` (25+ call sites in `public/js/app.js`).
The UA rule `[hidden] { display: none }` has specificity 0-1-0, so ANY author rule that sets
`display` on the element's class wins and the "hidden" node stays visible.

FIXED 2026-08-20: `.plaque-pair[hidden]` (styles.css:258) and `.lobby-actions[hidden]` (styles.css:191)
added next to their rules; both re-verified live (real server game + two clients), see below.

Most of `public/styles.css` guards this explicitly (`.bar[hidden]`, `.ribbon[hidden]`,
`.banner[hidden]`, `.hand-wrap[hidden]`, `.fade[hidden]`, `.turn-token[hidden]`,
`.you-status[hidden]`, `.action-row[hidden]`, `.net-banner[hidden]`). Two rules were missed:

- `.plaque-pair { display: flex }` (styles.css:256) → `#match-or-wrap` — after a WILD, the
  centre plaque renders a dangling "or" with no value ("Cheese or ").
- `.lobby-actions { display: flex }` (styles.css:190) → `#host-controls` — every NON-HOST in
  the lobby sees "Add bot" and "Start game" directly above "Waiting for the host to start…".
  Cosmetic only: `server/index.js` gates `addBot`/`startGame`/`removeSeat`/`newRound` on
  `room.isActingHost(seatId)` and refuses, so it is not an authorization hole.

**Why:** invisible to every headless check — the DOM says `hidden=true`, only
`getComputedStyle(el).display` reveals it. Found by eyeballing screenshots, not by tests.

**How to apply:** any new CSS rule that sets `display` on a class whose element is toggled
via `.hidden` in app.js MUST ship a matching `[hidden] { display: none }` guard. When
reviewing a `hidden`-toggle bug, verify with `getComputedStyle(el).display`, never with
`el.hidden`. See [[2026-08-polish-pass]].
