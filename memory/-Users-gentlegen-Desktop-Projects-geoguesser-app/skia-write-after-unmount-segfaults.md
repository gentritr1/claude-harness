---
name: skia-write-after-unmount-segfaults
description: Skia 2.2.12 SIGSEGV in RNSkJsiViewApi::setJsiProperty when a UI-thread worklet writes to a Canvas whose native view is gone; 4307 green tests and 3 reviews missed it
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-08T08:48:23.806Z
---

ART-4b d3401e0, 2026-10-08 10:45 on the Pixel_8_Pro AVD: `Fatal signal 11 ... null pointer dereference` in librnskia `RNSkJsiViewApi::setJsiProperty` lambda <- `ViewRegistry::withViewInfo` <- libworklets <- hermes, on the main thread. It came ~200 ms after `[globe] spin skip why=notReady missing=warm`: an entrance layer had skipped and unmounted. Earlier "app back on the launcher, no log line" moments in the same flow were probably the same crash. The crash and context are in docs/plan/evidence/art-4b/crash-1045/.

**Why:** dispose() is a native no-op, and Skia's view registry is not null-safe. Any shared-value write that reaches a Canvas after (or racing) its unmount derefs a dead view. Headless fakes cannot segfault, so every test and review passed. This is the same class as [[never-read-nativeevent-inside-a-state-updater]].

**How to apply:**
- Skia Canvas unmount = stop the UI frame callbacks and mappers first, ack from the UI thread plus one frame, THEN let React unmount.
- Test fakes must THROW on a write to an unmounted Canvas.
- Device harnesses check `logcat -b crash` for the app after every step and clear it at the start.
- A "the app went to the launcher" observation is a crash until proven otherwise.

**Variant (2026-10-08, ART-4c v2): unmount by REPARENT.** The return Skia layer was rendered inside each hero variant (`'layer'` View, `'settled'` View, and the `'off'` EnteringView, whose settle swaps Animated.View for View). So a hero variant change, a key change, or an EnteringView settle silently remounts the native layer with no stop -> ack. A full review plus a re-review missed it; I found it while merging.

Rule: for any native/Skia layer driven from a worklet, write down its tree position. Every ancestor between it and a stable parent must be unable to change element type, key or parent. A test must trigger every ancestor change mid-animation and assert the same instance and the same native view.
