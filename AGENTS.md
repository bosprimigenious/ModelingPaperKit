# ModelingPaperKit — Agent Rules

## Paper body prose (hard)

When writing or editing any contest paper `.tex` (templates or contest packages):

1. **Load before writing**
   - `skills/cumcm-sentence-polish/references/banned-prose.md`
   - `skills/cumcm-sentence-polish/references/style-rules.md`
2. **Never put into 正文**
   - Hollow inference: `根据…可知`、`由…可知`、`由此可见`、`不难发现`、`It can be seen that`
   - Empty connectors: sentence-initial `然而，` / `但是，` / `However,` / `Therefore,` / `Thus,`
   - Stray English filler such as bare `ever`
   - AI praise: `近年来`、`具有重要意义`、`效果较好`、`较为合理`…
   - Instructional meta: `不要…`、`Do not…`、`作为AI`、`我将帮你`
3. **Every result sentence** ties to 表/图/式/数据/参数范围 in the same sentence when making a claim.
4. **After every body edit**, run and clear:
   ```bash
   python3 scripts/check_prose_style.py --path <edited-file-or-dir> --strict-prose
   ```
5. Skill/checklist “Must not / Do not” language stays in skills and notes — **never paste into the paper**.

## Tooling truth

- Change checkers/skills/templates in this repo first.
- Sync contest workspace with `python3 scripts/sync_to_contest_repo.py --dest ../math_modeling2026`.

## External skills (reference only)

See `external-skills/README.md`. Do not treat vendor skills as final authority.
Writing / humanize arsenal: `writing-skills/README.md` (H=EN humanize, Z=中文去味, A=学术管线).
Native gates: `check_prose_style`, `check_model_fitness`, `preflight`, `skills/cumcm-*`.
Repair links: `bash scripts/install_external_skills.sh`；写作软链：`bash scripts/install_writing_skills.sh`.

竞赛仓 loop（字体/AI详情/writing/prose/model/lock/paper）：见竞赛仓 `docs/MODELING_LOOP.md` 与 `scripts/modeling_loop_manager.py`（本仓有副本）。状态落在 `math_modeling2026/iterator/`。
