---
name: device-feel-gate-round1
description: "First device feel-gate of the combined v2 loop — verdict \"way better\", plus the intuitiveness fixes and a native-dep blocker."
metadata: 
  node_type: memory
  type: project
  originSessionId: 055e11c1-e558-4c66-b0dc-b4986591cb9e
---

First device feel-gate of the full redesigned loop (LOOP_V2 + TAG_SYNERGY + BUILD_STEERING +
GOAL_LADDER on together, signatures off), 2026-07-07. Relay played it on the iOS sim.

**Verdict: "overall its way better than before"** — the redesign lands. Remaining gap = *intuitiveness*
("not quite understandable what the point is"). Feel-gate feedback → fixes (committed `4a554cf`,
`ddb5bc2`):
1. Supplier caption looked like a search input → plain instructional text.
2. Sell cards showed bare "Sell" → now "Sell +N" (real coins), centered.
3. "Reroll · 2" read as *2 rerolls* → "Reroll · 2c" (coins).
4. Wanted drag-to-place on restock (not just the button) → wired `heldItem`+`onPlace` into the restock
   ShelfScene (reuses the arrange drag).
5. Wanted first-session coachmarks → refreshed the one-time OnboardingHint copy for the new loop
   (buy → arrange → synergy → target) and bumped its storage key to v2 to re-show.
6. **Share is just text** → wants a shareable IMAGE. **NOT DONE — blocked** (see below).

**Balance finding for Fable (surfaced by showing real sell values):** tier-1 items sell for **+0**
coins (`sellPrice = floor(baseValue/3)`). Display is correct/honest but selling cheap items is
worthless — a lean-sell-back balance choice; logged in the Fable sign-off queue. [[loop-v2-phase3-goal-ladder]]

**Scar CORRECTED 2026-07-07 — pnpm IS usable here, the "broken" note was incomplete.** The failure was
never pnpm itself; it was two stacked issues: (1) default PATH node is **v14**, and the corepack pnpm@11.7.0
shim throws `ERR_VM_DYNAMIC_IMPORT_CALLBACK_MISSING` on old node; (2) pnpm 11.7.0 hard-requires the
**`node:sqlite`** builtin, which only exists on node ≥22.5 **and only behind `--experimental-sqlite`**.
**Working recipe (VERIFIED — installed react-native-view-shot@5.1.0):**
`source ~/.nvm/nvm.sh && nvm use 23.3.0` then export `NODE_OPTIONS='--experimental-sqlite'` +
`COREPACK_ENABLE_DOWNLOAD_PROMPT=0`, then `npx expo install <pkg>` (or `pnpm …`). Under that env `pnpm -v`
returns 11.7.0 clean. So native deps CAN be added + rebuilt from this harness after all.

**Share-as-image — BUILT + VERIFIED + committed `c2dbd26`, 2026-07-07** (was #6 above).
`react-native-view-shot@5.1.0`; [share.tsx](src/app/share.tsx) wraps the card `View` with
`ref`+`collapsable={false}`, `onShare` does `captureRef(cardRef,{format:'png',quality:1})` →
`Share.share({url,message})`, text-only fallback on failure. **Verified on the iOS sim (simctl-only,
computer-use denied):** temp-booted into `/share`, captured on mount, surfaced the file path on screen,
then **pulled the PNG off the sim host FS and Read it** — a clean 1086×1044 image of exactly the framed
card. captureRef → real image is PROVEN. Only the Share-*sheet* tap (image thumbnail in the iOS share UI)
is left as a human eyeball. tsc clean.

**Full working iOS-build recipe here (chain of 4 gotchas, each cost a failed build — the memory that said
"needs node 20" was too thin):**
1. **pnpm**: `nvm use 23.3.0` (pnpm 11.7.0 needs the `node:sqlite` builtin) + `NODE_OPTIONS=--experimental-sqlite`
   (node ≥22.5 gates it behind the flag). Only needed for `expo install`/`pnpm`, NOT the build.
2. **CocoaPods locale**: export `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8` or pod install dies with
   `Encoding::CompatibilityError`.
3. **CocoaPods version**: system `/usr/local/bin/pod` is 1.12.1 and too old for RN 0.86's `visionos`
   podspec key → `undefined method 'visionos'`. The working one is Homebrew `/opt/homebrew/bin/pod` **1.16.2**;
   `export PATH="/opt/homebrew/bin:$PATH"` to shadow the old one.
4. **xcodebuild scripts reject the sqlite flag**: the Hermes/RNDeps build-phase scripts run their own node
   (v20.19.4) and error `--experimental-sqlite is not allowed in NODE_OPTIONS`. So **`unset NODE_OPTIONS`
   before `npx expo run:ios`** (pods already installed → no pnpm needed at build time).
   Then `CI=1 npx expo run:ios --device CD14DAE0-…` → Build Succeeded, installs + launches on the sim.

See [[ios-ui-verify-on-simulator]] for the simctl-only verification used throughout (computer-use to the
Simulator was denied).
