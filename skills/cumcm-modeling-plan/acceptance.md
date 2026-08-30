# Acceptance — cumcm-modeling-plan

## When to use

- After problem-reading, before locking the main model family.
- When a shallow baseline would be chosen by most teams.

## Required inputs

- `artifacts/task_matrix.md`
- Available data schema

## Required outputs

- `artifacts/modeling_decision_card.md` filled
- Chosen baseline + main method per subproblem

## Must not

- Do not pick the flashiest model without a data fit story.
- Do not skip a baseline.
- Must-not rules stay outside the paper body.

## Acceptance

- `artifacts/modeling_decision_card.md` answers all required prompts.
- Each subproblem names baseline and validation mode.
- Manual review: direction is problem-fitting, not only popular.

## Gate status

- **guidance-only** until a deterministic script covers the skill end-to-end.
- Related machine gates: `check_skills.py`, `check_skill_contract.py`, `check_prose_style.py`, `check_claim_coverage.py`, `preflight.py` as applicable.
