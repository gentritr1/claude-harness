---
name: adsense-script-head-pattern
description: "How the AdSense loader is embedded in Loony (plain <script> hoisted to head, not next/script), and why"
metadata: 
  node_type: memory
  type: project
  originSessionId: 5f354963-9a1a-4ad8-85d6-b1daacbdb1bd
  modified: 2026-08-20T05:47:48.576Z
---

The AdSense loader (ca-pub-9813131856455133) lives in `src/app/layout.tsx` as a **plain `<script async ... crossOrigin="anonymous" />`**, not `next/script`.

**Why:** Next 16 runs React 19, which hoists async scripts into the SSR `<head>` — verified 2026-08-20 by curling the dev server and finding the tag inside `</head>`. Using `next/script strategy="afterInteractive"` instead made Google's own script log "AdSense head tag doesn't support data-nscript attribute" and kept the tag out of the initial HTML (bad for AdSense site verification).

**How to apply:** For third-party tags that must be in the served `<head>` in this app, render a plain async `<script>` in the root layout and verify placement via `curl` of the SSR output, not just the live DOM.

Environment gotchas hit the same day: fresh checkout needs `npx prisma generate` after `npm install` (client output is `src/generated/prisma`, gitignored), and there is no `.env` in the checkout — `/api/auth/session` 500s until one is created from `.env.example`. A stale prototype server from `~/Documents/Codex/2026-08-18/...` was holding port 3000.
