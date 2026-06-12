# ModelingPaperKit Frontend Plan

日期：2026-06-12

本文定义 `ModelingPaperKit Studio` 的前端产品形态。它面向数学建模比赛论文，不是通用 Markdown 编辑器、普通 LaTeX IDE，也不是营销站点。它的核心任务是让用户在比赛高压时间内清楚知道：

- 当前论文项目处于什么状态。
- 哪些章节还没写。
- 哪些图表、引用、支撑材料、AI 使用记录有风险。
- 编译是否成功。
- 最终提交还差什么。

## 1. 产品定位

前端应是一个 **数学建模论文交付工作台**。

```text
左侧：项目结构和章节状态
中间：当前章节 / PDF / 检查结果
右侧：Agent 建议、任务清单、风险提示
顶部：赛事、题号、倒计时、Build/Review 状态
```

它不应该是：

- 营销首页。
- 全屏聊天机器人。
- 纯代码编辑器。
- 泛用论文写作工具。
- “一键自动获奖”产品。

## 2. 目标用户工作流

数学建模论文前端要围绕真实比赛流程设计。

### 2.1 初始化项目

用户目标：

- 选择比赛类型。
- 选择题号。
- 选择模板。
- 生成项目结构。

界面需求：

- 比赛选择：CUMCM / MCM / Wuyi / Beijing。
- 题号输入：A/B/C/D/E/F 或自定义。
- 安全模式：`off` / `cumcm_active` / `mcm_active`。
- 模板预览：主文件、章节列表、特殊页说明。

关键提示：

- CUMCM active 模式下提示不能浏览公开赛题讨论平台。
- MCM active 模式下提示外部来源必须记录引用。

### 2.2 写作推进

用户目标：

- 知道哪些章节未完成。
- 把模型结果写入论文。
- 插入图表、表格、公式和算法。

界面需求：

- 章节状态：missing / placeholder / draft / reviewed / ready。
- 每个章节显示：
  - 字数或行数。
  - TODO/DRAFT 标记数量。
  - 图表数量。
  - unresolved reference 数量。
  - 最近修改时间。
- 章节编辑器提供 LaTeX 片段插入：
  - figure via `\figplot`
  - booktabs table
  - algorithm block
  - equation block
  - `\cref` reference
  - keywords block

### 2.3 编译排错

用户目标：

- 一键编译。
- 快速知道失败原因。
- 让 Agent 做最小修复。

界面需求：

- Build 按钮。
- Clean Build 选项。
- BibTeX 选项。
- Log Summary 面板。
- Findings 分级：
  - Critical
  - Warning
  - Info
- “Apply suggested fix” 必须由用户确认。

### 2.4 终稿检查

用户目标：

- 知道能不能提交。
- 发现身份信息、缺图、缺引用、格式和特殊页风险。

界面需求：

- Final Review 按钮。
- 按赛事显示 checklist。
- 检查项分组：
  - Build
  - Structure
  - Figures & References
  - Identity & Anonymity
  - AI Usage
  - Supporting Materials
  - Contest-Specific Rules
- 每个 finding 可跳转到文件/行号。
- 输出最终 review report。

## 3. 信息架构

### 3.1 顶部状态栏

显示：

- 项目名。
- 赛事。
- 题号。
- 安全模式。
- 当前阶段。
- 最近 build 状态。
- 最近 review 状态。
- 截止时间倒计时，后续可选。

示例：

```text
CUMCM · Problem C · cumcm_active · Day 3 Paper · Build: Failed · Review: 3 Critical
```

### 3.2 左侧导航

一级分组：

- Overview
- Paper
- Figures & Tables
- Sources
- AI Usage
- Supporting Materials
- Build
- Final Review

Paper 下展示章节：

- Cover / Summary Sheet / AI Declaration
- Abstract
- Problem
- Analysis
- Assumptions
- Notation
- Model
- Solution
- Results
- Validation
- Evaluation
- Conclusion
- References
- Appendix

