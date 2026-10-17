---
name: agent-playbooks-reference
description: Owner's evidence-backed playbooks repo (installed plugin) — which rules apply to the LOMN port and known gaps
metadata:
  type: reference
---
Owner's repo `~/Desktop/Projects/agent-playbooks` = github.com/gentritr1/agent-playbooks (private, v0.2.1, installed as plugin `agent-playbooks`; 10 skills, rule ids PREFIX-NNN). `python3 tools/check-applicability.py <project>` marks rules APPLIES/UNKNOWN.

Applied to LOMN 2026-10-07: TEST-001..006 (red-first + mutants, positive controls beside zeros, perf null+replication, sample reconciliation, runtime-asserted build flags, number provenance), UI-003 (pixel gate null + positive control) and UI-007 (width sweep) added to the REF4/M1b brief, VERC-001..005 for the M6 deploy, PROC-004..007, TOOL-*.

v0.3.0 (7078906, pushed 2026-10-07 with owner's yes): ctx:web now detects non-JS web apps, new ctx:wasm, new skill `binary-and-wasm-porting` PORT-001..005 (oracle re-derivation, measured parser caps, fuzz depth/teeth, headless WebGPU blank canvas, native==wasm32). Open: PORT-001 firing 3 evidence says call order unresolved — update after T4 re-review; PORT-003 deep-reach/bite parts INFERRED until M1a-4 T1 results land in measurements.md. Push: plain `git push` fails (credential.helper=store has no creds); use `git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push`. Every push still needs the owner's yes.
Related: [[lomn-toolchain-gotchas]], [[autonomy-and-knowledge-capture]].
