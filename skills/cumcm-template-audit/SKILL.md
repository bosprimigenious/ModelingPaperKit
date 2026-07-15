---
name: cumcm-template-audit
description: Audit the ModelingPaperKit CUMCM LaTeX template for 2026 CUMCM paper-format compliance, electronic versus paper submission behavior, page order, margins, fonts, section structure, AI declaration placement, references, appendix, and build risks. Use when reviewing or editing templates/cumcm or preparing a template-quality pass.
---

# CUMCM Template Audit

Use this skill for focused template review, not paper content judging.

## Workflow

1. Inspect `templates/cumcm/main_cumcm.tex` first.
2. Inspect only affected section files under `templates/cumcm/sections/`.
3. Check electronic submission defaults before paper submission extras:
   - electronic PDF starts at title/abstract
   - commitment and numbering pages are opt-in
   - AI details are not inserted as a normal paper page
4. Check local LaTeX conventions in `skills/modeling-paperkit/references/latex-patterns.md` if macros or style packages are being changed.
5. Run `git diff --check` and `python3 scripts/check_tex_links.py --target cumcm`; run `python3 scripts/build.py --target cumcm` when `xelatex` exists.
6. Read `references/checklist.md` for the audit list.
7. Read `references/format-rubric.md` for page-flow and layout details.
8. Read `references/examples.md` when choosing electronic versus paper audit scope.

## Report

Report findings as `Critical`, `Warning`, and `Info`. Include file paths and line numbers when possible.
