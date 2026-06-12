# ModelingPaperKit Skill 建设计划

计划日期：2026-06-09

本文基于当前 `ModelingPaperKit` 仓库结构，以及对公开数学建模 skill / agent / workflow 项目的联网调研，规划一个面向数学建模论文交付的专用 Codex skill。

相关调研见：[数学建模 Skill 市场调研报告](math-modeling-skill-market-report.md)。

真实参赛流程调研见：[真实数学建模比赛工作流调研](real-competition-workflow-research.md)。

全栈与 Agent 升级蓝图见：[ModelingPaperKit 升级架构蓝图](modeling-paperkit-upgrade-architecture.md)。

前端产品计划见：[ModelingPaperKit Frontend Plan](modeling-paperkit-frontend-plan.md)。

## 0. 核心决策

本项目不应把 **Agent 开发** 和 **Skill 集成** 视为二选一。更合理的判断是：

```text
Skill 是专业能力层，Agent 是调度执行层。
先把 Skill 和确定性脚本做扎实，再开发轻量 Agent。
```

当前最紧迫的问题不是缺少一个复杂 Agent 平台，而是缺少一套能让现有仓库被稳定调用的能力规范：

- Codex/Agent 不知道什么时候该读哪个模板。
- Codex/Agent 不知道哪些 LaTeX 宏是本仓库推荐写法。
- 编译错误、缺图、缺引用、身份信息泄露等问题还缺少确定性检查脚本。
- 数学建模论文的终稿检查还没有沉淀成可复用 checklist。

因此路线应分两层推进：

1. **先做 `modeling-paperkit` Skill**：沉淀仓库知识、赛事模板规则、LaTeX 写法、编译排错、终稿检查。
2. **再做轻量 Agent**：调度 skill、维护项目状态、串联写作/编译/检查流程。

短期目标是让任何 Agent 都能可靠使用本仓库；中期目标才是开发一个独立的 Math Modeling Agent。

## 1. 背景判断

当前仓库已经具备较完整的数学建模论文排版基础：

- `core/` 提供共享 LaTeX 排版引擎，包括页面、图表、表格、数学环境、算法、引用和写作标记。
- `templates/` 提供 CUMCM、MCM/ICM、五一杯、北京赛四套赛事模板。
- `scripts/build.py` 支持多赛事编译、清理、BibTeX、自定义 TeX 引擎和 watch 模式。
- `scripts/verify_build.py` 能全量编译并检查 PDF、LaTeX Error、Overfull/Underfull。
- `examples/` 已有示例论文、示例数据和图表生成脚本。
- `docs/` 已有快速开始、模板指南和 FAQ。

联网对标后可以看到，市面上数学建模类 skill 常见方向是“全流程自动建模”：读题、建模、求解、写作、评审一条龙。但这类方案通常范围很大，容易变成泛化 agent；而 `ModelingPaperKit` 的独特优势在于论文落地能力。因此本计划建议先建设一个 **PaperKit 专用交付 skill**，把现有模板、构建脚本和论文检查流程包装成稳定的专业能力。

## 2. Skill 定位

建议 skill 名称：

```text
modeling-paperkit
```

一句话定位：

> 帮助 Codex 使用 `ModelingPaperKit` 完成数学建模竞赛论文的写作组织、LaTeX 排版、图表插入、编译排错、合规检查和终稿交付。

它不承诺自动完成完整数学建模比赛，也不承担“选模型拿奖”的全部职责。它专注于：

- 把已有模型、数据结果和图表组织成竞赛论文。
- 帮用户正确使用本仓库模板。
- 降低 LaTeX 编译与格式排查成本。
- 在提交前检查结构、脱敏、引用、图表和赛事页面。

## 3. 适用场景

当用户提出以下需求时，应触发该 skill：

