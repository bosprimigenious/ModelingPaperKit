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
- [ ] 添加更多常用数学环境（如 `remark`, `property` 等）
- [ ] 添加矩阵快捷命令：`\mat`, `\vec`, `\trans`
- [ ] 确保定理环境同时支持中英文（通过语言选项）

### Task 1.3 — 增强 `core/paperkit-utils.sty`
- [ ] 添加 `\todo` 和 `\draft` 标记宏（用于写作过程）
- [ ] 完善 pseudo-code 汉化（补齐所有 `\algrenewcommand`）
- [ ] 添加 `\email`, `\phone` 占位符命令（编译时自动替换为 `[已脱敏]`）

---

## Phase 2: 模板完善

### Task 2.1 — CUMCM 模板 (国赛/高教杯)
- [ ] 检查 `main_cumcm.tex` 中所有 section 引用与实际 section 文件名一致
- [ ] 完善 `sections/problem.tex` — 添加国赛典型的问题重述结构指导
- [ ] 完善 `sections/model.tex` — 添加流程图插入示例
- [ ] 完善 `sections/appendix.tex` — 添加代码清单示例
- [ ] 确认承诺书 `cover.tex` 格式与最新国赛官方要求一致
- [ ] 添加 `\maketitle` 替代方案（不使用 ctexart 默认标题页）

### Task 2.2 — MCM 模板 (美赛)
- [ ] 完善 `summary_sheet.tex` — 复刻美赛官方 Summary Sheet 精确布局
- [ ] 添加 Control Number 和 Problem Choice 的醒目占位
- [ ] 确保 MCM 模板不使用任何中文命令/宏
- [ ] 添加 MCM 典型的 Introduction/Assumptions/Model/Results/Conclusion 章节文件
- [ ] 创建独立的 `sections/` 子文件（不要把所有内容塞在 main_mcm.tex 里）
- [ ] 添加 Table of Contents 支持

### Task 2.3 — Wuyi 模板 (五一杯)
- [ ] 确认五一杯承诺书格式与 2026 年官方模板一致
- [ ] 检查与 CUMCM 模板的差异，确保不存在冗余代码
- [ ] 添加五一杯特有的 AI 使用声明页（如适用）

---

## Phase 3: 构建系统

### Task 3.1 — 完善 `scripts/build.py`
- [ ] 添加 `--bibtex` 选项支持 BibTeX 编译链
- [ ] 添加编译错误检测与友好提示（解析 .log 文件中的 Error 行）
- [ ] 支持自定义 TeX 引擎路径
- [ ] 添加 `--watch` 模式（文件变化自动重编译）

### Task 3.2 — 完善 `scripts/clean.py`
- [ ] 添加 `--dry-run` 模式（只列出将删除的文件，不实际删除）
- [ ] 添加交互式确认（`--interactive`）

### Task 3.3 — 创建 `scripts/new_contest.py`
- [ ] 一键脚手架工具：`python scripts/new_contest.py --name <name> --lang zh/en`
- [ ] 自动创建模板目录、section 文件、main.tex
- [ ] 自动注册到 TARGETS 配置

---

## Phase 4: 示例与脱敏数据

### Task 4.1 — 创建 dummy 数据集
- [ ] 在 `examples/dummy_data/` 创建合成的 CSV 数据文件
- [ ] 数据包含典型的建模场景（时间序列、回归、分类）
- [ ] 添加数据说明 README

### Task 4.2 — 创建完整示例论文
- [ ] 在 `examples/` 下创建一个完整可编译的示例（如一个简化的国赛论文）
- [ ] 使用 dummy 数据，包含完整的建模流程
- [ ] 展示 paperkit 的主要功能（表格、图片、算法、代码块）

---

## Phase 5: 文档

### Task 5.1 — 撰写使用文档
- [ ] 在 `docs/` 创建 `getting-started.md`（中英文双语）
- [ ] 创建 `template-guide.md` 说明每个 section 的写作要点
- [ ] 创建 `faq.md` 常见问题（字体缺失、编译报错等）

### Task 5.2 — 撰写 LaTeX 类/包文档
- [ ] 为 `paperkit-base.sty` 的所有命令写文档注释
- [ ] 为 `paperkit-math.sty` 的定理环境写使用说明
- [ ] 为 `paperkit-utils.sty` 的算法环境写使用说明

---

## Phase 6: 质量保证

### Task 6.1 — 编译验证
- [ ] 确保 `python scripts/build.py --target all` 三项全部通过
- [ ] 检查所有 PDF 输出无 Overfull/Underfull 警告
- [ ] 验证交叉引用（\ref, \cite）在所有模板中正确解析

### Task 6.2 — 脱敏审计
- [ ] `grep -r` 搜索所有文件中是否残留真实姓名、学号、电话、邮箱、学校名
- [ ] 特别注意承诺书/cover 文件中不应用出现任何可识别个人身份的信息
- [ ] 确保无 .env 或 credentials 文件被提交

---

## 执行说明

1. 按 Phase 顺序执行，每个 Task 完成后提交一个 commit
2. Commit 格式：`feat: <简短描述>` 或 `fix: <简短描述>`
3. 跨 Phase 依赖：Phase 2 依赖 Phase 1 完成，Phase 6 依赖 Phase 2-5 完成
4. 遇到不确定的设计决策，在代码中以 `% TODO(director): <问题描述>` 标记，并继续执行
5. 完成后输出执行摘要，列出每个 Task 的状态
