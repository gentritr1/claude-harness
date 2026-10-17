---
name: cosmicbody-shader-already-sophisticated
description: "CosmicBody.shader already does fake-sphere normal + diffuse + rim + spec + terminator; don't re-add those"
metadata: 
  node_type: memory
  type: reference
  originSessionId: b7b5666e-42d5-4a69-918e-ab5a27fc74d2
---

`Assets/_Project/Art/Shaders/CosmicBody.shader` already implements sophisticated fake-sphere
2D shading — any "add sphere lighting / normal / terminator / rim" suggestion (e.g. from
generic shader research that lacks code access) is mostly REDUNDANT. Verify against the code
before acting. What already exists (line numbers approx):
- Fake-sphere normal from disc UV: `z = sqrt(saturate(1 - dot(p,p)))`, normal = normalize(p.x,p.y,z) (~294-295)
- NdL diffuse ramp (~296, applied ~328) + radialGradient surface mix (~297,327)
- Per-style surface fns: Rocky/Terrestrial/Gas/Star/Cataclysm/Cosmic via _Style (~300-324)
- Gated rim with style-specific color (~330-336)
- Fixed-position fake specular highlight (~338-341)
- Soft terminator darken (~343-345)
- Emissive boost when _Emits (~347-350)

Staging status (RE-VERIFIED against shader 2026-07-03 — the original gap list is now almost fully SHIPPED, don't re-brief it):
- Stage A DONE: fwidth edge AA (`edgeAa = max(fwidth(radius01), 0.002)` ~411), style-gated specular weights (rocky/mid/emitter ~501-508).
- Stage B DONE: theme tint is luma-normalized × `_TierThemeWeight` × midtone mask (~550-552); MergeBody sets the weight per tier via MPB.
- Stage C MOSTLY DONE: gas latitude bands (~277), supernova shell (~334), black-hole accretion w/ Doppler (~315-324), ring fwidth AA.
- Stage C COMPLETE 2026-07-03: `PlanetStyle.Galaxy = 6` shipped via PR #34 (squash `1b3c74e`) — two-arm log-spiral + dark heart for tier 11, tier 12 stays Cosmic; legendary step() gates unaffected (both styles ≥ 4.5, tier-11 glow 0.78 < 0.9). PlanetThumbnailBaker has a matching Galaxy branch — keep shader and baker in sync for any future style. No shader gaps remain from the research staging; only user eyeball acceptance is pending ([[open-verification-gaps]]).

Deep-research dossier: docs/PLANET_VISUAL_RESEARCH.md. The report (deep-research output) had
NO shader access and wrongly assumed the sphere cues were missing — see [[reviewing-codex-output]]:
always vet research/Codex claims against the real code.
