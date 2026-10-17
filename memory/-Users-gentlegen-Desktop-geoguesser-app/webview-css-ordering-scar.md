---
name: webview-css-ordering-scar
description: "Leaflet.css overrode the app's dark .leaflet-container background — style order, not zoom, was the cause"
metadata: 
  node_type: memory
  type: project
  originSessionId: a067363c-ba38-4d38-8a74-8d9d95ca553e
  modified: 2026-08-08T13:42:52.205Z
---

The "white/gray background on deep map zoom-out" bug (visible again on the result map, fixed 2026-08-08 in v1.2.2) was a CSS ordering issue: `webviewHtml.ts` emits its `<style>` block *before* the leaflet.css `<link>`, so leaflet's own `.leaflet-container { background: #ddd }` won the same-specificity tie. The 1.2.1 "fix" (minZoom: 1) only shrank the band — symptom, not cause. Real fix: background lives on the `#map` / `#pano` id selector, which outranks class rules regardless of order.

**Why:** classic treat-the-symptom trap; the bug "came back" because it was never gone.
**How to apply:** any new rule in `baseHead()` that must beat leaflet/mapillary CSS needs id-level specificity (or move the style after the links). When a "fixed" visual bug reappears in a different spot, re-derive the root cause instead of re-applying the old mitigation.
