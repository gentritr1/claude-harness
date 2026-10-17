---
name: verifying-motion-locally
description: How to verify animations in Offday — the browser pane cannot, use Playwright with the installed Chrome
metadata:
  type: project
---

Motion in Offday cannot be verified in the Claude browser pane when the pane is hidden: `document.visibilityState` is `hidden`, `requestAnimationFrame` never fires, and a rAF-based sampler just times out (2026-09-30).

**Why:** Playwright's own Chromium is not downloaded on this machine (`npm test` fails with "Executable doesn't exist"), but Google Chrome is installed.

**How to apply:**
- Run tests or probes with `channel: "chrome"` (a temporary config spreading `playwright.config.ts` plus `use.channel`, deleted afterwards) instead of downloading a browser.
- Sample frames with rAF inside `page.evaluate`; use `page.mouse.click` for pointer paths — `el.click()` has `detail === 0`, which the help tour treats as a keyboard step and skips the bubble arrival.
- When sampling something that follows scroll, read from a rAF queued by a scroll listener added after the component's own, and confirm `scrollY` actually changed first. A React `setState` inside rAF commits after the frame (one-frame trail) unless wrapped in `flushSync`.

2026-10-04: when the browser pane is hidden, its clicks fail too ("not compositing frames"), not just rAF. Drive manual regression passes with a throwaway Playwright script on `channel: "chrome"` against the dev server instead; give every run unique names/emails, because earlier runs' rows stay in data/offday.db and make locators ambiguous.
