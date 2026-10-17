---
name: gallery-is-one-art-exhibition
description: Every photo on the live site comes from a single art-exhibition opening; there is not one wedding photograph, and /events has no photos at all
metadata:
  type: project
---

Verified 2026-09-09 by fetching the live pages (`curl` + reading alt text):
- `/gallery` shows **13 Cloudinary images**, all with real descriptive Albanian alt text.
- `/venue` shows **4**. `/events` shows **ZERO** photographs (only 2 logo badges).
- Every one of those photos is from the venue's **first event: the collective art exhibition
  "Kujtesë e Vlerave artistike"** by local artists. Alt text describes paintings on walls,
  visitors photographing artworks, a buffet table, a balloon arch, sound equipment.

**Why this matters:** the site sells Dasma (weddings), Darka private, Festime and Evente
korporative, and has **not one photograph of any of them**. A family shopping for a wedding
venue lands on what looks like an art show. No amount of animation or ornament fixes this — it
is plausibly the highest-leverage problem on the site.

**How to apply:** any proposal that depends on photography must state whether the venue actually
has it. Before promising a visual upgrade, ask the owner what shoots exist or are planned. The
room's own selling point per the owner is its **ceiling, worked as an artwork** — currently not
featured anywhere. See [[venue-ground-truth]].
