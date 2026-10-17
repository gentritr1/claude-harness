---
name: annex-mvp-shipping-backlog
description: Website-shipping hygiene backlog from the game-engine skill gap analysis (2026-07-19)
metadata: 
  node_type: memory
  type: project
  originSessionId: bbb02cb4-bacc-420f-823a-32ec093c9721
  modified: 2026-07-19T12:17:42.476Z
---

**UPDATE 2026-07-19 (evening): items 1, 3, 4 DONE + review-verified** (Opus executor): PNG moved to docs/assets/civic-archive-original.png (provenance preserved, PROVENANCE.md updated), styles.css WebP-only (hero verified rendering live), og/twitter meta + og-card.jpg 1200×630 + apple-touch-icon + favicon-32 + robots.txt + LCP preload in index.html. dist now 568 KB (was ~2.5 MB). Item 2 (Vite base) N/A — hosting is Vercel root domain. **Still open:** og:url TODO comment in index.html (fill when Vercel domain exists), cross-browser matrix (item 5), save-migration design note (item 6), optional audio/PWA. Repo still has ZERO git commits.

From the github/awesome-copilot game-engine skill analysis (Opus executor, 2026-07-19; skill installed at .claude/skills/game-engine). Architecture verdict: the project already follows all portable engine principles (modularity, data-driven content, deterministic reducer, serializable event log, FSM phases, versioned validated saves); ~70% of the skill (loops/physics/collision/sprites/WebGL/gamepad/multiplayer/monetization) is correctly NOT applicable to a turn-based reducer game — reject, don't retrofit. Remaining gaps are web-shipping hygiene, not engine design:

1. **1.9 MB PNG ships in deploy** (VERIFIED: dist/images/civic-archive.png = 1,944,753 B beside the 98 KB WebP). Drop the PNG fallback from the three image-set() blocks in styles.css (~283, ~731, ~991) or re-encode to ~200 KB. ~0.5h.
2. **No Vite `base`** (VERIFIED: vite.config.ts has none) — hard 404s on subpath hosts like GitHub Pages project sites. Set before deploy.
3. **Zero OG/Twitter meta** (VERIFIED: grep = 0 in index.html), SVG-only favicon, no apple-touch-icon/robots.txt. Add og-image (reuse WebP hero ~1200×630). ~1-2h.
4. **No LCP preload** for the hero WebP; confirm host Brotli. 249 KB JS (77 KB gz) needs NO code-splitting — don't add manualChunks.
5. **Cross-browser matrix undocumented**; specific risks: heavy oklch() (~93% support) and image-set() fallback behavior on older Safari. ~2-3h manual.
6. **Save-migration note**: decodeGameState hard-rejects schemaVersion !== 1 (persistence.ts:170) — before case #2 or any schema change, write the migration branch or every save silently drops. Design note now, not code.

Optional (genre-fit, not blockers): quiet ambient audio + UI SFX (autoplay-unlock via first click, default-off toggle mirroring reducedMotion pattern — needs owner's ear, it's a juice task); PWA/installability via vite-plugin-pwa (game is ideal candidate: static, local-first). Fullscreen API: rejected, low value for reading UI. Distribution: itch.io + GitHub Pages fit; arcade ad portals (Poki/CrazyGames) do not. See [[annex-mvp-verified-state]], [[annex-mvp-next-features]].
