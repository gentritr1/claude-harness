#!/bin/bash
# Install a reviewed release of the skills listed in skills.txt, then record it as the new baseline.
# Usage: apply.sh [version]   (defaults to the pending release found by check.sh)
set -eo pipefail   # no -u: macOS /bin/bash 3.2 treats empty arrays as unbound

HOME_DIR="${SKILL_UPDATES_HOME:-$HOME/.claude/skill-updates}"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
STATE="$HOME_DIR/state"
ver="${1:-$(cat "$STATE/pending_release" 2>/dev/null || true)}"
[ -n "$ver" ] || { echo "No pending release. Run check.sh first or pass a version."; exit 1; }

skill_hash() {
  (cd "$1" && find . -type f ! -path '*/.cache/*' ! -name .DS_Store ! -path '*/node_modules/*' -print0 \
    | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256 | cut -d' ' -f1)
}

# Only pass skills that still exist in that release; the report lists any that were removed.
available=$(curl -fsS --max-time 60 \
  "https://raw.githubusercontent.com/sickn33/agentic-awesome-skills/v$ver/skills_index.json" \
  | /usr/bin/python3 -c 'import json,sys;print("\n".join(s["id"] for s in json.load(sys.stdin)))')
keep=()
for s in $(grep -vE '^[[:space:]]*(#|$)' "$HOME_DIR/skills.txt"); do
  if grep -qx "$s" <<<"$available"; then keep+=("$s"); else echo "skipping $s: not in v$ver"; fi
done
list=$(IFS=,; echo "${keep[*]}")

echo "Installing v$ver: $list"
npm exec --yes --ignore-scripts --package="agentic-awesome-skills@$ver" -- \
  agentic-awesome-skills --release "$ver" --path "$SKILLS_DIR" --skills "$list"

# Bookkeeping only after the install above succeeded (set -e stops here otherwise).
for s in "${keep[@]}"; do printf '%s\n' "$(skill_hash "$SKILLS_DIR/$s")" > "$STATE/hash.$s"; done
printf '%s\n' "$ver" > "$STATE/installed_release"
printf '%s\n' "$ver" > "$STATE/last_checked_release"
rm -f "$STATE/pending_release"
echo "Done: ${#keep[@]} skills at v$ver. Restart Claude sessions to pick up the new versions."