- 使用 `ModelingPaperKit` 写国赛、美赛、五一杯、北京赛论文。
- 选择或复制某个赛事模板。
- 填写或重构 `sections/*.tex`。
- 把结果表、图片、算法、公式插入论文。
- 修复 `xelatex` 编译错误。
- 检查 `out/*.log` 中的 LaTeX 报错。
- 检查论文是否脱敏、是否缺少承诺书/AI 声明/Summary Sheet。
- 做最终提交前 review。

不建议触发该 skill 的场景：

- 单纯询问某个数学模型原理。
- 单纯处理 Excel 或 CSV 数据，且不涉及论文交付。
- 写普通学术论文而不是数学建模竞赛论文。
- 构建 WebUI 或 Agent 平台。

## 4. 对标借鉴点

从公开项目中提炼出以下可落地设计：

| 对标做法 | 借鉴方式 |
|---|---|
| 阶段化工作流 | 将 PaperKit 使用流程拆成“识别赛事 -> 检查模板 -> 写作组织 -> 编译 -> 终审” |
| 竞赛特化配置 | 为 CUMCM、MCM、Wuyi、Beijing 分别写 references |
| 状态文件 | 后续可维护 `.paperkit/state.json`，记录赛事、题号、章节、图表、编译状态 |
| 多层反馈 | 增加结构检查、LaTeX 检查、合规检查、终稿检查 |
| 资源分层 | `SKILL.md` 只写触发和核心流程，细节放入 `references/` |
| 确定性脚本 | 用 Python 脚本做可验证检查，避免只靠语言模型判断 |

## 4.1 什么值得认真开发

以下功能是真实有效、和当前仓库强相关、值得认真做的能力。

| 功能 | 类型 | 必要性 | 原因 |
|---|---|---|---|
| LaTeX 编译日志摘要 | 脚本 + Skill | 急缺 | 编译失败是用户最常遇到的问题，必须从 `out/*.log` 提取可操作错误 |
| 提交前合规检查 | 脚本 + checklist | 急缺 | 数学建模论文容易出现身份信息、缺页、缺图、引用未解析等硬伤 |
| 模板识别与章节状态检查 | 脚本 | 急缺 | Agent 需要知道当前使用哪个赛事模板、哪些章节缺失 |
| 本仓库 LaTeX 宏用法库 | references | 急缺 | 避免 Codex 临时发明和仓库风格不一致的写法 |
| 赛事规则 references | references | 必要 | CUMCM/MCM/Wuyi/Beijing 的特殊页和章节顺序不同 |
| 终稿 review checklist | references/assets | 必要 | 比赛最后阶段价值很高，能直接减少提交事故 |
| 项目状态文件 `.paperkit/state.json` | Agent 基础 | 必要但后置 | Agent 需要长期任务状态，但第一版 skill 不强依赖 |
| 轻量 CLI Agent | Agent | 必要但后置 | 能串联 init/build/review/fix-log，但必须等 skill/scripts 可用后做 |

## 4.2 暂时不要认真开发的功能

以下功能看起来高级，但当前阶段投入产出比不高，容易拖慢项目。

| 功能 | 暂缓原因 |
|---|---|
| 全自动读题建模 Agent | 范围过大，容易偏离本仓库“论文交付基础设施”的优势 |
| WebUI 平台 | 在 skill 和脚本不稳定前做 UI，只会把不确定性包装起来 |
| RAG 知识库 | 当前没有足够结构化、持续维护的赛规和模型知识库 |
| 多 Agent 协作 | 对当前问题过重，先用单 Agent + 多 skill 更稳 |
| 自动生成完整论文 | 风险高，容易产出空泛文本；更适合辅助章节改写和终稿检查 |
| 大型模型算法库 | 与本仓库核心价值不完全重合，后续可作为独立 data/modeling skill |
| 自动评分器 | 数学建模评分主观性强，第一版应做 checklist，不做伪精确打分 |

## 4.3 当前最急缺的能力

按紧迫度排序：

