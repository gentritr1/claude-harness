---
name: offday-landing
description: "Offday split to its own repo (SnaxxTech/offday, ~/Desktop/Projects/offday); landing page at /, app moved to /app — gotchas found building it"
metadata:
  node_type: memory
  type: project
  originSessionId: 337d83f0-e9b0-46f3-adab-bcee2054ca39
  modified: 2026-09-29T00:07:43.806Z
---

2026-09-29: Offday extracted from snaxx-tech `apps/offday` into github.com/SnaxxTech/offday (history kept via subtree split; CI at `.github/workflows/ci.yml`). Landing page added at `/`, app moved to `/app` — the landing page actually shipped via PR #1 (merged 2026-09-29 14:27, incl. dark theme); #2–#5 merged after. This session's PR #8 (same branch name, reused after #1's branch was deleted) is a stale duplicate built on an unfetched local main — closed 2026-09-29. PR screenshots live on the never-merged `pr-assets` branch, one folder per PR, linked by pinned commit SHA (#6 has a before/after set).

Gotchas:
- globals.css has a bare `main { padding: 38px }` rule — any new page using `<main>` inherits it (landing overrides via `.lp main`).
- globals.css reduced-motion block kills ALL animation/transition with `!important`, so page-level gentler reduced-motion fades never apply.
- Inline `<script>` in a server component triggers React 19 "script tag" + hydration warnings; use `<noscript><style>` fallback instead.
- Deep links: `/app?auth=login|register` open the dialogs; old `/?invite=` links redirect to `/app?invite=`.
- The browser-pane screenshot is too downscaled to judge detail and its zoom is unsupported; headless Playwright with `channel: "chrome"` (no bundled browsers installed) works for full-res shots.
- CI (`ci.yml`) only runs on push to main and on PRs — a pushed feature branch gets no CI until a PR is opened.
- `next/og` share images can't read woff2; load fontsource `.woff` files via fs in `app/opengraph-image.tsx`.
- Local `main` in ~/Desktop/Projects/offday was hours behind origin (several agents/sessions push here). ALWAYS `git fetch` and branch from `origin/main`, and check `gh pr list --state all` for existing work before opening a PR. → future briefs: "fetch + check open/merged PRs first".
- PR screenshots: never take an element screenshot mid-drag — Playwright scrolls the element into view with the mouse held, and the release lands on the wrong day (looked like a range-selection bug in #6; it wasn't).
- Disk hit 100% full mid-session (ENOSPC breaks every Bash call); freed space by deleting lockfile-backed node_modules only.

Related: [[hero-world-within-concept]]
