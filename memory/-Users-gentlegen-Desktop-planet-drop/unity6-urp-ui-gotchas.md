---
name: unity6-urp-ui-gotchas
description: "Unity 6.5 / URP 2D + TMP/uGUI pitfalls confirmed during the art-polish pass (RT bake, TMP outline, layout, bloom)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 03b57214-d236-47ce-a59d-f567125c1022
---

Concrete gotchas confirmed in Planet Drop (Unity 6.5, URP 2D render graph), each cost a review/verify cycle:

- **Offscreen RenderTexture bake** (e.g. `PlanetThumbnailBaker`): `Camera.Render()` is unsupported under URP render graph — it spams "Renderer2D Pass: Fake or uninitialized surface", "EndRenderPass: Not inside a Renderpass", and "output Render Texture must have a depth buffer". Fix: build the RT from a `RenderTextureDescriptor` WITH a depth-stencil (`GraphicsFormat.D24_UNorm_S8_UInt`), and render via `RenderPipeline.SubmitRenderRequest(camera, new RenderPipeline.StandardRequest{ destination = rt })` (keep `camera.Render()` only as the non-SRP fallback). The thumbnails may render anyway, so the bug shows as console spam, not a blank — watch for it.

- **TMP outline leaks to all text**: setting `TextMeshProUGUI.outlineColor`/`outlineWidth` mutates the SHARED font material, so the outline appears on every label using that font. For a per-text outline, read `.fontMaterial` (that instances the material) and set `ShaderUtilities.ID_OutlineColor` / `ID_OutlineWidth` on the instance.

- **TMP `.fontMaterial` on an INACTIVE GameObject throws `ArgumentNullException: source`** (`new Material(null)` — the component hasn't run setup so its source material is null). Build the UI while the root is ACTIVE, then hide it. The modal scaffold (`UIKit.CreateModalScreen`) and Home both call `ModalAnimator.SetVisibleImmediate(false)` which DEACTIVATES the root — so any per-instance material/outline (e.g. the hero wordmark's `.fontMaterial`) must be applied BEFORE that hide. Deactivating first aborted the entire Home menu build at boot (fixed commit `b235a0e`).

- **VerticalLayoutGroup exact-fit overflow**: when child content height == panel height and `childAlignment` is UpperCenter, the last child kisses/overflows the rounded panel edge. Give the panel slack (content < panel height) and switch that group to MiddleCenter so margins split evenly. Hit when sizing the Home button panel.

- **Bloom-lit "neon" needs HDR-bright values**: the URP bloom threshold is set high (only tiers ≥7 / highlights bloom per ART_DIRECTION). A glow that must actually bloom needs channel values pushed well above 1 (e.g. teal ~2.5 in G/B); pair it with a wider low-alpha halo sprite so it still reads where bloom is weak (the glassy-container rim, commit `552d93d`).

Workflow: play from Boot.unity (Main floods benign ServiceLocator/NoSubscription errors); add PlanetDrop/CosmicBody + PlanetDrop/Starfield to Always-Included Shaders before Android builds; revert ProjectSettings app-id contamination after PlayMode before committing.
