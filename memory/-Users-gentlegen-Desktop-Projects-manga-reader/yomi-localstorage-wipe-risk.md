---
name: yomi-localstorage-wipe-risk
description: Five localStorage prefixes still use the retired "Yomi" brand — renaming them silently wipes user reading progress.
metadata:
  type: project
---

The product was renamed Yomi → Manga Orbit (July 2026), but these localStorage key prefixes
still carry the old brand and are load-bearing:

`yomi-progress:<chapterId>`, `yomi-tint:<mangaId>`, `yomi-reader-prefs:<mangaId>`,
`yomi-language`, `yomi-image-quality`

**Why:** localStorage is the source of truth for exact-position resume mid-session (the server
write is only a ~60s checkpoint). A cosmetic "fix the stale brand name" rename would wipe every
existing reader's position, tint cache and reader preferences with no migration.

**How to apply:** treat these strings as persisted schema, not as copy. Renaming requires a
read-old-write-new migration shim, and the change belongs in a PR that says so explicitly.
Related: [[inert-motion-layer]].
