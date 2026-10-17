---
name: za-arcade-direction
description: "Arcade redesign branch, its design-kit source, and what the kit defers"
metadata: 
  node_type: memory
  type: project
  originSessionId: 36810674-ff73-4118-8cbb-668e7af1b950
  modified: 2026-08-06T22:10:21.237Z
---

The `arcade` branch (pushed 2026-08-06) implements "Direction 1c — ZA! Arcade" from the claude.ai/design project **"ZA! Game Design Concepts"** (projectId `1f5741af-4f9d-4620-bc05-5d07346c9518`, read via the DesignSync tool). Key files there: `ZA Arcade Kit.dc.html` (the spec: tokens, deck, screens, effects, ambience, handoff) and `za-arcade-tokens.css` (drop-in :root with legacy aliases).

- The kit's handoff intentionally scopes the build: tokens + fonts (Press Start 2P / VT323 / Kaushan Script) + ASCII card indexes + one `.crt-overlay` div. Card art PNGs stay pizzeria-style for now — **sprite regeneration prompts and lobby/round-over mobile layouts are explicitly "not done yet" in the kit**; ask the design side before inventing them.
- The kit's "chain" effect spec (+2 on +2 stacking with combo multipliers and sound cues) describes a rules mechanic the engine does not have — it is a feature request, not a restyle item. Parked.
- The arcade branch was fast-forward **merged into `main` on 2026-08-07** and the branch deleted; the parlour look survives as the git tag `parlour` (commit ce05003). The 55 parlour card PNGs remain on disk in public/assets/cards/ but are unused (USE_IMAGES=false; the deck is DOM + 9 window sprites in public/assets/sprites/).
- Deploy target: user is setting up a Render web service (Node, Frankfurt, `npm install` / `node server/index.js`, branch main). net.js is wss-aware and the server binds process.env.PORT, so no code changes were needed. Free tier spin-down kills in-memory rooms — flagged to user.
- Browser-pane automation scar: the pane can spontaneously resize between screenshots; clicks computed from a stale screenshot then land on the wrong element (this fabricated two "ghost" wild plays before diagnosis). Rule: re-screenshot immediately before any coordinate click, or click by ref.
