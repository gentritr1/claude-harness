---
name: prod-migration-not-wired
description: Manga Orbit's build script never runs prisma migrate deploy, and a shipped migration depends on it.
metadata:
  type: project
---

`package.json` build is `prisma generate && next build --webpack` — there is no
`prisma migrate deploy`. The `20260704120000_add_reading_progress_page` migration was applied to
production by hand via SQL editor and is therefore **not recorded in `_prisma_migrations`**, and
a later migration (`ReadingHistoryEntry`) depends on the missing step.

**Why:** any PR that adds a migration will appear to work locally (dev runs SQLite / `prisma dev`)
and fail or diverge on deploy. This is an owner-level production decision, not an implementer's.

**How to apply:** resolve the production migration state *before* merging anything schema-touching
— baseline with `prisma migrate resolve --applied <name>` against production first, then wire
`migrate deploy` into build using `DIRECT_URL` (unpooled), never the pooled URL. Tracked as Q1 in
`docs/next-level-plan.md`.