### 3.3 中间工作区

根据当前路由切换：

- 章节编辑器。
- PDF 预览。
- Build 日志摘要。
- Review 报告。
- 图表 manifest。
- AI 使用记录。

### 3.4 右侧 Agent 面板

右侧不是纯聊天窗口，而是“行动建议面板”。

包含：

- 当前上下文。
- 推荐下一步。
- 可执行动作按钮：
  - Inspect
  - Build
  - Review
  - Fix Log
  - Insert Figure
  - Draft Section
- 风险提示。
- Agent run 历史。

## 4. 页面设计

### 4.1 Dashboard

用途：列出项目。

内容：

- Project name。
- Contest。
- Problem。
- Last build。
- Last review。
- Last modified。
- Create Project 按钮。

不需要 hero，不需要营销文案。

### 4.2 Project Overview

用途：项目总览。

内容：

- 项目状态卡片：
  - Sections complete
  - Figures linked
  - Build status
  - Critical findings
  - AI usage entries
  - Supporting materials status
- Timeline / Next Milestone。
- Immediate risks。
- Quick actions。

### 4.3 Paper Editor

用途：编辑 `sections/*.tex`。

布局：

```text
Left: section tree
Center: LaTeX editor
Right: section findings + snippets + agent actions
```

编辑器要求：

- MVP 可用 textarea 或 CodeMirror/Monaco。
- 显示保存状态。
- 支持跳转 line。
- 支持插入模板片段。
- 不自动改写大段内容，除非用户确认。

### 4.4 Build View

用途：编译和排错。

内容：

- Build configuration：
  - target
  - clean
  - bibtex
  - engine path
- Build history。
- Latest PDF status。
- Log Summary。
- Critical findings。
- Suggested fixes。

### 4.5 Final Review View

用途：提交前检查。

内容：

- Contest-specific checklist。
- Findings by severity。
- Export review report。
- Go to file/line links。
- AI usage and supporting materials status。

### 4.6 Figures & Tables View

用途：管理图表和结果一致性。

内容：

- Figure/table list。
- Source script。
- Source data。
- Generated file path。
- Used in section。
- LaTeX label。
- Missing file / unused asset warnings。

### 4.7 AI Usage View

用途：维护 AI 使用记录。

内容：

- AI usage entries。
- Add entry。
- Export CUMCM AI usage details。
- Export MCM AI use report。

### 4.8 Supporting Materials View

用途：管理 CUMCM 支撑材料。

内容：

- Code files。
- Data files。
- Result files。
- README status。
- Identity scan result。
- ZIP/RAR readiness checklist。

## 5. 核心组件

```text
AppShell
TopStatusBar
ProjectSidebar
SectionTree
SectionEditor
SnippetToolbar
AgentPanel
BuildStatus
BuildRunList
LogSummary
FindingList
ReviewChecklist
FigureManifestTable
AIUsageTable
SupportingMaterialsPanel
ContestModeBadge
RiskBadge
ActionButtonGroup
```

组件原则：

- 使用紧凑、信息密度高的工作台布局。
- 不做大 hero。
- 不做装饰性卡片堆叠。
- 卡片只用于重复项、状态块和结果分组。
- 按严重程度使用稳定颜色：
  - Critical: red
  - Warning: amber
  - Info: blue/gray
  - Ready/Pass: green

## 6. 前端状态模型

前端应围绕后端/API 的结构化状态渲染。

核心类型：

```ts
type Severity = "critical" | "warning" | "info";
type Contest = "cumcm" | "mcm" | "wuyi" | "beijing" | "example";
type ContestMode = "off" | "cumcm_active" | "mcm_active";
type SectionStatus = "missing" | "placeholder" | "draft" | "reviewed" | "ready";

type Finding = {
  severity: Severity;
  code: string;
  message: string;
  path: string | null;
  line: number | null;
};

type ProjectState = {
  projectId: string;
  contest: Contest;
  target: Contest;
  contestMode: ContestMode;
  problemId?: string;
  title?: string;
  sections: Record<string, SectionStatus>;
  lastBuild?: BuildRun;
  lastReview?: ReviewRun;
};
```

