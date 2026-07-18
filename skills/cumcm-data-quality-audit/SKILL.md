---
name: cumcm-data-quality-audit
description: Audit CUMCM datasets for missing values, units, duplicates, outliers, inconsistent identifiers, impossible ranges, time/order problems, leakage, and preprocessing decisions. Use when reviewing raw or processed data before modeling, writing data cleaning notes, or deciding whether results are trustworthy.
---

# CUMCM Data Quality Audit

Use this skill before fitting models or when a result looks suspicious.

## Workflow

1. Inventory files, fields, row counts, units, time span, and identifiers.
2. Check missingness, duplicates, impossible values, outliers, and inconsistent encodings.
3. Separate true data problems from domain-valid rare cases.
4. Record every cleaning decision and whether it affects reproducibility.
5. Recommend plots/tables needed to justify preprocessing in the paper.
6. Read `references/checklist.md` for the audit list.
7. Read `references/issue-taxonomy.md` when classifying data findings.
8. Read `references/examples.md` when writing the data-quality section.

## Guardrails

- Do not silently drop rows or columns.
- Do not replace missing data without recording the rule.
- Keep raw data immutable; write cleaned data to a separate processed path.
