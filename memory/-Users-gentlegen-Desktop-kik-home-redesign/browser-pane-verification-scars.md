---
name: browser-pane-verification-scars
description: Browser pane tooling failure modes hit in this project and the workarounds that verify truthfully
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0157fad9-ce3b-44e7-ad02-c9c9f0325873
---

Two pane failure modes observed 2026-07-12 (both on live kik-home.com AND local prototype, so they are pane bugs, not site bugs):
1. Coordinate `computer` clicks can silently not reach the page (no error, no effect) — almost reported "add-to-cart gives no feedback" as a site defect when the button worked fine.
2. Screenshots render blank/background-only after any scroll (scrollY>0); DOM geometry stays sane.

**Why:** both produce false findings — one invents a bug, the other hides real content.
**How to apply:** verify interactions via `javascript_tool` (dispatch real .click(), read localStorage/DOM state) before reporting a UI defect; for full-page visuals, resize viewport very tall (e.g. 1280×5200) + fresh `navigate` and screenshot at scrollY=0 — this captures the whole page in one shot. Also: after editing a served HTML file, `navigate` may serve a stale cached copy — cache-bust with `?v=N` before re-verifying, or you'll test old code (hit this once: fix looked ineffective but the page was stale).
