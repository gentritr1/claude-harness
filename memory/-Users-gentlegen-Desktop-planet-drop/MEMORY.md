# Memory Index

- [Merge-kit RN spinoff](merge-kit-rn-spinoff.md) — reusable RN merge-game factory at ~/Desktop/merge-kit; v0.1 delegated to Opus 5 2026-07-25; PLAN.md is source of truth
- [Model split UI experiment](model-split-ui-experiment.md) — testing Opus 4.8 for UI taste vs Codex (home-screen brief 2026-07-05); outcome PENDING

- [Higgsfield asset workflow](higgsfield-asset-workflow.md) — nano_banana_2 @2K = 2 credits/img, style-ref pipeline; codex cards DONE (PR #40, eyeball-gated), hero next

- [Open verification gaps](open-verification-gaps.md) — user-side checks deliberately deferred (wells feel check + A/B, sweep eyeball, taptics, IAP); surface when user opens editor or asks what's pending

- [Document learnings as we go](document-learnings-as-we-go.md) — user wants every fix/mistake recorded durably so future choices compound
- [Planet Drop orchestrator workflow](planet-drop-orchestrator-workflow.md) — I orchestrate/review + own git, Codex codes, user runs Unity
- [Monetization Kosovo constraint](monetization-kosovo-constraint.md) — AdMob banned for Kosovo; ad SDK is LevelPlay; IAP/Google Play merchant payout still unverified
- [UI/art polish direction](ui-art-polish-direction.md) — Post-MVP #3: hybrid procedural+AI art on URP 2D, gameplay-wow-first chunk order
- [Save additive-schema safety](save-additive-schema-safety.md) — adding any SaveModel field can wipe saves via the checksum gate; how to evolve schema safely
- [Unity6 URP/UI gotchas](unity6-urp-ui-gotchas.md) — RT bake needs SubmitRenderRequest+depth, TMP outline leaks shared material, layout/bloom traps
- [uGUI preferred height ignored](ugui-layout-preferred-height-ignored.md) — UIKit vertical groups use childControlHeight=false, so SetPreferredHeight is a no-op; set sizeDelta explicitly
- [Visual calibration briefs lesson](visual-calibration-briefs-lesson.md) — spec proportions + layered glow + alpha floors, require screenshot acceptance; multipliers on tiny constants ship invisible
- [Reviewing Codex output](reviewing-codex-output.md) — verify claimed fixes/tests hit the real failing path, not the unit Codex touched
- [Merge feel convergence gap](merge-feel-convergence-gap.md) — Approach A convergence SHIPPED: merged to main 2026-07-03 via PR #31 (squash d4d323f)
- [Progression bible + era backdrops](progression-bible-era-backdrops.md) — 4-act ladder redesign (Cosmic Egg ending) in docs/PROGRESSION_BIBLE.md; 5 Higgsfield plates + EraBackdropController shipped in PR #31; renames 5/5 DONE (PR #34); galaxy spiral + pause-safe notices also in PR #34
- [Unity batchmode licensing blocked](unity-batchmode-licensing-blocked.md) — Unity MCP EditModeTestCommand.RunAllNoExit is the working test path (2026-07-03); batchmode needs -licensingIpc channel as fallback
- [Celebration/tension feature wave](celebration-tension-feature-wave.md) — forge banner, PB chip, danger tension, planet rarity ladder + briefs 1-3, convergence, cosmic days, pause fix: MERGED to main 2026-07-03 via PR #31 (squash d4d323f); PR #30 closed as superseded (combo banner deleted by brief 3)
- [CosmicBody shader already sophisticated](cosmicbody-shader-already-sophisticated.md) — planet shader already has normal/diffuse/rim/spec/terminator; the real gaps are spec-gating, fwidth AA, tint reweight, per-style signatures
- [Stormhaven brief carries Planet Drop lessons](stormhaven-brief-carries-planetdrop-lessons.md) — new game's orchestrator brief folds in our Unity scars; keep it synced each new convo
- [Retention/addictiveness plan](retention-addictiveness-plan.md) — Post-MVP #4: phased retention pass from 2 research docs (docs/RETENTION_PLAN.md); Threads A/B/C all COMPLETE & merged (PRs #24/#26/#27/#28); deterministic-sim DEFERRED
- [Agent playtest harness](agent-playtest-harness.md) — dev-only bot plays the real game for balance analytics; chosen INSTEAD of deferred deterministic sim core; Phases 1-3 MERGED to main (PR #29); finding: tier 12 unreachable (merge-economics wall, not config)
- [Merge spawn escape bug](merge-spawn-escape-bug.md) — chain merges eject planets through the 0.35 floor (unclamped spawn overlap + solver depenetration); 3-layer fix briefed 2026-07-03
- [Chamber is camera-fit not config](chamber-is-camera-fit-not-config.md) — runtime chamber width/fail-line come from FitCameraToChamber (aspect), NOT GameConfig chamberSize.x/failLineY; read live chamber.InnerBounds
- [Gravity Wells feature](gravity-wells-feature.md) — Post-MVP #5: Phase 1 MERGED (PR #32, default OFF); feel check DEFERRED = step zero of Phase 2 brief (in docs/briefs/); Phase 3 locked behind A/B gate
- [Audio polish next](audio-polish-next.md) — premium audio pass COMPLETE (A/B/C/D shipped on post-mvp/3-ui-art-polish): procedural SFX+UI sounds, 3 real theme-music beds w/ crossfade, ducking/pause-lowpass, iOS taptic (UNVERIFIED — no device); MERGED to main via PR #23 (squash 9e8ebfc)
