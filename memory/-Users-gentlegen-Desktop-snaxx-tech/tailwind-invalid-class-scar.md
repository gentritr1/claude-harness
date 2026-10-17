---
name: tailwind-invalid-class-scar
description: "Tailwind classes outside the configured scale (duration-800 etc.) silently generate nothing — verify motion timing in dist CSS / computed styles, never from class names."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a0526348-b91b-4181-a123-eb1a0c614fcf
  modified: 2026-07-22T19:19:08.099Z
---

Pattern: a Tailwind utility whose value isn't in the default scale or config (`duration-800`, `duration-400`, `duration-350`) compiles to NOTHING — no error, no warning — and the element silently falls back to the 150ms default baked into `transition-*` utilities. 14 call sites shipped this way; every "800ms cinematic reveal" actually ran at 150ms.

**Why:** class names look like working code; JIT only emits what matches a known scale. Reading TSX proves nothing about timing.

**How to apply:** any motion-timing claim must be verified against runtime truth: grep the generated class in `dist/assets/*.css` or read `getComputedStyle(el).transitionDuration` in the browser. When adding non-scale values, either extend the theme or use bracket syntax (`duration-[800ms]`). Detection sweep: `grep -roE 'duration-[0-9]+' src | sort -u` and diff against the config + default scale (75/100/150/200/300/500/700/1000).

Related: preview-pane screenshots in this project only render fixed-position elements (compositing bug) — DOM probes (`elementFromPoint`, computed styles) are the reliable runtime oracle; screenshots are not. See [[motion-round2-2026-07-22]].
