# CUMCM Sentence Style Rules

Load this file when polishing a CUMCM-style paper, especially abstracts, result sections, captions, AI-use notes, and final submission text.

## Official Constraints To Preserve

- A4 paper; all margins at least 2.5 cm.
- Electronic paper starts on the abstract page and excludes the commitment page and numbering page.
- The abstract page includes title, Chinese abstract, and keywords; no English abstract is required.
- Do not include a table of contents.
- Main text should not exceed 30 pages; appendix pages are not limited.
- Abstract, body, appendix, supporting materials, and filenames must not expose team, school, or contest-area identity.
- Cite public or external sources in the body and references.
- If AI tools are used, mark relevant generated or assisted content, list tools in references, and prepare a support-material PDF named `AI 工具使用详情`.
- If no AI tools are used, state after references that no AI tools were used.

Sources to re-check before final submission:

- Official 2026 format specification: https://dxs.moe.gov.cn/zx/a/hd_sxjm_gsyw/260702/2046411.shtml?source=hd_sxjm_gsyw
- CUMCM mirror of the 2026 format specification: https://www.mcm.edu.cn/html_cn/node/4cd596519c9eb9fbd866398f6df0caa3.html
- Official 2026 participation rules: https://www.mcm.edu.cn/html_cn/node/9d8e511fe7a1447b35f53a82c908e2e0.html
- Official AI tool rules, 2025 trial version: https://www.mcm.edu.cn/html_cn/node/eebcfb6dc37fd2de9603dc16026fdf01.html

## Abstract Pattern

Use one compact paragraph sequence:

1. Problem background and objective.
2. Data processing and indicators.
3. Model family and key equations or decision variables.
4. Main quantitative results and comparison, or a visible placeholder if data is unavailable.
5. Robustness, sensitivity, and practical conclusion.

Prefer direct verbs: `建立`, `构造`, `估计`, `求解`, `验证`, `得到`, `给出`.

Avoid empty verbs: `进行了一定研究`, `具有重要意义`, `效果较好`, `较为合理`.

## Body Sentence Rules

- Start paragraphs with the modeling purpose or result, not a long general background.
- Keep each paragraph centered on one action: data processing, parameter estimation, model construction, result interpretation, or validation.
- Pair every method with why it fits the problem.
- Pair every result with the data table, figure, or code output that supports it.
- Replace absolute claims with scoped claims when evidence is incomplete.
- Convert repeated passive wording into clear actions by the team/model.

## Captions And Tables

- Captions should say what is plotted and why it matters.
- Table titles should include object, metric, and scenario.
- Do not describe trends in captions unless the visual or table actually shows them.

## Experience-Derived Heuristics

These are non-official writing practices distilled from public excellent-paper examples and community experience posts.

- Treat the abstract as the first screening surface: it should reveal model, result, and validation, not only background.
- Let the model author participate in model-section writing; otherwise formulas and prose often diverge.
- Write concrete problem sections first, then polish abstract, conclusion, and transitions.
- Use simple flow diagrams and compact tables only when they reduce reading effort.
- Show at least one baseline, validation, or sensitivity comparison for each important conclusion.

## Before And After Patterns

Weak:

```text
本文对该问题进行了研究，建立了相关模型，并取得了较好的效果。
```

Stronger:

```text
本文将该问题转化为带状态更新的长期平均成本最小化问题，并通过滚动预测比较不同维护策略的年均成本。
```

Weak:

```text
模型具有一定准确性和实用性。
```

Stronger:

```text
在附件数据导入后，模型通过时间滚动验证、残差诊断和成本扰动实验检验预测稳定性。
```

## Banned Phrases (AI filler)

Reject or rewrite these when they carry no evidence:

- 近年来 / 随着…的发展
- 具有重要意义 / 进行了一定研究
- 效果较好 / 较为合理 / 众所周知
- 赋能 / 助力 / 深度融合
- 在一定程度上 / 发挥着重要作用
- 广阔的应用前景 / 提供参考意义
- 模型具有一定准确性和实用性

Prefer: purpose → method fit → numeric result with table/figure → validation scope.

## Meta-Language Ban (must not enter paper body)

These belong only in skills, agent notes, or checklists — never in `.tex` body:

- 不要… / 请勿… / 禁止…
- Do not… / You should not…
- 作为AI / 作为助手 / 我将帮你 / 根据你的要求
- Guardrails / Must not / this skill

If polish finds them, delete or rewrite into scientific statements. Report under:

```text
Removed meta-language / AI-filler:
- ...
```

Machine gate:

```bash
python3 scripts/check_prose_style.py --target cumcm
python3 scripts/check_prose_style.py --path path/to/section.tex --strict-prose
```

Inline suppress (rare, justified quotes only): `%# prose:allow` on the same line.

## Hollow Inference Ban (根据…可知)

See full table and rewrites in `banned-prose.md`.

Never in body:

- 根据…可知 / 由…可知 / 由此可见 / 由此可得 / 据此可知
- 不难发现 / 显而易见 / 我们得出结论
- It can be seen that / As can be seen / We can see that
- Sentence-initial However, / Therefore, / Thus, / Hence,
- Bare English filler `ever`
- Sentence-initial 然而， / 但是，

Replace with artifact-led facts: 由表2… / 由式(3)… / 在参数…范围内….
