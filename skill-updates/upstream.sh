#!/bin/bash
# Daily check of each skill's ORIGINAL repo (upstream.txt): new commits, or the path renamed/removed.
# The catalog copies can lag their originals for weeks, so check.sh alone can't tell you a skill is
# stale. Notifies once per new upstream commit; the baseline is the last commit you were told about.
set -eo pipefail
export PATH="/usr/bin:/bin:/usr/sbin:/sbin"

HOME_DIR="${SKILL_UPDATES_HOME:-$HOME/.claude/skill-updates}"
STATE="$HOME_DIR/state"; NOTIFY="${NOTIFY:-1}"
mkdir -p "$STATE" "$HOME_DIR/reports"
log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $*"; }

PARSE=$(cat <<'PY'
import json, sys
c = json.load(sys.stdin)
if c:
    m = c[0]["commit"]
    print(c[0]["sha"], m["committer"]["date"][:10], m["message"].splitlines()[0][:80])
else:
    print("MISSING")
PY
)

# GitHub GET. Uses the signed-in gh CLI when present (5,000 req/h), else anonymous curl (60 req/h).
# Prints the body; returns 4 for HTTP 404, 1 for any other failure.
GH=/opt/homebrew/bin/gh; tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
api() {
  if [ -x "$GH" ]; then
    if "$GH" api "$1" 2>"$tmp/err"; then return 0; fi
    grep -q 'HTTP 404' "$tmp/err" && return 4
  fi
  local code; code=$(curl -sS --max-time 30 -o "$tmp/body" -w '%{http_code}' "https://api.github.com/$1") || return 1
  [ "$code" = 404 ] && return 4
  [ "$code" = 200 ] && cat "$tmp/body" && return 0
  return 1
}

findings=(); errors=0
while read -r skill repo path renamed; do
  case "$skill" in ''|\#*) continue ;; esac
  # Commit history still lists a deleted path (its last commit is the deletion), so test existence first.
  rc=0; api "repos/$repo/contents/$path" >/dev/null </dev/null || rc=$?
  if [ "$rc" = 4 ]; then latest=MISSING
  elif [ "$rc" != 0 ] || ! latest=$(api "repos/$repo/commits?path=$path&per_page=1" </dev/null | /usr/bin/python3 -c "$PARSE"); then
    errors=$((errors + 1)); log "WARN: could not query $repo/$path"; continue
  fi
  sha=${latest%% *}; base=$(cat "$STATE/upstream.$skill" 2>/dev/null || true)
  [ "$sha" = "$base" ] && continue
  if [ "$sha" = MISSING ]; then
    findings+=("- **$skill**: no longer exists at \`$repo/$path\`. ${renamed:+Upstream renamed it to \`$renamed\`. }Your copy will not receive upstream fixes; switch to the upstream skill.")
  elif [ -n "$base" ]; then
    findings+=("- **$skill**: upstream changed on ${latest#* }  (\`$repo\`, commit ${sha:0:10}). The catalog copy may not include it yet.")
  else
    log "baseline: $skill at ${sha:0:10}"   # first sight: record silently
  fi
  echo "$sha" > "$STATE/upstream.$skill"
done < "$HOME_DIR/upstream.txt"

if [ ${#findings[@]} -gt 0 ]; then
  report="$HOME_DIR/reports/$(date +%Y-%m-%d)-upstream.md"
  { echo "# Upstream changes to your skills ($(date +%Y-%m-%d))"; echo; printf '%s\n' "${findings[@]}"; } >> "$report"
  log "UPSTREAM: ${#findings[@]} finding(s) → $report"
  [ "$NOTIFY" = 1 ] && /usr/bin/osascript -e "display notification \"${#findings[@]} skill(s) changed at their original source. Ask Claude to review skill updates.\" with title \"Claude skill updates\"" || true
elif [ "$errors" -eq 0 ]; then
  log "OK: no upstream changes"
fi

# A failing check must not fail silently forever: notify on the 3rd consecutive failing day.
if [ "$errors" -gt 0 ]; then
  n=$(( $(cat "$STATE/upstream_failures" 2>/dev/null || echo 0) + 1 )); echo "$n" > "$STATE/upstream_failures"
  log "ERROR: $errors of the upstream queries failed (consecutive failing runs: $n)"
  [ "$n" -eq 3 ] && [ "$NOTIFY" = 1 ] && /usr/bin/osascript -e 'display notification "Upstream skill check has failed 3 runs in a row. See ~/.claude/skill-updates/logs." with title "Claude skill updates"' || true
  exit 1
fi
echo 0 > "$STATE/upstream_failures"
