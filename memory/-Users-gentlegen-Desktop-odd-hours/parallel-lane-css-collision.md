---
name: parallel-lane-css-collision
description: Parallel UI lanes collided on global class names (.oh-*) — namespace shared primitives per owner
metadata: 
  node_type: memory
  type: project
  originSessionId: c0bff7d7-4d12-4eb5-addf-8dea9a66ddb9
  modified: 2026-08-16T11:01:41.807Z
---

Lanes C and D, working in disjoint FILES, still collided in the global CSS
namespace: both defined `.oh-btn`, `.oh-face*`, `.oh-panel*`, `.oh-stamp`;
import order silently decided which won. Lane C detected it visually and
namespaced shared primitives to `ohc-*`.

**Why:** file ownership does not partition global namespaces (CSS classes,
localStorage keys, route params, window events).

**How to apply:** future parallel-UI briefs must assign a class prefix per lane
(e.g. `ohc-` components, `oh-` table screen) up front, and the ownership doc
should list namespace ownership alongside file ownership.
