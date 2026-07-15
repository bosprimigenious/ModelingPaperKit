# Example Uses

## Organize A Contest Folder

User asks: "把代码和数据目录规范一下。"

Do:

- Propose raw/processed/code/outputs/logs layout.
- Keep raw data immutable.
- Add run order and generated-artifact mapping.

## Reproducibility Review

User asks: "这套代码能不能复现论文结果？"

Do:

- Trace paper tables/figures to scripts.
- Check relative paths and random seeds.
- Flag notebook-only or manual-copy steps.
