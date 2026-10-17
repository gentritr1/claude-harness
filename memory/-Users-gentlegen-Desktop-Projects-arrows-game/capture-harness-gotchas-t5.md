---
name: capture-harness-gotchas-t5
description: POLISH-T5 (2026-09-24) capture/build gotchas - zsh glob abort skips Metro cache clear; screenrecord VFR frame-at-time; home screen never idles for uiautomator; Ink Night colour metric
metadata:
  type: project
---
- zsh: `rm -rf $TMPDIR/metro-* $TMPDIR/haste-map-*` aborts entirely on a no-match glob -> Metro cache NOT cleared, silently. Use `find ... -exec rm` and print remaining count (artifacts/POLISH-T5/scripts/build.sh).
- screenrecord is variable-frame-rate: `ffmpeg -ss t` gives the first frame AFTER t, not the one on screen at t (showed a blank hand-off frame as "+150 ms"). Select last pts <= t.
- `uiautomator dump` fails "could not get idle state" on the home screen; Play is at (720,1925), theme toggle (1300,209) on 1440x3120. Game screen dumps fine.
- Colour classifier "mean of strongest px vs bg" breaks in Ink Night (stray near-white neighbour px outrank rose); use per-pixel nearest-class majority. Positive control for pixel diffs: flag ON vs OFF after a mark = 5994 px.
- Clean HEAD baseline without git checkout: tar-backup modified files, `git show HEAD:f > f`, gradle build, untar, compare `git diff | shasum` before/after.
- W2-09 (2026-09-26): on a loaded host (load ~10) one screenrecord session produced 17 frames in 20.9 s with 300-400 ms injected taps — always check frame count per capture before analysing; `uiautomator dump` can also return nothing mid-series (T11 s3blocked aborts "NOT AT LEVEL 1 START") — re-run that one run. Colour "settled within floor" cannot resolve heart->missed-mark (~67 RGB vs ~10 RGB H.264 floor); use ink-settling taps (T6 arrow 38) for phase-pinned colour criteria. Reduced-motion heart frames are the same-build colour reference (measured Daylight heart = (232,75,125), not #E4327D).
