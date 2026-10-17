---
name: multiplayer-is-the-destination
description: "Owner correction 2026-08-10 — the game is multiplayer with real people; AI bots are scaffolding, not the product"
metadata: 
  node_type: memory
  type: project
  originSessionId: e5a4db00-7bc4-41ad-90f6-fbade73485ac
  modified: 2026-08-10T21:13:16.616Z
---

Owner, 2026-08-10: *"i think u are trying too hard on making this as AI, but we will make it with people... this is meant to be multiplayer so thats why."*

The discussion gates (D1–D4) over-invested in **bot** sophistication. Real players do the talking; bots are test scaffolding and single-player filler.

**What carries forward (built, and worth more in multiplayer than in solo):**
- `src/engine/floor.js` — the structured claim schema IS the multiplayer speech protocol: canonical, validated, replayable, seat-addressed, no free text to moderate.
- `src/engine/view.js` — the player-safe projection is the **server's authoritative per-client filter**; the leak suites become anti-cheat tests.
- Deterministic engine + driver = server authority + replay from a seed and an action log.
- The ledger renders human claims exactly as it renders bot ones.

**What is now scaffolding, not product:** `src/engine/orator.js` (bots choosing what to say/lie about), and any further work on bot rhetorical depth. Keep it working for solo/testing; stop deepening it.

**How to apply:** do not brief further AI-discussion sophistication. When multiplayer work starts, the architecture is already shaped for it (original roadmap Stage 14) — server owns `G`, clients receive `viewFor(seat)`, clients send structured actions incl. utterances. The intent strip (player speech UI) still matters — it is how a *human* speaks — but it is now a multiplayer feature, not a way to argue with bots.
