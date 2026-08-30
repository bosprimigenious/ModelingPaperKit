# Acceptance — cumcm-problem-reading

## When to use

- Before choosing methods on a new contest problem.
- When the team disagrees on what each subproblem asks.

## Required inputs

- Official problem statement (PDF/DOCX/text)
- Attachment file list if any

## Required outputs

- Filled `artifacts/task_matrix.md` (Subproblem | Required answer | Data | Method | Output artifact | Validation)
- Short uncertainty notes

## Must not

- Do not invent hidden data or performance numbers.
- Do not start coding before the matrix exists.
- Must-not rules stay in skills/docs; never paste into the paper body.

## Acceptance

- `artifacts/task_matrix.md` exists with one row per subproblem.
- `python3 scripts/check_claim_coverage.py --artifacts artifacts` reports no empty output artifacts (after paths are filled).
- Manual: every Required answer is a concrete deliverable type (number/table/ranking/design), not vague prose.

## Gate status

- **guidance-only** until a deterministic script covers the skill end-to-end.
- Related machine gates: `check_skills.py`, `check_skill_contract.py`, `check_prose_style.py`, `check_claim_coverage.py`, `preflight.py` as applicable.
