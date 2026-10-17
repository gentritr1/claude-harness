---
name: reanimated-dead-tag-mechanism
description: "PERF-DEADTAG (2026-09-25) - \"synchronouslyUpdateUIProps failed for tag\" is Reanimated re-applying its props registry during the next screen's first draw, not an animation outliving its view; cancel-on-unmount does not fix it"
metadata:
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-09-25T19:40:12.061Z
---

- Mechanism (Reanimated 4.5.1 + RN 0.86, source + emulator-5556): Reanimated keeps the last props of every view it
  animated in the last ~2 s (the settled sweep drops entries 2-2.5 s after the last update; an endless animation never
  leaves). A removed view's entry is dropped only in handleNodeRemovals, which runs from Fabric's reportMount, posted
  AFTER the frame. Every event dispatched during that frame's draw pass (react-native-svg VirtualView.setClientRect,
  one per shape on first draw) triggers performNonLayoutOperations -> re-apply of the whole registry via
  synchronouslyUpdateUIProps -> exception + ~90-line stack per dead tag per event. Flag-independent (pre-POLISH-T8 logs
  W0-02/W0-07/ADMOB-C show it); ANDROID_SYNCHRONOUSLY_UPDATE_UI_PROPS only adds 1 frame-path warning per exit.
- Disproved premise: cancelAnimation in the effect cleanup (the brief's fix) measured 0 change (V1 build); a splash view
  whose animation had FINISHED still failed, and a button pressed 1 s before the exit failed (6 s: not).
- Fix that measured 0 warnings (round 1): App keeps the left screen mounted at opacity 0 until 2 UI rAFs after the
  switch commit, and stops the leaving screen's registered animations with ONE async scheduleOnUI when it starts
  leaving (src/ui/screenHandoff.tsx useStopWhenScreenLeaves). Round 0's runOnUISync-in-layout-cleanup was rejected by
  the controller (JS stall at Next/Retry, deadlock risk). Hand-off ALONE still leaked frame-path warnings at the removal
  frame (splash 8/45, `‹` 3/5): an async stop at leave-start is needed because the hand-off gives >= 1 frame of slack.
- In-screen unmounts (win->Next, lose->Retry, LEVEL_TRANSITION on/off) never warned; lose->Retry harness taps 3
  Board.canExit-false arrows (win-next.py lose mode).
- Detector gotcha: the menu has no svg unless sound is OFF (the ♪ strike) -> transitions INTO the menu are blind with
  sound on; seed arrows_sound_on=0 as the positive control. Tag map: [deadtag] probe hooking
  PropsRegistryGarbageCollector.registerView + React fiber owner chain (artifacts/PERF-DEADTAG/scripts/deadtagProbe.ts.txt).
- Level-1 solver for win->Next at 1080x1920@240 (fit camera even with META_ZOOMED_CAMERA): artifacts/PERF-DEADTAG/scripts/win-next.py,
  calibrated from the dot grid (calibrate.py, 264/264 cells).
- Results (emulator): gallery first frame 56.1->22.5 ms (n=12+12, p=0.0003; replicate 38.7->22.2); game first frame
  not robust (p=0.037 / 0.63). Brief premise ("animation outlives view") and its cancel-in-cleanup fix were WRONG.
- Gotchas: the Browser pane can reopen a STALE page from an earlier session (old bundle, "Disconnected from Metro") -
  prove the served bundle (fetch index.ts.bundle, grep a new symbol) before trusting a web check. ffmpeg
  `-frame_pts 1` on screenrecord output silently overwrites frames that share a rounded pts - extract sequentially and
  read pts with ffprobe. win-next / settle runs change persisted counters (total_solved etc.) - pin them in any pixel
  diff of the menu, and restore the DB at the end.
