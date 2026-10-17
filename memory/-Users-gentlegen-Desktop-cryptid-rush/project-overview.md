---
name: project-overview
description: "What cryptid-rush is, how it was built (3-agent contract-first split), and its debug hooks"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08b7d6ff-99c6-48f9-a148-270af845d6ae
  modified: 2026-08-15T13:09:07.921Z
---

Cryptid Rush = standalone vanilla-JS port (no build, no frameworks) of the claude.ai/design
prototype "Cryptid Rush Table B Arcade.dc.html" (project cfbfe887-c6c4-4b03-bb72-060eb9b46ca8);
an UNO-like 4-seat card game with bots. Built 2026-08-15 via 3 parallel Opus agents with
disjoint file ownership (engine / UI / FX) anchored by CONTRACT.md + js/constants.js written
by the orchestrator first. Source of truth: reference/design.dc.html.

Key facts:
- Deck is 108 cards (25/clan + 8 wilds), NOT 112 — first contract draft got this wrong; the
  design's buildDeck is authoritative.
- AWOOO stamp fires on handBefore === 2 (pre-play count). Engine 'play' events carry both
  handBefore and handAfter for this reason.
- `game._test.setState()` does NOT notify subscribers — nudge a render with `game.setView('table')`
  after using it. `window.CR_GAME` is the debug handle exposed in js/main.js.
- Engine tests: `node --test test/engine.test.mjs` (33 cases). Run app: `.claude/launch.json`
  serves via `python3 -m http.server 8734`.
- Design quirks ported deliberately: wild played from 2 cards skips the no-howl check; deck
  recycle at <=8 builds a brand-new 108 deck (doesn't reshuffle discard); the reference
  runtime's own event banner never rendered (nested setState bug) — our port renders it.
