---
name: apollonia-design-direction
description: "Visual/brand direction and hard \"avoid\" list for Apollonia Events UI"
metadata: 
  node_type: memory
  type: project
  originSessionId: 20921973-35dd-49e8-a651-efd709be5e50
---

Apollonia Events design language: modern luxury inspired by Ancient Greek aesthetics, NOT cliché.
Feel: elegant, calm, premium, spacious, handcrafted.

Use: symmetry, marble/stone surfaces, Aegean blue, antique gold, ivory/white, olive details,
subtle Greek-key accents (sparingly, as thin rules — never wallpaper), elegant serif headings,
generous spacing.

Hard AVOID list (user explicit): cheesy mythology, cartoon gods, Spartan helmets, parchment look,
overused columns, generic AI-looking UI.

Palette + type are defined as tokens (Tailwind theme + DESIGN.md) so polish is systematic.
The public site + reservation form are where the brand is won; admin is a clean tool, not precious.
See [[apollonia-stack]].

As of July 2026 (phase 2, brief in DESIGN-UPGRADE-BRIEF-2.md at repo root):
- Public site copy is ALBANIAN (formal "ju", elegant/spare); admin + internal emails stay English.
  Dates use date-fns `sq` locale. Brand story ties to Apolonia e lashtë (ancient city near Fier).
- Button system: `.btn` (h-12) / `.btn-sm` (h-11) pill recipes in globals.css — no padding-sized pills.
- One extra ornament allowed: `<TempleLine>` engraved-line glyph, ONLY for loading/empty/404 states
  (max 72px, stroke-only) — the exception negotiated against the "overused columns" avoid rule.
- Design passes are implemented by Codex from brief files; Claude writes the briefs + guardrails.
- Phase 3 brief (DESIGN-UPGRADE-BRIEF-3.md): free-Saturdays strip, /venue heritage band with
  engraved Adriatic coastline (one-off artifact), time-based "dusk mode" (whisper-subtle),
  WhatsApp link + FAQ accordion on /reserve, next/og share cards, gallery→lightbox morph.
  Explicitly rejected: splash screens, custom cursors, chat widgets, map/Instagram embeds.
