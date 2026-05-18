# 模板写作指南 (Template Guide)

## CUMCM / 五一杯（中文）

| 文件 | 写作要点 |
|------|----------|
| `sections/problem.tex` | 背景 → 要求 → 分问题列表 |
| `sections/model.tex` | 每问：思路、公式、求解；可用 `\figplot` 插入流程图 |
| `sections/results.tex` | 用表格/图呈现定量结果 |
| `sections/appendix.tex` | `listings` 或 `\lstinputlisting` 附代码 |

## MCM（英文）

| 文件 | 写作要点 |
|------|----------|
| `sections/summary_sheet.tex` | 一页摘要，Control Number 醒目 |
| `sections/introduction.tex` | Background / Tasks / Our Work |
| `sections/models.tex` | Per-task model + figures |
| `sections/conclusion.tex` | Takeaways and limitations |

## English / 中文切换

- 定理环境：`paperkit-math` 选项 `zh` / `en` / `auto`
- 算法浮动：`paperkit-utils` 同上
