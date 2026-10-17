---
name: apollonia-operations
description: Live URLs, health endpoint, monitoring, rate limiting and Sentry for the deployed Apollonia site
metadata:
  type: project
---

**The site went live 2026-08-01** at https://www.apolloniaevents.com (apex 308-redirects to `www` — always use `www`). Deployment Protection is off. `RUNBOOK.md` at the repo root is the full operational reference; keep it updated rather than duplicating it here.

Key facts that are easy to get wrong:

- **`/api/health`** returns 503 when Postgres is unreachable, 200 otherwise, plus `commit` so you can confirm which build is serving. `?token=<CRON_SECRET>` adds a config breakdown; it is withheld anonymously on purpose.
- **Never monitor `/` for uptime.** It is statically generated and returns 200 from the CDN even with the database completely down — which happened three times on 2026-08-01.
- **Rate limiting** is Postgres-backed (`RateLimitHit` table): reservations 5/hour/IP and 3/day/email, login 8/15min/email and 20/15min/IP. It **fails open** by design. Verified end to end — 12 failed logins recorded exactly 8 accepted hits.
- **Sentry** is wired (`apollonia-events`/`javascript-nextjs`). The wizard shipped demo routes into the production build and left `error.tsx` console-only, so route-level errors reached Sentry not at all — both fixed. `.env.sentry-build-plugin` holds the auth token and is gitignored.
- **`next.config.ts` caps `deviceSizes` at 2048.** Do not raise it: the gallery originals are 2560px, so a 3840 request makes Cloudinary upscale — slow on first derive and a wasted transformation credit. This was the cause of "images not loading" on retina.

See [[apollonia-neon-env]], [[apollonia-brand-logo]], [[apollonia-verification-scars]].
