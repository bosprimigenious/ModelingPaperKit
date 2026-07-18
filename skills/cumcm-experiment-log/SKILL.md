---
name: cumcm-experiment-log
description: Maintain CUMCM experiment records for datasets, preprocessing versions, model parameters, random seeds, metrics, generated figures, result tables, and paper claims. Use when tracking runs, comparing model variants, reproducing outputs, or preparing appendix and supporting-material logs.
---

# CUMCM Experiment Log

Use this skill once modeling code starts producing outputs.

## Workflow

1. Assign each meaningful run an ID, date, data version, code version, parameters, seed, and output paths.
2. Link every paper table or figure to the script and run that generated it.
3. Record failed runs only when they changed decisions.
4. Keep result claims traceable to metrics or generated files.
5. Read `references/checklist.md` for fields.
6. Read `references/run-log-schema.md` when creating a log.
7. Read `references/examples.md` when summarizing experiments in the paper.

## Guardrails

- Do not overwrite final outputs without preserving how they were produced.
- Do not report a metric if the run configuration is unknown.
- Keep logs concise enough to maintain during contest pressure.
