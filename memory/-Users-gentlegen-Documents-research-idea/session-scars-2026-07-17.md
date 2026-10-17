---
name: session-scars-2026-07-17
description: "Review gotchas from the drag/meta/assets session — synthetic drags, lift offset, clipboard verification, Recraft SVG pipeline."
metadata: 
  node_type: memory
  type: project
  originSessionId: 2b50cf8f-d345-445f-acf6-221a183ff5b7
---

Scars from the 2026-07-17 polish session (drag-to-place + daily meta + icons):

- **Synthetic browser drags lie.** The in-app browser's atomic `left_click_drag` collapses to a tap for PanResponder code (movement never registers) and can even text-select the page. Pattern → detection rule: never conclude "drag is broken" from one synthetic drag; verify with a dispatched JS event sequence (mousedown + ≥10 spaced mousemoves + mouseup, ~25ms apart) which exercises the real handler path. Also: `computer` coordinates are CSS viewport px (what ref-clicks report), NOT the 2× screenshot pixel space.
- **Drag lift offset moves the drop target.** Pieces float ~72px above the pointer and the snap follows the floated piece — aim drops ~72px BELOW the intended cell. Two "failed placements" in review were mis-aims (one was dragging an already-emptied tray slot). Confirm the piece/slot state before concluding a bug.
- **Clipboard success paths are verifiable.** Automated contexts deny clipboard-write, so agents can't see the success branch; stub `navigator.clipboard.writeText` with a resolving spy before clicking — this both captures the text and lets the "Copied" UI branch run.
- **Recraft V4.1 (model_type "vector") on Higgsfield returns real SVGs** — one 2.5-credit generation yields the whole icon set (adaptive foreground/monochrome/splash/favicon) via local edits + `rsvg-convert` (installed). nano_banana_pro failed instantly twice on this account (no charge).
- Icon source of truth: assets/images/icon-source.svg; store hero in assets/store/. Fills: blocks rgb(24,35,45), sage rgb(191,212,145), bg rgb(247,248,246).
- **Open verification gaps (device-only, still open as of 2026-07-17):** native touch drag (incl. drag-vs-ScrollView contention), animation frame feel, haptics, real share sheet on iOS/Android, new app icon rendering on device. Also user eyeball pending: cream-and-forest palette tension with PRODUCT.md anti-references.

Related: [[project-overview]], [[node-and-ports]].
