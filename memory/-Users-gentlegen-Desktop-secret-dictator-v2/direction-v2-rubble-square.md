---
name: direction-v2-rubble-square
description: Owner pivot on 2026-09-05 from the fairy-tale half-timber square to a 1946 German rubble-years town, run with the FUTURISMA art workflow; where the brief and mood frames live and the content rules
metadata:
  type: project
---

On 2026-09-05 the owner asked for Secret Dictator to be polished "the way FUTURISMA is", with a post-WW2 Germany setting. The style bible's principles stay (warm scarce = attention, dark blue never black, silhouette-first citizens, toy-theatre staging, three lighting states); the setting and palette move to 1946.

Files: `docs/briefs/RUBBLE-SQUARE-ART-PASS.md` (self-contained Codex brief, six phases, acceptance), `design/concepts/rubble/` (four FLUX.2 mood frames + README with the GPT Image 2 sheet/hero templates + generation.json). Both were uncommitted when written.

Measured starting point: every shipped asset has 0 textures (flat vertex colour), grey sky, blocky 1.2k-tri citizens; systems, sockets, gates all work. Same defect FUTURISMA had before its painted-atlas pass.

**Why:** the workflow that fixed FUTURISMA (GPT Image 2 count-exact sheets → hero → material-ID → Blender MCP → painted 1024 atlases → fixed-camera acceptance) transfers directly; Codex has GPT Image 2 only, the orchestrator runs Higgsfield for mood frames.

**How to apply:** hard content rule for every asset and every generated frame: no swastikas, SS runes, eagle-and-wreath, real party names/slogans, real flags or persons; fictional stamps only; a `test/content.test.js` grep gate is part of the brief. Review = re-measure warm% with the project's own classifier on a worktree at the branch point first (see [[warm-budget-and-anti-tell]]), then the silhouette 8/8 test and hero-versus-model five details. Dev server for the Browser pane: launch config `secret-dictator` on port 5300 in the futurisma repo's .claude/launch.json; `npm ci` was needed (node_modules were absent).
