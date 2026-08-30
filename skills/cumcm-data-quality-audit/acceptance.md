# Acceptance — cumcm-data-quality-audit

## When to use

- When the task described in SKILL.md description applies.

## Required inputs

- Contest paper or workspace paths named in SKILL.md
- Relevant `references/*.md`

## Required outputs

- Structured findings or updated artifacts as described in SKILL.md workflow

## Must not

- Follow SKILL.md Guardrails.
- Never paste instructional Must-not / Do-not lists into the paper body.

## Acceptance

- `python3 scripts/check_skills.py skills/cumcm-data-quality-audit` passes.
- Manual checklist in `references/checklist.md` completed when present.
- No TODO left in skill references.

## Gate status

- **guidance-only** until a deterministic script covers the skill end-to-end.
- Related machine gates: `check_skills.py`, `check_skill_contract.py`, `check_prose_style.py`, `check_claim_coverage.py`, `preflight.py` as applicable.
