# Cursor Tasks — ModelingPaperKit 待办清单

> 总监 (Bosprimigenious) 已搭建好架构骨架。以下任务由 Cursor 逐项执行。
> 每完成一项，在任务末尾标记 `[x]` 并提交一个原子 commit。

---

## Phase 1: 核心引擎完善

### Task 1.1 — 审查 `core/paperkit-base.sty` 的包依赖
- [x] 检查所有 `\RequirePackage` 是否必要且不重复
- [x] 确认 `paperkit-base.sty` 不与 ctexart 内置功能冲突
- [x] 验证 `\figplot` 宏在三个模板中都能正常工作
- [x] 确保 `hyperref` 在所有包之后加载

### Task 1.2 — 增强 `core/paperkit-math.sty`
- [x] 添加更多常用数学环境（如 `remark`, `property` 等）
- [x] 添加矩阵快捷命令：`\mat`, `\vb`, `\trans`（向量用 `\vb`，不覆盖内置 `\vec`）
- [x] 确保定理环境同时支持中英文（通过语言选项）

### Task 1.3 — 增强 `core/paperkit-utils.sty`
- [x] 添加 `\todo` 和 `\draft` 标记宏（用于写作过程）
- [x] 完善 pseudo-code 汉化（补齐所有 `\algrenewcommand`）
- [x] 添加 `\email`, `\phone` 占位符命令（编译时自动替换为 `[已脱敏]`）

---

## Phase 2: 模板完善

### Task 2.1 — CUMCM 模板 (国赛/高教杯)
- [x] 检查 `main_cumcm.tex` 中所有 section 引用与实际 section 文件名一致
- [x] 完善 `sections/problem.tex` — 添加国赛典型的问题重述结构指导
- [x] 完善 `sections/model.tex` — 添加流程图插入示例
- [x] 完善 `sections/appendix.tex` — 添加代码清单示例
- [x] 确认承诺书 `cover.tex` 格式与最新国赛官方要求一致
- [x] 添加 `\maketitle` 替代方案（不使用 ctexart 默认标题页）

### Task 2.2 — MCM 模板 (美赛)
- [x] 完善 `summary_sheet.tex` — 复刻美赛官方 Summary Sheet 精确布局
- [x] 添加 Control Number 和 Problem Choice 的醒目占位
- [x] 确保 MCM 模板不使用任何中文命令/宏
- [x] 添加 MCM 典型的 Introduction/Assumptions/Model/Results/Conclusion 章节文件
- [x] 创建独立的 `sections/` 子文件（不要把所有内容塞在 main_mcm.tex 里）
- [x] 添加 Table of Contents 支持

### Task 2.3 — Wuyi 模板 (五一杯)
- [x] 确认五一杯承诺书格式与 2026 年官方模板一致
- [x] 检查与 CUMCM 模板的差异，确保不存在冗余代码
- [x] 添加五一杯特有的 AI 使用声明页（如适用）

---

## Phase 3: 构建系统

### Task 3.1 — 完善 `scripts/build.py`
- [x] 添加 `--bibtex` 选项支持 BibTeX 编译链
- [x] 添加编译错误检测与友好提示（解析 .log 文件中的 Error 行）
- [x] 支持自定义 TeX 引擎路径
- [x] 添加 `--watch` 模式（文件变化自动重编译）

### Task 3.2 — 完善 `scripts/clean.py`
- [x] 添加 `--dry-run` 模式（只列出将删除的文件，不实际删除）
- [x] 添加交互式确认（`--interactive`）

### Task 3.3 — 创建 `scripts/new_contest.py`
- [x] 一键脚手架工具：`python scripts/new_contest.py --name <name> --lang zh/en`
- [x] 自动创建模板目录、section 文件、main.tex
- [x] 自动注册到 TARGETS 配置

---

## Phase 4: 示例与脱敏数据

### Task 4.1 — 创建 dummy 数据集
- [x] 在 `examples/dummy_data/` 创建合成的 CSV 数据文件
- [x] 数据包含典型的建模场景（时间序列、回归、分类）
- [x] 添加数据说明 README

