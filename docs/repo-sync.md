# 双仓同步约定

## 角色

| 仓库 | 角色 |
|------|------|
| **ModelingPaperKit** | 工具真源：`core/`、`templates/`、`scripts/check_*.py`、`scripts/preflight.py`、`skills/cumcm-*`、`skills/modeling-paperkit`、`skills/cumcm-sentence-polish` |
| **math_modeling2026** | 赛题实战仓：`51/`、`bnu/`、`校赛/`、`shared/`、pipeline/pack，以及从 PaperKit 同步来的工具层副本 |

## 改哪里

1. 改模板、引擎、检查器、CUMCM skills → **先改 ModelingPaperKit**
2. 改真实赛题数据、论文正文、建模代码 → **只改 math_modeling2026**
3. 实战仓若做出更好的通用 skill（例如润色规则）→ **回流 PaperKit 后再同步**

## 同步命令

在 ModelingPaperKit 根目录：

```bash
python3 scripts/sync_to_contest_repo.py \
  --dest ../math_modeling2026 \
  --dry-run
python3 scripts/sync_to_contest_repo.py \
  --dest ../math_modeling2026
```

默认同步：

- `core/`
- `templates/`
- `scripts/check_*.py`、`scripts/preflight.py`、`scripts/inspect_template.py`、`scripts/summarize_build_log.py`、`scripts/build.py`、`scripts/clean.py`、`scripts/new_contest.py`、`scripts/check_skill_contract.py`、`scripts/check_prose_style.py`、`scripts/check_claim_coverage.py`、`scripts/sync_to_contest_repo.py`
- `skills/cumcm-*`、`skills/modeling-paperkit`、`skills/cumcm-sentence-polish`
- `docs/2026-cumcm-*.md`、`docs/repo-sync.md`、`docs/getting-started.md`、`docs/template-guide.md`、`docs/faq.md`
- `tests/test_preflight.py`、`tests/fixtures/`（若存在）

**不同步**实战仓独有内容：`51/`、`bnu/`、`校赛/`、`shared/`、`build.py`（根流水线）、`scripts/pipeline.py` 等。

实战仓独有 skill `modeling-agent-orchestrator` 暂留实战仓，不覆盖 PaperKit。

## 验收

两边分别：

```bash
python3 scripts/check_skills.py skills
python3 scripts/check_skill_contract.py skills
python3 scripts/check_prose_style.py --target cumcm
python3 scripts/preflight.py --target cumcm --skip-git-diff-check
```

## External skills

`external-skills/` are local symlinks into `~/Projects/FullStack/math_modeling_skills_catalog/`.
They are **not** synced by `sync_to_contest_repo.py`. Install on each machine:

```bash
bash scripts/install_external_skills.sh
```
