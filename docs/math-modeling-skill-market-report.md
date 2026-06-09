# 数学建模 Skill 市场调研报告

调研日期：2026-06-09

本文调研对象是公开网络中与“数学建模 skill / agent / workflow”相关的仓库、目录页和平台页，重点观察它们如何组织数学建模比赛流程，以及这些做法对 `ModelingPaperKit` 的 skill 设计有什么启发。

## 结论摘要

市面上已经出现了专门面向数学建模竞赛的 skill 仓库。它们大致分成四类：

1. **竞赛全流程 Skill**：把国赛、美赛等比赛拆成阶段化流程，包含选题、建模、求解、写作、评审。
2. **Agent 平台型项目**：提供 WebUI、后端、代码解释器、RAG、联网搜索、人机审批等完整系统。
3. **轻量工作流 Skill**：一个 `SKILL.md` 描述三到五个阶段，适合快速安装和复用。
4. **资源库 / Prompt 库**：收集模型、算法、模板、AI prompt，不一定是标准 skill，但可作为 skill 的 reference 资源。

对 `ModelingPaperKit` 来说，最值得借鉴的是：**分阶段工作流、竞赛特化配置、状态文件、反馈评审层、可复用模板资源、最终提交检查**。但本仓库已有明显优势：它已经拥有稳定的 LaTeX 模板和构建脚本，因此不宜简单复制“全自动写论文 Agent”，更适合做一个“排版 + 写作 + 合规 + 交付”方向的 Codex skill。

## 调研样本