1. **日志摘要脚本**：把 `main_*.log` 中真正导致失败的 LaTeX 错误提出来。
2. **提交检查脚本**：PDF、log、图片、引用、身份信息、特殊页一体检查。
3. **模板/章节检查脚本**：识别目标模板、主文件、章节缺失、输出目录状态。
4. **LaTeX pattern reference**：明确插图、表格、算法、公式、引用的本仓库推荐写法。
5. **CUMCM/MCM references**：先覆盖最常用中文/英文模板。
6. **final-review checklist**：按严重程度输出必须修复、建议修复、可接受风险。
7. **CLI Agent 原型**：只做固定流程调度，不做复杂自主建模。

## 5. 建议目录结构

第一版建议放在未来的 skill 目录中，例如：

```text
skills/modeling-paperkit/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── workflow.md
│   ├── repository-map.md
│   ├── cumcm.md
│   ├── mcm.md
│   ├── wuyi.md
│   ├── beijing.md
│   ├── latex-patterns.md
│   ├── writing-patterns.md
│   ├── figure-table-style.md
│   └── final-review.md
├── scripts/
│   ├── inspect_template.py
│   ├── summarize_build_log.py
│   ├── check_submission.py
│   └── check_tex_links.py
└── assets/
    └── checklists/
        ├── cumcm-final.md
        ├── mcm-final.md
        ├── wuyi-final.md
        └── beijing-final.md
```

如果不希望把 skill 直接放入仓库根目录，也可以先在 `docs/skill-design/` 中设计，再迁移到实际 skill 安装位置。

## 6. 文件职责

### `SKILL.md`

只保留最关键的触发条件和流程，避免变成大型教材。

应包含：

- 什么时候使用本 skill。
- 先读哪些仓库文件。
- 工作流程。
- 何时运行 `scripts/build.py`。
- 何时运行 skill 自带检查脚本。
- 输出要求和安全边界。

### `references/workflow.md`

描述标准工作流：

1. 识别赛事和目标模板。
2. 检查主文件、章节文件、图片目录。
3. 整理论文结构。
4. 插入或修复 LaTeX 内容。
5. 编译并解析日志。
6. 做最终检查。

### `references/repository-map.md`

说明本仓库关键路径：

- `core/paperkit-base.sty`
- `core/paperkit-math.sty`
- `core/paperkit-utils.sty`
- `templates/*/main_*.tex`
- `templates/*/sections/*.tex`
- `scripts/build.py`
- `scripts/verify_build.py`
- `examples/cumcm_walkthrough`

### 赛事 references

每个赛事文件记录：

- 文档语言。
- 主文件路径。
- 必要页面。
- 推荐章节顺序。
- 特殊命令。
- 提交前检查重点。

例如：

- `cumcm.md`：承诺书、AI 声明、中文摘要、关键词、正文、参考文献、附录、脱敏。
- `mcm.md`：Summary Sheet、Control Number、Problem Choice、英文章节、references、appendix。
- `wuyi.md`：五一杯承诺书、AI 声明、中文章节。
- `beijing.md`：北京赛承诺书、AI 声明、中文章节。

### `references/latex-patterns.md`

收集本仓库已有宏和推荐写法：

- `\figplot{题注}{高度}{label}{占位说明}{文件名}{制图说明}`
- `\keywords{}`
- `\vb{}`
- `\mat{}`
- `\topline` / `\midline` / `\bottomline`
- `algorithm` / `algpseudocode`
- `\cref{}`
- `\email{}` / `\phone{}`

### `references/final-review.md`

定义终稿审查流程：

- 章节完整性。
- 每个子问题是否有回答。
- 图表是否有正文引用。
- 公式是否解释变量。
- 参考文献是否被引用。
- 附录是否包含必要代码或说明。
- 编译日志是否有 Error。
- 是否出现真实姓名、学校、学号、电话、邮箱。
- 是否保留或注释了正确的赛事特殊页。

## 7. 脚本规划

### `inspect_template.py`

用途：识别当前目标模板和章节状态。

输入：

```bash
python inspect_template.py --target cumcm
```

输出：

