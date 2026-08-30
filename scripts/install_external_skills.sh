#!/usr/bin/env bash
# Install/repair external math-modeling skill symlinks (community catalog).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
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

# Batch 1
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

# Batch 2 — community / GitHub extras
clone_one https://github.com/zhnnky329/MathModeling-skills.git zhnnky329-MathModeling-skills
clone_one https://github.com/xzwwwwww/Enhanced-mathmodel-Codex-skills.git xzwwwwww-Enhanced-mathmodel-Codex-skills
clone_one https://github.com/Yoki-cmd/math-modeling-single.git Yoki-cmd-math-modeling-single
clone_one https://github.com/jihe520/MathModelAgent.git jihe520-MathModelAgent
clone_one https://github.com/usail-hkust/LLM-MM-Agent.git usail-hkust-LLM-MM-Agent
clone_one https://github.com/LiXiang106991/MathModelAgent.git LiXiang106991-MathModelAgent
clone_one https://github.com/skillforCUMCM/math-modeling-skill-pro.git skillforCUMCM-math-modeling-skill-pro
clone_one https://github.com/y3519712124-ui/math-modeling-contest-route-selection.git y351-route-selection
clone_one https://github.com/capwitf/My-MathModeling-skills.git capwitf-My-MathModeling-skills
clone_one https://github.com/Leionel/math-model-skill.git Leionel-math-model-skill

link_into() {
  local dest_root="$1"
  local ext="$dest_root/external-skills"
  mkdir -p "$ext"
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
    "13-zhnnky329-MathModeling-skills|zhnnky329-MathModeling-skills"
    "14-enhanced-mathmodel-codex|xzwwwwww-Enhanced-mathmodel-Codex-skills"
    "15-yoki-math-modeling-single|Yoki-cmd-math-modeling-single"
    "16-jihe520-MathModelAgent|jihe520-MathModelAgent"
    "17-usail-LLM-MM-Agent|usail-hkust-LLM-MM-Agent"
    "18-lixiang-MathModelAgent|LiXiang106991-MathModelAgent"
    "19-skillforCUMCM-pro|skillforCUMCM-math-modeling-skill-pro"
    "20-y351-route-selection|y351-route-selection"
    "21-capwitf-My-MathModeling|capwitf-My-MathModeling-skills"
    "22-leionel-math-model-skill|Leionel-math-model-skill"
  )
  for item in "${MAP[@]}"; do
    name="${item%%|*}"
    src_name="${item##*|}"
    src="$CATALOG/$src_name"
    if [ -e "$src" ]; then
      ln -sfn "$src" "$ext/$name"
      echo "LINK $ext/$name"
    else
      echo "SKIP $name (missing $src)"
    fi
  done
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

echo "Done. Catalog entries: $(ls -1 "$CATALOG" | wc -l | tr -d ' ')"
