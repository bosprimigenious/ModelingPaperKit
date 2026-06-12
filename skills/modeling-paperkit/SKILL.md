---
name: modeling-paperkit
description: Use this skill when working with the ModelingPaperKit repository to write, edit, compile, review, or prepare math modeling contest papers for CUMCM, MCM/ICM, Wuyi, Beijing, or the included example templates. Use it for LaTeX template edits, section organization, figure/table insertion, build-log diagnosis, final submission checks, contest safety constraints, AI usage/source logging, and PaperKit-specific workflows.
metadata:
  short-description: Work on ModelingPaperKit math modeling papers
---

# ModelingPaperKit

Use this skill for math modeling contest paper delivery inside the `ModelingPaperKit` repository. The job is to help with structure, LaTeX, build/review loops, contest-specific checks, and safe handoff to deterministic scripts.

Do not treat this as an automatic contest-solving skill. Do not fabricate data, model results, citations, figures, awards, or submission readiness.

## First Steps

1. Identify the target: `cumcm`, `mcm`, `wuyi`, `beijing`, or `example`.
2. Inspect the relevant main file and sections before editing.
3. Load only the reference files needed for the task:
   - Repository layout: `references/repository-map.md`
   - Standard workflow: `references/workflow.md`
   - LaTeX macros and local conventions: `references/latex-patterns.md`
   - Final review: `references/final-review.md`
   - Contest safety: `references/contest-safety.md`
   - CUMCM: `references/cumcm.md`
   - MCM/ICM: `references/mcm.md`
   - Wuyi: `references/wuyi.md`
   - Beijing: `references/beijing.md`
4. Prefer existing repository scripts over ad hoc shell logic:
   - Build: `python scripts/build.py --target <target>`
   - Full verification: `python scripts/verify_build.py`
   - Clean: `python scripts/clean.py`
   - New contest scaffold: `python scripts/new_contest.py --name <name> --lang zh|en`

## Workflow

For writing or editing:

1. Read the target `main_*.tex`.
2. Read only the relevant `sections/*.tex`.
3. Use local PaperKit macros and style conventions.
4. Keep edits scoped to user-requested sections.
5. Build or run checks when the user asks for verification or when edits may break LaTeX.

For build failures:

1. Run the target build if needed.
2. Read the corresponding `out/*.log`.
3. Summarize the first actionable errors.
4. Make the smallest safe LaTeX fix.
5. Rebuild and report remaining issues.

For final review:

1. Check build status and PDF presence.
2. Check labels, references, figures, tables, and special pages.
3. Check suspected identity leaks.
4. Check contest-specific AI/source/supporting-material requirements.
5. Report findings as `Critical`, `Warning`, or `Info`.

## Contest Safety

If the user is actively competing:

- Ask or infer whether the mode is `cumcm_active`, `mcm_active`, or `off`.
- In `cumcm_active`, do not proactively search public discussion platforms or solution repositories for current contest problems.
- In `mcm_active`, public inanimate sources may be used only with source logging and citation discipline.
- Never help submit files automatically.

Read `references/contest-safety.md` when current-contest rules, browsing, AI use, or source logging matters.

## Output Style

When reporting review results, lead with findings:

```text
Critical
- ...

Warning
- ...

Info
- ...
```

When making edits, mention the files changed and the verification command run. If tests or builds were not run, say so clearly.

