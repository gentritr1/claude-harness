---
name: w4-06-repack-and-harness-gotchas
description: W4-06 (2026-09-25) - git-archive repack loses fonts; RNTL press walks composite onPress; Browser pane resizes mid-batch; 360x640 menu has 21 dp under the pill
metadata:
  type: project
---
- JS repack of an OLD commit from a `git archive` scratch copy with a symlinked node_modules: Metro resolves assets via realpath, so font res names differ and Fredoka silently falls back to the system font (caught only on screenshot). Build BASE by swapping the modified files to `git show <sha>:f` in the working tree, repack, restore, compare `git diff | shasum`.
- RNTL `fireEvent.press` walks up to ANY ancestor element with an `onPress` prop, including composite components: a non-pressable label inside `<X onPress={...}>` "fires". Name non-handler callback props differently (onOpen) and pass them only when active.
- Claude Browser pane can resize mid click-batch (1024x768 -> 632x911 CSS): later clicks land off-plan and blocked taps cost hearts. Re-read the board `<g>` getScreenCTM and "N left" after every batch.
- Menu at 360x640 dp with banner loaded: Play pill bottom 458.7 dp, stats line top 479.7 dp (21 dp). Anything added under the pill needs the column to move (W4-06 used upper marginBottom 56->36).
- HBC bundles embed a source hash: a comment-only change changes bundle_sha256; not usable as an inertness check.
