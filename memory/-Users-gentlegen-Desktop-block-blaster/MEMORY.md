# Memory index

- [Release keystore setup](release-keystore-setup.md) — upload keystore in gitignored credentials/ (back up externally!); /android is prebuild-generated so the gradle signing edit dies on prebuild --clean

- [Shell Node version trap](shell-node-version.md) — default shell Node is v14; prepend nvm 20.19.4 to PATH or verify fails cryptically
- [AdMob migration](admob-migration.md) — 2026-07-27 replaced LevelPlay with AdMob inside the custom Expo module (not react-native-google-mobile-ads: its Android full-screen ads are still legacy on a New-Arch-mandatory SDK 56); play-services-ads pinned 25.2.0; Kosovo payout wall still unresolved
- [Rowflare → Blockrow rename](rowflare-to-blockrow-rename.md) — 2026-07-27 renamed to Blockrow / com.blockrow.game before publication; storage falls back newest-first through @rowflare then @block_blaster
- [Blockrow → Block Destroy rename](blockrow-to-block-destroy-rename.md) — CURRENT NAME. Package permanently com.blockrow.game (Play listing exists); display name only from now on. Long names wrap mid-word — re-screenshot at 320pt after any rename
- [Helper wallet + colour Break](helper-wallet-and-colour-break.md) — 2026-07-27 Break destroys a whole colour; helpers persist across runs (the per-run refill made the rewarded ad unearnable). colorIndex 0 is falsy — never truthiness-check a colour
- [Interstitial on Game Over](interstitial-on-game-over.md) — 2026-07-27 added, fires only on Game Over → Play Again (never the mid-run reset); pacing unit-tested. Adding an ad format falsified "no forced ads" copy in 5 places — always re-grep
- [Release folder recipe](release-folder-recipe.md) — how the Desktop release + listing folders are built; store art and frames regenerate from scripts; emulator screenshot recipe for 3 sizes
- [Hermes bundle is not greppable](hermes-bundle-not-greppable.md) — grep/strings find nothing in a release bundle even when the string is there; always grep a control string first, and verify env inlining via UI that only renders when the value exists
- [Gradle false green from cached task](gradle-false-green-cached-task.md) — editing a dependency version and re-running a compile task can report success without recompiling; always --rerun-tasks when bisecting
- [zsh does not word-split](zsh-no-word-splitting.md) — `for f in $FILES` silently no-ops here; use `while IFS= read -r`, then re-grep to confirm the edit landed
- [LevelPlay migration](levelplay-migration.md) — SUPERSEDED by admob-migration; 2026-07-17 moved ads to LevelPlay 9.5; app.json strips ADSERVICES_ATTRIBUTION deliberately (still true under AdMob)
- [LevelPlay pending approval](levelplay-pending-approval.md) — SUPERSEDED by admob-migration; historical: `is_deviceid_optout=true` blocked all fill (509). Still-live fact: store artifact is the AAB, not the root APK
- [Local Android build traps](local-android-build-traps.md) — export ANDROID_HOME for gradle; never pipe gradle through tail (masks failure); check APK mtime before adb install
- [Localhost port collision](localhost-port-collision.md) — localhost can resolve to a stray IPv6 listener from another app; curl the title + lsof before trusting a preview
- [Fixed overlay narrow-viewport trap](fixed-overlay-narrow-viewport.md) — left:50% fixed overlays shrink against half the viewport; force-show and verify all overlays at 320/375px
