#!/bin/bash
# Daily check: did any skill we installed from agentic-awesome-skills change in a newer release?
# Read-only toward ~/.claude/skills: it never installs. When something changed it writes a report
# under reports/ and posts a macOS notification; review it, then run apply.sh.
#
# Overrides (used by the self-test): SKILL_UPDATES_HOME, SKILLS_DIR, NOTIFY=0, FORCE_RELEASE=<ver>.
set -eo pipefail   # no -u: macOS /bin/bash 3.2 treats empty arrays as unbound
export PATH="/usr/bin:/bin:/usr/sbin:/sbin"

HOME_DIR="${SKILL_UPDATES_HOME:-$HOME/.claude/skill-updates}"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
REPO="https://github.com/sickn33/agentic-awesome-skills.git"
PKG_URL="https://registry.npmjs.org/agentic-awesome-skills"
STATE="$HOME_DIR/state"
NOTIFY="${NOTIFY:-1}"
EXCLUDES=(-x .cache -x .DS_Store -x node_modules)   # runtime droppings (expo-cicd-workflows writes .cache/)

mkdir -p "$STATE" "$HOME_DIR/reports" "$HOME_DIR/logs"
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*"; }
get() { cat "$STATE/$1" 2>/dev/null || true; }
put() { printf '%s\n' "$2" > "$STATE/$1"; }
notify() {
  [ "$NOTIFY" = 1 ] || return 0
  /usr/bin/osascript -e "display notification \"$1\" with title \"Claude skill updates\"" || true
}

# A failing check must not fail silently forever: notify on the 3rd consecutive failure.
on_error() {
  local f; f=$(get failures); local n=$(( ${f:-0} + 1 )); put failures "$n"
  log "ERROR: check failed (consecutive failures: $n)"
  [ "$n" -eq 3 ] && notify "Skill update check has failed 3 days in a row. See ~/.claude/skill-updates/logs."
  exit 1
}
trap on_error ERR

# Hash a skill folder by content and relative path, ignoring runtime droppings.
skill_hash() {
  (cd "$1" && find . -type f ! -path '*/.cache/*' ! -name .DS_Store ! -path '*/node_modules/*' -print0 \
    | LC_ALL=C sort -z | xargs -0 shasum -a 256 | shasum -a 256 | cut -d' ' -f1)
}

SKILLS=$(grep -vE '^[[:space:]]*(#|$)' "$HOME_DIR/skills.txt")
nskills=$(printf '%s\n' "$SKILLS" | wc -l | tr -d ' ')
installed=$(get installed_release)

meta=$(curl -fsS --max-time 30 "$PKG_URL/${FORCE_RELEASE:-latest}")
read -r latest githead < <(printf '%s' "$meta" | /usr/bin/python3 -c \
  'import json,sys;d=json.load(sys.stdin);print(d["version"], d.get("gitHead") or "-")')

if [ -z "${FORCE_RELEASE:-}" ] && [ "$latest" = "$(get last_checked_release)" ]; then
  put failures 0; log "OK: latest is still v$latest (installed v$installed); nothing new"; exit 0
fi

tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
git clone -q --depth 1 --branch "v$latest" --filter=blob:none --sparse "$REPO" "$tmp/repo" 2>/dev/null
head=$(git -C "$tmp/repo" rev-parse HEAD)
if [ "$githead" != "-" ] && [ "$head" != "$githead" ]; then
  log "ERROR: tag v$latest is at $head but npm published it from $githead; refusing to compare"
  notify "Skill update check: release v$latest failed commit verification. Not trusted."
  put failures 0; put last_checked_release "$latest"; exit 1
fi
git -C "$tmp/repo" sparse-checkout set $(for s in $SKILLS; do echo "skills/$s"; done)

changed=(); removed=(); edited=()
for s in $SKILLS; do
  new="$tmp/repo/skills/$s"; cur="$SKILLS_DIR/$s"
  base=$(get "hash.$s")
  if [ -d "$cur" ] && [ -n "$base" ] && [ "$(skill_hash "$cur")" != "$base" ]; then edited+=("$s"); fi
  if [ ! -d "$new" ]; then removed+=("$s")
  elif [ ! -d "$cur" ] || ! diff -rq "${EXCLUDES[@]}" "$cur" "$new" >/dev/null; then changed+=("$s"); fi
done

put failures 0
put last_checked_release "$latest"

if [ ${#changed[@]} -eq 0 ] && [ ${#removed[@]} -eq 0 ]; then
  log "OK: v$latest has no changes to your $nskills skills (installed v$installed)$([ ${#edited[@]} -gt 0 ] && echo "; locally edited: ${edited[*]}")"
  exit 0
fi

stamp=$(date +%Y-%m-%d)
report="$HOME_DIR/reports/$stamp-v$latest.md"
fulldiff="$HOME_DIR/reports/$stamp-v$latest.diff"
: > "$fulldiff"
for s in "${changed[@]}"; do
  diff -ruN "${EXCLUDES[@]}" "$SKILLS_DIR/$s" "$tmp/repo/skills/$s" >> "$fulldiff" || true
done
{
  echo "# Skill updates: v$installed → v$latest ($stamp)"
  echo
  echo "Release commit: \`$head\` (matches npm gitHead: $([ "$githead" = "$head" ] && echo yes || echo 'not published'))"
  echo
  echo "## Changed (${#changed[@]})"
  for s in "${changed[@]}"; do
    echo "- **$s**: $(diff -ruN "${EXCLUDES[@]}" "$SKILLS_DIR/$s" "$tmp/repo/skills/$s" | grep -cE '^[+-][^+-]' || true) changed lines"
  done
  if [ ${#removed[@]} -gt 0 ]; then
    echo; echo "## Removed from the catalog (${#removed[@]}): keep your copy or delete it yourself"
    printf -- '- %s\n' "${removed[@]}"
  fi
  if [ ${#edited[@]} -gt 0 ]; then
    echo; echo "## You edited these locally: apply.sh would overwrite your edits"
    printf -- '- %s\n' "${edited[@]}"
  fi
  echo; echo "## Risk scan of the new versions"
  hits=$(for s in "${changed[@]}"; do grep -rnEi \
    'curl[^|]*\|\s*(ba|z)?sh|wget .*\|\s*sh|rm -rf (/|~)|\.ssh/|\.aws/credentials|base64 (-d|--decode)|ignore (all |previous |prior )?instructions|webhook\.site|ngrok|requestbin' \
    "$tmp/repo/skills/$s" | sed "s#$tmp/repo/##"; done || true)
  echo "${hits:-No risky patterns found.}" | sed 's/^/    /'
  echo; echo "## New or changed scripts (read these in full before applying)"
  scripts=$(grep -E '^\+\+\+ .*\.(sh|js|mjs|cjs|py|ts)\b' "$fulldiff" | sed -E "s#^\+\+\+ $tmp/repo/##; s#\t.*##" || true)
  echo "${scripts:-None.}" | sed 's/^/    /'
  echo; echo "## Diff"
  echo "Full unified diff: \`$fulldiff\` ($(wc -l < "$fulldiff" | tr -d ' ') lines)"
  echo; echo "Apply after review: \`~/.claude/skill-updates/apply.sh $latest\`"
} > "$report"

put pending_release "$latest"
log "UPDATE: ${#changed[@]} changed, ${#removed[@]} removed in v$latest → $report"
notify "${#changed[@]} of your skills changed in v$latest. Ask Claude to review skill updates."
