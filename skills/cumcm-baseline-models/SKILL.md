---
name: cumcm-baseline-models
description: Design simple, defensible baseline models for CUMCM prediction, classification, evaluation, optimization, simulation, and ranking tasks before using stronger methods. Use when a team needs a minimum viable model, method comparison, ablation baseline, or fallback path under contest time pressure.
---

# CUMCM Baseline Models

Use this skill to create a simple model that can anchor the paper and expose whether a complex method is actually better.

## Workflow

1. Identify the task type: prediction, classification, evaluation, optimization, simulation, network, or ranking.
2. Choose a baseline that is explainable and quick to implement.
3. Define the metric or objective before comparing models.
4. State what the baseline ignores and why the main model improves on it.
5. Plan one table or figure comparing baseline versus main model.
6. Read `references/checklist.md` for baseline selection.
7. Read `references/baseline-map.md` for task-to-method mapping.
8. Read `references/examples.md` when writing baseline sections.

## Guardrails

- Do not skip the baseline for a complex model.
- Do not claim improvement without the same metric and data split.
- Prefer a working simple model over a fragile impressive model.
