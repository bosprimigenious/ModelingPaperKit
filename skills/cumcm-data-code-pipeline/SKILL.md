---
name: cumcm-data-code-pipeline
description: Organize reproducible data processing, modeling code, generated outputs, and supporting materials for 2026 CUMCM. Use when creating or reviewing code folders, data provenance, preprocessing scripts, experiment logs, generated figures/tables, appendix code listings, or reproducibility instructions.
---

# CUMCM Data Code Pipeline

Use this skill to make contest code reproducible and submission-safe.

## Workflow

1. Separate raw data, processed data, scripts, outputs, and paper assets.
2. Keep generated figures and tables traceable to scripts.
3. Prefer deterministic scripts over notebook-only workflows for final artifacts.
4. Add a support-material file list in the appendix or submission notes.
5. Check for identity leaks and absolute local paths before packaging.
6. Read `references/checklist.md` for the expected file layout.
7. Read `references/directory-layout.md`, `references/reproducibility-rules.md`, and `references/support-material-list.md` when preparing a real project package.
8. Read `references/examples.md` when organizing or reviewing an actual code/data folder.

## Guardrails

- Do not include private credentials, local usernames, school names, or personal metadata.
- Do not overwrite raw data.
- Do not fabricate data to fill missing contest inputs.
