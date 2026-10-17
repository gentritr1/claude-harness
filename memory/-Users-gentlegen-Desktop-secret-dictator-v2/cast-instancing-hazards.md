# Instancing a cast from a shared cache (2026-08-09, Gate 3 citizens)

Four `chr-citizen-*` GLBs replaced the bot capsules in play.html. Scars worth
keeping:

## Shared geometry turns a correct teardown into a fatal one

`clearCast()` disposed every geometry and material it could reach. Correct while
each capsule built its own; **fatal the moment the geometry lives in a cache and
is shared by several seats and every future deal** — the second Restart renders
an empty square, which looks exactly like a loader failure and is not.

- **Detection rule:** when a build step moves from per-instance to cached/shared
  resources, audit every `.dispose()` in the same breath. Each instance must
  record what it *made* and free only that.
- **Test that would have caught it:** N restarts with `renderer.info.memory`
  read back. 35 restarts held at 35 geometries / 72 calls.

## Grey-when-dead needs a per-seat material clone

The merged material is in the cache. Writing to it greys every citizen of that
variant at once. Clone per seat (≤2 per seat), write to the clone, and restore
the **authored** colour on revive, not a constant. The pipeline's own words: the
cache owns shared resources; a cast member must not recolour a shared material.

## Merge per material at load, or blow the draw-call budget

8 `VIS_*` meshes × 10 seats = 80 calls against a `<100` whole-scene target.
Merging per material into the cache: 10 seats → 77 total calls, 21 456 tris.
`mergeGeometries` refuses mismatched attributes — normalise to the intersection
(keep `uv` only if every piece has one). Same seam that bit the Gate 2 collider
harvest.

## Numbers must come off the asset

- Nameplate = `SOCKET_label` (1.62 / 1.80 / 1.95 / 2.15 across four figures) —
  one hardcoded height floats over the short one and sits inside the tall one's
  hat.
- Topple lift = the asset's own `bounds.max.z`. Rotating −90° about X maps +Y to
  +Z, so the former **depth** holds the body off the floor: 0.239 (tall) vs
  0.499 (hunched, which leans 0.50 m forward of its feet).
- Facing needed **no** correction: `lookAt` points +Z at the target and the
  World contract makes +Z the front. Verified as dot product = 1, not by eye.

## Test checks a generic sweep would miss

- **Feet, not bounding box.** `chr-citizen-hunched`'s bbox centre is `z=0.159`
  by design; assert the centre of the vertices within 5 cm of the ground.
- **Assert the ABSENCE of `COL_`** on a decorative asset: the runtime harvests
  none, so a collider would be invisible dead weight in every copy.
- **One bad file must cost one variant** — a whole-cast failure cannot
  demonstrate per-row independence.

## Comment literals break grep gates

Writing `G.rng()` in a *comment* in `src/play/assets.js` failed the project's
`grep -rn "rng(\|Math.random" src/play/` gate. Third time this family has bitten
(also `Math.random` and `eventLog` in Gate 3 comments). **Never write a banned
token in prose inside a file the gate greps** — describe it instead ("the engine
stream", "the platform's generator").
