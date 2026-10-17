---
name: art-chrome
description: §7 art-chrome decisions — the MJ room backdrop is a Title hero only; gameplay stays clean cream.
metadata: 
  node_type: memory
  type: project
  originSessionId: 20ac0a0c-8bf3-4a85-8236-545a804b58ac
---

Decided 2026-07-07 (Fable ruling, user-accepted via screenshots).

**The painted room backdrop does NOT go behind live gameplay.** Tested MJ backdrop (`assets/scene/room-day.png`, MJ v8 "cozy general-store interior" variant _1) behind the `/run` shelf: it looked bad. Two reasons, both structural, not tunable: (1) the opaque saturated Skia shelf is a flat game object that reads as *pasted onto* a soft watercolor painting — two visual languages; (2) ink-on-cream HUD text can't stay legible over painted beams/lattice — any cream wash strong enough to fix text muddies the art into brown sludge. Pattern → rule: **detailed painterly backdrops belong where there's no flat game furniture and no small body text; behind live UI, keep the clean cream.**

**What shipped (option A + card-screens):** backdrops go on screens with **no flat game furniture and opaque content** — the Title and the Draft/Delivery screen. The interactive `/run` and `/restock` shelves stay clean cream.
- **Title** ([src/app/index.tsx](src/app/index.tsx)): full-bleed `assets/scene/room-day.png` (cover) + **0.18** cream scrim, mascot `shop-cat` over it, wordmark on a translucent cream "shop-sign" plate (`rgba(255,248,235,0.82)`), settings gear on a matching cream disc. Wordmark plate gets a small `translateX` optical nudge right (window sits left-of-centre).
- **Draft** ([src/app/draft.tsx](src/app/draft.tsx)): full-bleed `assets/scene/room-delivery.png` (cover) + a **light 0.22** wash. Bare text does NOT rely on the wash — instead each text group gets a **legibility plate** (`palette.plate` = translucent creamBright, new token): the top bar became a header bar, and the section-label + caption sit on their own cream pills. Cards + WoodButton are opaque, no plate. This is the general rule now (see design-system doc): light wash + per-element plates beats a heavy scrim, which just muddies the art. A heavy full-screen scrim (0.52) was the first attempt and looked bad — text still fought the painting and the top bar looked pasted on.

Images are MJ v8, **1:2 (768×1536)** so `cover` barely crops on phones — the fix for the earlier "too zoomed" (the first room-day was 9:16 → zoomed on tall screens). Home = the "wide establishing, pulled back" prompt variant `_0`; delivery = "morning delivery" variant `_0`. Verified via mobile-preset screenshots; tsc clean. Sources in `lucky-shelf-midjourney/new ones/`.

**Gotchas:** `StyleSheet.absoluteFillObject` is NOT in this RN version's types (errors) — use explicit `position:'absolute'` + `top/left/right/bottom:0`. Don't spread a ViewStyle (e.g. `shadows.lifted`) into a style used on `<Image>` — ImageStyle's `overflow` union rejects it (tsc error). Judge backdrops at **mobile preset**, not the desktop browser — a tall desktop window makes `resizeMode="cover"` zoom the image hugely (that's the "it's scaling wrong" symptom), which is not what a phone shows.

**Not wired:** the 4 MJ shelf-frame variants (`_2` was best, true front-elevation) — parked; the playable shelf is a dynamic 3×4→4×5 Skia grid, so a fixed painted shelf can't be the interactive surface. Dusk/other backdrops unneeded for the title (always golden hour). Source PNGs live in `lucky-shelf-midjourney/` (gitignored-ish, untracked). See [[audio-system]] for the sibling per-screen wiring pattern.