- 主文件是否存在。
- `sections/` 中有哪些章节。
- 必要章节是否缺失。
- 是否存在 `figures/` 或 `../02_figures/`。
- 是否已有 `out/*.pdf` 和 `out/*.log`。

### `summarize_build_log.py`

用途：压缩 LaTeX 日志，给 Codex 易读错误摘要。

检查：

- `! LaTeX Error`
- `Undefined control sequence`
- `Missing $ inserted`
- `File ... not found`
- `Citation ... undefined`
- `Reference ... undefined`
- `Overfull \hbox`
- `Underfull \hbox`

### `check_submission.py`

用途：最终提交检查。

检查：

- PDF 是否存在且大小合理。
- log 中是否存在 LaTeX Error。
- 是否疑似包含手机号、邮箱、学号、身份证号。
- 必要页面是否被 `\input`。
- 图片文件是否存在。
- `\ref`、`\cref`、`\cite` 是否有明显 unresolved 警告。

### `check_tex_links.py`

用途：检查 LaTeX 内部引用闭环。

检查：

- `\label{}` 是否重复。
- `\ref{}` / `\cref{}` 是否找不到 label。
- `\includegraphics{}` 或 `\figplot` 第五参数是否能找到文件。
- `sections/*.tex` 是否被主文件引用。

## 8. MVP 范围

第一版只做最小但可用的交付 skill，并补齐最急缺的确定性脚本。不要在 MVP 中开发 WebUI 或完整 Agent。

必须包含：

- `SKILL.md`
- `references/workflow.md`
- `references/repository-map.md`
- `references/cumcm.md`
- `references/mcm.md`
- `references/latex-patterns.md`
- `references/final-review.md`
- `scripts/summarize_build_log.py`
- `scripts/check_submission.py`

强烈建议同时包含：

- `scripts/inspect_template.py`
- `scripts/check_tex_links.py`

暂缓：

- WebUI。
- 多 agent 协作。
- 自动建模算法库。
- RAG 知识库。
- 状态文件自动维护。
- 复杂评分器。

## 8.1 功能优先级

### P0：必须先做

这些功能直接决定 skill 是否真的可用。

| 功能 | 产物 | 验收方式 |
|---|---|---|
| Skill 入口说明 | `SKILL.md` | 触发条件清楚，正文小而准，不塞模型大全 |
| 仓库地图 | `references/repository-map.md` | 能指导 Codex 找到模板、core、scripts、docs |
| 标准工作流 | `references/workflow.md` | 明确从识别赛事到终稿检查的步骤 |
| LaTeX 宏模式库 | `references/latex-patterns.md` | 覆盖插图、表格、公式、算法、引用、脱敏 |
| 编译日志摘要 | `scripts/summarize_build_log.py` | 能从 log 输出错误摘要和疑似修复方向 |
| 终稿提交检查 | `scripts/check_submission.py` | 能检查 PDF、log、身份信息、特殊页、未解析引用 |

### P1：第二阶段做

这些功能能显著提升可靠性，但可以在 P0 后推进。

| 功能 | 产物 | 验收方式 |
|---|---|---|
| 模板状态检查 | `scripts/inspect_template.py` | 输出主文件、章节、out、figures 状态 |
| LaTeX 引用/图片闭环检查 | `scripts/check_tex_links.py` | 能发现重复 label、缺失 label、缺图 |
| CUMCM/MCM 赛事规则 | `references/cumcm.md`, `references/mcm.md` | 能按赛事选择章节、特殊页、build target |
| final review 文档 | `references/final-review.md` | 能按严重程度组织检查项 |
| README skill 使用说明 | `README.md` 或 `docs/` | 用户知道 skill 的定位和边界 |

### P2：第三阶段做

这些功能对产品化有帮助，但不要阻塞 MVP。

