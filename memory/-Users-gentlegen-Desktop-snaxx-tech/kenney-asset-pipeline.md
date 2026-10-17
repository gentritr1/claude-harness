---
name: kenney-asset-pipeline
description: Kenney CC0 kits and the proven Godot GLB→sprite render pipeline shared by battleship and merge-kit.
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6cebbdce-da03-4c9c-a4e7-e3084ee9d5ce
  modified: 2026-07-28T22:07:35.354Z
---

Kenney (kenney.nl) packs are **CC0** — commercial use, no attribution required. Two repos now
consume them, and both use the same containment contract: the `.glb` files are **never
imported** into the Godot project; a `SceneTree` script loads them with `GLTFDocument` from an
absolute path outside `res://` and only the rendered PNGs are committed.

- `~/Desktop/battleship` — Kenney **Watercraft Kit 2.1**, top-down ship sprites.
  Tool: `tools/render_watercraft_sprites.gd` (575 lines, the original).
- `~/Desktop/merge-kit` — Kenney **Food Kit 2.0**, 12-tier dessert ladder for the cakes theme.
  Tool: `tools/kenney-food-render/render_food_sprites.gd` (3/4 view) +
  `render_ladder_preview.gd` (true-scale eyeball artifact). Added 2026-07-29.

Gotchas that cost time and will again:

- **`--headless` produces no pixels** (dummy renderer). These tools must run windowed or they
  silently emit empty images. Both scripts hard-fail on `DisplayServer.get_name() == "headless"`.
- Kenney's bundled `Previews/` are **64×64 thumbnails** — never usable as game art. Render the
  GLBs yourself.
- Food Kit textures live at `Models/GLB format/Textures/colormap.png`, not `Models/Textures/`.
- Every output must be gated on non-empty alpha bounds, ≥2% opaque coverage, and four
  transparent corners — that check is what catches a silently-black render.

Kenney's own kits share one tan/orange colormap, so a food/dessert ladder cannot be made
globally colour-distinct. Design for **adjacent-tier** distinction only, and let silhouette
carry the rest. See [[merge-kit-cakes-theme]].
