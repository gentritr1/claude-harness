---
name: annex-preview-pane-quirks
description: "Annex preview driving quirks — synthetic clicks don't reach React (use el.click()), vite ignores assigned PORT (lands on 4174), page can silently reload back to start screen"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3cde3ba2-d335-4a55-befd-d33aa1a0aa0b
  modified: 2026-07-22T21:14:29.136Z
---

Found during the 2026-07-20 Case 77 diorama review (related: [[browser-pane-stale-screenshot]]):

1. **Browser-pane `computer` clicks land at the right coordinates but never reach React** in this app — phase stayed `start-screen` after repeated correct-coordinate clicks. `javascript_tool` with `element.click()` advances the app fine. Drive all Annex flow traversal via `el.click()`; reserve `computer` for screenshots.
2. **Port drift:** `.claude/launch.json` now has `autoPort: true`, but Vite ignores the harness-assigned PORT and picks its own (4173 in use → served on **4174** while the pane tab pointed at the assigned port and showed chrome-error). After preview_start, read `preview_logs` for the REAL port and navigate there explicitly (`http://127.0.0.1:<port>`). Also `window.location.reload()` can snap the tab back to the dead assigned-port URL — re-`navigate` instead of reloading.
3. **Silent reload to start screen:** mid-session the page returned to the start screen (save intact, "Continue local case" restores). Re-check `document.title` before trusting earlier navigation state.

**How to apply:** verification path that works end-to-end: preview_start → preview_logs for real port → navigate → advance phases with el.click() → measure via javascript_tool (label rects, canvas pixel samples, dispatched PointerEvent for parallax, temporary data-scene-state/class toggles for CSS gates) → screenshot only for final eyeball evidence.

Added 2026-07-21 (camera-travel review):

4. **Pane tab can be `document.hidden: true`** (user not viewing the pane) — the scene rAF loop hard-pauses by design, so NO motion/travel/transform writes happen; timers throttle to ~500ms too. tabs_select does not un-hide it. For any rAF-timing measurement, don't fight the pane: run `scripts/evidence-travel.mjs <url>` style headless-CDP harnesses instead (headless Chrome fires rAF normally).
5. **Pane restart = fresh browser profile** — localStorage (the game save) is gone after the pane fully closes; only keys the app re-creates on load (accessibility) reappear. A vanished save after a pane restart is an environment artifact, NOT a schema-wipe bug — check persistence.ts diff before panicking.
6. **Default shell node is v14 (nvm)** — eslint 9 dies with `Object.hasOwn is not a function`, npm output looks old-format. Prefix gate commands with `export PATH="$HOME/.nvm/versions/node/v24.18.0/bin:$PATH"`.

Added 2026-07-22 (stagecraft review):

7. **Hidden pane sticks in `travel` presentation** (rAF suspended → promote-to-closeup never fires), so the `Return to concourse` button NEVER MOUNTS — `find(...)?.click()` silently no-ops and any "after return" probe measures nothing. The rm-toggle workaround only half-works: rm ON renders closeup via the derived coercion but the underlying state stays `travel`, so toggling rm OFF snaps back. Anything depending on an actual return (worldLine, return-emphasis) must be verified headless, not in the pane. Also hidden-pane setTimeout throttling (~1s) makes sub-second one-shots (the 950ms emphasis hold) unsamplable — use an in-page MutationObserver and read its log afterward.
