---
name: cumcm-model-fitness
description: Gate whether a proposed or implemented math-modeling route is usable for the contest problem—matches required deliverables, can run on available data, produces the answer form judges expect, and is not merely code that runs. Use when locking models, reviewing modeling plans, after baselines, before paper claims, or when the team risks “successful participation without award”.
---

# CUMCM Model Fitness Gate

**Goal:** decide *pass / refine / reject* for each subproblem model path.

This is not “does the script exit 0?”.  
It is “does this model **answer what the problem asks** in a form **judges can score**?”.

## When to use

- After `cumcm-problem-reading` (task matrix exists) and a candidate model is proposed.
- Before locking code as the main route.
- After first real runs (baseline + main).
- Whenever someone says “模型很高级” but the paper still cannot state a one-sentence answer per subproblem.

## Required reads

1. `references/fitness-rubric.md` — three layers: usable / problem-answer / judge-answer.
2. `references/deliverable-match.md` — answer-form matching.
3. `references/checklist.md` — pass criteria.
4. Workspace `artifacts/task_matrix.md` (from problem-reading).
5. Optional: `artifacts/modeling_decision_card.md`.

## Workflow

### 1. Freeze the question contract (per subproblem)

From the official statement only, write:

| Field | Content |
| --- | --- |
| Qi | subproblem id |
| Required answer form | number / ranking / prediction path / scheme / classification / explanation+metric |
| Direct answer sentence template | “本题要求给出的是：…” |
| Must-report objects | variables, units, time range, decision vars |
| Forbidden substitutes | e.g. giving a heatmap when a ranking is required |

If the team cannot fill **Required answer form**, stop modeling; re-read the problem.

### 2. Map model → deliverable (fitness layer A)

For the candidate model, fill:

| Field | Content |
| --- | --- |
| Model name | short |
| Input fields | real columns/files |
| Mechanism in one line | what math does |
| Output object | exact type the code emits |
| Maps to required form? | yes/no + how |
| If no | what is missing |

**Reject** if output object cannot be transformed into the required answer form without inventing data.

### 3. Usability on this data (fitness layer B)

Check with real files when possible:

- Required fields exist; units/granularity match assumptions.
- Sample size / missingness allow the method (not just “in theory”).
- Train/val/test or time split is defined without leakage.
- A **baseline** of the same deliverable form is defined.
- Code path is runnable; smoke result exists (even tiny).
- Failure modes known (non-convergence, empty feasible set, singular matrix…).

**Reject or refine** if the method needs data you do not have, or only works after hidden future labels.

### 4. Problem-answer closed loop (fitness layer C)

Produce or verify:

1. One **direct answer sentence** per Qi (no “根据分析可知”).
2. One **primary artifact** path (csv/table/figure) that the sentence cites.
3. Recompute rule: how a stranger regenerates the number from artifact + script.
4. Consistency with other Qi interfaces (units, shared symbols).

Run when artifacts exist:

```bash
python3 scripts/check_claim_coverage.py --artifacts artifacts
python3 scripts/check_model_fitness.py --artifacts artifacts
```

### 5. Judge-facing score signals (fitness layer D)

Judges (and instructors) typically reward:

| Signal | Pass look |
| --- | --- |
| Task closure | Each Qi answered in the asked form |
| Method–problem fit | Why this model for *this* deliverable |
| Baseline contrast | Same metric, same split |
| Validation / sensitivity | At least one honest stress |
| Assumptions used | Each assumption appears in math or data step |
| Limitations | Where it fails; no fake robustness |
| Clarity | Formula → algorithm → number → meaning |

**Soft fail (refine)** if model is novel but: no baseline, no sensitivity, answer buried, or black-box stack with no interpretation.

**Hard fail (reject)** if: wrong deliverable form, fabricated metrics, leakage, or cannot state the answer without the model name fluff.

### 6. Verdict

Per Qi emit exactly one:

- `PASS` — usable, answers the asked form, judge signals present or scheduled.
- `REFINE` — direction OK; list blocking gaps with owners.
- `REJECT` — wrong form / data impossible / only “looks advanced”.

Write `artifacts/model_fitness.md` using the template in `references/fitness-report-template.md`.

## Guardrails

- Do not equate “code runs” with “model is correct”.
- Do not equate “complex model” with “award route”.
- Do not invent that judges want deep learning / fancy names; they want **closed answers + evidence**.
- Do not change problem requirements to fit a favorite model.
- Must-not / Do-not language stays out of the paper body.

## Machine gate

```bash
python3 scripts/check_model_fitness.py --artifacts artifacts
python3 scripts/check_model_fitness.py --artifacts artifacts --require-pass
```
