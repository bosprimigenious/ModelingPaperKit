# CUMCM

Target: `cumcm`

Main file:

```text
templates/cumcm/main_cumcm.tex
```

Build:

```bash
python scripts/build.py --target cumcm
```

## Structure

Common sections:

- `sections/cover.tex`
- `sections/numbering_page.tex`
- `sections/ai_declaration.tex` (supporting-material template; not included in the submitted paper by default)
- `sections/problem.tex`
- `sections/analysis.tex`
- `sections/assumptions.tex`
- `sections/notation.tex`
- `sections/model.tex`
- `sections/solution.tex`
- `sections/results.tex`
- `sections/validation.tex`
- `sections/evaluation.tex`
- `sections/conclusion.tex`
- `sections/references.tex`
- `sections/appendix.tex`

## Key Checks

- Paper title is set with `\PaperTitle`.
- Chinese fonts may require SimSun, SimHei, FangSong, Microsoft YaHei.
- Electronic submission must start from the abstract page; keep `\cumcmPaperSubmissionfalse` for the submitted PDF.
- Paper submission can enable `\cumcmPaperSubmissiontrue` to generate commitment and numbering pages.
- If no AI tools are used, keep the no-AI statement after references. If AI tools are used, mark the relevant body text, list the tools in references, and add a supporting-material PDF named `AI 工具使用详情`.
- Supporting materials should not leak identity or school information.
- Scan for phone, email, student number, advisor, school, and team member names.

## Safety

During active CUMCM competition, follow `references/contest-safety.md` and avoid browsing public problem-discussion sources.
