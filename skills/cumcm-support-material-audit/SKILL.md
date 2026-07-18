---
name: cumcm-support-material-audit
description: Audit CUMCM supporting materials for required code, data, generated outputs, AI-use details, appendix file lists, package size, cache files, identity leaks, and paper-to-file traceability. Use when preparing ZIP/RAR support packages or checking whether materials can reproduce paper results.
---

# CUMCM Support Material Audit

Use this skill before packaging supporting materials.

## Workflow

1. Identify required materials from the paper: code, data, generated figures, result tables, AI-use details, and large intermediate outputs.
2. Compare the appendix file list with actual files.
3. Check package risks: cache files, local paths, credentials, identity names, missing README/run notes, and oversized archives.
4. Ensure paper claims can be traced to included outputs or reproducible scripts.
5. Run `python3 scripts/check_submission.py --target cumcm --support-dir <dir>` when a support directory exists.
6. Read `references/checklist.md` for package contents.
7. Read `references/package-risks.md` when classifying findings.
8. Read `references/examples.md` when writing final package notes.

## Guardrails

- Do not include private or school-identifying files.
- Do not delete raw data without approval.
- Do not claim reproducibility when scripts require missing local paths or unavailable files.
