---
name: cumcm-anonymity-check
description: Scan CUMCM papers, LaTeX files, metadata, code, paths, figures, data files, and supporting materials for identity leaks before 2026 CUMCM submission. Use when checking anonymity, removing school/team/member/advisor names, detecting phone/email/student IDs, or reviewing electronic submission safety.
---

# CUMCM Anonymity Check

Use this skill before packaging or submitting electronic materials.

## Workflow

1. Search text files for names, school names, advisor names, phone numbers, email addresses, student numbers, local usernames, and absolute paths.
2. Check LaTeX special pages are disabled for electronic submission.
3. Check PDF and image metadata when tools are available.
4. Check code comments, notebook outputs, CSV headers, and generated figures.
5. Run `python3 scripts/check_identity_leaks.py templates/cumcm` for deterministic text scanning.
6. Read `references/checklist.md` for patterns and surfaces.
7. Read `references/patterns.md` for concrete search patterns and red flags.
8. Read `references/examples.md` when choosing paper-only versus support-package scan scope.

## Guardrails

- Do not delete user data without explicit approval.
- Prefer reporting findings and patching obvious template placeholders.
- Keep paper-submission identity fields isolated to paper-only pages.
