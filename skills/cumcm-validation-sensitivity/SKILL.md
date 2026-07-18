---
name: cumcm-validation-sensitivity
description: Design and review validation, robustness, sensitivity analysis, error analysis, and uncertainty checks for CUMCM models. Use when deciding how to prove model credibility, comparing parameter choices, checking stability, or writing validation and sensitivity sections.
---

# CUMCM Validation Sensitivity

Use this skill after a baseline exists and before claiming results are reliable.

## Workflow

1. Match the validation method to the task and available data.
2. Define what would falsify or weaken the model.
3. Test sensitivity to key parameters, weights, assumptions, and data splits.
4. Convert validation into paper artifacts: metric table, residual plot, scenario chart, sensitivity curve, or robustness statement.
5. Read `references/checklist.md` for review.
6. Read `references/method-map.md` for task-specific validation choices.
7. Read `references/examples.md` when writing the validation section.

## Guardrails

- Do not use vague phrases such as "the model is robust" without evidence.
- Do not validate on training data only unless clearly disclosed.
- Keep sensitivity tests small enough to finish within contest time.
