---
name: 2026-08-polish-pass
description: "State after the 4-agent Opus review + full polish pass (2026-08-15) — what was fixed, what is still unverified"
metadata: 
  node_type: memory
  type: project
  originSessionId: 98212e7f-52fe-4101-89d2-52f2f68ae4e0
  modified: 2026-08-14T22:32:07.648Z
---

On 2026-08-15 four Opus review agents (correctness / animation / frontend design / UI-UX) audited v0.1 and a full fix pass was applied. Key architecture decisions that now hold:

- **Keyed hand rendering**: `renderHand` reconciles by card id (no `innerHTML` wipe) so transitions, scroll, and focus survive snapshots. Seats/queue use HTML-string memoization instead. Breaking this reintroduces the dead-transition class of bugs.
- **One geometry variable**: `--table-d` on `.stage` drives ring diameter AND seat positions (clamped with `max()`/`min()` for narrow screens). Never position seats independently of it.
- **Server invariants added**: empty-room TTL is computed in `tickRoom` from observed state (never armed at call sites); a seat token outranks a half-open socket (takeover + close-handler socket guard); `isActingHost()` unfreezes tables with absent hosts; joins/addBot allowed during `roundOver`.
- **Tests**: `test/rooms.test.js` pins those fixes; 7 of 10 fail on pre-fix HEAD (verified). `npm test` runs both suites.
- **Mock drift is real**: `?mock=1` scenes don't process `play` in most scenes — wire sends were verified by console log, engine paths by rules tests, not by mock UI.

Still open / UNVERIFIED (close these before calling the polish shipped):
- ~~Reduced-motion behavior only reasoned from CSS~~ CLOSED 2026-08-22 via headless-Chrome CDP media emulation (confetti 24→0, `.celebration` display none) — see [[headless-cdp-media-emulation]]. Still not observed with the OS toggle on a device.
- Safe-area insets + 100dvh need a real notched iPhone check.
- Card-flight / deal-ghost / turn-token "does it read?" needs the user's eyeball on a recording (taste gate per harness §2).
- User was live-editing styles.css and app.js during the session (flatter buttons, new keyframes `top-card-land`, `table-turn` — possibly not yet wired to anything). Re-read files before editing; check whether those keyframes got consumers.
