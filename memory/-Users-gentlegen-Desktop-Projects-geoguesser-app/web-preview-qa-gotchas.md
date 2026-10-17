---
name: web-preview-qa-gotchas
description: "Expo-web QA traps seen 2026-09-07 — RN Modal fade looks like broken opacity for seconds after load; browser clicks time out when the pane is covered, drive via JS instead"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8cc01d9f-953c-4c68-8443-67b91ef3a0c2
  modified: 2026-09-07T21:38:09.419Z
---

Two things that nearly produced wrong verdicts while QA-ing the HowToPlay modal
on expo web (390×844 emulation):

1. **RN-web `Modal animationType="fade"` on first load** rendered the card at
   ~15% opacity in a screenshot taken 8 s after navigate; 2 s later it was
   fully opaque. Not a bug — the fade starts late while the bundle settles.
   Always take a second screenshot before diagnosing opacity/transform issues
   (computed style walk confirmed opacity 1, transform identity).
2. **`computer left_click` timed out (30 s)** repeatedly because the Claude
   window was covered. Dispatching `pointerdown/mousedown/pointerup/mouseup/click`
   MouseEvents on the RN-web `[role="button"]` element from `javascript_tool`
   works for Pressable and lets a whole flow (Next → Next → Start) run in one
   exec with `await sleep()` between steps.

The store harness from [[seed-store-from-browser-for-visual-qa]] now also
covers `usePlayerStore` (`globalThis.__playerStore`) — seed `gamesCompleted`
to test review timing; `lastReviewPromptAt` gets set ~1.6 s after the count-up
settles even on web, where the dialog itself never shows.

**Why:** both traps make working code look broken; the first would have sent
me hunting a reanimated web bug.

**How to apply:** screenshot twice, click via JS when the pane is hidden, and
remember the harness lines must be stripped before commit (tsc + grep).