### Task 4.2 — 创建完整示例论文
- [x] 在 `examples/` 下创建一个完整可编译的示例（如一个简化的国赛论文）
- [x] 使用 dummy 数据，包含完整的建模流程
- [x] 展示 paperkit 的主要功能（表格、图片、算法、代码块）

---

## Phase 5: 文档

### Task 5.1 — 撰写使用文档
- [x] 在 `docs/` 创建 `getting-started.md`（中英文双语）
- [x] 创建 `template-guide.md` 说明每个 section 的写作要点
- [x] 创建 `faq.md` 常见问题（字体缺失、编译报错等）

### Task 5.2 — 撰写 LaTeX 类/包文档
- [x] 为 `paperkit-base.sty` 的所有命令写文档注释
- [x] 为 `paperkit-math.sty` 的定理环境写使用说明
- [x] 为 `paperkit-utils.sty` 的算法环境写使用说明

---

## Phase 6: 质量保证

### Task 6.1 — 编译验证
- [x] 确保 `python scripts/build.py --target all` 三项全部通过
- [x] 检查所有 PDF 输出无 Overfull/Underfull 警告
- [x] 验证交叉引用（\ref, \cite）在所有模板中正确解析
- 复检命令：`python scripts/verify_build.py`（清理后全量编译 + 日志/PDF 检查）

### Task 6.2 — 脱敏审计
- [x] `grep -r` 搜索所有文件中是否残留真实姓名、学号、电话、邮箱、学校名
- [x] 特别注意承诺书/cover 文件中不应用出现任何可识别个人身份的信息
- [x] 确保无 .env 或 credentials 文件被提交

---

---

## Phase 7: 借鉴 CUMCMThesis 增强排版引擎

