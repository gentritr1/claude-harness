---
name: higgsfield-asset-pipeline
description: Measured results of the 2026-09-05 Higgsfield vs GPT Image 2 test for FUTURISMA asset sheets, plus the image-to-3D-to-Blender path and its credit costs
metadata:
  type: project
---

Test on 2026-09-05 (16 credits total, balance 133 -> 117, starter plan). Files: `polarity_work/art/references/higgsfield-test/`.

- **Orthographic sheets with long count-heavy prompts:** `gpt_image_2` (1.5 cr, same model Codex's native image_gen uses) matched every count on the 46 m gantry; `flux_2` pro at 1k failed it outright (side = copy of front, top nonsense, no lamps/drum/ladder). FLUX.2 handled the simpler crusher sheet well. Rule: complex sheet -> gpt_image_2; simple prop or hero/concept -> flux_2 (1 cr, stronger painted PS2 look).
- **Concept/hero:** flux_2 gave the best Blastworks concept frame (stylised, readable countdown board); `soul_location` reads like a modern engine screenshot, not painted.
- **Image-to-3D:** `sam_3_3d` (1 cr) FAILS on grey-background ortho crops (no object detected) but works on a hero frame with a prompt naming the object; output is a normalised 1 m diorama mesh (24.5k tris, one baked texture, base slab included) = a reference maquette, not a game asset. `tripo_h3_1_image_to_3d` (9 cr, texture on, pbr off, face_limit 20000, orientation align_image) produced a clean single-object 15.6k-tri textured GLB from the ortho front crop. Meshy `image_to_3d` is 20 cr untextured / 30 textured, untested.
- **Blender path works end to end:** media_upload (presigned PUT + media_confirm) -> generate_3d -> curl the GLB -> `bpy.ops.import_scene.gltf` via the blender MCP (addon reports "outdated", fallbacks still work). Whole loop ~2 minutes.

**How to apply:** these lifts are reference maquettes for silhouette/proportion; the game asset is still rebuilt low-poly with the six painted atlases (see [[polarity-work-fork]]). Never ship a lifted mesh: wrong scale (normalised), one baked texture, no material roles, triangle counts 4-8x the budget.

**2026-09-09 corrections and additions (Dream Island kit, 15 images, 11.5 cr measured against the balance delta 72.48 -> 60.98):**
- **`gpt_image_2` costs 0.5 cr, not 1.5**, at the server defaults it applies when you omit them (`resolution: 1k`, `quality: low`). Quality was more than good enough for ortho model sheets and 16-cell sprite sheets. `flux_2` confirmed at 1.0 cr. Don't pay for `high` on a sheet without a reason.
- **The mirrored-quadrant sheet failure is beatable.** State the grid AND the total in words ("a 4 by 4 grid of SIXTEEN DIFFERENT single detached palm fronds"), add "each isolated in its own cell with clear empty grey space around it" and "no cell repeated, no mirrored duplicates". Held on all four multi-cell sheets.
- **The perspective failure that killed the 2026-09-03 ground tiles is beatable too**: "orthographic, camera pointing exactly perpendicular at the surface, absolutely zero perspective and no vanishing point" produced true flat-on stone swatches. Generated materials still come back photoreal-leaning and non-tiling — posterise and seam-check before use.
- **Ortho model sheets are the best value for handing 3D work to an implementer** (0.5 cr each): name all four views and their grid positions, "all four at exactly the same scale", "no ground plane, no dimension lines, no arrows, no text". Two came back buildable, including a through-tunnel drawn correctly in both front and back elevations. These beat a 9 cr Tripo maquette for modelling reference.
- **Unfixed drift:** flux_2 ignores "hover craft with NO wheels" roughly half the time. Never treat a generated frame as craft reference.
- `flux_2` returns 429 rate_limit_reached when more than ~6 jobs are submitted at once; resubmit the failed indices, they succeed immediately.
