---
name: rubble-vite-ipv6-localhost
description: "Vite 8 dev servers on this Mac bind [::1] only, so the rubble measurement scripts' 127.0.0.1 defaults fail; pass http://localhost:PORT and use the gitignored launch entries rubble-review / rubble-baseline"
metadata: 
  node_type: memory
  type: project
  originSessionId: df4dd4c1-38f3-4c2b-8e0b-c496f217dd8b
  modified: 2026-09-05T22:36:40.286Z
---

Vite 8.2.1 started from the Browser pane launch config listens on IPv6 loopback only (`[::1]:5184`), and the rubble scripts (scripts/capture-rubble-baseline.mjs, measure-rubble-ground-floor.mjs, review-rubble-phase-1.mjs) default to `http://127.0.0.1:518x`, which fails with a Playwright navigation error. Pass `http://localhost:5184` as the URL argument or `REVIEW_URL`.

Two launch entries were added on 2026-09-06 to the repo's gitignored `.claude/launch.json`: `rubble-review` serves /private/tmp/rubble-square-review (a detached review worktree, port 5184) and `rubble-baseline` serves /private/tmp/rubble-square-baseline (branch point f738316, port 5183). Both worktrees have node_modules installed via `npm ci` with Node 20.19.4.

**Why:** the reviewer must re-run Codex's measurement scripts against both builds to verify a phase; the first attempt lost a round trip to the IPv4/IPv6 mismatch.

**How to apply:** start both with preview_start by name, then run the scripts from the review worktree with localhost URLs and scratchpad output dirs. Related: [[rubble-floor-threshold-unmeasured]].