| 项目 | 类型 | 主要特点 | 参考链接 |
|---|---|---|---|
| `handsomeZR-netizen/mathmodel-skill` | 竞赛全流程 skill | 支持 CUMCM、MCM/ICM、电工杯；10 阶段、4 层反馈、问答式 Friendly Mode；兼容 Claude Code 与 Codex | [GitHub Topics 摘要](https://github.com/topics/mathematical-modeling), [README raw](https://raw.githubusercontent.com/handsomeZR-netizen/mathmodel-skill/main/README.md), [SKILL.md raw](https://raw.githubusercontent.com/handsomeZR-netizen/mathmodel-skill/main/SKILL.md) |
| `Lupynow/math-modeling-skills` | 竞赛工具链 skill | 标称覆盖 CUMCM A/B/C 与 MCM/ICM A-F，从拿题到论文一条龙 | [GitHub 仓库](https://github.com/Lupynow/math-modeling-skills), [GitHub Topics 摘要](https://github.com/topics/mathematical-modeling) |
| `usail-hkust/LLM-MM-Agent` | 学术/平台型 Agent | NeurIPS 2025 项目；四阶段：问题分析、数学建模、计算求解、报告生成；含开源 demo | [GitHub 仓库](https://github.com/usail-hkust/LLM-MM-Agent) |
| `jihe520/MathModelAgent` | 平台型 Agent + skills | WebUI、CLI、Docker、本地部署；规划支持 HIL、Evaluator、RAG、联网搜索、LaTeX 模板 | [GitHub 仓库](https://github.com/jihe520/MathModelAgent) |
| ClaudSkills `mathematical-modeling` | 通用建模 skill | 面向科学研究/分析；覆盖建模循环、优化、概率模型、仿真、模型批判 | [ClaudSkills 页面](https://claudskills.com/skills/mathematical-modeling/) |
| SkillsMP `math-modeling` | 轻量竞赛 skill | 三阶段：建模分析、代码实现、论文撰写；适用于 CUMCM、MCM/ICM | [SkillsMP 页面](https://skillsmp.com/zh/skills/diegosouzapw-awesome-omni-skill-skills-data-ai-math-modeling-skill-md) |
| XiaoMaColtAI `math-modeling-skill` | 轻量竞赛 skill | 三阶段：模型分析、代码实现、论文写作；强调 Python/MATLAB 和 docx 输出 | [Claude Marketplace 页面](https://claudemarketplaces.com/skills/xiaomacoltai/math-modeling-skill/math-modeling) |
| `sixtdreanight/math-modeling-resources` | 资源库 | 模型、算法、赛事指南、AI 辅助工具集合 | [GitHub Topics 摘要](https://github.com/topics/cumcm?o=asc&s=stars) |
| `openai/skills` skill-creator | Skill 规范参考 | 说明 skill 由 `SKILL.md`、可选 `agents/openai.yaml`、`scripts/`、`references/`、`assets/` 组成 | [OpenAI skills 仓库](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md) |

## 别人是怎么做的

### 1. 阶段化是主流

几乎所有成熟方案都会把数学建模拆成阶段。`mathmodel-skill` 是最工程化的例子：它声明 10 个阶段、4 层反馈、3 种模式，并把竞赛特化内容放进 `competitions/`。`MM-Agent` 则采用更抽象的四阶段：问题分析、数学建模、计算求解、报告生成。

这说明数学建模 skill 不应该只是一份“模型大全”。真正有用的是流程约束：先读题，再做假设与变量，再建模，再求解，再写论文，再做终审。

### 2. 竞赛特化配置很重要

竞赛之间差异很大。国赛重中文论文、摘要、承诺书、AI 声明、问题拆解；美赛重 Summary Sheet、英文表达、communication、letter 或 memo；电工杯更偏工程场景和多子问。

`mathmodel-skill` 的做法是把 CUMCM、MCM、Diangong 放在 `competitions/` 目录下，每个竞赛有自己的 winning patterns、phrase bank、anti-patterns、abstract template、paper skeleton。这种方式比在一个 `SKILL.md` 里硬塞所有规则更健康。

### 3. Skill 不是只有说明，还要有资源

根据 `openai/skills` 的 skill-creator 说明，一个 skill 可以包含：

- `SKILL.md`：触发说明与核心流程
- `agents/openai.yaml`：UI 元数据
- `scripts/`：确定性脚本
- `references/`：按需加载的参考材料
- `assets/`：模板、图片、字体、样例等输出资源

数学建模类 skill 正好适合这种结构。模型目录、论文骨架、评分表、图表规范、LaTeX 片段都不应该全部塞进 `SKILL.md`，而应该做成 references 和 assets。

### 4. 状态文件和问答式交互是加分项

`mathmodel-skill` 强调 Friendly Mode：用户只回答编号问题，agent 自动维护 `state/decision_log.json`。这很适合数学建模比赛，因为比赛周期长、任务容易中断、队友可能切换工具。

对 `ModelingPaperKit` 来说，状态文件可以记录：

- 当前比赛类型
- 题号和子问题
- 论文标题
- 各章节完成度
- 图表清单
- 参考文献清单
- 编译状态
- 最终提交检查结果

### 5. 反馈层越来越常见

平台型项目和高级 skill 都在加入评估器、重跑、panel review、人机审批。`MathModelAgent` 的路线图包括 HIL、Evaluator + Feedback、RAG、联网搜索、Fallback handoff；`mathmodel-skill` 也包含多层 critic 和终局多视角评审。

这说明一个强 skill 不只会生成内容，还要能检查内容。数学建模尤其需要检查：

- 子问题是否全部回答
- 模型假设是否支撑后文
- 公式是否有变量解释
- 图表是否被正文引用
- 摘要是否覆盖方法、结果、结论
- 代码结果是否和论文表格一致
- 是否存在身份信息泄露

## 对 ModelingPaperKit 的启发

`ModelingPaperKit` 当前是 LaTeX 模板与构建工具包，它的天然优势不是“自动建模”，而是“把最终论文交付做好”。因此建议不要做一个过大的万能 agent，而是围绕本仓库能力做一个专用 skill：

```text
modeling-paperkit
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── workflow.md
│   ├── cumcm.md
│   ├── mcm.md
│   ├── wuyi.md
│   ├── beijing.md
│   ├── latex-patterns.md
│   ├── final-review.md
│   └── figure-table-style.md
├── scripts/
│   ├── inspect_template.py
│   ├── check_submission.py
│   └── summarize_build_log.py
└── assets/
    └── section-checklists/
```

建议定位：

> 用于数学建模竞赛论文的 `ModelingPaperKit` 写作、排版、编译、检查和终稿交付。触发场景包括使用 CUMCM/MCM/Wuyi/Beijing 模板、填写 sections、插入图表公式、修复 LaTeX 编译错误、检查脱敏和提交格式。

## 推荐 Skill 分层

### 第一层：PaperKit 专用交付 skill

优先级最高，直接服务当前仓库。

功能包括：

- 识别用户使用哪个模板
- 指导填写 `main_*.tex` 和 `sections/`
- 插入公式、表格、算法、图片
- 调用 `scripts/build.py`
- 解析 LaTeX 错误日志
- 检查 PDF 生成结果
- 做最终提交 checklist

### 第二层：论文写作 skill

可以作为独立 skill，也可以作为 PaperKit skill 的 references。

功能包括：

- 摘要生成与压缩
- 问题重述
- 模型假设
- 符号说明
- 模型建立与求解
- 结果分析
- 模型评价
- 参考文献与附录

### 第三层：建模与数据 skill

这层不必一开始做得很大，因为市面上的全流程 Agent 已经很多。可以先做轻量版本：

- 题型识别
- 模型候选推荐
- 数据清洗建议
- 图表清单生成
- 结果解释模板

### 第四层：最终评审 skill

比赛后期价值最高。

检查项包括：

- 章节完整性
- 子问题对应关系
- 图表引用闭环
- 公式变量解释
- 编译日志
- 身份脱敏
- AI 声明
- 页数和文件命名

## 建议的最小可行版本

第一版不建议做“自动完成数学建模”，而应做一个能可靠帮用户用好本仓库的 skill：

1. `SKILL.md` 只保留核心流程：识别赛事、检查模板、协助写作、编译、终审。
2. `references/` 按赛事拆规则：`cumcm.md`、`mcm.md`、`wuyi.md`、`beijing.md`。
3. `references/latex-patterns.md` 收集本仓库已有宏：`\figplot`、`\keywords`、`\vb`、`\mat`、`\topline`、`\midline`、`\bottomline`。
4. `scripts/check_submission.py` 做可确定的检查：PDF 是否存在、日志是否有 Error、是否出现邮箱电话、是否缺图、是否缺引用。
5. `scripts/summarize_build_log.py` 解析 `out/*.log`，给 Codex 更短的错误摘要。

## 和市面方案的差异化

市面方案大多想覆盖完整比赛流程，从读题到生成论文。`ModelingPaperKit` 更适合走一条更稳的路：

- 不承诺替用户建模拿奖。
- 不把模型大全硬塞进上下文。
- 专注“论文落地”：结构、排版、编译、合规、终审。
- 利用已有 `templates/` 和 `scripts/`，把 skill 做成仓库的自然延伸。

这会比泛化 Agent 更容易可靠，也更贴合本仓库已经具备的价值。

## 参考来源

- GitHub Topics: mathematical-modeling: https://github.com/topics/mathematical-modeling
- GitHub Topics: cumcm: https://github.com/topics/cumcm?o=asc&s=stars
- handsomeZR-netizen/mathmodel-skill README: https://raw.githubusercontent.com/handsomeZR-netizen/mathmodel-skill/main/README.md
- handsomeZR-netizen/mathmodel-skill SKILL.md: https://raw.githubusercontent.com/handsomeZR-netizen/mathmodel-skill/main/SKILL.md
- Lupynow/math-modeling-skills: https://github.com/Lupynow/math-modeling-skills
- usail-hkust/LLM-MM-Agent: https://github.com/usail-hkust/LLM-MM-Agent
- jihe520/MathModelAgent: https://github.com/jihe520/MathModelAgent
- ClaudSkills Mathematical Modeling: https://claudskills.com/skills/mathematical-modeling/
- SkillsMP math-modeling: https://skillsmp.com/zh/skills/diegosouzapw-awesome-omni-skill-skills-data-ai-math-modeling-skill-md
- Claude Marketplace XiaoMaColtAI math-modeling: https://claudemarketplaces.com/skills/xiaomacoltai/math-modeling-skill/math-modeling
- OpenAI skills skill-creator: https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md