> 参考仓库 [latexstudio/CUMCMThesis](https://github.com/latexstudio/CUMCMThesis) (cumcmthesis.cls, 664 行)，
> 将其成熟的排版技巧融入我们的 Core+Plugins 架构。**原则：能力进 core/，赛事差异留 template/。**

### Task 7.1 — 集成 cleveref 智能交叉引用
- [x] 在 `core/paperkit-base.sty` 末尾添加 `\RequirePackage{cleveref}`
- [x] 配置中文引用格式：`\crefformat{figure}{图~#2#1#3}`，同理 table、equation
- [x] 配置英文回退：`\ifpkm@langzh` 分支（参考 paperkit-math.sty 的 zh/en/auto 模式）
- [x] 对 theorem/lemma/definition 等也配置 `\crefformat`（中英双语）
- [x] 确保 `cleveref` 在所有包之后加载（已在 paperkit-base.sty 末尾则自动满足）

### Task 7.2 — 修复浮动体排版参数
- [x] 在 `core/paperkit-base.sty` 的 `\geometry` 之后添加浮动参数：
  - `\renewcommand*{\textfraction}{0.05}`（允许页面 95% 为浮动体）
  - `\renewcommand*{\topfraction}{0.9}`
  - `\renewcommand*{\bottomfraction}{0.8}`
  - `\renewcommand*{\floatpagefraction}{0.85}`
- [x] 添加 `\DeclareGraphicsExtensions` 和 `\graphicspath`（搜索 figures/ 等常见目录）

### Task 7.3 — 添加上标引用命令
- [x] 在 `core/paperkit-math.sty` 添加 `\newcommand{\upcite}[1]{\textsuperscript{\cite{#1}}}`

### Task 7.4 — 优化目录 (TOC) 格式
- [x] 在 `core/paperkit-base.sty` 中添加 `tocloft` 的配置（中文模板下）：
  - `\cftsecfont` → 黑体四号
  - `\cftsecdotsep` → 4.5
  - `\cftbeforesecskip` → 7pt
- [x] 确保英文模板下不影响原有 TOC 样式

### Task 7.5 — 重构 CUMCM 封面为 Token 模式
- [x] 参考 CUMCMThesis 的 `\tihao{}`、`\baominghao{}` 设计
- [x] 在 `templates/cumcm/sections/cover.tex` 顶部添加 token 命令定义：
  ```latex
  \newcommand{\cumcmTihao}[1]{\renewcommand{\pkb@tihao}{#1}}
  \newcommand{\cumcmBaominghao}[1]{\renewcommand{\pkb@baominghao}{#1}}
  % ... schoolname, membera/b/c, supervisor, date
  ```
- [x] 将承诺书中的 `[在此填写...]` 替换为 `\pkb@tihao` 等 token
- [x] 在 `main_cumcm.tex` 中添加 token 赋值区域（注释引导用户填写）
- [x] 保留 `% TODO(director): 请核对是否与 2026 年国赛最新承诺书版式一致`

### Task 7.6 — 添加 withoutpreface 编译选项
- [x] 参考 CUMCMThesis 的 `withoutpreface` 选项
- [x] 在 `main_cumcm.tex` 添加注释：电子版提交时可注释掉 `\input{sections/cover}`
- [x] 在 `templates/wuyi/main_wuyi.tex` 同样添加注释引导
- [x] 无需修改 core/（这是赛事特定行为）

---

## Phase 8: 补齐 CUMCMThesis 剩余排版能力

> 第二轮深度对比。Phase 7 已集成 cleveref/浮动体/TOC/Token，本阶段补齐 cross-ref 多引用、图表标题样式、关键词命令、列表优化。

### Task 8.1 — 补齐 cleveref 多引用格式
- [ ] 在 `core/paperkit-utils.sty` 的 cleveref 块中补充 `\crefrangeformat` 和 `\crefmultiformat`
- [ ] 覆盖 figure / table / equation / theorem / lemma / definition（中英双语）
- [ ] 示例效果：`\cref{fig:a,fig:b,fig:c}` → "图~(1, 2, 3)"；`\crefrange{fig:a}{fig:c}` → "图~(1~3)"

### Task 8.2 — 添加图表标题样式
- [ ] 在 `core/paperkit-base.sty` 末尾添加 `\captionsetup`（中文模板下）：
  - figure: 宋体小四加粗，hang 缩进，标题放底部
  - table: 宋体小四加粗，hang 缩进，标题放顶部
- [ ] 英文模板保持原有 caption 样式不变

### Task 8.3 — 添加 `\keywords` 关键词命令
- [ ] 在 `core/paperkit-utils.sty` 添加 `\newcommand{\keywords}[1]`（基于 `\ifpkuLangZh` 显示"关键词"或"Keywords"）
- [ ] 格式：`{\noindent\heiti 关键词：}~{#1}`（中文）/ `{\noindent\bfseries Keywords:}~{#1}`（英文）

### Task 8.4 — 优化列表环境间距
- [ ] 在 `core/paperkit-base.sty` 添加 `\setlist` 全局配置（需 `\RequirePackage{enumitem}`）
- [ ] 参数：`topsep=0.3em, itemsep=0ex plus 0.1ex, leftmargin=1.5em`
- [ ] 中文论文列表紧凑，不浪费版面对

### Task 8.5 — CUMCM 模板中文节号
- [ ] 在 `templates/cumcm/main_cumcm.tex` 的 preamble 区添加：
  ```latex
  \renewcommand{\thesection}{\chinese{section}、}
  ```
  使一级标题显示为"一、问题重述"而非"1 问题重述"
- [ ] 同时更新 `templates/wuyi/main_wuyi.tex` 同步此配置
- [ ] 确保 MCM 模板不受影响

---

## 执行说明

1. 按 Phase 顺序执行，每个 Task 完成后提交一个 commit
2. Commit 格式：`feat: <简短描述>` 或 `fix: <简短描述>`
3. 跨 Phase 依赖：Phase 2 依赖 Phase 1 完成，Phase 6 依赖 Phase 2-5 完成
4. 遇到不确定的设计决策，在代码中以 `% TODO(director): <问题描述>` 标记，并继续执行
5. 完成后输出执行摘要，列出每个 Task 的状态
