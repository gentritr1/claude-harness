---
name: browser-pane-stale-screenshot
description: Browser pane screenshots can freeze on a stale composite frame while the DOM stays healthy
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bbb02cb4-bacc-420f-823a-32ec093c9721
  modified: 2026-07-19T10:21:32.966Z
---

During the 2026-07-19 Annex review, the in-app Browser pane's screenshot capture froze on one stale frame (page looked black with content ghosted at wrong positions) across multiple screenshots, resizes, and scrolls — while `read_page`, `javascript_tool`, and the console all showed a perfectly healthy page. A forced `navigate` reload fixed rendering. `zoom` region crop also returned the same stale full frame.

**Why:** trusting the screenshot alone would have produced a false "app is broken" verdict — the runtime truth (DOM/a11y tree) contradicted the pixels.

**How to apply:** when a Browser-pane screenshot looks catastrophically wrong, cross-check with `read_page` + a JS probe (scroll metrics, computed styles) before diagnosing an app bug; if DOM is healthy, treat it as a capture artifact, reload the tab, and drive verification through the accessibility tree instead of pixels. Never report a visual defect from a single frozen screenshot.
