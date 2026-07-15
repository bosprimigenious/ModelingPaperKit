# 2026 国赛备战：GitHub 开源生态与 Skill 建设调研

调研日期：2026-07-16

本文面向 `ModelingPaperKit` 的 2026 年全国大学生数学建模竞赛（CUMCM / 高教社杯）备战工作，梳理 GitHub 开源项目中可复用的论文写作、LaTeX 排版、数学建模、数据代码复现、引用与终审检查思路，并转化为本仓库的 skill 建设路线。

目标不是复制一个“全自动写论文 Agent”，而是建立一组可组合、可审计、能支撑真实交赛的 Codex skills。

## 一句话结论

2026 国赛备战应该采用“多 skill + 确定性脚本 + 官方赛规监控”的架构：

```text
官方赛规监控
  -> CUMCM 模板与交赛格式
  -> 论文写作结构
  -> 建模方案设计
  -> 数据/代码复现
  -> 图表结果表达
  -> 引用与 AI 使用记录
  -> 匿名与身份泄露检查
  -> 提交打包
  -> 终审复盘
```

这比单个巨型 skill 更稳，因为国赛工作天然分阶段，且每一阶段的风险不同。

## GitHub 开源项目雷达

### 1. CUMCM / 数学建模 LaTeX 模板

| 项目 | 借鉴点 | 对我们的启发 |
|---|---|---|
| [`latexstudio/CUMCMThesis`](https://github.com/latexstudio/CUMCMThesis) | 国赛 LaTeX 模板、承诺书、编号页、摘要页、withoutpreface 思路 | `templates/cumcm` 应继续保持电子版安全默认，纸质页 opt-in；承诺书和编号专用页应独立维护 |
| GitHub 上大量 `cumcm` / `CUMCM` 模板仓库 | 参赛者会直接寻找可编译模板，而不是复杂系统 | 我们的核心价值首先是“可靠、合规、可编译”的模板基础设施 |
| 通用 LaTeX 学术模板生态，如 [`ElegantLaTeX/ElegantPaper`](https://github.com/ElegantLaTeX/ElegantPaper) | 将排版风格、宏包选择、文档结构封装成模板 | 国赛模板也应把可复用宏沉入 `core/`，赛规差异留在 `templates/cumcm/` |

### 2. 开源论文写作与出版工具

| 项目 | 借鉴点 | 对我们的启发 |
|---|---|---|
| [`quarto-dev/quarto-cli`](https://github.com/quarto-dev/quarto-cli) | 技术写作、代码、图表、引用、导出流程统一 | 论文 skill 要关心“数据/代码 -> 图表 -> 文本 -> PDF”的链路，不只写 LaTeX |
| [`manubot/manubot`](https://github.com/manubot/manubot) | 协作论文、引用管理、自动化构建 | `cumcm-citation-ai-log` 可借鉴引用记录与自动化检查思路 |
| [`jupyter-book/jupyter-book`](https://github.com/jupyter-book/jupyter-book) | 可执行内容、章节组织、文档构建 | 建模过程中的 notebook / scripts / figures 应能追踪到论文结果 |
| [`Wandmalfarbe/pandoc-latex-template`](https://github.com/Wandmalfarbe/pandoc-latex-template) | 文档模板参数化、Pandoc 生成 PDF | 后续可考虑从 Markdown 草稿生成 LaTeX 章节，但第一阶段不必引入复杂转换链 |

### 3. 数据科学与可复现研究

| 项目 | 借鉴点 | 对我们的启发 |
|---|---|---|
| [`drivendata/cookiecutter-data-science`](https://github.com/drivendata/cookiecutter-data-science) | 标准化数据项目目录 | `cumcm-data-code-pipeline` 应给出 raw/processed/code/outputs/logs 的推荐布局 |
| [`great-expectations/great_expectations`](https://github.com/great-expectations/great_expectations) | 数据质量检查与断言 | 国赛中可做轻量版数据检查：缺失值、异常值、单位、列名、范围 |
| [`pytest-dev/pytest`](https://github.com/pytest-dev/pytest) | 可重复测试 | 对关键数据处理脚本和评分函数，可以准备最小测试样例 |
| [`pre-commit/pre-commit`](https://github.com/pre-commit/pre-commit) | 提交前自动检查 | 后续可把身份泄露、路径泄露、构建日志检查做成 pre-submit 检查脚本 |

### 4. 数学建模与优化计算

| 项目 | 借鉴点 | 对我们的启发 |
|---|---|---|
| [`scipy/scipy`](https://github.com/scipy/scipy) | 科学计算、优化、统计、数值算法基础 | 建模 skill 应优先推荐稳定基础方法，不追求花哨模型 |
| [`scikit-learn/scikit-learn`](https://github.com/scikit-learn/scikit-learn) | 机器学习建模、评估、交叉验证 | CUMCM 常见预测/分类问题可沉淀为“基线 -> 强模型 -> 解释”的流程 |
| [`statsmodels/statsmodels`](https://github.com/statsmodels/statsmodels) | 统计建模、回归、时间序列 | 国赛论文更看重可解释性时，统计模型 often 比黑盒模型更合适 |
| [`cvxpy/cvxpy`](https://github.com/cvxpy/cvxpy) | 凸优化建模语言 | 优化类题目可形成变量、目标、约束、求解器、可行性分析模板 |
| [`Pyomo/pyomo`](https://github.com/Pyomo/pyomo) | 通用优化建模语言 | 适合复杂约束、整数规划、资源调度类题目 |
| [`anyoptimization/pymoo`](https://github.com/anyoptimization/pymoo) | 多目标优化 | 多指标权衡题可沉淀 Pareto、加权评分、敏感性分析写法 |
| [`SALib/SALib`](https://github.com/SALib/SALib) | 敏感性分析 | 终稿 review 应检查是否有参数敏感性或鲁棒性说明 |

### 5. LaTeX 检查与编辑生态

| 项目 | 借鉴点 | 对我们的启发 |
|---|---|---|
| [`James-Yu/LaTeX-Workshop`](https://github.com/James-Yu/LaTeX-Workshop) | LaTeX 编译、日志、预览工作流 | `summarize_build_log.py` 和 build review 应优先提炼可操作错误 |
| [`latexindentpl/latexindent.pl`](https://github.com/cmhughes/latexindent.pl) | LaTeX 自动格式化 | 后续可给 `.tex` 文件增加格式化建议，但不应在比赛临近时大规模改格式 |
| [`chktex/chktex`](https://github.com/chktex/chktex) | LaTeX 静态检查 | 可借鉴为 PaperKit 做轻量“缺图、缺 label、未引用、身份泄露”检查 |

## Skill 设计原则

### 原则 1：小 skill，多组合

不要把“国赛备战”写成一个巨大 skill。建议一组窄职责 skill：

| Skill | 主要职责 | 关键输出 |
|---|---|---|
| `cumcm-2026-rules-watch` | 官方赛规、通知、AI 规定、格式变化 | 赛规差异报告、模板更新建议 |
| `cumcm-template-audit` | LaTeX 模板格式和提交模式检查 | 模板审计 findings |
| `cumcm-paper-structure` | 论文结构、章节逻辑、摘要 | 章节大纲、改写计划 |
| `cumcm-modeling-plan` | 读题、建模候选、方法路线 | 模型方案与 fallback |
| `cumcm-data-code-pipeline` | 数据处理、代码复现、输出追踪 | 目录结构、复现实验清单 |
| `cumcm-figures-tables` | 图表设计、结果表达 | 图表清单、caption 改进 |
| `cumcm-citation-ai-log` | 引用、来源、AI 工具记录 | 参考文献与 AI 使用说明 |
| `cumcm-anonymity-check` | 身份泄露、路径泄露、元数据 | 脱敏 findings |
| `cumcm-submission-pack` | 电子版/纸质版/支撑材料打包 | 提交 checklist |
| `cumcm-final-review` | 终审综合检查 | Critical / Warning / Info 报告 |

### 原则 2：skill 只做决策与流程，脚本做确定性检查

Skill 适合做：

- 判断什么时候查官方赛规。
- 指导论文结构怎么排。
- 判断图表和模型是否支撑子问题。
- 汇总终审风险。

脚本适合做：

- 解析 LaTeX log。
- 检查缺图、缺 label、未引用。
- 扫描邮箱、手机号、学校名、绝对路径。
- 检查 PDF 是否存在、页数、是否包含纸质版页面。
- 对支撑材料文件列表和实际文件做 diff。

### 原则 3：官方赛规优先于开源模板

GitHub 模板只能作为工程参考，不能作为赛规依据。每次涉及以下事项都应优先查官方来源：

- 2026 年赛程和提交截止时间。
- 论文格式规范。
- 承诺书和编号页是否变化。
- AI 工具使用规定。
- 支撑材料提交要求。
- 电子版/纸质版页面顺序。

### 原则 4：备赛期和比赛期分开

备赛期可以查开源项目、往年论文、模型库、教程；比赛期必须切换到更严格的安全模式：

- 不主动浏览当前题目的公开讨论或解答。
- 不复制外部论文段落。
- 所有来源和 AI 使用必须记录。
- 不自动提交。

## 论文写作 Skill 规划

### `cumcm-paper-structure`

重点能力：

- 将题目要求映射到论文章节。
- 生成摘要骨架：背景、方法、结果、鲁棒性、结论。
- 检查每个子问题是否有“模型 -> 求解 -> 结果 -> 验证”闭环。
- 检查假设是否在后文真正使用。
- 检查符号表是否覆盖公式变量。

建议 references：

```text
references/
  checklist.md
  abstract-patterns.md
  section-skeletons.md
  common-anti-patterns.md
```

后续可以补的内容：

- 国赛摘要优秀论文样式分析。
- A/B/C/E 题型常见章节结构。
- 常见空话和弱表达替换表。

## 建模 Skill 规划

### `cumcm-modeling-plan`

重点能力：

- 将问题拆成输入、输出、约束、评价指标。
- 生成候选模型族：基线模型、主模型、备选模型。
- 明确变量、参数、目标函数、约束、求解方法。
- 给出验证、敏感性分析和误差分析计划。
- 输出图表需求清单。

建议 references：

```text
references/
  checklist.md
  problem-taxonomy.md
  model-family-map.md
  validation-patterns.md
  sensitivity-patterns.md
```

模型族地图建议先覆盖：

- 预测：回归、时间序列、机器学习、集成模型。
- 分类：逻辑回归、树模型、SVM、聚类辅助解释。
- 优化：线性规划、整数规划、非线性规划、多目标优化。
- 评价：层次分析、熵权、TOPSIS、灰色关联、主成分。
- 仿真：蒙特卡洛、离散事件、元胞自动机、系统动力学。
- 图网络：最短路、最大流、匹配、社区发现。

## 数据与代码 Skill 规划

### `cumcm-data-code-pipeline`

重点能力：

- 推荐比赛目录布局。
- 追踪 raw data、processed data、outputs、figures、tables。
- 提醒使用相对路径。
- 将最终论文图表连接到生成脚本。
- 生成支撑材料文件列表。
- 检查代码中是否有身份信息、绝对路径和不可复现依赖。

建议 references：

```text
references/
  checklist.md
  directory-layout.md
  reproducibility-rules.md
  support-material-list.md
```

后续脚本：

```text
scripts/check_supporting_materials.py
scripts/check_identity_leaks.py
scripts/check_generated_assets.py
```

## 图表 Skill 规划

### `cumcm-figures-tables`

重点能力：

- 给每个子问题规划结果表和图。
- 检查图表是否被正文引用。
- 检查 caption 是否解释含义，而不是只写名称。
- 检查单位、坐标轴、图例、精度。
- 建议将复杂模型流程图、结果对比图、敏感性分析图放到关键位置。

建议 references：

```text
references/
  checklist.md
  plot-taxonomy.md
  table-patterns.md
  caption-patterns.md
```

## 引用与 AI 使用 Skill 规划

### `cumcm-citation-ai-log`

重点能力：

- 区分文献、数据源、软件工具、AI 工具。
- 检查正文引用与参考文献对应。
- 记录 AI 工具名称、版本、提供方、使用日期、用途、人工审核。
- 按官方要求决定是否在参考文献后放未使用声明，或在支撑材料中放 AI 使用详情。

建议 references：

```text
references/
  checklist.md
  ai-use-log-schema.md
  source-log-schema.md
  reference-examples.md
```

## 匿名与提交 Skill 规划

### `cumcm-anonymity-check`

重点能力：

- 扫描 `.tex`、`.bib`、`.md`、`.py`、`.ipynb`、`.csv`、`.log`。
- 查学校、姓名、导师、手机号、邮箱、学号、绝对路径、本机用户名。
- 检查电子版 PDF 是否误包含承诺书或编号页。
- 检查图像/PDF 元数据。

### `cumcm-submission-pack`

重点能力：

- 区分电子版论文、纸质版论文、支撑材料。
- 检查 appendix 文件列表和实际支撑材料是否一致。
- 检查 AI 使用详情是否应该进入支撑材料。
- 输出最终交赛 checklist。

## 终审 Skill 规划

### `cumcm-final-review`

终审输出统一采用：

```text
Critical
- 会导致不能提交、违规、编译失败、身份泄露、关键题未答的问题。

Warning
- 会明显影响论文质量或可复现性的问题。

Info
- 风格、表达、轻量优化建议。
```

终审检查面：

- 编译是否通过。
- PDF 是否存在。
- 电子版是否从摘要页开始。
- 所有子问题是否回答。
- 图表是否完整引用。
- 公式变量是否解释。
- 结果是否与代码输出一致。
- 引用和 AI 使用是否合规。
- 支撑材料是否齐全。
- 匿名是否安全。

## 当前仓库已完成的第一批 Skill

当前已经准备了 10 个 CUMCM 专用 skill：

```text
skills/cumcm-2026-rules-watch/
skills/cumcm-template-audit/
skills/cumcm-paper-structure/
skills/cumcm-modeling-plan/
skills/cumcm-data-code-pipeline/
skills/cumcm-figures-tables/
skills/cumcm-citation-ai-log/
skills/cumcm-anonymity-check/
skills/cumcm-submission-pack/
skills/cumcm-final-review/
```

每个 skill 采用相同结构：

```text
SKILL.md
agents/openai.yaml
references/checklist.md
```

这种结构适合继续扩展：`SKILL.md` 保持短小，详细赛规、样例和 schema 放进 references。

技能入口索引见：[2026 CUMCM Skill Index](2026-cumcm-skill-index.md)。

## 下一步开发优先级

### P0：让 skill 变得可验证

- 为每个 skill 增加 1-2 个真实调用样例。
- 已增加 `scripts/check_skills.py`，检查 frontmatter、TODO、目录结构、reference 链接，避免依赖 `PyYAML`。
- 后续可继续增加更严格的 reference 链接完整性检查。

### P1：补确定性检查脚本

- `scripts/summarize_build_log.py`
- `scripts/inspect_template.py`
- `scripts/check_tex_links.py`
- `scripts/check_identity_leaks.py`
- `scripts/check_submission.py`

这些脚本会让 skill 不只是“会说”，而是能稳定执行检查。

### P2：补深层 reference

优先补：

- `cumcm-modeling-plan/references/model-family-map.md`
- `cumcm-paper-structure/references/abstract-patterns.md`
- `cumcm-citation-ai-log/references/ai-use-log-schema.md`
- `cumcm-anonymity-check/references/patterns.md`
- `cumcm-submission-pack/references/package-layout.md`

### P3：建立比赛项目状态

后续可以引入：

```text
.paperkit/state.json
```

记录：

- 目标赛事和题号。
- 子问题状态。
- 章节完成度。
- 图表清单。
- 数据/代码产物。
- 参考文献和 AI 使用记录。
- 最终检查结果。

## 风险与边界

- 不把 skill 设计成作弊工具。
- 不在比赛期主动查当前题公开讨论。
- 不伪造数据、引用、结果或 AI 使用记录。
- 不自动提交文件。
- 不用开源模板替代官方赛规。
- 不承诺“自动获奖”，只承诺流程、质量、合规和可复现性提升。

## 参考项目

- CUMCMThesis: https://github.com/latexstudio/CUMCMThesis
- ElegantPaper: https://github.com/ElegantLaTeX/ElegantPaper
- Quarto CLI: https://github.com/quarto-dev/quarto-cli
- Manubot: https://github.com/manubot/manubot
- Jupyter Book: https://github.com/jupyter-book/jupyter-book
- Pandoc LaTeX Template: https://github.com/Wandmalfarbe/pandoc-latex-template
- Cookiecutter Data Science: https://github.com/drivendata/cookiecutter-data-science
- Great Expectations: https://github.com/great-expectations/great_expectations
- Pytest: https://github.com/pytest-dev/pytest
- Pre-commit: https://github.com/pre-commit/pre-commit
- SciPy: https://github.com/scipy/scipy
- scikit-learn: https://github.com/scikit-learn/scikit-learn
- statsmodels: https://github.com/statsmodels/statsmodels
- CVXPY: https://github.com/cvxpy/cvxpy
- Pyomo: https://github.com/Pyomo/pyomo
- pymoo: https://github.com/anyoptimization/pymoo
- SALib: https://github.com/SALib/SALib
- LaTeX Workshop: https://github.com/James-Yu/LaTeX-Workshop
- latexindent.pl: https://github.com/cmhughes/latexindent.pl
- ChkTeX: https://github.com/chktex/chktex
