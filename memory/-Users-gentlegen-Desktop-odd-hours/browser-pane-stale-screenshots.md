---
name: browser-pane-stale-screenshots
description: Browser pane screenshots can lag one frame — verify via read_page/JS before judging state
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c0bff7d7-4d12-4eb5-addf-8dea9a66ddb9
  modified: 2026-08-16T11:01:33.758Z
---

While live-testing this app, `computer{action:"screenshot"}` in the Browser
pane repeatedly returned a frame from BEFORE the last interaction (looked like
"click did nothing"), while `read_page` / `javascript_tool` showed the updated
DOM. Nearly misdiagnosed a working guided-mode flow as broken.

**Why:** screenshot pipeline latency vs. instant DOM reads.

**How to apply:** after an interaction, verify state with `read_page` or a
small `javascript_tool` DOM probe (aria-live text, headings) before concluding
a click failed; treat screenshots as illustration, not ground truth. Related:
[[port-env-collision]] produced real silent failures with the same "nothing
happened" look — distinguish the two by checking server logs.
