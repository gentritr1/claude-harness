---
name: talk-is-the-core
description: "Owner decision 2026-08-09 — the game's core is chat/discussion; three-layer plan (chatter → intents → LLM), player side = quick intents first"
metadata: 
  node_type: memory
  type: project
  originSessionId: e5a4db00-7bc4-41ad-90f6-fbade73485ac
  modified: 2026-08-09T21:09:45.248Z
---

Owner (2026-08-09): "most of things will be through chat... overall the feel of game" — the discussion layer IS the game; visuals/movement are the stage. Agreed plan:

- **Layer 1 (in flight)**: v1's `AI.chatter` wired as ambient murmurs — speech bubbles at beats, via an `Object.create(G)` facade carrying a derived mulberry rng so the byte-frozen engine's chatter never touches the seeded stream (see [[rng-stream-discipline]]). Invariance proof chatter-on vs chatter-off required.
- **Layer 2 (next major gate, task #11)**: structured discussion — bots speak from their real ai.js internal state (claims/suspicion/defense); player uses quick intents (accuse/defend/claim/silent). Architecture rule: **intent → text, back end swappable**, so an LLM can replace the template prose later without touching deterministic game logic.
- **Layer 3 (parked experiment)**: free-text player input + LLM bots; costs replay determinism + per-match API unless sandboxed to the text layer only.

**How to apply:** any chat/dialogue brief must keep intents deterministic and testable and treat text generation as presentation; never let dialogue generation consume `G.rng()` or read the omniscient event log; leak-sweep all generated prose like the view model.

**Layer 2 architecture upgraded (2026-08-10, external design review adopted):** speech is CANONICAL — if it changes bot beliefs it changes outcomes, so structured speech actions (CLAIM_HAND/ACCUSE/SUPPORT/QUESTION/SILENCE with typed basis fields) live in the deterministic engine log, not presentation. This means a deliberate, tested EXTENSION of the engine (new discussion module) — the byte-freeze was a porting discipline; parity tests keep guarding legacy paths while v2 grows engine-native features v1 never had. UI timer auto-submits SILENCE; engine stays wall-clock-free. Floor opens EVENT-DRIVEN (contradiction, vote flip, new power, direct accusation, isolation), not on a schedule — target one meaningful exchange per day. Anti-tell rule is testable law: no presentation channel (animation/light/timing) may correlate with hidden roles across seeds — sweep it like the leak tests. Movement question: council-view (elevated ring-readable camera, clickable seats, walking optional) to be A/B'd BY THE OWNER'S HANDS against walking before any rebuild — the reviewer read screenshots, the owner has played; feel verdicts need hands.
