#!/usr/bin/env bash
# Install the kit's skills into a project for one or more AI clients.
#   scripts/install.sh [--client claude|copilot|codex|all] [--copy] [TARGET_DIR]
# Default: --client all, symlink, TARGET_DIR = current directory.
# claude  -> TARGET/.claude/skills/<skill>
# copilot -> TARGET/.github/skills/<skill> + TARGET/.github/prompts/<skill>.prompt.md
# codex   -> TARGET/.agents/skills/<skill>   (Agent Skills spec location, also read by Codex/Cursor/Gemini)
set -euo pipefail

client=all
mode=link
target=""
while [ $# -gt 0 ]; do
  case "$1" in
    --client) client="$2"; shift 2 ;;
    --copy) mode=copy; shift ;;
    -h|--help) sed -n '2,7p' "$0"; exit 0 ;;
    *) target="$1"; shift ;;
  esac
done
target="${target:-$PWD}"
kit="$(cd "$(dirname "$0")/.." && pwd)"
target="$(cd "$target" && pwd)"

case "$client" in claude|copilot|codex|all) ;; *) echo "unknown client: $client" >&2; exit 2 ;; esac

place() { # place SRC DEST
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  rm -rf "$dest"
  if [ "$mode" = link ]; then ln -s "$src" "$dest"; else cp -R "$src" "$dest"; fi
  echo "$dest -> $src"
}

for skill_dir in "$kit"/skills/*/; do
  name="$(basename "$skill_dir")"
  [ -f "$skill_dir/SKILL.md" ] || continue
  if [ "$client" = claude ] || [ "$client" = all ]; then
    place "$skill_dir" "$target/.claude/skills/$name"
  fi
  if [ "$client" = copilot ] || [ "$client" = all ]; then
    place "$skill_dir" "$target/.github/skills/$name"
    if [ -f "$kit/.github/prompts/$name.prompt.md" ]; then
      place "$kit/.github/prompts/$name.prompt.md" "$target/.github/prompts/$name.prompt.md"
    fi
  fi
  if [ "$client" = codex ] || [ "$client" = all ]; then
    place "$skill_dir" "$target/.agents/skills/$name"
  fi
done

# The skill calls scripts/ux_radar.py relative to the kit; a copy of the skill needs it too.
if [ "$mode" = copy ]; then
  mkdir -p "$target/scripts"
  cp "$kit/scripts/ux_radar.py" "$target/scripts/ux_radar.py"
  echo "$target/scripts/ux_radar.py -> $kit/scripts/ux_radar.py"
fi
echo "done ($mode, $client) in $target"
