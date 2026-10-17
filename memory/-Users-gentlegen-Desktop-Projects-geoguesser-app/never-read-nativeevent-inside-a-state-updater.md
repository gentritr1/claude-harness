---
name: never-read-nativeevent-inside-a-state-updater
description: "RN recycles layout/touch events — reading event.nativeEvent inside a setState updater crashes later, not at the call site"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-09-30T16:11:21.692Z
---

React Native nulls `event.nativeEvent` once the handler returns. A functional state updater runs
later, during React's render pass, so this crashes the app:

```tsx
onLayout={e => setX(prev => ({ ...prev, w: e.nativeEvent.layout.width }))}   // TypeError: … 'layout' of null
```

Capture the number in the handler, let the updater close over it:

```tsx
onLayout={e => { const w = e.nativeEvent.layout.width; setX(prev => ({ ...prev, w })) }}
```

Shipped on feat/next-level in 67992ab (E3-2) and killed the app on **every round start** —
`FATAL EXCEPTION: mqt_v_native` at GameHud. It survived a task review, a re-review, tsc, 521 tests,
`npm run check` and a QA build, and wasted a full B1-3 device run plus ~10 days of the owner's QA
time on an unplayable APK. The sibling handler three lines above it captured the value correctly,
so the file contained both the right and the wrong pattern.

**Why:** every headless gate in this repo is blind to it — the crash needs a real event object that
gets recycled, which only a device or a test that *simulates recycling* produces. Type-checking
cannot see it either: `nativeEvent` is typed non-null.

**How to apply:**
- Grep `set[A-Za-z]+\((previous|prev|p) =>.*nativeEvent` before shipping any handler change; it must
  return nothing. Same rule for `onTextLayout`, `onScroll`, `onContentSizeChange`, gesture events.
- Put the handler in a pure module and test it with an event whose `nativeEvent` is set to null
  *after* the handler returns but *before* the updater runs — that is the only test that fails on
  the bug. `src/utils/hudMeasure.ts` + `tests/hud-measure.test.ts` are the template.
- Any sub-unit that edits a screen's layout/measurement path must launch the app and reach the
  screen before it can be called done. "Tests pass and the APK builds" never covered this.
- Verify a QA APK actually plays one full round before handing it to the owner.

Related: [[device-and-web-qa-harness-traps]], [[reduced-motion-delayed-entering-hides-view]],
[[next-level-execution-paused]].