| 功能 | 产物 | 验收方式 |
|---|---|---|
| Wuyi/Beijing references | `references/wuyi.md`, `references/beijing.md` | 覆盖两套中文模板特殊页 |
| 图表风格参考 | `references/figure-table-style.md` | 明确论文图表视觉和排版规则 |
| 写作模式参考 | `references/writing-patterns.md` | 提供摘要、假设、结果分析等写作约束 |
| 状态文件 schema | `.paperkit/state.schema.json` | 为 Agent 做准备 |
| CLI Agent 原型 | `paperkit-agent` 或 `scripts/agent_cli.py` | 能执行 init/build/review/fix-log 固定流程 |

### P3：长期增强

这些功能适合在仓库交付能力稳定后再做。

| 功能 | 说明 |
|---|---|
| WebUI | 展示章节状态、编译日志、检查清单 |
| 多 skill 调度 Agent | 调度 problem-analysis、data-analysis、visualization、paperkit |
| RAG | 用于规则、范文、模型库检索 |
| 自动评分器 | 仅作为辅助 rubric，不做最终判断 |
| GitHub Actions | 自动全量编译和 smoke test |

## 8.2 Agent 技术路线

Agent 不应在第一阶段吞掉全部范围。推荐从 CLI Agent 起步：

```text
Python CLI + Pydantic + 本地 state.json + ModelingPaperKit scripts
```

当 CLI 流程稳定后，再升级为：

```text
FastAPI + LangGraph + Pydantic + SQLite/Postgres + React/Vite
```

建议分层：

```text
MathModeling Agent
├── State: contest, target, title, sections, figures, build status
├── Skills: modeling-paperkit, data-analysis, visualization, final-review
├── Tools: build.py, verify_build.py, check_submission.py, summarize_build_log.py
└── UI: CLI first, WebUI later
```

Agent 第一版只做四个固定命令即可：

```bash
paperkit-agent init --target cumcm
paperkit-agent build --target cumcm
paperkit-agent review --target cumcm
paperkit-agent fix-log --target cumcm
```

不要在 Agent 第一版中加入自由度过高的“自动建模”“自动写完整论文”。这些能力可以通过独立 skill 渐进接入。

## 9. 里程碑

### 阶段一：P0 Skill 骨架与日志能力

目标：让 Codex 能正确理解何时使用该 skill，并能处理最常见的编译失败。

产物：

- `SKILL.md`
- `agents/openai.yaml`
- `references/workflow.md`
- `references/repository-map.md`
- `references/latex-patterns.md`
- `scripts/summarize_build_log.py`

验收：

- 用户说“帮我用这个仓库写国赛论文”时，skill 能引导先识别 `templates/cumcm`。
- 用户说“编译报错”时，skill 会先检查 `out/*.log` 和 `scripts/build.py`。
- 对已有 log 能输出短错误摘要。

### 阶段二：P0/P1 提交检查

目标：让终稿检查从语言模型判断变成脚本 + checklist 双层检查。

产物：

- `scripts/check_submission.py`
- `scripts/inspect_template.py`
- `scripts/check_tex_links.py`
- `references/final-review.md`

验收：

- 能发现 PDF 缺失、log Error、缺图、未解析引用、疑似身份信息。
- 能输出按严重程度排序的问题。

### 阶段三：赛事规则 references

目标：把最常用赛事模板差异固化下来。

产物：

- `references/cumcm.md`
- `references/mcm.md`
- `references/wuyi.md`
- `references/beijing.md`

验收：

- 能说明每个赛事的主文件、章节顺序、特殊页和检查重点。
- 能根据赛事选择正确的 build target。

### 阶段四：轻量 CLI Agent

目标：在 skill 和脚本稳定后，开发只负责调度固定流程的 Agent。

产物：

- `paperkit-agent` CLI 或 `scripts/agent_cli.py`
- `.paperkit/state.json`
- `.paperkit/state.schema.json`

验收：

- 能执行 init/build/review/fix-log。
- 能记录目标赛事、章节状态、最近一次编译状态。
- 不做复杂自由规划，只串联已有 skill 和脚本。

### 阶段五：产品化增强

目标：根据真实使用反馈，再考虑 UI 和多 skill 协同。

产物：

- WebUI 原型。
- 多 skill 调度。
- GitHub Actions 全量编译验证。

