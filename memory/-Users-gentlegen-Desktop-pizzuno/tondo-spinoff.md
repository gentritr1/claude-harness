---
name: tondo-spinoff
description: "New simple UNO-like repo \"Tondo\" at ~/Desktop/tondo, spun off ZA Ring Table design; protocol frozen, 2 Opus implementers"
metadata: 
  node_type: memory
  type: project
  originSessionId: 73ff2d19-3bc0-45bd-9ea4-3e6caa46064f
  modified: 2026-08-14T21:24:49.985Z
---

Started 2026-08-14. New repo `/Users/gentlegen/Desktop/tondo` — a deliberately SIMPLE
multiplayer UNO-like based on the "ZA Ring Table" design (claude.ai/design project
1f5741af-4f9d-4620-bc05-5d07346c9518, file copied to docs/design/ring-table.dc.html).

- Name: **Tondo** (Italian "round"; pizza tonda + ring table). Checked 2026-08-14: no
  existing game found ("Slice" and "Crust" are taken by real pizza games).
- Stack copied from ZA's spine per Explore-agent audit: Node ≥18 + `ws` only, no build
  step, server-authoritative, full per-seat snapshot on every change (no deltas),
  seat tokens for reconnect. Deliberately NOT copied: idle tiers, bot callout lottery,
  personalities, host re-election, ETag static server, 9k-line app.js.
- Contract: PROTOCOL.md in repo root is FROZEN v1; both halves built against it.
  Port 4600. Call is "TONDO" at 2 cards; callout penalty draw 2; bots callout 35%.
- Split: Opus agent A = server/ + test/ + scripts/ (smoke: scripts/host-smoke.js);
  Opus agent B = public/ (port of ring-table design, mock mode ?mock=1, QA shots in
  docs/qa/). Orchestrator owns git.
- Related: [[pizzuno-setup]], [[za-fleet-build]]
- 2026-08-14 outcome: v0.1 committed (c30d845). Both halves APPROVED after review:
  34 rule tests + 4 smoke bot games re-run by orchestrator; full human game played
  live in browser (wild picker, skip/reverse/+2, draw paths, TONDO call, win banner,
  new round). Open gaps: drawn-playable decision bar and callout bar verified only
  in mock + server probes, not over the live wire in browser; reconnect retry ladder
  and iOS Safari untested; ws ping/pong terminate path unobserved. color-mix() CSS
  needs Safari ≥16.4. Known nit: plaque slightly overlaps side seat plates at 375px.
