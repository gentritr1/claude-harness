---
name: apollonia-neon-env
description: Neon DATABASE_URL vs DIRECT_URL must be the same endpoint (pooled vs not); 2026-08-01 both were wrong and broke the build
metadata: 
  node_type: memory
  type: project
  originSessionId: 933891dd-9679-4626-b65f-30d816eff62b
  modified: 2026-08-01T12:53:35.682Z
---

Apollonia uses Neon + Prisma with `url = env("DATABASE_URL")` and `directUrl = env("DIRECT_URL")` in `prisma/schema.prisma`. They must point at the **same database**, differing only by `-pooler` in the host:

- `DATABASE_URL` = `ep-divine-cloud-asiz18y0-pooler.c-4.eu-central-1.aws.neon.tech` (pooled, app runtime)
- `DIRECT_URL`  = `ep-divine-cloud-asiz18y0.c-4.eu-central-1.aws.neon.tech` (unpooled, migrations/introspection)

Real data (admin user + reservations) lives on the `ep-divine-cloud-asiz18y0` Neon project. `ep-crimson-wave-asnio2bc` is an empty leftover project — not the app database.

On 2026-08-01 the build failed twice because `.env` `DATABASE_URL` was mangled by a bad paste: protocol was `ostgresql://` (missing `p`), host pointed at the empty crimson-wave project, and the query string was truncated to `sslmode=req`. Symptoms in order: Prisma "the URL must start with the protocol `postgresql://`", then `P2021 The table public.GalleryImage does not exist`.

**Why:** `next build` prerenders `/` (ISR, revalidate 1h), which calls `db.galleryImage.findMany()`. So a bad `DATABASE_URL` is a hard **build** failure, not just a runtime one — on Vercel too.

**How to apply:** when a Prisma/Neon error appears, diff the two URLs' hosts before anything else — `db pull` uses `DIRECT_URL` while the app uses `DATABASE_URL`, so "introspection works but the app says table missing" means they target different databases. Confirm which endpoint holds data by row-counting through each URL rather than assuming. There is no `prisma/migrations/` dir; schema is applied with `pnpm db:push`, so Vercel builds do not migrate — push schema changes manually before deploying. See [[apollonia-stack]] and [[apollonia-verification-scars]].
