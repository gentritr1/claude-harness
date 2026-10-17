---
name: sprite-generation-pipeline
description: How to add item sprites that match the set — Higgsfield recipe + remove_background + crop/pad/resize 256 + wire registry. Signature-item art done (1b3be87).
metadata: 
  node_type: memory
  type: reference
  originSessionId: a55d034b-799c-4add-95d3-38f4c5c38f10
---

**Adding item sprites (proven `1b3be87`, 2026-07-08 — the 5 Phase-2c signature items).**
Recipe is locked in [assets/art-status.md](assets/art-status.md); the 36-item set is transparent 256×256
RGBA, style-anchored to `shop-cat.png` (warm gouache, brown wobble outline, golden-hour light from
upper-left, cream field pre-removal).

**Pipeline:**
1. **Generate** via Higgsfield MCP `generate_image`, model `nano_banana_2`, `aspect_ratio "1:1"`
   (server ran it as `nano_banana_flash`, 1024², ~1.5 cr). Prompt = the locked template in art-status.md
   with `[SUBJECT]` swapped. Poll with `job_display`; download `results.rawUrl`.
2. **Transparency** via `remove_background` (media_id = the generation job_id, media_type image) — matches
   the set (existing sprites have corner alpha 0). It even preserved a glass-dome cloche correctly.
3. **Frame to match** (local Python/PIL): crop to alpha bbox → paste centered on a transparent square
   sized so `max(content)/side ≈ 0.76` (existing set fills ~0.68–0.79) → resize 256×256 LANCZOS.
4. **Wire**: add `require()` line to [src/juice/sprites.ts](src/juice/sprites.ts) `ITEM_SPRITES` keyed by
   **itemId** (spriteFor looks up by item id — the placeholder bug was that signature item ids weren't
   keys), and mirror into [assets/sprites/manifest.json](assets/sprites/manifest.json).
5. **Verify**: relaunch the sim (Metro re-bundles new assets on reload) + seed a shop with the items.

**Gotchas:** make each new sprite visually distinct from any look-alike existing item (there are BOTH a
regular `golden-scale` item and the signature `brass-scale`; `maneki-neko` white vs `lucky-cat` gold).
Purely additive (UI only) — no determinism/test impact. Generating images spends the user's Higgsfield
credits — only do it when they ask (they did). See [[art-chrome]], [[lane-b-signposting]].
