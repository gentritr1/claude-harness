---
name: Reanimated settledProps and rest states (PANEL-STUCK, 2026-09-28)
description: Reanimated 4.5.1 FORCE_REACT_RENDER_FOR_SETTLED_ANIMATIONS syncs the last UI write back into React after your styles and drops it if backgrounded; a rest state needs both halves
type: project
---
- Reanimated 4.5.1 here has FORCE_REACT_RENDER_FOR_SETTLED_ANIMATIONS on: every 500 ms JS copies each view's last UI-thread write (1-2 s old) into AnimatedComponent state `settledProps`, rendered AFTER your styles; entries >2 s old are erased unsynced (app backgrounded).
- So a static "rest" style on an Animated.View that animated loses to a stale mid-leg `settledProps` (W5-19 frozen lose panel: backstop settled mid-leg, detach beat the snap's write), and keeping the animated style attached leaves React props at the first-render values (win panel invisible after HOME right after the settle). Fix pattern: keep attached until a UI-thread double-rAF confirms the snap landed, then swap to static rest.
- Review recipe: probe build forcing the settle mid-leg (EXPO_PUBLIC_PANEL_PROBE_MARGIN_MS=-150 overlay) + background 1.2-2 s after the settle, on device; web never runs the collector.
- Pattern → rule: "fixed" rest-state change verified by forced runs + 60 natural panels still regressed under backgrounding → acceptance loops must include HOME around and right after the settle.
- Harness gotchas: remap-citations.py is not idempotent (restore DESIGN.md/contrastAudit.ts from base first); zsh `$A shell` with A="adb -s …" does not word-split (use an array); PERF-DEADTAG tap points (Play 540,1172 / Gallery 809,1352) miss the menu once META_SETTINGS_SHEET etc. are on (540,1065 / 757,1245 at 360 dp).
