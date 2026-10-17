---
name: art-skins-08-review
description: ART-SKINS-08 (cuter launch skins) review 2026-10-02 — approved as look check; emulator opening numbers unusable when Classic OFF itself runs 6x slower; open look findings
metadata:
  node_type: memory
  type: project
  originSessionId: 529758e6-3b29-4422-a19a-51e6c72a0675
  modified: 2026-10-02T09:15:57.700Z
---

ART-SKINS-08 was reviewed 2026-10-02 and APPROVED as a default-OFF look check and as the content of the vc11 phone test build. Docs and tooling are in commit 4cdfe49. The code lives in artifacts/ART-SKINS-08/patches/skin-code-on-a4fa166.patch (apply alone on a clean tree; do not stack 07/07b).

- **What changed:** eight polish skins (Cinnamon, Sherbet, Candy Gloss, Jelly, Critter, Rainbow, Campfire, Strawberry) got rim .48 / body .425, head half-width .44 with .10 corner fillets, eye radius .045, a caterpillar Critter (beads .52 at .5 pitch over a .30 tube) and a play-area tint per skin. K8 now allows a face on one-cell arrows for head-anchored faces only (owner ruling changed 2026-10-02).
- **Opening numbers are unusable:** ON medians 143–407 ms, but Classic OFF was 31–48 ms versus 5–9 ms in ART07 (11.8 GB swap, load 9–25).
  - Pattern: a paired benchmark whose control arm itself moved 6x between rounds.
  - Detection rule: compare the control arm with the previous round before reading the treatment arm.
  - Brief update: stop emulator opening measurements; the owner's phone is the instrument.
- **ART07's 316-pixel OFF failure is explained:** in ART08 base/base and base/OFF are identical and hash the same as ART07's OFF capture, so ART07's base capture was the odd one. The null control from [[art-skins-07-review]] worked.
- **Owner look findings, pending:** eyes sit on the roll spiral (Cinnamon/Strawberry); Critter shine runs into the face; heads look stubbier; Archery's pale fletch is faint on light.
- **Open risks:** possible blank tinted board for a moment at level open; a picker choice reverted after a hard emulator shutdown (cause unproven); skinDiagnostic logs still fire in picker builds.

Related: [[art-skins-07-review]], [[shared-host-contention]], [[range-inside-range-criterion-invalid]]

**2026-10-02 owner ruling:** the skins were APPROVED after the Play test builds vc11/vc12. The exact patch is merged in commit c6f9b98 behind EXPO_PUBLIC_META_SKIN_PICKER (default OFF). Play builds turn it on through the build environment. Still open: phone performance numbers, skinDiagnostic logs in picker builds, and the shutdown-revert report.
**2026-10-02:** the skinDiagnostic log finding is FIXED and pushed (44642bb). Logs are opt-in via the artSkinProcedural extra or `setprop log.tag.ArtSkin DEBUG`, verified on emulator-5556. The app on 5556 is now versionCode 6 (a test APK installed with -d), so later installs need `-d`.
