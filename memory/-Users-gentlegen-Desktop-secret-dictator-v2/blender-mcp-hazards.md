---
name: blender-mcp-hazards
description: "Blender-via-MCP scars — transform_apply bakes location in this build, review renders are the real validator, socket restarts"
metadata: 
  node_type: memory
  type: project
  originSessionId: e5a4db00-7bc4-41ad-90f6-fbade73485ac
  modified: 2026-08-09T16:07:47.067Z
---

Scars from driving Blender 5.2 over MCP on env-dais-a (2026-08-09):

1. **`transform_apply(scale=True)` baked LOCATION into vertex data too** (objects created via `primitive_cube_add(location=…)` ended with origin at world zero and world-space geometry). An object handled differently (the lectern desk kept object-level location + rotation) then got double-transformed and rotated around world origin — it rendered floating twice in a row while `matrix_world` read "correct". **How to apply:** after any scripted build, print `matrix_world.translation` for every object AND eyeball a render — node-side GLB validation (names/bounds/materials) cannot catch a part floating inside the overall bounds. Prefer baking all geometry to world space consistently (origin at root) for static environment pieces.

2. **The review render is the real validator.** Two defects (floating desk, then the same defect worse) were only visible in renders; every headless check stayed green. Fixed-camera captures per stage are not bureaucracy.

3. **The addon socket dies when Blender closes.** Relaunch: `open -a Blender --args --python-expr "import bpy; bpy.ops.blendermcp.start_server()"`, then wait ~15-25s before probing port 9876 (first probe right after launch fails).

4. Blender writes `.blend1` backups next to the source — gitignored (commit 5daf918). Purge orphaned datablocks before export or old names collide into `.001` suffixes, which the pipeline treats as a review failure.
