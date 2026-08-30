#!/usr/bin/env bash
# Install/repair writing + humanize skill symlinks from catalog/writing/.
# Does NOT clone; catalog is filled separately. Soft-links only.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CATALOG="${MATH_MODELING_SKILLS_CATALOG:-$HOME/Projects/FullStack/math_modeling_skills_catalog}"
WRITING="$CATALOG/writing"
MM="${MATH_MODELING_CONTEST_REPO:-$HOME/Projects/FullStack/math_modeling2026}"

if [ ! -d "$WRITING" ]; then
  echo "FATAL: writing catalog missing: $WRITING" >&2
  exit 1
fi

link_into() {
  local dest_root="$1"
  local ext="$dest_root/writing-skills"
  mkdir -p "$ext"

  # name|relative-path-under-writing/
  # H = English humanize / stop-slop; Z = 中文 Humanizer-zh / 说人话
  # A = academic / paper writing pipeline
  declare -a MAP=(
    # --- H: English humanize / de-slop ---
    "H-blader-humanizer|blader-humanizer"
    "H-stop-slop|hardikpandya-stop-slop"
    "H-jpeggdev-humanize-writing|jpeggdev-humanize-writing"
    "H-YKehinde-humaniser|YKehinde-humaniser"
    "H-aihxp-humanizer|aihxp-humanizer"
    "H-WhimseyAI-humanizer|WhimseyAI-humanizer-skill"
    "H-Skillproofdev-text-humanizer|Skillproofdev-text-humanizer"
    "H-199-humanise-text|199-humanise-text-skill"
    "H-timolabs-humanize|timolabs-claude-humanize"
    "H-lguz-humanize-writing|lguz-humanize-writing-skill"
    "H-gregorymm-humanize-text|gregorymm-humanize-text"
    "H-isatimur-de-slop|isatimur-de-slop"
    "H-kimhons-humanize|kimhons-humanize"
    "H-harshaneel-humanize|harshaneel-humanize"
    "H-lakshitha-ai-humanizer|lakshitha-ai-humanizer-skill"
    "H-glebis-de-ai|glebis-claude-skills/de-ai"
    # --- Z: 中文去 AI 味 ---
    "Z-op7418-Humanizer-zh|op7418-Humanizer-zh"
    "Z-ai-zixun-humanizer-zh|ai-zixun-humanizer-zh"
    "Z-syw2039-humanizer-zh|syw2039-humanizer-zh"
    "Z-RobinZorro86-humanizer-zh-plus|RobinZorro86-humanizer-zh-plus"
    "Z-MrGeDiao-shuorenhua|MrGeDiao-shuorenhua"
    "Z-zhi-ai-lab-shuorenhua|zhi-ai-lab-shuorenhua"
    # --- A: academic / paper (含学术向 humanize) ---
    "A-AIScientists-academic-humanizer|AIScientists-academic-humanizer"
    "A-SyntaxSmith-humanize-paper|SyntaxSmith-humanize-paper"
    "A-celestialdust-humanize-prose|celestialdust-humanize-prose"
    "A-momo2young-humanize-academic|momo2young-humanize-academic-writing"
    "A-crabin-paper-humanizer|crabin-paper-humanizer-skill"
    "A-SNL-UCSB-paper-writing|SNL-UCSB-paper-writing-skill"
    "A-SyntaxSmith-nature-writing|SyntaxSmith-nature-writing-skill"
    "A-huguryildiz-ieee-acm|huguryildiz-ieee-acm-paper-writing"
    "A-borgr-paper-sharpener|borgr-paper-sharpener"
    "A-WenyuChiou-academic-writing|WenyuChiou-academic-writing-skills"
    "A-kgraph57-paper-writer|kgraph57-paper-writer-skill"
    "A-lishix520-academic-paper|lishix520-academic-paper-skills"
  )

  local ok=0 miss=0
  for item in "${MAP[@]}"; do
    name="${item%%|*}"
    src_rel="${item##*|}"
    src="$WRITING/$src_rel"
    if [ -e "$src" ]; then
      ln -sfn "$src" "$ext/$name"
      echo "LINK $ext/$name"
      ok=$((ok + 1))
    else
      echo "SKIP $name (missing $src)"
      miss=$((miss + 1))
    fi
  done

  if [ -f "$ROOT/writing-skills/README.md" ] && [ "$dest_root" != "$ROOT" ]; then
    cp -f "$ROOT/writing-skills/README.md" "$ext/README.md"
  fi
  echo "→ $dest_root/writing-skills: linked=$ok missing=$miss"
}

link_into "$ROOT"
if [ -d "$MM" ]; then
  link_into "$MM"
else
  echo "Contest repo not found: $MM (skipped)"
fi

echo "Done. Catalog writing entries: $(ls -1 "$WRITING" | wc -l | tr -d ' ')"