## 7. API Dependencies

前端 MVP 需要这些 API：

```text
GET    /api/projects
POST   /api/projects
GET    /api/projects/{id}
GET    /api/projects/{id}/files
GET    /api/projects/{id}/files/{path}
PATCH  /api/projects/{id}/files/{path}
POST   /api/projects/{id}/build
GET    /api/projects/{id}/builds/{run_id}
POST   /api/projects/{id}/review
GET    /api/projects/{id}/reviews/{run_id}
POST   /api/projects/{id}/agent/run
```

没有后端时，可以先用 mock JSON 文件开发 UI。

建议 mock 文件：

```text
frontend/mocks/project-state.json
frontend/mocks/build-run.json
frontend/mocks/review-run.json
frontend/mocks/findings.json
frontend/mocks/figure-manifest.json
```

## 8. 前端开发阶段

### FE Phase 0: Static Mock Workbench

目标：不用后端，先验证信息架构。

任务：

- 创建 `frontend/`。
- 创建 React + Vite + TypeScript 项目。
- 使用 mock JSON 渲染：
  - Dashboard
  - Project Overview
  - Paper Editor placeholder
  - Build View
  - Final Review View
- 不接 Agent。
- 不接真实文件系统。

验收：

- 能在浏览器打开工作台。
- 能看到章节状态、build 状态、review findings。
- UI 信息密度合理，不像 landing page。

### FE Phase 1: Backend Integration

目标：接入 FastAPI。

任务：

- 接入 project API。
- 接入 file read/write API。
- 接入 build API。
- 接入 review API。
- 增加 loading/error/empty 状态。

验收：

- 用户能打开项目。
- 用户能查看/编辑章节文件。
- 用户能触发 build/review。
- 用户能看到结构化 findings。

### FE Phase 2: Agent Actions

目标：让 Agent 作为可控动作出现。

任务：

- AgentPanel 接入 `/agent/run`。
- 支持动作：
  - inspect
  - build
  - review
  - fix-log
  - insert-figure
- Agent 修改文件前显示 diff 或 patch preview。

验收：

- 用户能确认或拒绝 Agent 修改。
- Agent run 有历史记录。
- 失败时显示清楚原因。

### FE Phase 3: Contest Delivery Views

目标：覆盖真实比赛交付。

任务：

- AI Usage View。
- Supporting Materials View。
- Figure Manifest View。
- Source Log View。
- Export review report。

验收：

- CUMCM 用户能看到支撑材料和 AI 使用风险。
- MCM 用户能看到 source citation 和 AI report 风险。

## 9. 前端不做什么

MVP 不做：

- 全自动论文生成。
- 复杂协同编辑。
- 富文本 WYSIWYG LaTeX。
- 实时多人编辑。
- 在线提交比赛。
- 大型模型选择向导。
- 花哨视觉首页。

## 10. 设计验收标准

一个合格的前端 MVP 应满足：

- 用户 10 秒内知道论文是否能编译。
- 用户 10 秒内知道最终提交还有几个 Critical 问题。
- 用户能直接跳转到有问题的文件和行。
- 用户能看到每个章节的完成状态。
- 用户能区分 CUMCM 和 MCM 的不同提交风险。
- 用户能控制 Agent 修改，而不是被 Agent 自动覆盖。

## 11. 推荐下一步

在当前仓库阶段，不要立刻实现前端。先完成：

1. Phase 0 check scripts。
2. Skill references。
3. CLI Agent。

当前可以做的前端准备：

- 保留本计划。
- 后续从 `FE Phase 0: Static Mock Workbench` 开始。
- 先用 mock JSON 验证信息架构，再接后端。
