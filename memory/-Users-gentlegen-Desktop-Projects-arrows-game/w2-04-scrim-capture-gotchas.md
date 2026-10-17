---
name: w2-04-scrim-capture-gotchas
description: W2-04 (2026-09-24) level-transition scrim - soak gfxinfo 120-frame cap, test interstitial close, ad-exit reveal vs cover, HOME snapshot cross-fade, zoomed tutorial taps
metadata:
  type: project
---
- Soak `summary.frames.transitions` is pinned at gfxinfo's 120-frame history per window (2393 = 20 x ~120 every run): frame
  counts cannot prove a new effect rendered there; use P-02 captures. Null run A/B/ON x5 = 15 x 23 min.
- Scrim adds a replicated +1 surface 2+-refresh interval per transition (static covered hold), no p95/p99 change above null.
- AdMob TEST interstitial ignores BACK; close = the X at (1357,83) on 1440x3120 after its countdown (never the creative).
- Starting a cover right when the interstitial promise resolves overlaps Android's ad-activity exit reveal (~185 ms): the panel is
  never seen. Fix = wait AppState active + a beat (awaitAdThenPanelBeat).
- HOME inside a ~300 ms transition: on return Android cross-fades the task snapshot (old panel) into the live new level for
  ~100-200 ms (window manager, not app). OFF control shows new level.
- META_ZOOMED_CAMERA opens tutorial T1 zoomed: POLISH-T9 rec.sh tutorial taps fail. Clear tutorials on the fit build, then
  `install -r` the zoomed APK (same debug signer + versionCode 6) to keep progress.
- PERF gradle host versionCode != T9 (6): switching needs uninstall (INSTALL_FAILED_VERSION_DOWNGRADE).
- Mixed-frame detector needs discriminative-pixel residuals for Retry (same board + LEVEL text); positive control via synthetic
  header/board composites (8/10, blind at >= 90 % scrim).
