---
name: cumcm-figures-tables
description: Design, review, and improve figures, tables, captions, result summaries, and visual evidence in 2026 CUMCM papers. Use when deciding what plots or tables to include, improving captions, checking figure/table references, converting results into competition-readable visuals, or aligning assets with ModelingPaperKit LaTeX macros.
---

# CUMCM Figures Tables

Use this skill to make results easy to inspect and defend.

## Workflow

1. Match each subproblem to at least one result table or figure.
2. Use figures for trends, spatial patterns, workflows, distributions, and sensitivity.
3. Use tables for numeric answers, parameter values, ablation results, and comparison metrics.
4. Ensure captions state what is shown and why it matters.
5. Check that every figure/table is referenced in the text.
6. Run `python3 scripts/check_tex_links.py --target cumcm` when checking TeX labels, references, citations, and figure assets.
7. Read `references/checklist.md` when auditing all visuals.
8. Read `references/plot-taxonomy.md`, `references/table-patterns.md`, and `references/caption-patterns.md` when planning or revising result presentation.
9. Read `references/examples.md` when deciding whether to plan new visuals or audit existing ones.

## LaTeX Notes

- Prefer local PaperKit helpers such as `\figplot` where they fit.
- Keep figure filenames ASCII and meaningful.
- Put generated assets under `figures/` or the configured graphics path.
