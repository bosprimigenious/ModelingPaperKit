---
name: cumcm-result-consistency
description: Check consistency between CUMCM paper claims, formulas, tables, figures, units, code outputs, appendix records, and subproblem conclusions. Use when reviewing a draft for mismatched numbers, stale figures, inconsistent symbols, unsupported conclusions, or broken result narrative.
---

# CUMCM Result Consistency

Use this skill after results are inserted into the paper and before final review.

## Workflow

1. Extract major claims from abstract, results, conclusion, tables, and figures.
2. Trace each numeric claim to a table, figure, formula, or generated output.
3. Check units, symbols, signs, percentages, ranking direction, and decimal precision.
4. Find stale references where text describes an old model or old output.
5. Read `references/checklist.md` for consistency surfaces.
6. Read `references/claim-map.md` when building a traceability table.
7. Read `references/examples.md` when reporting findings.

## Guardrails

- Do not change numbers unless the source output is identified.
- Do not smooth over contradictions with prose.
- Prefer one clear correction path per finding.
