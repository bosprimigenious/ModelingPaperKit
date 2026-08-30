# Acceptance — cumcm-submission-pack

## When to use

- After final review pass.
- When assembling electronic package.

## Required inputs

- Final PDF
- Code/data support files
- AI-use log if required

## Required outputs

- Submission folder matching package-layout.md
- File checklist

## Must not

- Do not include identity-bearing filenames.
- Do not omit runnable source when paper claims computation.

## Acceptance

- `python3 scripts/check_submission.py --target cumcm --format json` has no criticals.
- Support materials listed in appendix match real files.

## Gate status

- **guidance-only** until a deterministic script covers the skill end-to-end.
- Related machine gates: `check_skills.py`, `check_skill_contract.py`, `check_prose_style.py`, `check_claim_coverage.py`, `preflight.py` as applicable.
