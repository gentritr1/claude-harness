---
name: third-party-style-repaint-must-guard-each-call
description: ART-5m widened the basemap repaint from 11 to ~35 layers with only getLayer checks; one upstream layer-type change throws and kills the guess map
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-09T23:47:19.989Z
---

**What happened (2026-10-10).** ART-5m (map look A) repainted about 35 layers of OpenFreeMap's live dark style, guarded only by `map.getLayer`.
- The review served the same style with `building` changed to fill-extrusion.
- `setPaintProperty` then threw a TypeError in MapLibre 5.24.0, the guess page posted `error`, and the map-failed panel showed.
- Base survived the same style.
- Tests, gates and renders were all green, because they all used today's style.

**Pattern → detection rule → brief update.**
- **Pattern:** code that applies settings to a third-party resource we do not version (a live style, a remote config) fails as a whole when any one item changes upstream.
- **Detection rule:** guard each item (type check plus try/catch), and run a "hostile upstream" probe, a mutated copy of the resource served locally, in the review.
- **Brief update:** any brief that touches the `repaintBasemap` layer lists names that probe as an acceptance item.

Related: [[maplibre-page-css-and-repaint]], [[webviews-load-libs-from-unpkg]].

**Same unit, round 2 re-review (2026-10-10).**
- In MapLibre 5.24.0 a missing `['get', X]` inside text-field coerces to "", not null, so a `coalesce` fallback chain never reaches `name`.
- The test's hand-written evaluator returned null and "proved" the fallback. That is an oracle sharing the implementation's reading.
- **Rule:** prove any style expression with MapLibre's own `layer.layout.get(prop).evaluate(...)`, and use `case` + `has` rather than `coalesce` over `get`.

**Round 5 (Spain missing).**
- **Cause:** the flat 0.12 em letter-spacing widened SPAIN's collision box into ITALY's at the world view. Fixed with spacing that ramps up with zoom plus text-padding 0.
- **My mistake:** I wrote "every base label must still be drawn at 8 cameras" without measuring it first. Greedy label placement makes a strict superset unreachable once the text changes.
- **Rule:** for label sets, the target is "superset at the default camera, net gain elsewhere, plus a list of names that must show", measured on base first.
