---
name: art-skins-07-review
description: ART-SKINS-07 (15 canvas skins) review 2026-10-02 — approved as default-OFF look check; exact-pixel OFF gate lacks a null control; owner look findings
metadata:
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-10-01T23:00:53.106Z
---

ART-SKINS-07 was reviewed 2026-10-02 and APPROVED as a default-OFF look check. It is not ship-ready. Docs and tooling are in commit a024ba6. The code lives in artifacts/ART-SKINS-07/patches (skin-catalogue-code-on-bad7903.patch, plus the checks and docs patches). Skin ids 3–17 are in canvas order.

- **Opening budget:** 3 pass / 14 fail. The Strawberry max was 884 ms and the Lava max 280 ms, on a host with load 5–27.
- **Exact-pixel OFF gate failed** (316 pixels, mostly one shaft edge off by 1/255). The flag-OFF native path is unchanged when skin == null.
  - Pattern: the gate compared two installs of different APKs with no base-vs-base reinstall control.
  - Detection rule: any exact-pixel cross-APK gate needs a same-APK reinstall null control first.
  - Brief update: future briefs must require that control.
- **Owner look findings, pending:**
  - Archery's orange fletch reads as a backward arrowhead.
  - Ink Pro is ghostly in dark mode.
  - Clear Glass is faint in light mode.
  - Paper Craft's crease looks like a glitch.
- **Minor:** skinDiagnostic logs fire in every picker build. Gate them on openingTraceEnabled.

Related: [[art-skins-01-review]], [[range-inside-range-criterion-invalid]], [[detector-needs-positive-control]]
