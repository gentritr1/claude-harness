---
name: three-composer-clear-colour
description: "three.js r186 + EffectComposer/OutputPass: renderer.setClearColor dark hex reads grey (double sRGB); use scene.background"
metadata:
  node_type: memory
  type: project
  originSessionId: 71d00c39-45c1-490a-8542-7433d53286cb
  modified: 2026-10-10T21:36:50.621Z
---

In `src/drafts/event-horizon` (three 0.186, EffectComposer → UnrealBloomPass → OutputPass), `renderer.setClearColor(0x050508)` rendered as (38,38,50), a visible grey, because the clear colour was sRGB-encoded twice. Fixed 2026-10-10 by setting `scene.background = new THREE.Color(0x050508)` and clearing to black.

**Why:** the bug looked like particle haze. Turning bloom off and removing dust particles didn't fix it. Reading a corner pixel with `gl.readPixels` inside a rAF found it at once.

**How to apply:** when a three.js page with post-processing looks washed out, read one background pixel before tuning particles or bloom.

Also: the Claude browser pane pauses rAF while it is hidden, so a screenshot after a `wait` shows a stale frame. A run of screenshots advances the scene a few frames each. Don't read a stale frame as a bug. See [[event-horizon-draft]].
