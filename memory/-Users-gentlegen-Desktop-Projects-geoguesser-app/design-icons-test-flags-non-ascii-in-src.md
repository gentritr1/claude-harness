---
name: design-icons-test-flags-non-ascii-in-src
description: "tests/design-icons.test.ts flags src characters the Overpass subset can't draw (≈, →, emoji), comments included; em dash and middle dot pass, so it is not an ASCII gate"
metadata:
  node_type: memory
  type: project
  originSessionId: 8af59ba5-d560-4c15-8328-20f7ae41a70b
  modified: 2026-10-04T08:48:42.309Z
---

`tests/design-icons.test.ts` (`symbolsInUiCode`) scans every UI src file, comments included, for characters that are neither ASCII nor in the Overpass subset (`inSubset`). Any it finds must be listed in src/design/icons/inventory.ts.
- Flagged, unless inventoried: "≈", "→" and emoji (B3-1 hit this on 2026-10-02).
- Not flagged: em dash and middle dot, because the subset has them. So the test is NOT an ASCII-only gate. On 2026-10-04 a literal em dash in D1-4 passed the whole suite and only grep caught it.

**Why:** the test guards against glyphs the bundled font cannot render. It does not enforce ASCII.

**How to apply:**
- Briefs keep the "ASCII only in src" convention (escapes like `—`).
- Check it at the controller gate with a perl `[^\x00-\x7F]` scan of added src lines. macOS grep has no `-P`.
- A new emoji needs an inventory entry. Reusing an existing codepoint still needs a site count entry (COPY-1's DROPPED_SYMBOLS).
