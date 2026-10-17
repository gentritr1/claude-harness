---
name: w6-01-mask-rebuild-and-trace-gotchas
description: W6-01 (2026-09-17) blocked-tap mask rebuild is tiny; commit frames are the cost; export/Perfetto/harness gotchas
metadata:
  type: project
---
- Mask rebuild on emulator (3827, 250 arrows): JS build ~0.04 ms median; Fabric UPDATE_PROPS batch holding only the mask <=0.43 ms (upper bound on native setVisibleMask). Blocked frame p95 39-47 ms comes from commit frames (UI ~3.5 + RT ~3.8 ms + GPU wait), not O(n). Direct native Trace capture still BLOCKED on disk (docs/perf-mask-rebuild-2026-09-17.md).
- `npx expo export` after flipping an EXPO_PUBLIC_* var reuses Metro's transform cache: positive control read 0 until `--clear`. Always pair a bundle-absence grep with a positive control.
- Perfetto ftrace events come in per-CPU bundles: sort by timestamp before B/E matching or slices go negative.
- benchmark.mjs force-stops per sample, so "log on unmount" never fires in PERF runs; an idle-flush log is needed.
- Re-tapping a shaking arrow inside the 340 ms window commits nothing (no mount batch) — usable null run.
