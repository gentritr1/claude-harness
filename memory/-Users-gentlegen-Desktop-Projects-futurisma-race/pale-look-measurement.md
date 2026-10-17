---
name: pale-look-measurement
description: "The measured cause of FUTURISMA looking \"pale\" — no highlights at all, and the render halving its own textures' chroma (2026-09-09)"
metadata: 
  node_type: memory
  type: project
  originSessionId: 662a742d-ce8a-498d-8dae-4a833d439e98
  modified: 2026-09-09T14:35:43.339Z
---

The user said the game "looks pale". Measured it instead of guessing, with `scripts/visual/grade/measure-frames.py` (Pillow+numpy; BT.709 luma, HSV sat, **CIELAB chroma**, luma percentiles, black/white pixel share). Use CIELAB chroma, not HSV saturation — HSV reads dark tinted pixels as fully saturated and made Polarity/Tideline look colourful at 158 when their real chroma is 11-13.

**Two measured facts, 16 frames, every circuit:**

| | shipped game | approved concept refs |
|---|---:|---:|
| whitePct (>239) | **0.00 on every frame** | 0.4 – 3.3 |
| p99 luma | 94 – 201 (Ascension stations mean 183) | 220 – 254 |
| CIELAB chroma | 6.3 – 12.8 (mean 9.5) | jungle atlas source **18.7** |

1. **The world never reaches white.** Not one pixel above 239/255 in 16 frames across 5 circuits. Tideline's brightest 1% is under 37% grey.
2. **The render halves the chroma of its own art.** Source atlas textures measure chroma 18.7; the rendered world measures 9.5.

So "pale" is a *highlight-range and material-response* problem, not a saturation-slider problem. The approved painted hero (`device-road-pair-v3/pair-1-A.png`) is itself only chroma 9.3 — the concepts read rich because of **range** (p99 254) and specular, not because of saturation.

**How to set any target here:** measure the concept references with the same script and quote the delta. Never write a chroma/contrast target that was not produced by this instrument — see the §6 red flag about numbers never computed from live data.

Related: [[hud-integration-scars]], [[higgsfield-asset-pipeline]], [[p20-ambience-program]].
