---
name: user-music-taste
description: "The user wants FUTURISMA's soundtrack to be real, vintage 90s jungle / old-school drum and bass, not the synthesised stems; personal-use copies from YouTube are fine, never committed"
metadata: 
  node_type: memory
  type: user
  originSessionId: 987a7b69-2aad-4112-9a77-dcd9cd894d02
  modified: 2026-09-04T19:12:44.790Z
---

The user wants **real music tracks** in FUTURISMA, and the genre is **old / vintage drum and bass and jungle** (93–99 era: old-skool jungle, intelligent/atmospheric DnB, techstep). When I searched "2025 mixes" on 2026-09-04 they answered "why 2025 i want old vintage?". They had told me the genre before and it was lost in a context reset, which annoyed them.

Copyright: they said it is personal use, "don't worry about copyright". Rule I follow: the files stay local and gitignored (`public/assets/audio/music/`), the public GitHub repo never carries a track.

**Why:** the synthesised 174 BPM F-minor stems (STEM_GAIN < 0.1 through a 2100 Hz low-pass) read as a hum, not music; the user reported "there is no music".
**How to apply:** any soundtrack work = vintage jungle/DnB mixes via `scripts/music-import.mjs` (yt-dlp + ffmpeg loudnorm), see [[p20-ambience-program]] and [[futurisma-architecture-facts]].
