---
name: annex-worktree-stale-server-scar
description: "Evidence harnesses default to port 3000, which may be a stale main-checkout vite server — a worktree session's ALL PASS can measure unedited code"
metadata: 
  node_type: memory
  type: project
  originSessionId: e6c09c85-1530-49c1-a994-33d4e5c957e6
  modified: 2026-07-27T09:33:26.184Z
---

Fired 2026-07-27 (casefile-portal high-contrast fix): all evidence scripts
(`audit-contrast-probe.mjs`, `evidence-document-semantics.mjs`,
`evidence-record-search.mjs`) default `APP_URL` to `http://127.0.0.1:3000/`.
A vite dev server from the MAIN checkout (`--port 3000 --strictPort`, started a
day earlier by another session) was still listening there, so a worktree
session's first probe run came back ALL PASS while measuring the **unedited**
CSS. The probe passes with or without the fix, so the green run was worthless.

**Why:** worktrees share nothing with the main checkout's running dev server;
the harness URL default silently points at whichever repo copy started port
3000 first.

**How to apply:** in any worktree session, before trusting a harness run:
1. `curl -s http://127.0.0.1:3000/src/styles.css | grep <the new selector>` —
   confirm the served file contains the edit (or check `lsof -p <pid> | grep cwd`).
2. If stale, start a worktree server (`npx vite --port 3100 --strictPort`) and
   pass the URL as argv to every script: `node scripts/<harness>.mjs http://127.0.0.1:3100/`.
3. Close the loop with a computed-value check, not the PASS line — e.g. the fix
   is proven by `textColor` in the probe JSON flipping to the expected token
   (here `oklch(0.83 0 0)`), not by ALL PASS.

Related: [[annex-preview-pane-quirks]] (vite port drift), [[annex-css-and-contrast-scars]].
