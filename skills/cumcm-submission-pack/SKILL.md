---
name: cumcm-submission-pack
description: Prepare and review 2026 CUMCM electronic and paper submission packages, including final PDF, supporting materials, code/data folders, AI-use details, appendix file list, paper-only commitment and numbering pages, naming conventions, and last-mile safety checks. Use when packaging deliverables or making a submission checklist.
---

# CUMCM Submission Pack

Use this skill for final assembly, not for solving the problem.

## Workflow

1. Identify submission mode: electronic, paper, or both.
2. Build or locate the final PDF.
3. Verify electronic PDF starts at the title/abstract page.
4. Verify paper mode includes commitment and numbering pages when needed.
5. Verify supporting materials include code, data notes, generated outputs, and AI-use details if applicable.
6. Run `python3 scripts/check_submission.py --target cumcm` for deterministic preflight checks.
7. Run anonymity and final review checks before declaring readiness.
8. Read `references/checklist.md` for package contents.
9. Read `references/package-layout.md` when assembling electronic, paper, or supporting-material packages.
10. Read `references/examples.md` for final assembly and last-mile review patterns.

## Guardrails

- Never submit files automatically.
- Do not claim readiness when build, anonymity, or AI-use checks were skipped.
- Do not package raw personal or institution-identifying files into electronic materials.
