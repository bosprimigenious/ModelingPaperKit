---
name: cumcm-modeling-plan
description: Create rigorous modeling plans for 2026 CUMCM problems from problem statements, data descriptions, and constraints. Use when decomposing a CUMCM task, selecting candidate models, defining assumptions, metrics, algorithms, validation plans, sensitivity analysis, or contest-time modeling strategy.
---

# CUMCM Modeling Plan

Use this skill before writing code or prose for a contest problem.

## Workflow

1. Restate each subproblem as inputs, outputs, constraints, and evaluation criteria.
2. Propose 2-3 candidate model families with tradeoffs.
3. Select a primary path and a fallback path.
4. Specify:
   - variables and parameters
   - objective or loss function
   - required data transformations
   - solver or algorithm
   - validation and sensitivity tests
   - expected figures/tables
5. Read `references/checklist.md` when producing a full modeling plan.
6. Read `references/problem-taxonomy.md` before model selection, `references/model-family-map.md` for candidate methods, and validation/sensitivity references for review design.
7. Read `references/examples.md` when converting a problem statement or method comparison into an action plan.

## Guardrails

- Separate assumptions from conclusions.
- Mark dependencies on unavailable data or ambiguous problem wording.
- Prefer robust, explainable methods over brittle novelty unless the problem rewards it.
