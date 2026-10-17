---
name: ci-build-only
description: Offday repo is private (billed CI minutes) — CI only type-checks and builds on PRs; the Playwright suite runs locally before every PR
metadata:
  type: feedback
---
The owner asked on 2026-10-04 that CI do only the build: "we are in a private repo… we can run locally and don't want to spend minutes". `.github/workflows/ci.yml` (PR SnaxxTech/offday#27) now runs `npm ci`, typecheck and `next build` on `pull_request` only, skips `**.md` and `docs/**`, and can be started by hand. It no longer runs on push to main or runs Playwright.

**Why:** a run was ~3.5 minutes (billed as 4), 2 of them tests, and each PR ran twice.

**How to apply:**
- Run `npm run build && CI=true npx playwright test -c playwright.chrome.config.ts` locally before every PR, and put the result in the PR body.
- "Merge when green" now means CI built AND the local full suite passed.
- Don't add test steps, matrices or push triggers back to CI without asking.
- The plan has no branch protection (403 on the API), so job names aren't required checks.

Related: [[undo-windows-and-side-effects]]
