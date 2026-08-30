#!/usr/bin/env bash
# Install/repair external math-modeling skill symlinks into this repo and the contest repo.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# Prefer repo root = parent of scripts/
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CATALOG="${MATH_MODELING_SKILLS_CATALOG:-$HOME/Projects/FullStack/math_modeling_skills_catalog}"
MM="${MATH_MODELING_CONTEST_REPO:-$HOME/Projects/FullStack/math_modeling2026}"

mkdir -p "$CATALOG"

clone_one() {
  local url="$1" dir="$2"
  if [ -d "$CATALOG/$dir/.git" ]; then
    echo "EXISTS $dir"
    return 0
  fi
  echo "CLONE $dir"
  git clone --depth 1 "$url" "$CATALOG/$dir"
}

echo "Catalog: $CATALOG"
clone_one https://github.com/XiaoMaColtAI/math-modeling-skill.git XiaoMaColtAI-math-modeling-skill
clone_one https://github.com/yushui2022/MathModel-Skill.git yushui2022-MathModel-Skill
clone_one https://github.com/Lupynow/math-modeling-skills.git Lupynow-math-modeling-skills
clone_one https://github.com/handsomeZR-netizen/mathmodel-skill.git handsomeZR-mathmodel-skill
clone_one https://github.com/xuec699-sudo/math-modeling-skills.git xuec699-math-modeling-skills
clone_one https://github.com/RealSeaberry/AutoMCM-Pro.git RealSeaberry-AutoMCM-Pro
clone_one https://github.com/woodfishhhh/EZ_math_model.git woodfishhhh-EZ_math_model
clone_one https://github.com/sweetcornna/mathodology.git sweetcornna-mathodology
clone_one https://github.com/WuXinbo-bo/Math-model-skills.git WuXinbo-Math-model-skills
clone_one https://github.com/VectorAC/math-modeling-skill.git VectorAC-math-modeling-skill
clone_one https://github.com/ai-lcs/math-modeling.skill.git ai-lcs-math-modeling.skill
clone_one https://github.com/gdl1605/MCM.skill.git gdl1605-MCM.skill

link_into() {
  local dest_root="$1"
  local ext="$dest_root/external-skills"
  mkdir -p "$ext"
  # Keep README if present
  declare -a MAP=(
    "01-xiaoma-math-modeling-skill|XiaoMaColtAI-math-modeling-skill"
    "02-yushui-MathModel-Skill|yushui2022-MathModel-Skill"
    "03-lupynow-math-modeling-skills|Lupynow-math-modeling-skills"
    "04-handsomeZR-mathmodel-skill|handsomeZR-mathmodel-skill"
    "05-xuec699-math-modeling-skills|xuec699-math-modeling-skills"
    "06-automcm-pro|RealSeaberry-AutoMCM-Pro"
    "07-ez-math-model|woodfishhhh-EZ_math_model"
    "08-mathodology|sweetcornna-mathodology"
    "09-wuxinbo-Math-model-skills|WuXinbo-Math-model-skills"
    "10-vectorac-math-modeling-skill|VectorAC-math-modeling-skill"
    "11-ailcs-math-modeling.skill|ai-lcs-math-modeling.skill"
    "12-gdl1605-MCM.skill|gdl1605-MCM.skill"
  )
  for item in "${MAP[@]}"; do
    name="${item%%|*}"
    src_name="${item##*|}"
    src="$CATALOG/$src_name"
    if [ -e "$src" ]; then
      ln -sfn "$src" "$ext/$name"
      echo "LINK $dest_root/external-skills/$name"
    else
      echo "SKIP $name (missing $src)"
    fi
  done
  # Ensure README exists
  if [ -f "$ROOT/external-skills/README.md" ] && [ "$dest_root" != "$ROOT" ]; then
    cp -f "$ROOT/external-skills/README.md" "$ext/README.md"
  fi
}

link_into "$ROOT"
if [ -d "$MM" ]; then
  link_into "$MM"
else
  echo "Contest repo not found: $MM (skipped)"
fi

echo "Done."
