# Common Paper Anti-Patterns

- Abstract lists work but no results.
- Problem restatement copies the original statement too closely.
- Assumptions are decorative and never used.
- Variables appear in formulas before definition.
- Model section explains software commands instead of math logic.
- Results are buried inside prose without tables or figures.
- Sensitivity analysis changes a parameter but does not interpret the effect.
- Conclusion repeats the abstract without answering each subproblem.
- Appendix includes code but no file list or run instructions.

## Prose anti-patterns (de-AI)

- Hollow inference: 根据…可知, 由…可知, 由此可见, It can be seen that.
- Empty connectors at sentence start: 然而， / 但是， / However, / Therefore, / Thus,.
- AI filler: 近年来, 具有重要意义, 效果较好, 较为合理.
- Instructional meta leaked from agent notes: 不要…, Do not….
- Claim sentences with no 表/图/式/数据 reference.

Before writing sections, load `skills/cumcm-sentence-polish/references/banned-prose.md`.
After writing, run `python3 scripts/check_prose_style.py --path <section> --strict-prose`.
