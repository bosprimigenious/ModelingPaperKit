---
name: cumcm-paper-structure
description: Structure, outline, and revise a 2026 CUMCM paper for strong mathematical-modeling narrative flow, including abstract, problem restatement, assumptions, notation, model construction, solution, results, validation, sensitivity, evaluation, conclusion, references, and appendix. Use when asked to plan sections, improve paper logic, rewrite section skeletons, or prepare a writing roadmap.
---

# CUMCM Paper Structure

Use this skill to turn modeling work into a coherent paper.

## Workflow

1. Identify the problem type and target question count.
2. Run `python3 scripts/inspect_template.py --target cumcm` when checking repository section status.
3. Build the paper around the task sequence: problem -> method -> result -> validation -> insight.
4. Keep the abstract one-page oriented: background, methods, key quantitative results, robustness, conclusion.
5. Ensure each model section contains:
   - objective and variables
   - assumptions and rationale
   - equations or algorithm
   - solving procedure
   - result interpretation
6. Use `references/checklist.md` when rewriting a full outline or reviewing section completeness.
7. Read `references/abstract-patterns.md` for abstract work, `references/section-skeletons.md` for full outlines, and `references/common-anti-patterns.md` for review.
8. Read `references/examples.md` when turning a vague writing request into concrete paper actions.

## Guardrails

- Do not invent results, data, citations, or performance numbers.
- Flag placeholders that must be filled during the actual contest.
- Keep writing competition-ready but not over-polished into vague marketing prose.
