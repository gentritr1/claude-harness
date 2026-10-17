---
name: ios-ui-verify-on-simulator
description: "RN/iOS UI fixes can't be verified on web (drag-gated) or blind — run the iOS simulator + computer-use to see and iterate. Two concrete gotchas inside."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b64ec080-bda3-4267-9ae4-93fecb2d7c5b
---

Lucky Shelf is React Native / Expo (native `ios/` project with Skia). Two rounds of **blind** UI fixes shipped wrong (a coin fix clipped "0"→"U", then a no-op fix), because I couldn't see them: web preview can't reach gameplay screens (they're behind **drag-placement**, and synthetic web drags don't fire), and I was guessing at font/layout metrics.

**The fix that works:** build to the **iOS simulator** and drive it with **computer-use** (screenshot + zoom + real `left_click_drag`, which the app's gesture handler accepts). Build: boot a sim (`xcrun simctl boot "iPhone 16 Pro"`, `open -a Simulator`), then `CI=1 npx expo run:ios --device "iPhone 16 Pro"` (needs node v20 on PATH; first build ~few min; it reuses a running Metro). Fast-refresh applies edits live, so I can nudge → screenshot → adjust in a loop. Verified the coin + cascade-footer fixes this way (2026-07-07).

**Gotcha 1 — iOS text vertical centering:** `includeFontPadding` and `textAlignVertical` are **Android-only** (no-ops on iOS). To optically center a display-font number (Baloo2) against an icon on iOS, nudge with `transform: [{ translateY: N }]` (2 for the coin pill, 3 for the slam) — NOT by shrinking `lineHeight` below the glyph (that clips the top).

**Gotcha 2 — cascade "double shelf":** the run cascade drew TWO shelves — the HUD's `ShelfScene` (dimmed behind the scrim in [run.tsx](src/app/run.tsx)) AND `CascadeLayer`'s own Board on top — misaligned, producing "extra slots + a cut-off item under the Day Total." Fix: don't render the HUD shelf while `cascadeMount` is set; the cascade owns the shelf visual.

**Fallback when computer-use to the Simulator is DENIED (2026-07-07 Phase 4 UI):** you can still verify screens headlessly with `xcrun simctl` alone — no Simulator control needed. Assets: sim already booted (`iPhone 16 Pro` CD14…), a built `LuckyShelf.app` in DerivedData, Metro on 8081; bundle id `com.gentlegen.luckyshelf`, URL scheme `luckyshelf`. Loop: edit JS → `simctl terminate` + `simctl launch` (reloads the Metro bundle, picks up edits) → `simctl io booted screenshot out.png` → Read the png. **Navigation without tapping:** `simctl openurl luckyshelf://settings` prompts an "Open in…" dialog you can't dismiss, so instead **temporarily boot straight into the target screen**: add `return <Redirect href={'/run'} />;` at the top of `app/index.tsx`'s return (after the hooks — never before), relaunch, screenshot, revert. **To verify a populated/HUD state** (e.g. synergy badge needs ≥3 same-tag items, goal HUD needs `dailyTarget`), temporarily seed the store: `createRunStore({ initialState: makeState([...items], { phase:'arrange', dailyTarget:45, freeRerollTokens:1 }) })` from `src/sim/testkit`, plus flip the relevant flag const, then revert everything (grep for a `TEMP-VERIFY` marker to confirm clean). This verified TopBar centering, supplier picker, goal HUD, and synergy badge on-device without computer-use.

**Gotcha 3 — the seed `<Redirect>` creates an empty-history root → a false `GO_BACK` redbox.** Booting
straight into a gameplay screen via `<Redirect href={'/run'}/>` REPLACES the root, so there's no screen
beneath. Tapping a "‹ Menu" button that calls `router.back()` then throws *"The action 'GO_BACK' was not
handled by any navigator"*. This is a **seed artifact, not a shipping bug** (the real flow pushes gameplay
onto the title, so back() resolves). Fixed properly anyway in `4bc0ffb`: gameplay Menu buttons +
"Run Complete" now `router.replace('/')` (go to menu, history-independent), matching summary.tsx;
push-navigated leaves (catalog/settings/share) keep `router.back()` = return to caller. To verify a
nav fix without tapping (computer-use denied): one-shot `<Redirect>` to make the empty-history root, then
a temp `useEffect(setTimeout(() => router.replace('/'), 1500))` to fire the nav, and screenshot the clean
title. When re-launching a seeded screen, relaunch FRESH afterward to clear the artifact for the user.

**Gotcha 4 — a module-level `seeded` guard in the seed harness survives a Metro reload.**
When seeding a screen via a temp `<Redirect>` + `seedSummary()` in `index.tsx`, a
`let seeded=false; if(seeded)return;` guard (added to avoid setState-in-render loops) will
**no-op on the next `simctl terminate`+`launch`** because Metro preserves module state across
the reload — so the store keeps a *default fresh run* (phase `delivery`) and the summary's
own routing effect bounces you to `/draft`. Fix: **drop the guard, re-seed on every index
mount** (it's idempotent — same setState — and index redirects away immediately, so no loop).
Symptom that flags it: your seeded screen shows real gameplay (a live draft with art) instead
of the target. (B-M4, 2026-07-08.)

**Rule:** don't hand the user another blind UI build when the simulator is available — verify there first (via computer-use, or the simctl-only fallback above). See [[lane-b-web-verification]] for why web can't do it.
