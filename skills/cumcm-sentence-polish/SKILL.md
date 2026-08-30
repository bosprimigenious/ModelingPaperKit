---
name: cumcm-sentence-polish
description: Polish Chinese CUMCM/math-modeling contest paper sentences, paragraphs, abstracts, captions, and section transitions while preserving formulas, labels, citations, data, units, and claims. Use when drafting or rewriting body prose, removing AI filler, hollow connectors (根据…可知 / 由此可见 / However), meta-language, or tightening national-contest style without changing facts.
---

# CUMCM Sentence Polish

Use this skill **before and after** drafting body prose, and whenever a section needs de-AI cleanup.

## Write-time (mandatory before any body draft)

1. Read `references/banned-prose.md` in full.
2. Read `references/style-rules.md` for abstract/body patterns.
3. Draft only with evidence-bound sentences (表/图/式/数据/参数范围 in claim sentences).
4. Never open paragraphs with empty connectors: 然而 / 但是 / However / Therefore / Thus.
5. Never use hollow inference scaffolds: 根据…可知 / 由…可知 / 由此可见 / It can be seen that.

## Workflow (polish pass)

1. Identify the target text: abstract, problem analysis, assumptions, model, solution, result, validation, evaluation, conclusion, caption, or appendix.
2. Scan for banned classes: hollow inference, AI filler, meta-language.
3. Preserve all LaTeX commands, labels, citations, equations, table/figure numbers, filenames, data values, units, and uncertainty marks unless the user explicitly asks to fix them.
4. Rewrite in layers:
   - delete hollow scaffolds; put the artifact name first;
   - move concrete result or modeling purpose earlier;
   - replace vague praise with verifiable descriptions;
   - connect method, parameter, result, and validation in the same paragraph when possible;
   - shorten repeated background sentences.
5. Flag missing evidence instead of hiding it. Keep placeholders such as `待附件数据计算` visible until scripts produce values.
6. Report removals under:

```text
Removed meta-language / AI-filler / hollow-inference:
- ...
```

## Output Rules

- For small edits, return a polished replacement paragraph.
- For repository edits, patch the target `.tex` file directly and summarize changed sections.
- When a factual issue is found, report it separately as `Needs data`, `Needs citation`, or `Needs consistency check`.
- Keep the tone concise, mathematical, and competition-ready. Do not use marketing language.

## Guardrails

- Do not invent numbers, rankings, experiments, algorithms, citations, or conclusions.
- Do not strengthen a claim unless it is supported by existing data or code output.
- Do not erase AI-use declarations, source notes, identity-leak warnings, or missing-data warnings.
- In active CUMCM mode, do not browse or summarize public discussions about the current contest problem.
- Guardrail wording itself must never be pasted into the paper body.

## Machine Gate

After drafting or polishing, run and fix until exit 0:

```bash
python3 scripts/check_prose_style.py --path <edited-tex> --strict-prose
```

Rules file: `scripts/prose_rules.json` (shared with this skill’s banned list).
