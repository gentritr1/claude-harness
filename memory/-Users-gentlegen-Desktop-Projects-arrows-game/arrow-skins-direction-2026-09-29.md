---
name: arrow-skins-direction-2026-09-29
description: Owner's art direction for Arrows as of 2026-09-29 — cute/cozy/ASMR-feel arrow skins, iterated on Claude Design canvases
metadata:
  type: project
---

Owner (2026-09-29) wants the game to feel **cute, cozy, easy to be drawn to, ASMR-satisfying, never forced/jittery**; 60 fps stable. First CSS-mockup exit animations were judged "not that good" → focus moved to **arrow skins** (the arrow itself polished: tail cap, shaft layers, bends, head, states).

Canvases (Claude Design): art directions + elemental exits https://claude.ai/artifact/UExfQuPs8dbz3o4ZLBkRFz ; arrow skins https://claude.ai/artifact/BLpq6sX8RZ4GfknZk22xQP (one SkinBoard.dc.html component with a `skin` enum; 9 skins: ink, candy, jelly, critter, yarn, paper, archery, pixel, neon).

**Why:** owner iterates visually on canvases before anything is built.
**How to apply:** use the installed design skills (Emil's 13 skills from github.com/emilkowalski/skills installed globally 2026-09-29, frontend-design, ui-ux-pro-max); nothing ships until owner picks; any in-game skin goes behind a flag and is perf-gated like [[perf-architecture-and-evidence]]. Build scripts must pin Node v20.19.4 ([[shared-host-contention]]).
