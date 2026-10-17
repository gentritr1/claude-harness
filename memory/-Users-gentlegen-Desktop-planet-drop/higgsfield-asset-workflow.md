---
name: higgsfield-asset-workflow
description: Proven Higgsfield MCP pipeline + real costs for Planet Drop art; codex cards done (PR
metadata: 
  node_type: memory
  type: project
  originSessionId: 97338cad-3b85-429b-9e94-5de7fae81eb7
---

Higgsfield MCP asset pipeline, validated 2026-07-04 generating the 12 codex card portraits:

- **Model:** `nano_banana_2` at 2K, 1:1 = **2 credits/image** (the "~130 credits for 12 portraits" estimate assumed a pricier model; actual spend was 24). Balance after: 60.5 on starter plan.
- **Style-lock workflow:** `media_upload` (curl PUT to presigned URL) → `media_confirm` → pass the sheet as `medias:[{role:"image"}]` on every `generate_image` call + a shared style boilerplate paragraph (toon bands, gloss blob upper-left, dark cartoon edge, big smooth shapes, navy starfield ~60% fill). One test image first, then batch in parallel — style stayed consistent across all 12.
- Reference sheet media_id `65a2c879-dce0-463f-baae-a9db9b5aab8f` (planet-ladder-candy-ref.png) is reusable for follow-up gens (hero art) while it lives on their CDN.
- Prompts used the **shipped `PlanetVisualTable` hexes**, not the bible's pre-candy hexes — cards must match the board (see [[cosmicbody-shader-already-sophisticated]], [[ui-art-polish-direction]]).
- Output: `docs/concepts/codex-cards/tier-01..12.png` (2048²) — **MERGED to main 2026-07-04 (PR #40, user-accepted)**. App icons PR #39 also merged same day.
- Home-screen hero: **user picked `home-hero-falling.png`** (PR #41 merged 2026-07-04); `home-hero-ensemble.png` designated splash art. Icon reference media_id `9a113924-a86d-47c4-9381-ca83fcf03302`. Balance after all gens: ~56.5.

**Transparent-cutout pipeline, validated 2026-07-06 (Opus home-UI session).** To make the home hero composite over ANY era backdrop with no rectangle, the home_hero painting was turned into an alpha PNG. Key learning: `remove_background` on the FULL painted scene FAILED — it kept the whole illustration (stars/comet/nebula are treated as subject, output was ~identical, `hasAlpha:yes` but fully opaque). What WORKED = two-step: (1) `flux_kontext` with the original as `medias:[{role:"image_references"}]`, prompt "replace entire background with flat solid magenta #FF00FF, keep only Earth + planet cluster, same style" → clean subject-on-magenta plate; (2) `remove_background` on THAT job_id → clean transparent cutout (`home_hero_planets.png`). Verify alpha by flattening to JPEG via `sips -s format jpeg` and viewing (transparent→white). Minor magenta spill on the glow rim; acceptable over dark. Compositing tricks (additive/screen to hide a dark bg) only work over dark backdrops — over bright ones (orange nebula era) they wash the subject out, so a true alpha cutout is the only theme-agnostic fix. Integrated in HomeScreen round 6 (commit cd175b3, branch post-mvp/9b-opus-home-ui): dropped the mask/frame, cutout floats over a cyan bloom; `home_hero_planets.png` uses a cloned Sprite `.meta` (fresh guid) so it imports without editor fiddling; ArtResourceTests guards the new path. Awaiting user in-game screenshot.

**Status:** Codex implemented the integration brief → **PR #42 open, awaiting user 19.5:9 screenshots** (home, codex gallery, boot splash). Review passed: imports correct (512/1024/2048, ASTC), hero replaces glyph, splash wired incl. AndroidBuildConfig (build tool would've reverted greybox splash — good Codex catch), cards cached w/ baker fallback + locked tint intact.
Two flagged-not-fixed items in the PR body: `m_ShowUnitySplashLogo` 0→1 (no-op on Personal license; flip back if ever on paid), and the wordmark scrim's sliced border (24px on a 32px texture) is invalid — fix before ever enabling `UseWordmarkScrim`.
After #42 merges: back to open-verification-gaps queue (wells feel check etc.).
