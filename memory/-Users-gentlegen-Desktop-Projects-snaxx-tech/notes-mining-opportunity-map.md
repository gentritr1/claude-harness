---
name: notes-mining-opportunity-map
description: "2026-10-13 mining of 1,021 Apple Notes + 760 Claude memory/project files into ranked business bets; dashboard URL, top picks, redactor gotchas, secrets to rotate"
metadata:
  node_type: memory
  type: project
  originSessionId: 5bb56d09-6e53-4a9f-87a4-708273fd5c90
  modified: 2026-10-12T23:05:31.512Z
---

On 2026-10-13 the owner's Apple Notes (1,021) and Claude memory/project docs (760) were mined for business ideas, prompts, lessons and markets. Private dashboard: https://claude.ai/artifact/NZha8EyA1T9kbAULWDbyyg (source + data in `design/notes-mining/`, reusable redactor in `design/notes-mining/tools/redact.py`).

Ranked bets (lanes): Cash now = Play Deadline RN/Expo upgrade (Play API 36 extension ends 2026-11-01, verified on developer.android.com), Launch-Safe Check for vibe-coded apps, Balkan COD growth package, real-product AI video packs. Build next = Agent Guardrails install (agency), Agent UI verification kit (open-core), scars content series, Play compliance + monetisation leak audit. Own later = AppCare scanner, evidence-gated PR reviewer, COD refusal guard, FJALË diaspora. Parked: RPM/CCM (employer Vianova IP + offshore PHI), PRD→Jira SaaS (saturated), trading bots (regulatory).

**Why:** owner wants SaaS + a problem-solving agency; the thesis is that their measured agent-verification discipline is the moat.
**How to apply:** treat these as the current strategy until the owner picks; open questions (employer IP, AdMob-from-Kosovo contradiction, capacity) are listed on the dashboard's Systems tab.

Owner answers (2026-10-13): Vianova contract ends 2026-10-31 (IP/confidentiality clauses still to check); AdMob runs via the Polish company (Kosovo ban not a blocker); Paddle is the billing route for SaaS only (Paddle AUP excludes human services and trading tools, so agency work is invoiced by the Polish company); clear-scope projects take days to a week. Site is now 7 linked pages (index, now, next, later, markets, library, decisions) built by `build_site.py`; playbooks in `_playbooks.json`; RN offer drafts in `design/notes-mining/rn-deadline/`. 16 KB Play enforcement is 2027-02-01, not now.

Redactor scar (pattern → detection rule → future brief): label-based secret matching missed `NAME_TOKEN=` (underscore defeats `\btoken\b`), dotted Discord tokens and value-before-label lines (`<pw> -> password for mongo`); partial values of a MongoDB password, a Discord bot token and one credential in note 0031 reached subagents → after any redaction pass, run a shape-only residual scan and have readers report leaks before trusting it → owner told to rotate those three plus 11 ROTATE rows in SECRETS-INVENTORY.md. Also: nested-optional regex `(?:\s*\d*[.)]?\s*[a-z]{3,8}){11,25}` hung for minutes on one file; require a mandatory separator.

Related: [[hero-world-within-concept]], [[brand-3d-fresh-direction]]
