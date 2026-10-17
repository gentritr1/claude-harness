---
name: w5-art-batch-gotchas
description: W5-07/W5-05/W5-14 (2026-09-27) - RN Image source size beats absoluteFill; P-02 tolerance blind to faint effects; pgrep self-match; JS repack cannot add resources; leg-position bias in A/B/A
metadata:
  type: project
---
- RN `<Image source={require(png)} style={StyleSheet.absoluteFill}>` draws at the SOURCE size (256 dp) in the corner: the static source's width/height beat left/right/top/bottom. Add width/height '100%'. Jest passed the broken version; only the emulator capture caught it (W5-14).
- P-02 pixel-diff tolerance (max channel > 24) is BLIND to effects under ~10% opacity (grain 0.08 = max delta 18): use tolerance >2 / luminance std-dev as the positive control.
- `until ! pgrep -f <script>` in a Bash wait loop matches its OWN zsh command line and never ends: wait on a PID (`kill -0`).
- A JS repack cannot add an Android resource: a new require()'d PNG must be routed into an existing host drawable (artifacts/W5-14/scripts/repack514.sh) or needs gradle.
- A brief's "pixel 3 px inside the panel edge" lands on the anti-aliased 1 dp hairline at 560 dpi (3.5 px/dp) and on the fill at 480 dpi: measure hairline (1 px in) and fill (8 px in) separately.
- Emulator RenderThread fast/slow mode in an OFF/ON/OFF A/B/A tracked LEG POSITION (3rd leg fast 6/10 vs 2/10): compare ON with the adjacent leg and report the A/A as the MDE.
- Disk fell 3.9 -> 0.18 GB in minutes while another session ran; `android/app/build` (786 MB) is the only deletable in-repo cache.
