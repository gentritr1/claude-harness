---
name: dev-environment-gotchas
description: Node version and port gotchas for running FJALË locally
metadata: 
  node_type: memory
  type: project
  originSessionId: 1a376e78-fea1-4e3f-b833-76f2dbc19ef6
  modified: 2026-08-04T21:22:39.489Z
---

- Default shell Node is v14.19.3 (nvm) — `npm run check` fails on `??=` syntax. Use `/Users/gentlegen/.nvm/versions/node/v24.18.0/bin/node` (or any nvm 20+). Repo now declares `"engines": {"node": ">=20"}` (since ~2026-07-19); still no .nvmrc.
- **`server.mjs` holds `publicPaths` in memory at boot** — a preview server started before a commit that adds a new asset will 404 it, showing a broken image that looks exactly like a bad file. Restart the preview after any commit touching `publicPaths` before believing a missing-asset symptom (cost a false-alarm investigation 2026-08-04).
- Port 3000 is occupied by an unrelated "Manga Orbit" node server; port 4173 is ALSO taken (a `research-idea-4` project server from a Codex runtime, as of 2026-07-19). `.claude/launch.json` now has `"autoPort": true` — preview_start assigns a free port via PORT env; don't hardcode.
- Synthetic `type` events in the in-app browser do NOT reach the game's document keydown handler — but `computer` `key` actions (e.g. Escape) DO, and programmatic `.click()` on `#keyboard button[data-key="…"]` drives the real handler path reliably (verified 2026-07-19).
- rAF-scheduled behavior (e.g. focus moves) can appear broken in the embedded pane because frames are throttled when not painting — instrument `requestAnimationFrame` to prove the callback fires before calling it a bug (hit 2026-07-19 on hint-confirmation focus).
- A bare `node --test` (what `npm test` runs) discovers test files RECURSIVELY, including other agents' git worktrees under `.claude/worktrees/` — a "green" run can be contaminated by (or credit you with) another tree's tests (hit 2026-08-01: a not-yet-merged conformance suite appeared in the main tree's results). For local verification always run `node --test tests/`; CI is unaffected (no worktrees there).
