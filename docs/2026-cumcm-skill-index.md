# 2026 CUMCM Skill Index

This index maps common 2026 CUMCM preparation tasks to the repository skills.

## Skill Map

| Need | Skill | Key References |
|---|---|---|
| Track official notices and rule changes | `cumcm-2026-rules-watch` | `official-sources.md`, `checklist.md`, `examples.md` |
| Audit the LaTeX template | `cumcm-template-audit` | `format-rubric.md`, `checklist.md`, `examples.md` |
| Plan or review paper structure | `cumcm-paper-structure` | `abstract-patterns.md`, `section-skeletons.md`, `common-anti-patterns.md` |
| Build a modeling strategy | `cumcm-modeling-plan` | `problem-taxonomy.md`, `model-family-map.md`, `validation-patterns.md`, `sensitivity-patterns.md` |
| Organize reproducible code/data | `cumcm-data-code-pipeline` | `directory-layout.md`, `reproducibility-rules.md`, `support-material-list.md` |
| Design result figures/tables | `cumcm-figures-tables` | `plot-taxonomy.md`, `table-patterns.md`, `caption-patterns.md` |
| Manage references and AI records | `cumcm-citation-ai-log` | `source-log-schema.md`, `ai-use-log-schema.md`, `reference-examples.md` |
| Scan for identity leaks | `cumcm-anonymity-check` | `patterns.md`, `checklist.md`, `examples.md` |
| Assemble submission package | `cumcm-submission-pack` | `package-layout.md`, `checklist.md`, `examples.md` |
| Run final review | `cumcm-final-review` | `rubric.md`, `checklist.md`, `examples.md` |

## Suggested Preparation Loop

1. Use `cumcm-2026-rules-watch` to verify current rules.
2. Use `cumcm-template-audit` to keep `templates/cumcm` safe.
3. Use `cumcm-paper-structure` and `cumcm-modeling-plan` during problem work.
4. Use `cumcm-data-code-pipeline` and `cumcm-figures-tables` while producing results.
5. Use `cumcm-citation-ai-log` continuously, not only at the end.
6. Use `cumcm-anonymity-check`, `cumcm-submission-pack`, and `cumcm-final-review` before submission.

## Validation

Run:

```bash
python3 scripts/check_skills.py skills
python3 scripts/check_identity_leaks.py templates/cumcm
python3 scripts/check_tex_links.py --target cumcm
python3 scripts/check_submission.py --target cumcm
python3 scripts/summarize_build_log.py --target cumcm
git diff --check
```

Run the CUMCM build when `xelatex` is installed:

```bash
python3 scripts/build.py --target cumcm
```
