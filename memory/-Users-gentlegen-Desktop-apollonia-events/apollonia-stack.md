---
name: apollonia-stack
description: Confirmed stack and architecture decisions for the Apollonia Events reservation site
metadata: 
  node_type: memory
  type: project
  originSessionId: 20921973-35dd-49e8-a651-efd709be5e50
---

Apollonia Events — premium event reservation site (Next.js). Greenfield as of 2026-06-28.
Repo: github.com/gentritr1/apollonia-events (public, SSH remote, branch `main`).

Confirmed decisions (user picked, 2026-06-28):
- **DB host:** Neon (serverless Postgres). No local Postgres/Docker on the machine. Connection string needed at M2.
- **ORM:** Prisma.
- **Admin auth:** Auth.js (NextAuth) credentials, email+password, sessions in own DB.
- **Booking flow:** Request → admin approves. Reservations land as PENDING, admin confirms/declines.
- **Package manager:** pnpm 8. Node 20.

Build is milestone-by-milestone, commit each: M0 scaffold+design tokens, M1 public shell,
M2 db+reservation form, M3 admin auth+list, M4 calendar+manual+dashboard, M5 email reminders.
See [[apollonia-design-direction]].

Progress:
- M0 DONE: Next 16 + Tailwind v4 (CSS-first @theme, no tailwind.config) + shadcn/ui.
  Cormorant Garamond (serif) + Inter (sans). Logo wordmark = "apolloniaevents" with the
  "i" as a fluted temple column (src/components/brand/logo.tsx).
- M1 DONE: shadcn tokens remapped to Apollonia palette in globals.css; SiteHeader/SiteFooter;
  (public) route group; Home/Venue/Events/Gallery pages + /reserve placeholder.
  Content lives in src/lib/content.ts; placeholder visuals via GalleryTile (tonal gradients,
  swap in real <Image> later).
- M2 DONE: Prisma 6 (NOT 7 — v7 moved URLs to prisma.config.ts + driver adapters, too much
  churn). Neon connected via .env (DATABASE_URL pooled + DIRECT_URL non-pooled, derived by
  dropping "-pooler"). Reservation model + status/source enums; schema via `prisma db push`
  (no migrations dir yet). Client singleton src/lib/db.ts. createReservation server action
  (src/server/reservations.ts) writes PENDING. Form: react-hook-form + zodResolver, calendar
  date picker, time/occasion selects (src/components/public/reservation-form.tsx).
  IMPORTANT version pins: zod pinned to ~4.0 (4.0.17) because @hookform/resolvers@5.4 types
  require zod minor 0 — do NOT bump zod to 4.4 without bumping resolvers. guestCount validated
  as numeric string then Number()-converted in the action (avoids RHF input/output type split).
  Verified end-to-end: a test reservation (Elena Marlowe) persisted to Neon and remains in DB.
- M3 DONE (implemented by Codex, reviewed by Claude; branch m3-admin pushed): Auth.js v5
  credentials + JWT; edge-safe src/auth.config.ts + Node src/auth.ts; login page; admin shell +
  reservations table w/ status filter; updateReservationStatus action (auth-guarded). User model +
  bcrypt seed from ADMIN_EMAIL/ADMIN_PASSWORD. .env has AUTH_SECRET/ADMIN_* (gitignored).
- WORKFLOW (user's instruction): from M3 on, CODEX implements via prompts Claude writes; Claude
  reviews Codex's diffs. Claude does NOT implement features directly anymore.
- GOTCHA — Next 16 renamed Middleware → **Proxy**: file is src/proxy.ts (default export +
  `export const config = { matcher }`), NOT middleware.ts. Confirmed in
  node_modules/next/dist/docs/01-app/01-getting-started/16-proxy.md.
- GOTCHA — the machine's nvm default kept drifting to **node v14.19.3**, which can't run Next 16
  (breaks pnpm/corepack with `??=`, breaks Turbopack PostCSS worker). Claude reset it via
  `nvm alias default v20.19.4`. The Claude Preview sandbox pins an old node and ignores launch.json
  `env` — so live preview screenshots of this project may fail; rely on `next build` + Codex's
  browser verification instead. Build cleanly with v20: prepend
  /Users/gentlegen/.nvm/versions/node/v20.19.4/bin to PATH.
- M4 DONE (Codex impl, Claude review; branch m4-admin-calendar pushed, based on m3-admin):
  /admin dashboard (counts, upcoming/recent), /admin/calendar (UTC-safe month grid, nav, per-day
  chips + details dialog + per-day new-reservation prefill), manual reservation dialog +
  createManualReservation action (source MANUAL, choosable status, auth-guarded). Shared admin
  helpers in src/lib/admin/reservations.ts; manualReservationSchema extends the public schema.
- BRANCH STATE: feature branches stacked on main, NOT yet merged: main → (M3) m3-admin →
  (M4) m4-admin-calendar. Each pushed. Consider merging the stack to main at some point.
- MERGED TO MAIN: M3 (+review fixes, cherry-picked) and M4 are on origin/main (fa829e9).
  Branches m3-admin and m4-admin-calendar deleted (local+remote).
- M5 DONE (Codex impl, Claude review; branch m5-emails pushed, based on merged main): Resend
  transactional emails (fail-safe client, escaped HTML templates, guest receipt/confirm/decline +
  admin alert) and reminder cron (ReminderLog model, /api/cron/reminders bearer-auth, UTC windows,
  idempotent, daily vercel.json). Claude review fixes: replyTo (Resend v6 field; reply_to was
  silently dropped) and ADMIN-role gate on createManualReservation. NOT yet merged to main.
- KNOWN ISSUE (pre-existing from M4, now on main): lint fails react-hooks/set-state-in-effect in
  src/components/admin/manual-reservation-dialog.tsx. Build passes; lint advisory only. Unfixed.
- M5 MERGED to main (origin/main 5b6fe63 = all of M0–M5). m5-emails branch now == main (deletable).
- M6 DONE (Codex impl, Claude review — clean pass, NO fixes needed; branch m6-gallery pushed, based
  on main, ff-able, NOT yet merged): Cloudinary gallery. GalleryImage model; admin /admin/gallery
  (signed upload via next-cloudinary CldUploadWidget, list/edit/delete); admin-gated signature route
  /api/admin/cloudinary-sign (folder-enforced, param allowlist); src/server/gallery.ts actions
  (ADMIN-gated, re-fetch metadata from Cloudinary, delete asset before DB row); public /gallery + home
  use CldImage with placeholder fallback when empty. Secret stays server-side (only cloud name is
  NEXT_PUBLIC). Also fixed the pre-existing manual-reservation-dialog lint issue.
- DEPLOY NOTES: real email needs RESEND_API_KEY + verified Resend domain (or
  EMAIL_FROM="Apollonia <onboarding@resend.dev>", owner-only); Vercel cron needs CRON_SECRET in env.
  Gallery needs CLOUDINARY_CLOUD_NAME, NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY,
  CLOUDINARY_API_SECRET (+ optional CLOUDINARY_UPLOAD_FOLDER). All 6 milestones built.
- CONCURRENCY LESSON: Codex once wrote M5 into the main checkout while Claude did git surgery there
  — collision. Have Codex use a separate worktree (/private/tmp/...) per task to avoid this.
