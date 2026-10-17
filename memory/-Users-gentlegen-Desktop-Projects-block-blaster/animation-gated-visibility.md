---
name: animation-gated-visibility
description: "Lost tray pieces" investigation 2026-09-08 — emulator repro was a harness false positive; hardening (useSettle + tree swap) kept and verified for the reveal-vs-pause race; real-device cause unconfirmed
metadata:
  type: feedback
---

**What actually happened (corrected 2026-09-08):** the first "reproduction" of missing tray pieces on the Pixel 8 Pro emulator was a **harness artifact**: `adb shell sh -c "input tap …; input keyevent HOME"` never delivered the placement tap, so the tray legitimately held one (still-selected) piece and the redeal never occurred. Instrumented logs (no `deal N` render line) exposed it. A second false lead: my "floating piece" pixel scan included board cells. Lesson: **before fixing a repro, prove the expected state transition happened (logs/state), and make the harness's negative space explicit** — an unexpected "Shape selected" label was the tell.

**What is true:** (1) with a corrected harness (direct tap, 200 ms, HOME) the redeal reveal *was* in flight when the app paused; JS timers did NOT fire during the ~4 s background, and the AppState-active fallback in `src/animation/useSettle.ts` settled all three pieces on resume → 3 visible. Whether the old code would have lost them is unproven (never reproduced on the old build). (2) Views mounted while the app is active always rendered. (3) 20+ moves, 3 redeals, bg/fg cycles, cold restart→RESUME, Play Again restart: no lost pieces. (4) Unplayable pieces were drawn at 0.28 opacity — near-invisible on dim phones and a plausible reading of "pieces not appearing after some time"; raised to 0.45 (`UNPLAYABLE_OPACITY` in DraggableShape).

**Design kept:** reveal animations live in a keyed inner `<DealReveal>` swapped for a plain view on settle (React tree change — immune to any Reanimated prop desync); PlacedBlock and the game-over card use the same swap; ComboPopup/ClearBurst arm an `onDone` fallback.

**Still open:** the user's on-device report (device model / Android version / screenshot unknown). Ask for a screenshot before further changes. Related: [[reanimated-loop-parking]].
