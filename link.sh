#!/bin/bash
# Link the ~/.claude harness to this repo. Safe to re-run.
# - On a Mac that has the real files: copies each into the repo, checks it with diff -r,
#   keeps the original as <name>.bak-<date>, and puts a symlink in its place.
# - On a new computer: creates the symlinks from the repo.
# - Later runs adopt any new project memory folder Claude has created since.
# Never touches settings.json, plugins or transcripts.
set -uo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
C="$HOME/.claude"
B=".bak-$(date +%Y-%m-%d)"
fail=0

adopt() { # $1 = path under ~/.claude, $2 = path in this repo
  local src=$1 dst=$2
  if [ -L "$src" ]; then
    [ "$(readlink "$src")" = "$dst" ] || { echo "SKIP  $src already links to $(readlink "$src")"; }
    return
  fi
  if [ -e "$src" ]; then
    if [ -e "$dst" ]; then echo "STOP  both exist, merge by hand: $src  $dst"; fail=1; return; fi
    mkdir -p "$(dirname "$dst")"
    cp -a "$src" "$dst" || { echo "FAIL  copy $src"; fail=1; return; }
    if ! diff -r "$src" "$dst" >/dev/null; then
      rm -rf "$dst"; echo "FAIL  copy of $src differs (written to while copying?); re-run"; fail=1; return
    fi
    mv "$src" "$src$B" || { echo "FAIL  backup $src"; fail=1; return; }
  elif [ ! -e "$dst" ]; then
    return
  fi
  mkdir -p "$(dirname "$src")"
  ln -s "$dst" "$src" && echo "LINK  $src -> $dst"
}

adopt "$C/CLAUDE.md" "$R/CLAUDE.md"
adopt "$C/process-metrics" "$R/process-metrics"
adopt "$C/agents" "$R/agents"
adopt "$C/skill-updates" "$R/skill-updates"

# Project memory: repo -> links, then adopt real non-empty folders not yet in the repo.
for d in "$R"/memory/*/; do
  [ -d "$d" ] || continue
  n=$(basename -- "$d")
  adopt "$C/projects/$n/memory" "$R/memory/$n"
done
for d in "$C"/projects/*/memory; do
  [ -L "$d" ] || [ ! -d "$d" ] || [ -z "$(ls -A "$d")" ] && continue
  adopt "$d" "$R/memory/$(basename -- "$(dirname -- "$d")")"
done

exit $fail
