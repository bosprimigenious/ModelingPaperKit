# Model Fitness Report

Contest: demo  
Problem: sample structural check  
Date: 2026-08-29  
Authors of this gate: catalog bootstrap

## Global verdict

| Overall | REFINE |
| --- | --- |
| Blocking issues | Demo rows only — replace on real contest |
| Safe to write results sections? | no |

## Per-subproblem table

| Qi | Required form | Model | Output artifact | Form match Y/N | Data usable Y/N | Baseline | Validation | Judge signals (1–5) | Verdict | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q1 | prediction metrics table | baseline lag + main reg | tests/fixtures/prose_good.tex | Y | Y | lag-1 | holdout MAE | 4 | PASS | structural demo |
| Q2 | ranking of factors | TBD | TBD | N | Y | corr | sensitivity | 1 | REFINE | need scores table |

## Direct answers (draft, numbers only if verified)

| Qi | One-sentence answer (evidence-bound) | Artifact path |
| --- | --- | --- |
| Q1 | 在验证窗内主模型 MAE 为 0.12，相对基线下降 18%（见表2措辞样例）。 | tests/fixtures/prose_good.tex |
| Q2 | （待填）按…规则前三因素为… | TBD |

## Rejected / deferred routes

| Route | Why rejected | Fallback |
| --- | --- | --- |
| deep stack without baseline | form/baseline gaps | lag + linear first |

## Next actions

1. Replace this demo with live task_matrix-driven rows.
2. Fill Q2 ranking artifact before PASS.
3. Run `python3 scripts/check_model_fitness.py --artifacts artifacts`.
