# 2026 CUMCM Skill Index

This index maps common 2026 CUMCM preparation tasks to the repository skills.

## Skill Map

| Need | Skill | Key References |
|---|---|---|
| Track official notices and rule changes | `cumcm-2026-rules-watch` | `official-sources.md`, `checklist.md`, `examples.md` |
| Audit the LaTeX template | `cumcm-template-audit` | `format-rubric.md`, `checklist.md`, `examples.md` |
| Decompose a new problem statement | `cumcm-problem-reading` | `task-matrix.md`, `checklist.md`, `examples.md` |
| Plan or review paper structure | `cumcm-paper-structure` | `abstract-patterns.md`, `section-skeletons.md`, `common-anti-patterns.md` |
| Build a modeling strategy | `cumcm-modeling-plan` | `problem-taxonomy.md`, `model-family-map.md`, `validation-patterns.md`, `sensitivity-patterns.md` |
| Establish simple baseline models | `cumcm-baseline-models` | `baseline-map.md`, `checklist.md`, `examples.md` |
| Audit raw and processed data quality | `cumcm-data-quality-audit` | `issue-taxonomy.md`, `checklist.md`, `examples.md` |
| Organize reproducible code/data | `cumcm-data-code-pipeline` | `directory-layout.md`, `reproducibility-rules.md`, `support-material-list.md` |
| Track experiments and generated outputs | `cumcm-experiment-log` | `run-log-schema.md`, `checklist.md`, `examples.md` |
| Design result figures/tables | `cumcm-figures-tables` | `plot-taxonomy.md`, `table-patterns.md`, `caption-patterns.md` |
| Validate models and test sensitivity | `cumcm-validation-sensitivity` | `method-map.md`, `checklist.md`, `examples.md` |
| Check paper-result consistency | `cumcm-result-consistency` | `claim-map.md`, `checklist.md`, `examples.md` |
| Manage references and AI records | `cumcm-citation-ai-log` | `source-log-schema.md`, `ai-use-log-schema.md`, `reference-examples.md` |
| Scan for identity leaks | `cumcm-anonymity-check` | `patterns.md`, `checklist.md`, `examples.md` |
| Audit supporting materials | `cumcm-support-material-audit` | `package-risks.md`, `checklist.md`, `examples.md` |
| Assemble submission package | `cumcm-submission-pack` | `package-layout.md`, `checklist.md`, `examples.md` |
| Enforce active-contest safety | `cumcm-contest-safety-mode` | `red-lines.md`, `checklist.md`, `examples.md` |
| Run final review | `cumcm-final-review` | `rubric.md`, `checklist.md`, `examples.md` |

## Suggested Preparation Loop

1. Use `cumcm-2026-rules-watch` to verify current rules.
2. Use `cumcm-template-audit` to keep `templates/cumcm` safe.
3. Use `cumcm-contest-safety-mode` when working during the active contest window.
4. Use `cumcm-problem-reading` before choosing methods for a new problem.
5. Use `cumcm-paper-structure` and `cumcm-modeling-plan` during problem work.
6. Use `cumcm-baseline-models`, `cumcm-data-quality-audit`, and `cumcm-data-code-pipeline` before relying on results.
7. Use `cumcm-experiment-log`, `cumcm-figures-tables`, `cumcm-validation-sensitivity`, and `cumcm-result-consistency` while producing and writing results.
8. Use `cumcm-citation-ai-log` continuously, not only at the end.
9. Use `cumcm-anonymity-check`, `cumcm-support-material-audit`, `cumcm-submission-pack`, and `cumcm-final-review` before submission.

## Validation

Use `docs/2026-cumcm-official-rules-snapshot.md` as the current official-source
baseline for 2026 CUMCM template, AI-use, anonymity and submission-pack checks.

Run:

```bash
python3 scripts/preflight.py --target cumcm
python3 scripts/inspect_template.py --target cumcm
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
