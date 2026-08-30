# Acceptance — cumcm-final-review

## When to use

- Last pass before packaging submission.

## Required inputs

- Built PDF or main tex tree
- Supporting materials list

## Required outputs

- Findings ordered by Critical/Warning/Info
- Explicit list of checks run vs blocked

## Must not

- Do not claim submission-ready if build or identity checks fail.
- Must-not rules stay outside the paper body.

## Acceptance

- `python3 scripts/preflight.py --target cumcm --strict-prose --strict-placeholders` exit 0 or only accepted warnings.
- Rubric Critical items all addressed or explicitly deferred with reason.

## Gate status

- **guidance-only** until a deterministic script covers the skill end-to-end.
- Related machine gates: `check_skills.py`, `check_skill_contract.py`, `check_prose_style.py`, `check_claim_coverage.py`, `preflight.py` as applicable.
