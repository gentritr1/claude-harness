---
name: apollonia-brand-logo
description: "The owner's real logo (gold wordmark + Ionic column on a dark disc), how the transparent assets were derived, and where each size is used"
metadata: 
  node_type: memory
  type: project
  originSessionId: 933891dd-9679-4626-b65f-30d816eff62b
  modified: 2026-08-01T15:30:26.037Z
---

The venue's **real** logo arrived 2026-08-01 as `~/Desktop/apollonia-events-photos/apollonia-events-logo.jpeg` — 720×720 JPEG, gold serif "APOLLONIA" with an Ionic column standing in for the "I", "EVENTS" under a pediment, struck on a near-black disc with a gold rim, on a white square (no alpha).

Its gold samples `#997D56` at the ring, which already sits inside the site's `--color-gold: #a8854e` — the invented palette and the real mark agree, so no retuning was needed.

Assets were cut with Pillow in a scratchpad venv (no PIL/ImageMagick on this machine; `pip3 install` is blocked by PEP 668 — use `python3 -m venv`). Circle fit: threshold non-white, keep only rows/cols with >50 content pixels (kills JPEG speckle), giving centre (357, 356) r=348; alpha via a 4× supersampled ellipse inset 2px to bite off the JPEG fringe. **A naive "widest chord" fit put the centre 14px high and clipped the rim** — verify corner alpha == 0 and centre alpha == 255 before trusting the cut.

Shipped: `src/app/favicon.ico` (16/32/48, replaces the Next default), `src/app/icon.png` (256), `src/app/apple-icon.png` (180), `public/logo-badge-96.png` (header), `public/logo-badge-192.png` (footer), plus 512/1024 masters.

Usage: `src/components/brand/logo-badge.tsx` renders it `unoptimized` (see [[apollonia-verification-scars]] for why). The badge is paired with — never replaces — the typographic `<Logo />` wordmark in `src/components/brand/logo.tsx`, because below ~64px its lettering turns to mush; it carries `alt=""` so it doesn't double the brand name for screen readers. **Hidden below `sm` in the sticky header**: at 375px the badge+wordmark+Rezervo pill+burger leave only ~6px of clearance. It still shows in the mobile menu panel and the footer (72px, where "APOLLONIA" is legible).

**Venue reel (2026-08-01)**: `apollonia/reel/venue-reel.mp4` + `-vp9.webm` on Cloudinary is a 5s Higgsfield `kling3_0_turbo` image-to-video clip generated FROM the real room photo `u3dt0xmhzhfxck1xgael` (10 of 34 credits; 1080p cost 10, 720p 7.5). Rendered as a full-width band above the gallery section via `src/components/public/venue-reel.tsx`. The model returned 1764×1172 (source 3:2), NOT the requested 16:9 — check actual output dimensions rather than trusting the aspect_ratio param. Raw output was 6.1MB @10Mbps with an audio track; re-encoded locally with ffmpeg to 214KB mp4 / 128KB vp9 before upload. Never generate fake venue interiors — animating a real photo is the only honest use here.

**Uploaded 2026-08-01**: all 13 photos are live in `apollonia/gallery` with curated `sortOrder` 0-12 and hand-written Albanian alt text (they are all from the opening of the "Kujtesë e Vlerave Artistike" exhibition). Cloudinary was re-keyed that day — cloud name is now **`ejtikldj`** (Free plan), NOT the old `ds8jicms7`. Because the admin panel needs a login and I don't type passwords into forms, the upload ran server-side through the same path `addGalleryImage` uses (upload → `api.resource` for authoritative dimensions → `galleryImage.upsert`), which is the reusable route for bulk imports. **`/gallery` is a static (`○`) prerender**, so newly uploaded images do not appear on production until a redeploy or revalidation.

The 13 event photos in that same folder were downscaled to 2560px long edge (`sips --resampleHeightWidthMax 2560 --setProperty formatOptions 80` into `web/`), 149MB → 7.5MB — the originals were 26-30MP and 10 of 13 exceeded Cloudinary's 10MB free-tier upload cap. Upload them through `/admin/gallery`, never the Cloudinary console: the site reads the `GalleryImage` table, so a console upload creates no row and never appears. See [[apollonia-stack]].
