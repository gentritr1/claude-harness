---
name: named-intent-vs-measured-value
description: "Assets and materials whose NAME states an intent their measured value does not carry — read runtime values, never the name or the manifest prose"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e5a4db00-7bc4-41ad-90f6-fbade73485ac
  modified: 2026-08-11T22:10:56.436Z
---

**Pattern:** an asset's name, its manifest row and its code comments all describe an intent the actual value does not carry. Reviewing by reading agrees with the name every time.

Three instances, all found 2026-08-11/12 by reading **runtime** values:

- `env-backdrop-a` — manifest: "rooftop cut-outs as painted flats … against the sky gradient". Runtime: **lit** MeshPhysicalMaterial, night-blue albedo (#232b3a/#2c3547), tops at 35.3°/32.9° elevation vs a frame ending near 25°. It was not painted, not a roofline, and it **was the sky** — it occluded the dome in every shot. Also value-inverted: the distant town was the darkest thing in frame.
- `src/play/assets.js` promised "the sky gradient" in a comment for several gates. `scene.background` was one flat hex. There was no gradient.
- `CobbleWarm` — the square's floor — measures **#3e4244, hue ≈ 200° (cyan-grey)**. Its sibling `CobbleSlate` #384848 is ≈180°. Neither is warm; `PlasterWarm` #cbb794 at ≈40° is. **Still open** — an authored fix, not a runtime one.

**Why:** these are invisible in a diff and invisible in review prose, because the prose is the thing that's wrong. Every one of them survived multiple gates that were all reading the same description.

**How to apply:**
1. For any art claim, read the **runtime** value — `__play.scene()` exists in `src/play/main.js` for exactly this. Traverse, print material colours, bounding boxes, and elevations from eye height.
2. Convert a colour claim to a **number**: hue in degrees, or the value against its neighbours. "warm" is falsifiable; "looks warm" is not.
3. Before believing an asset is far away or small, compute its **angular size from the player's eye**, not its metres. 25.8 m at 26 m radius is not a distant roofline.
4. Where a colour is derived from another colour, derive it in code from one table (the sky drives the backdrop now) so the two can never drift into disagreement.

Related: [[lighting-and-agx-facts]], [[cast-instancing-hazards]], [[art-direction-realized]].
