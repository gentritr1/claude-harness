---
name: snaxxtech-hosting-and-app-ads
description: Site is Vercel at snaxxtech.com (apex 308s to www); static public/ files bypass the SPA rewrite — verified; app-ads.txt is live with pub-9813131856455133
metadata: 
  node_type: memory
  type: project
  originSessionId: b62b1de2-f7a8-4456-9ed0-e02fe8e3cc49
  modified: 2026-08-06T22:51:32.207Z
---

Hosting facts (verified 2026-07-27 by curl against production):

- The site is on **Vercel**, live at **snaxxtech.com** — and `https://snaxxtech.com/...` returns **HTTP 308 to `https://www.snaxxtech.com/...`**. The apex is not the primary domain. The deployment also answers on snaxx-tech.vercel.app (that host is in the og:image URLs in index.html).
- `vercel.json` has a catch-all rewrite `/(.*)` → `/index.html`. **Static files in `public/` still win** — verified: `/favicon.svg` → `image/svg+xml` 200, `/images/app-block-destroy.webp` → `image/webp` 200, while a *missing* path like `/images/app-rowflare.webp` returns `text/html` 200 (the SPA shell). So a real file at `public/app-ads.txt` serves as plain text; a missing one silently returns the HTML app shell with a 200, which is the exact app-ads.txt failure mode Google reports as invalid.
- `X-Frame-Options: DENY` is set, so **same-origin iframes do not work on production** — the iframe trick for batch-checking many routes works on the dev server only. On production, navigate per URL and read the DOM.
- Deploys are automatic on push to main. To confirm a deploy landed, compare the `assets/index-<hash>.js` in the live HTML against `dist/assets/` from a local `npm run build` — polling that hash is reliable; polling page text is not (content renders client-side).

**Caching (audited 2026-08-07):** `vercel.json` header rules — `/assets/*` and `/fonts/*` 1yr immutable, `/images/*` 30d+SWR, `/videos/*` 1yr immutable (added this date; `/videos/*` previously had **no rule**, so the 6MB hero revalidated on every visit). The hero video filename carries a content hash (`almanac-e.99b1c015.mp4`) to make immutable safe — **regenerating the video MUST update the hash in `src/config.ts`**. `vercel.json` is JSON-schema-validated: do NOT add `comment` keys to header objects, it can fail the deploy. Deploy is ~9.5MB after trimming unused clips (was 28MB). This is a static Vite SPA — no functions, middleware, or image optimizer, so Next.js-specific Vercel advice doesn't apply.

**Why:** app-ads.txt must be plain text, HTTP 200, at the exact root domain in the store listing. Both the SPA-rewrite fallback and the apex→www redirect can silently invalidate it.

**Status 2026-07-27:** `public/app-ads.txt` is live — `google.com, pub-9813131856455133, DIRECT, f08c47fec0942fa0`. Verified: `www.snaxxtech.com/app-ads.txt` → 200, `text/plain`, **0 redirects**; the apex serves the same body but with **1 redirect** (308 → www).

**Publisher ID derivation:** the user supplied the AdMob **App ID** `ca-app-pub-9813131856455133~1700371697`. The app-ads.txt publisher ID is the `pub-<16 digits>` segment; the `~<app>` suffix is app-specific and must never appear in the file. `f08c47fec0942fa0` is Google's standard TAG ID, not a per-account value.

**How to apply:** if the Play listing's website field is the bare apex and Google rejects the redirect, make the apex primary in Vercel domain settings (dashboard-only, user must do it) or point the listing at `www.snaxxtech.com`. Google re-crawls periodically and the seller list changes — never delete this file, and re-check it after any hosting change. See [[block-destroy-legal-2026-07-27]].
