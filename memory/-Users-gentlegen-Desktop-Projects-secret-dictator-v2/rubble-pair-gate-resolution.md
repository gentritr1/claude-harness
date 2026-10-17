---
name: rubble-pair-gate-resolution
description: "The frozen-scene warm pair harness has a resolution of a few pixels, so the per-asset zero-allowance gate counts a positive only above 0.001 pp (9 px); a 1-pixel \"failure\" is noise"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: df4dd4c1-38f3-4c2b-8e0b-c496f217dd8b
  modified: 2026-09-06T10:16:34.858Z
---

On 2026-09-06 the ochre facade "failed" the strict zero trial-allowance gate by one scene pixel at one of three frozen instants (83,674 → 83,675 of 921,600). Independent re-runs of an identical swap moved the HUD delta between −2 and −3 pixels, so the harness's own noise is larger than the reported failure. Ruling written into docs/briefs/RUBBLE-SQUARE-ART-PASS.md: a positive counts only above 0.001 percentage points at any instant; smaller positives are recorded verbatim, not rounded and not failed.

**Why:** this is the §6 "threshold compared with no allowance for jitter or measurement resolution" red flag firing again (third project). Codex correctly refused to round the pixel away, which is the right instinct; the gate definition was the defect. Pattern → detection rule → brief update: any gate written as "≤ 0" or "== baseline" on a sampled measurement must state its resolution, measured by repeating the identical comparison, before the first asset is judged against it.

**How to apply:** for every remaining phase-2 and phase-4 asset, read the pair harness's per-instant pixel deltas, apply the 9-pixel tolerance, and treat the full-scene trial number only against the 10% ceiling with its ~0.2-point instant spread. Related: [[rubble-warm-budget-lives-in-dusk]], [[rubble-floor-threshold-unmeasured]].
