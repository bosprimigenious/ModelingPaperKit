# Acceptance — cumcm-model-fitness

## When to use

- Before locking main models for any subproblem.
- After first baseline/main runs.
- When reviewing whether the team can award-level close the problem (not only run code).

## Required inputs

- Official problem statement (or accurate restatement).
- `artifacts/task_matrix.md` when available.
- Candidate model description and, if any, result paths.

## Required outputs

- `artifacts/model_fitness.md` filled from `references/fitness-report-template.md`.
- Per-Qi verdict: PASS / REFINE / REJECT.
- Direct answer sentence stubs for each Qi.

## Must not

- Do not pass a model that cannot emit the required answer form.
- Do not treat exit-code-0 as fitness.
- Do not invent judge preferences or metrics.
- Do not paste this checklist language into the paper body.

## Acceptance

- `artifacts/model_fitness.md` exists and has a data row per subproblem.
- Each row has non-empty Required form, Verdict, and Output artifact or explicit REFINE gap.
- `python3 scripts/check_model_fitness.py --artifacts artifacts` exits 0 for structure (use `--require-pass` only when all Qi are PASS).
- Manual: at least one Qi has a direct answer sentence that cites an artifact without 根据…可知.
