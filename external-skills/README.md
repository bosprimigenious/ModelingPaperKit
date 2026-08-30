# 外部数模 Skills（参考军火库）

本目录**不覆盖**仓库自有 `skills/cumcm-*` / `skills/modeling-paperkit`。  
内容为指向本地 catalog 的**符号链接**（真源在 `~/Projects/FullStack/math_modeling_skills_catalog/`）。

安装/修复链接：

```bash
# 从 ModelingPaperKit 或 math_modeling2026 根目录
bash scripts/install_external_skills.sh
```

## 布局与维度

| 目录 | 上游 | 维度（为何装） |
|------|------|----------------|
| `01-xiaoma-math-modeling-skill` | XiaoMaColtAI/math-modeling-skill | 社区热度 |
| `02-yushui-MathModel-Skill` | yushui2022/MathModel-Skill | 证据 / 门禁叙事 |
| `03-lupynow-math-modeling-skills` | Lupynow/math-modeling-skills | 算法 / 知识库 |
| `04-handsomeZR-mathmodel-skill` | handsomeZR-netizen/mathmodel-skill | 同行引用 + 多 harness 状态 |
| `05-xuec699-math-modeling-skills` | xuec699-sudo/math-modeling-skills | 证据门禁 + 吸收 01/04 的合成编排 |
| `06-automcm-pro` | RealSeaberry/AutoMCM-Pro | 自动化（高风险，慎用） |
| `07-ez-math-model` | woodfishhhh/EZ_math_model | 自动化流水线 |
| `08-mathodology` | sweetcornna/mathodology | 多赛事 skills 包 |
| `09-wuxinbo-Math-model-skills` | WuXinbo-bo/Math-model-skills | 重型全流程（体积大） |
| `10-vectorac-math-modeling-skill` | VectorAC/math-modeling-skill | 教学克制（人选型） |
| `11-ailcs-math-modeling.skill` | ai-lcs/math-modeling.skill | 轻量端到端 |
| `12-gdl1605-MCM.skill` | gdl1605/MCM.skill | 薄工作流 / 读题拆题 |

## 使用原则

1. **自有门禁优先**：`check_prose_style`、`check_model_fitness`、`preflight`、自有 `cumcm-*` 为终裁。  
2. **赛时只启用一套外部主编排**，不要 12 套同时自动触发。  
3. 外部 skill 提供流程/算法/证据结构**参考**，不替代当届官方规则与真实计算结果。  
4. 符号链接不进 git（见 `.gitignore`）；团队成员各自跑 `install_external_skills.sh`。

## 推荐启用组合（国赛）

```text
主编排参考: 01-xiaoma 或 04-handsomeZR / 05-xuec699
证据结构:   02-yushui
算法速查:   03-lupynow
教学刹车:   10-vectorac（防 AI 代选模型）
终裁:       本仓 skills/ + scripts/check_*.py
```
