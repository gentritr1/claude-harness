---
name: arrange-scroll-fix
description: The Arrange HUD scrolls when the full-shelf sell-list overflows; how to add a ScrollView around drag content without breaking the pan.
metadata: 
  node_type: memory
  type: project
  originSessionId: 523339a0-35c7-4643-bd36-369320df5b1d
---

2026-07-08 (Opus, commit ba192aa): user hit a layout bug at day 10 — full shelf + held item →
the "sell to make room" softlock list overflowed the Arrange screen (`src/app/run.tsx`).
`shelfWrap` used `flex:1 + justifyContent:'center'`, so when the sell list appeared the centered
content spilled BOTH ways: the `<SectionLabel>YOUR SHELF</SectionLabel>` ghosted UP over the
BuildSignpost panel, and the sell chips + primary button spilled off the bottom, unreachable (no
ScrollView on the screen at all).

Fix: wrapped the content column in a `ScrollView` with `contentContainerStyle={{ flexGrow: 1 }}`
(so the shelf stays centered via `shelfWrap flex:1` when content fits, and scrolls when it doesn't).

**REUSABLE PATTERN — scrolling a screen that contains gesture-driven content:** the shelf uses a
react-native-gesture-handler pan (drag-to-place). An RN `ScrollView` around it would compete with that
pan. Gate it: `scrollEnabled={heldFull}`. `heldFull` (shelf full + held item) is EXACTLY the state where
(a) content overflows and (b) the shelf has no active gestures — `movementEnabled` is false while holding
and there's no empty slot to place into. So the scroll only turns on when the drag is inactive; normal
drag states stay a non-scrolling column, byte-identical. General rule: enable scroll only in the state
where the competing gesture is provably off.

Verified on the iOS sim by SEEDING the exact repro (TEMP-VERIFY in store.ts: `makeState` full 12-slot
shelf + `heldItem: makeInstance('bread-loaf')` + `dailyTarget` to force the BuildSignpost, plus a temp
`<Redirect href='/run'>` in index.tsx — both reverted, grep-confirmed clean). Overlap gone, sell list
scrolls into reach. Regression check: normal arrange still renders identically and a real `left_click_drag`
placed the tray item into a slot. See [[ios-ui-verify-on-simulator]] for the seed technique;
[[device-feel-gate-round2]] for the original softlock fix (06771cf) this layout-completes.
