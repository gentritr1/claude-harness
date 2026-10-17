---
name: art-asset-pipeline
description: "How FJALË's signature art was made (2026-07-19) and the gotchas for regenerating or extending it"
metadata: 
  node_type: memory
  type: project
  originSessionId: 65a98170-6072-4511-a581-c285d9d4d9cc
  modified: 2026-07-19T19:17:34.156Z
---

Signature art round (commit 08e5a03): besa-seal-v1.svg (result panel, only genuine no-hint DAILY Besa win), stamp-digraph-v1.svg (passport frame; letters stay live text in the app font — one asset serves all 9 digraphs), og-fjale-v2 (v1 layout + cream ground + cup accent; v1 files stay published for old shared links).

Pipeline that worked:
- **Higgsfield → Recraft V4.1, `model_type: "vector"` outputs TRUE SVG** (rawUrl is .svg). ~1.25 credits/image. Pass the app palette as `colors` hex array (amber #C9932F, deep #97671C, cream #F7E8C4, charcoal #211C15, green #417D4B — converted from styles.css OKLCH tokens).
- Generated SVGs: first `<path>` is always the background rect — strip it for transparency; classify remaining paths by bbox from `d` coordinates (regex min/max is enough) to remove letters etc.; trim viewBox to content bounds.
- **OG PNG render: headless real Chrome** — `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --screenshot=out.png --window-size=1200,630 file://…svg`. Exact pixels, system fonts correct.
- **NEVER relay base64/binary through model context** (browser canvas → chunked toDataURL): I fabricated a corrupt chunk attempting it. Files must move via disk/CLI only.

Integration checklist for any new static asset (all enforced by "keeps the signature art wired end to end" in tests/launch.test.js):
1. server.mjs `publicPaths` (dev server 404s anything unlisted), 2. service-worker APP_SHELL + CACHE_FIRST_ASSETS (versioned filename!) + cache bump, 3. vercel.json immutable-cache header rule.

**Editing the JSON-LD in index.html (e.g. og image URL) breaks the CSP `script-src` sha256 pinned in BOTH vercel.json and server.mjs** — recompute with the same regex the test uses. Page CSP has `img-src 'self' data:` — blob: URLs are blocked in-page.

Round 2 (commit dc4a847) — help-hero-v1.svg (Si luhet banner) + manifest install screenshots. Extra lessons:
- **Generated illustrations miscount objects** (asked for 5 tiles, got 6 in the prettier variant). Recraft's charcoal linework is ONE continuous compound path — subpath surgery to delete an object is infeasible (produces orphan blobs). Winning move: pick the variant with the correct COUNT and fix its palette by per-path-index fill overrides (deterministic, free).
- Manifest screenshots: puppeteer-core (scratchpad npm i, drives installed Chrome) with `emulateMediaFeatures prefers-color-scheme light` + setViewport dpr 2 — plain `--headless --screenshot` follows macOS dark mode and clips mobile layouts with `--force-device-scale-factor`.
- Fixed-cream panel (`background:#f7e8c4` hard-coded) is the established pattern for art that must read identically in both themes (stamps, help hero).

Deliberately NOT done (roadmap "refine, never redesign", no folklore/eagle): logo/wordmark, favicon/app icons, rare-letter side-card chips (25px tall — stamp frame illegible there). See [[product-roadmap]], [[hint-attempt-design]].
