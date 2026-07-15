---
name: cumcm-final-review
description: Run a final 2026 CUMCM readiness review across paper content, LaTeX build, template compliance, result consistency, figures/tables, citations, AI-use records, anonymity, supporting materials, and submission packaging. Use when the user asks for final review, pre-submit review, readiness check, or overall quality audit.
---

# CUMCM Final Review

Use this skill as the last integrated pass.

## Workflow

1. Start with `git status --short` and avoid overwriting user work.
2. Run available checks:
   - `git diff --check`
   - `python3 scripts/summarize_build_log.py --target cumcm`
   - `python3 scripts/build.py --target cumcm` when `xelatex` is available
3. Review the PDF/log if generated.
4. Check paper logic, figures/tables, references, AI records, anonymity, and support-material list.
5. Read `references/checklist.md` for the final review rubric.
6. Read `references/rubric.md` when classifying findings by severity.
7. Read `references/examples.md` when selecting between full pre-submit review and paper-quality-only review.

## Report

Lead with findings:

```text
Critical
- ...

Warning
- ...

Info
- ...
```

End with verification commands run and any blockers such as missing `xelatex`.