验收：

- WebUI 能展示章节、编译、检查状态。
- CI 能验证模板至少可编译或脚本可运行。

## 10. 推荐实施顺序

建议按以下顺序推进：

1. 写 `SKILL.md` 和 `workflow.md`，先把行为边界定住。
2. 写 `repository-map.md`，让 skill 充分贴合本仓库。
3. 写 `latex-patterns.md`，沉淀本仓库宏包用法。
4. 实现 `summarize_build_log.py`。
5. 实现 `check_submission.py`。
6. 实现 `inspect_template.py` 和 `check_tex_links.py`。
7. 写 `cumcm.md` 和 `mcm.md`，先覆盖最常用的中文/英文两类模板。
8. 补齐 `wuyi.md`、`beijing.md`。
9. 增加 final review checklist。
10. 在 README 或 docs 中增加 skill 使用说明。
11. 开始 CLI Agent 原型。

## 11. 验收场景

### 场景一：新建国赛论文

用户请求：

```text
我要用这个仓库写国赛 C 题论文，帮我搭结构。
```

期望行为：

- 识别 CUMCM。
- 检查 `templates/cumcm/main_cumcm.tex`。
- 说明需要填写 `\PaperTitle` 和 `sections/`。
- 给出章节填充顺序。
- 不误用 MCM 的 Summary Sheet。

### 场景二：插入模型图表

用户请求：

```text
把这个时间序列预测图插到模型求解章节。
```

期望行为：

- 找到目标章节。
- 确认图片位置。
- 使用本仓库插图规范。
- 添加 label 和正文引用。

### 场景三：编译失败

用户请求：

```text
编译报错了，帮我修。
```

期望行为：

- 运行或读取 `scripts/build.py --target <target>` 的输出。
- 读取 `out/*.log`。
- 用 `summarize_build_log.py` 提取关键错误。
- 修改最小必要 LaTeX 内容。
- 重新编译验证。

### 场景四：提交前检查

用户请求：

```text
帮我最终检查一下能不能提交。
```

期望行为：

- 运行编译。
- 检查 PDF 是否生成。
- 检查日志、图表、引用、脱敏、特殊页。
- 输出按严重程度排序的问题清单。

## 12. 风险与边界

### 风险一：范围膨胀

如果把 skill 做成“自动建模总控”，会和市面上大型 Agent 走到同一条路，复杂度迅速增加。第一版应坚守论文交付边界。

### 风险二：竞赛规则随年份变化

承诺书、AI 声明、页数、提交格式可能每年变化。赛事 references 应标注适用年份，并允许用户提供最新赛规覆盖默认规则。

### 风险三：合规检查不能只靠正则

手机号、邮箱、学校名等可以用正则筛查，但不能保证完全准确。最终输出应标注“疑似”，由用户确认。

### 风险四：LaTeX 环境差异

字体和 TeX Live 版本会导致跨平台问题。skill 应优先引用 `docs/faq.md`，并把字体问题和引擎路径问题作为常见排错入口。

## 13. 成功标准

第一版成功标准：

- Codex 能稳定识别并使用 `ModelingPaperKit` 的四套模板。
- Codex 修改论文时优先遵循本仓库已有 LaTeX 宏和章节结构。
- 编译排错不再只凭猜测，而是基于日志摘要。
- 提交前 review 能发现大部分结构、引用、图片、脱敏和特殊页问题。
- 文档和脚本足够小，可以维护，不会变成难以更新的大型知识库。

## 14. 后续增强方向

第一版稳定后，可以考虑：

- 增加 `.paperkit/state.json`，记录项目状态。
- 增加 `scripts/init_paper_project.py`，从模板复制出独立参赛项目。
- 增加图表目录检查和图注质量检查。
- 增加中文摘要/英文 Summary Sheet 专项评审。
- 增加基于示例论文的章节示范片段。
- 增加与 GitHub Actions 的全量编译验证。
- 将 skill 打包成可安装的 Codex personal skill。
