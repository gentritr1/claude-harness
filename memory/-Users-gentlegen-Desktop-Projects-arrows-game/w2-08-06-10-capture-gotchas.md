---
name: w2-08-06-10-capture-gotchas
description: "W2-08/W2-06/W2-10 (2026-09-26) - symlinked-node_modules repack (font asset rewrite), sqlite-trigger write counter, zoomed-camera fit origin, pinch focal not kept, arrow ink reaches cell edges, recorder stalls, POLISH-T10 visible vs clock"
metadata:
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-09-26T21:30:20.397Z
---

- JS repack from `git archive HEAD` + SYMLINKED node_modules works if every bundle asset is checked against the host's `aapt2 dump resources` and the 2 Fredoka `httpServerLocation`s are rewritten to `/assets/node_modules/...` (artifacts/W2-08/scripts/repack.sh; menu 0 px vs host). jest in such a tree fails 10 HomeScreen.compose snapshots (testUri path) - run jest in the real tree.
- Count AsyncStorage writes without code: sqlite AFTER INSERT/UPDATE trigger on RKStorage catalystLocalStorage (app force-stopped, chown+restorecon after, drop after). Store coalesces same-task writes.
- W5-03 split the header counter into two Text nodes ("60", " left"): uiautomator readers must take the text before " left".
- META_ZOOMED_CAMERA on: fit centres ABOVE the nav bar (POLISH-T2 bottomInset), so P-02 cellCenterForBoard is 1.25 cells low on level 0; ArrowsWorkload pinch-in does NOT keep the focal point. Register the camera from a screencap (artifacts/W2-10/scripts/reg210.py: occupancy + stroke connections).
- arrowGeometry: tails end 0.492 cell past centre (TAIL_EXT 0.42 + cap), tips ON the cell edge: grown per-arrow masks catch neighbours/blocker; measure motion by template shift on the arrow's own cells.
- Under host load 5-16 the recorder stalls/misses the start of short effects in ~25 % of runs: flag gaps > 40 ms and exit < 60 % of plan, run 5-6 reps, decide on medians.
- POLISH-T10 exits: the clock (up to 1000 ms) != what is seen; use planExit visibleMs (90..187 ms at fit). Harness (validateWorkload/soak) needs a shell-profileable host; none exists with current native -> gradle (>= 5 GB) needed.
