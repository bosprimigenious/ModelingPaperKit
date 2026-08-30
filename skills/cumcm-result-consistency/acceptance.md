# Acceptance — cumcm-result-consistency

## When to use

- After numbers enter the paper draft.
- Before final review.

## Required inputs

- Paper `sections/*.tex`
- Generated tables/figures/code outputs

## Required outputs

- `artifacts/claim_map.md` (Claim | Paper location | Source artifact | Check)
- List of mismatches

## Must not

- Do not change numbers without identifying the source output.
- Do not smooth contradictions with prose.
- Must-not rules stay outside the paper body.

## Acceptance

- `artifacts/claim_map.md` has rows for abstract/results/conclusion numeric claims.
- `python3 scripts/check_claim_coverage.py --artifacts artifacts` finds no claim-without-source criticals.
- Spot-check: one abstract number recomputed from its CSV.

## Gate status

- **guidance-only** until a deterministic script covers the skill end-to-end.
- Related machine gates: `check_skills.py`, `check_skill_contract.py`, `check_prose_style.py`, `check_claim_coverage.py`, `preflight.py` as applicable.
