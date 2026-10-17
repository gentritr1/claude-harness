---
name: maplibre-page-css-and-repaint
description: "MapLibre 5.24 in the map WebViews: its CSS outranks the page's one-class rules; setPaintProperty fades 300 ms; load waits for tiles; headless Chrome needs SwiftShader for WebGL"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-16T23:37:44.984Z
---

Measured 2026-09-17 (E1b-2, art_v2 map repaint) on the generated pages in desktop Chrome, confirmed on the
Pixel_8_Pro AVD:

1. **Page CSS loses to MapLibre's.** The page `<style>` comes before the vendored maplibre-gl.css `<link>`, and
   MapLibre's rules are two-class (`.maplibregl-ctrl.maplibregl-ctrl-attrib`, the white `.maplibregl-compact`
   pill) or load later (`.maplibregl-ctrl-attrib a`). 1.4.0's one-class credit rules never applied (white pill,
   "Data from" in #cbd5e1 on white). Put page rules on the `#map` id selector. A CSS prototype appended at the
   end of <head> passes while the real page fails, so measure the generated page, not a prototype.
2. **`setPaintProperty` animates** over the style's default 300 ms (`transition` absent in the OpenFreeMap
   style): set `<property>-transition` to `{duration: 0, delay: 0}` first for an instant repaint.
3. **`load` fires after every visible tile has loaded**, so a repaint there leaves 7–14 frames in the old
   colours. `style.load` comes before the first frame.
4. **WebGL in headless Chrome:** `--disable-gpu` means no WebGL (the page falls into its map-error state). Use
   `--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader`; the canvas then DOES appear in
   screenshots. Measure per frame by wrapping `maplibregl.Map` from a preload script (a setter on
   `window.maplibregl`) and reading `map.style._layers[id].paint.get(prop)` on 'render'.

**How to apply:** any further map styling (E1b-3 result map, B1 reveal) must be verified on the generated page with
these instruments. Repainting only `background` leaves water and ice in the style's neutral greys (owner taste item).
Related: [[verify-webview-maps-without-a-device]], [[avd-stale-global-proxy]].
