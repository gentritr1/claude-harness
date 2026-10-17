---
name: art-direction-realized
description: "2026-08-11 milestone — the square is fully authored art, the player has a body, and a bot can accuse you and be answered"
metadata: 
  node_type: memory
  type: project
  originSessionId: e5a4db00-7bc4-41ad-90f6-fbade73485ac
  modified: 2026-08-11T02:23:22.863Z
---

As of 2026-08-11 (main @ 61a8c32), the chosen art direction is realized in `play.html` and **no graybox geometry remains** in the square. 19 verify gates green.

**World, all authored + manifest rows + browser capture sets:** `env-dais-a`, `env-ground-a` (cobbles; its collider top IS the walk plane), `env-facade-a` ×7 (town wall), `env-backdrop-a` (two painted-flat skyline rings, `scenery: true` + `fallback: 'omit'`), `env-lantern-a` ×5, `env-well-a`, `env-tree-a`, `env-barrel-a`/`env-crate-a` ×8, `env-bell-a`, `env-bench-a`, `env-board-a` (11 tile sockets, **unfilled — the open follow-up**).

**People:** four citizen variants with trades (messenger/baker/clockmaker/elder). **The player renders as a citizen too** (same `variantForSeat` mapping; collider unchanged — all 10 walk.html marks identical).

**Systems:** view-driven lighting, five lantern practicals with the Seize-extinguishes-a-lantern weather rule, layered audio, the five juice moments, floor discussion with structured claims, tray + private card + ledger, and **the intent strip** — a bot can accuse you and you answer with a keypress (reproduce: seed 1002, 7p, seat 0, day 2, Chen on `basis: gut`).

**Fingerprint changed deliberately at the strip gate:** seed 1000/7p C3 flag moved `u-18:u-17` → `u-22:u-16` (same lie, same citizen, same government) because seat 0 now speaks and shifts ordinals. Engine invariance still byte-identical floor-off/floor-on over 50 seeds.

**Open, needs the owner's hands, not a test:** the 10s-first-timer / 2s-expert strip acceptance; whether the 44px/140ms strip rise reads well (never watched); 700ms staging cap unverified on 60Hz hardware (measured on ~7fps headless GL). Next build items: tiles into `env-board-a`'s sockets, wall corner pieces, then multiplayer (see [[multiplayer-is-the-destination]]).
