---
name: browser-pane-screenshot-freeze
description: Claude Browser pane screenshots freeze/black out after any scroll — workaround via cross-origin nav + wait + body transform
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1a52912a-3b91-4a3f-b763-394d74765783
---

The in-app Browser pane (mcp__Claude_Browser) screencast freezes after any scroll (JS or `computer scroll`): screenshots return solid black/blank frames even though the DOM is fine, on any site (observed on casenovapremium.live and a local prototype, 2026-07-11). `location.reload()` does NOT recover it.

**Why:** compositor stops pushing frames to the capture; DOM/JS keep working.

**How to apply:**
- Recover fresh frames: navigate to a different origin (e.g. example.com) and back, then use `computer wait` 2–3s before screenshot (wait forces a frame push; screenshot alone returns stale frames).
- To "scroll" for screenshots without triggering the freeze: `document.body.style.transform='translateY(-Npx)'` instead of scrolling; reset with `''` before testing fixed/sticky elements.
- Verify behavior (classes, computed styles, layout) via javascript_tool — trust DOM state over frozen frames; screenshots only prove visuals after a fresh nav.
- `scrollIntoView` with `html{scroll-behavior:smooth}` gets interrupted in the pane — use `scrollTo({behavior:'instant'})`.
