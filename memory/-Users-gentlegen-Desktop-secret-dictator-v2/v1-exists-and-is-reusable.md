---
name: v1-exists-and-is-reusable
description: "v2 folder is empty; a complete v1 lives at ../secret-dictator with a pure, tested rules engine worth porting"
metadata: 
  node_type: memory
  type: project
  originSessionId: e5a4db00-7bc4-41ad-90f6-fbade73485ac
  modified: 2026-08-08T19:38:16.174Z
---

As of 2026-08-08, `~/Desktop/secret-dictator-v2` is an empty directory. The real prior art is `~/Desktop/secret-dictator` (v1): a complete, playable, single-player 2D web game — Secret Hitler-style ruleset (Speaker/Deputy elections, Reform/Seize tiles, power ladder, chaos track), 5–10 players where all opponents are AI. No build step, vanilla JS, Kenney assets, design doc in `Secret Dictator.dc.html`.

Key reusable piece: `js/engine.js` (725 lines) is a **pure seeded state machine — no DOM, no timers, deterministic** — with tests in `test/engine.test.js` (445 lines), plus `js/ai.js` (419 lines) bot opponents. This already satisfies the roadmap's Stage 8 (canonical state vs presentation), Stage 9 (complete offline loop), and Stage 12 (bots) for the v1 ruleset. Any v2 roadmap review should push to port this engine, not rewrite it.

Resolved 2026-08-08: v2 = v1's ruleset in a 3D three.js town, single-player vs AI first. The user confirmed **v1 is a live upstream they are still actively editing** (e.g. the 21:06 chatter polish was theirs). Standing procedure: at every step review, `diff` v1's `js/engine.js`+`js/ai.js` against v2's `src/engine/` and treat drift as a deliberate adopt-or-defer decision, re-proving `npm test` (28,881 baseline), `driver-parity`, and simulate after any adoption.

Product priorities confirmed by user 2026-08-08: nail the gameplay, no fast-tracking, and **ambience + characters are where they want depth and time spent** — polish is the point, not speed. Blender→glTF→three.js is the agreed art pipeline.
