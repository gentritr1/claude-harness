---
name: art-skins-01-review
description: ART-SKINS-01 (Codex AI-texture skin spike) reviewed 2026-09-30 — REQUEST CHANGES; what failed and the repo's new lessons file
metadata:
  type: project
---

Codex built ART-SKINS-01 (GPT-image sprite sheets + textured Cinnamon Roll renderer behind `ART_SKIN_TEXTURED`, default OFF) in the **working tree, uncommitted**; patches in artifacts/ART-SKINS-01/patches. Review verdict 2026-09-30: REQUEST CHANGES, stays OFF.

- All 9 AI sheets fail seam/alpha/fit (re-run matched). Static recording cost +2.2 ms per level open replicated (0.24 → 2.45 ms, non-overlapping, 16 shuffled runs). Exit-frame cost UNVERIFIED (loaded host).
- Found in review: build.gradle packages artifacts/ART-SKINS-01/runtime into EVERY build unconditionally (release risk while the tree is dirty); dense boards unreadable with textures (need cell-size fallback); tile borders, rotated tail faces, stray lines.
- The repo now has `docs/engineering-lessons.md` (AGENTS.md requires reading/updating it) — keep it and this memory consistent; owner adopted it as project practice.

**How to apply:** before any release build, make sure the working tree has no ART-SKINS-01 gradle line (or it is gated). Pattern → detection → brief update: "default-OFF flag but assets packaged anyway → list APK assets in the OFF check → briefs must say experiment assets are gated on the same flag". Related: [[arrow-skins-direction-2026-09-29]].

**ART-SKINS-02 (procedural, 2026-09-30): UNCERTAIN, keep OFF.** Seams/assets solved (no images, 7 draws/strip). Gap: its benchmark ran without META_ZOOMED_CAMERA → measured the 10 dp flat tier, but players see ~29 dp full detail; full-detail dense perf unmeasured. Host never quiet (load 10–29, other emulator). Native changes sit uncommitted in the working tree (default-off, no assets). Look needs owner eyeball (lollipop stub behind roll, dashed icing, detached head shine).

**ART-SKINS-03 (2026-10-01): UNCERTAIN, look ready for owner.** Real config (all META, zoomed camera) = 29.39 dp full detail on level 3828. Full-detail prep 45.9 ms median / 83.6 max per level open (budget 16), strip recording 0.19→2.97 ms; exits unmeasured (host load 15–17). Visual: good; heads barely wider than shaft, tail roll dominates — suggested 1.3× heads. Code moved out again: artifacts/ART-SKINS-03/patches/skin-code-removed-from-tree.patch (commit 7714e17 has docs only). **Codex works in this same working tree concurrently** — check file mtimes before moving/reverting anything.

**ART-SKINS-04 (2026-10-01): general skin system exists (TS SkinSpec registry + one native renderer + K1–K7 contract + docs/skins/README.md).** Accepted as the base; REQUEST CHANGES on look/speed: full level-open ≈136 ms median (Cinnamon) — the "12 ms cold preparation" headline hides a 116 ms first draw; my K4 rule (fill contrast) wrongly darkened the dough → now outline-only; one-cell arrows must not get roll+face (blob with eyes). Code out of tree: artifacts/ART-SKINS-04/patches/skin-code-removed-from-tree.patch (17 files). Commit 568ee88 = docs/tools only.

**ART-SKINS-05 (2026-10-01): look nearly there; speed REQUEST CHANGES.** Light dough back (K4 = outline), one-cell = head only (K8), straight accents on the head-oval axis (owner told Codex directly). Level open: Cinnamon 45.9/75.8 ms vs flat 6.0/20.8 (+36 median), Sherbet 33.8/54.4 vs 11.0/25.8 (+22). Biggest phase = first draw 31/61 ms. Code out of tree: artifacts/ART-SKINS-05/patches/skin-code-removed-from-tree.patch (17 files); commits 008f1ad, e34bc6a = docs/tools.

**Play build 2026-10-01:** ~/Desktop/Arrows-build-2026-10-01/arrows-cinnamon-e34bc6a-vc9.aab (sha256 de810153…) = commit e34bc6a + artifacts/ART-SKINS-05/patches/skin-code-removed-from-tree.patch applied temporarily, all 17 META flags, EXPO_PUBLIC_ART_SKIN=cinnamon, REAL ads, versionCode 9, both ABIs. Skin selection inferred from build env only (real-ads build can't run on the emulator). Patch reverted after the build; tree clean. The owner asked for the AAB only — no test APKs.

**Play build vc10 (2026-10-01):** ~/Desktop/Arrows-build-2026-10-01/arrows-cinnamon-5581670-vc10.aab = commit 5581670 (Settings shows "Version 1.0.0 (10)" via expo-application) + skin patch, real ads, all META. The original ART-SKINS-05 patch conflicts on contrastAudit.ts after 5581670; use `artifacts/ART-SKINS-05/patches/skin-code-on-5581670.patch` (clean apply). Owner wants AABs only (Play testing), not APKs.

**ART-SKINS-06 picker (2026-10-01): APPROVED default-OFF** (EXPO_PUBLIC_META_SKIN_PICKER; key arrows_skin, ids classic 0 / cinnamon 1 / sherbet 2). Save path read line-by-line, 1963 tests. Code out of tree: artifacts/ART-SKINS-06/patches/skin-picker-code-on-1d61234.patch (27 files, includes the skins) — applies on bad7903. ART-SKINS-07 (all canvas styles) starts from it.
