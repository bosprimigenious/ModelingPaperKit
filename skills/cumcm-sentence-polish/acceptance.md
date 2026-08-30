# Acceptance — cumcm-sentence-polish

## When to use

- After facts/figures are stable.
- When prose has AI filler or instructional tone.

## Required inputs

- Target `.tex` section(s)
- `references/style-rules.md`

## Required outputs

- Polished tex
- Report section `Removed meta-language / AI-filler`

## Must not

- Do not change formulas, labels, citations, numbers, units.
- Do not invent evidence.
- Do not leave Do-not/请不要 meta-language in the paper.

## Acceptance

- `python3 scripts/check_prose_style.py --path <edited files>` has zero critical meta findings.
- Under `--strict-prose`, no AI-filler criticals on polished sections.
- Diff does not alter numeric literals or \label/\ref/\cite tokens.

## Gate status

- **guidance-only** until a deterministic script covers the skill end-to-end.
- Related machine gates: `check_skills.py`, `check_skill_contract.py`, `check_prose_style.py`, `check_claim_coverage.py`, `preflight.py` as applicable.
