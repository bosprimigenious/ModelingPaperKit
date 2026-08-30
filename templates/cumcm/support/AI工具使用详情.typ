// ============================================================
//  AI 工具使用详情（支撑材料 / 附录 · 详尽可替换模板）
//  兼容：
//    - 全国大学生数学建模竞赛（2026 试行）：支撑包 PDF 名「AI 工具使用详情.pdf」
//    - 五一数学建模竞赛（2026）：附录标题「AI工具使用详情」+ 正文标注 + 参考文献列工具
//  用法：把所有 #fill[【…】] 换成实填；删掉未发生的情景行；目标成稿约 20–30 页。
//  编译：typst compile "AI工具使用详情.typ" "AI工具使用详情.pdf"
//        cp "AI工具使用详情.pdf" "AI 工具使用详情.pdf"
// ============================================================

#set document(title: "AI 工具使用详情", author: "参赛队（匿名）")
#set page(
  paper: "a4",
  margin: (top: 2.4cm, bottom: 2.4cm, left: 2.4cm, right: 2.4cm),
  numbering: "1",
  footer: context [
    #set align(center)
    #set text(size: 9pt)
    #counter(page).display()
  ],
)
#set text(font: ("Songti SC", "STSong", "Noto Serif CJK SC", "Source Han Serif SC", "SimSun"), size: 10.5pt, lang: "zh")
#set par(justify: true, leading: 0.82em, first-line-indent: 2em)
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  set text(font: ("Heiti SC", "STHeiti", "SimHei", "Noto Sans CJK SC"), weight: "bold", size: 13.5pt)
  set par(first-line-indent: 0em)
  v(0.75em)
  it
  v(0.35em)
}
#show heading.where(level: 2): it => {
  set text(font: ("Heiti SC", "STHeiti", "SimHei"), weight: "bold", size: 11.5pt)
  set par(first-line-indent: 0em)
  v(0.5em)
  it
  v(0.2em)
}
#show heading.where(level: 3): it => {
  set text(font: ("Heiti SC", "STHeiti", "SimHei"), weight: "bold", size: 10.5pt)
  set par(first-line-indent: 0em)
  v(0.35em)
  it
  v(0.15em)
}
#show raw: set text(font: ("Menlo", "Courier New", "Noto Sans Mono"), size: 8.5pt)
#show figure: set block(breakable: true)

#let fill(body) = text(fill: rgb("#8B0000"), body)
#let note(body) = text(size: 9pt, fill: rgb("#333333"), body)
#let ok = fill[【是 / 否】]
#let boxnote(title, body) = block(
  width: 100%,
  inset: 9pt,
  stroke: 0.6pt + rgb("#666666"),
  radius: 2pt,
  {
    set par(first-line-indent: 0em)
    text(weight: "bold")[#title]
    v(0.25em)
    body
  },
)
#let yn-row(name) = ([#name], fill[是/否], fill[【用途一句话】], fill[【T?】], fill[【核验一句话】])

// ======================== 封面可改字段 ========================
#let contest-track = fill[【勾选：五一数学建模竞赛 / 全国大学生数学建模竞赛 / 两者同用本模板整理】]
#let contest-year = "2026"
#let problem-id = fill[【A / B / C（或其他当届题号）】]
#let report-date = fill[【YYYY-MM-DD】]
#let team-internal-id = fill[【队内化名编号，勿写校名姓名】]
#let ai-used = true

#align(center)[
  #set par(first-line-indent: 0em)
  #v(0.8cm)
  #text(size: 17pt, font: ("Heiti SC", "STHeiti", "SimHei"), weight: "bold")[
    人工智能工具使用详情
  ]
  #v(0.35cm)
  #text(size: 11pt)[（详尽可替换模板 · 支撑材料 / 附录）]
  #v(0.9cm)
  #set align(left)
  #pad(left: 1.8cm)[
    #set par(first-line-indent: 0em, leading: 1.05em)
    适用赛道：#contest-track\
    竞赛年份：#contest-year\
    题号：#problem-id\
    报告日期：#report-date\
    队内备注：#team-internal-id\
  ]
]

#v(0.6cm)
#boxnote("提交前必读（按赛道执行）")[
  *国赛（CUMCM 2026 试行）*：论文参考文献前设「AI 工具使用声明」；若已使用，支撑材料压缩包内必须有 PDF，文件名精确为 `AI 工具使用详情.pdf`。\
  *五一（2026）*：正文相应位置标注；参考文献列出所用 AI 工具；附录以「AI工具使用详情」为标题写入本说明（可与支撑材料同文）。\
  *共同红线*：核心建模与分析由队伍主导；AI 输出须人工审查；隐瞒 / 虚假声明 / 未审查 AI 当核心成果 → 取消评奖或竞赛资格。\
  *匿名*：除承诺书外，本文件、截图、路径、文件名禁止出现校名、姓名、学号、指导教师、赛区、真实队号。
]

#pagebreak()

= 编制说明与双赛道规范对照

== 本文件定位

本文档用于一次性整理「何时、用何工具、提示了什么、采纳了什么、如何核验」。它不是论文正文，不替代可复现代码与数值结果。红色#fill[【填写】]为待替换占位；赛后只保留真实发生过的行。

== 国赛 vs 五一：要求对照

#table(
  columns: (auto, 1fr, 1fr),
  stroke: 0.5pt,
  inset: 5.5pt,
  [*项*], [*国赛（2026 试行）*], [*五一（2026）*],
  [是否允许使用], [可用，非强制；公开透明], [可用；公开透明；核心须独立完成],
  [论文声明], [参考文献前二选一固定句式], [正文相应位置标注；附录详写],
  [详情载体], [支撑材料 PDF：`AI 工具使用详情.pdf`], [附录标题「AI工具使用详情」],
  [必写内容], [名称版本；目的环节；提示与过程；采纳修改核验（润色除外）], [名称版本；目的环节；关键交互；采纳与人工修改],
  [参考文献], [可按惯例列工具], [须列出所用 AI，示例格式见官方],
  [违规], [隐瞒/虚假/未审查核心成果 → 取消评奖资格], [未标注说明 → 取消竞赛资格],
)

「官方文本复核日期：」 #fill[【YYYY-MM-DD】] \
「国赛来源：」 #fill[【如：全国大学生数学建模竞赛人工智能工具使用规定（2026年试行）.pdf】] \
「五一来源：」 #fill[【如：2026年五一数学建模竞赛人工智能工具使用规定.docx】]

== 本队填写原则

+ 真实：只记实际使用，不补造。
+ 可核对：关键提示可附摘要；完整日志队内另存。
+ 边界清晰：区分「AI 草稿」与「队内确认结论」。
+ 核心自持：模型选型、关键公式、关键数值、最终结论能说明「无 AI 也能复述复算」。
+ 体积：支撑包通常有上限（常见 ≤20MB，以当年通知为准）；交互原文宜摘要。

= 总开关与一句话用途

== 是否使用 AI

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 7pt,
  [*选项*], [*勾选（只留一项）*],
  [全程未使用任何 AI 工具], fill[【 】],
  [使用了 AI（辅助；核心建模由队内主导）], fill[【✓ 示例】],
)

若「未使用」：保留封面、规范对照、本总开关与第 15 节「未使用」声明即可；后面情景表可整节删除或标「无」。

== 写入论文声明的简要用途（建议 ≤40 字）

#boxnote("国赛声明填空 / 五一正文标注可复用")[
  #fill[【示例：代码调试与报错定位、中文表达润色、LaTeX 排错；核心模型与数值由队内完成并核验。】]
]

== 赛时时间线总表（建议按小时填，便于核对）

#table(
  columns: (auto, auto, 1fr, auto, auto),
  stroke: 0.5pt,
  inset: 4.5pt,
  [*时段*], [*是否用 AI*], [*主要用途*], [*工具*], [*产出是否进论文*],
  [开赛 0–6 h 读题], fill[是/否], fill[【】], fill[T?], fill[是/否],
  [6–24 h 数据/基线], fill[是/否], fill[【】], fill[T?], fill[是/否],
  [第 2 日建模实现], fill[是/否], fill[【】], fill[T?], fill[是/否],
  [第 2–3 日出图出表], fill[是/否], fill[【】], fill[T?], fill[是/否],
  [第 3 日论文成稿], fill[是/否], fill[【】], fill[T?], fill[是/否],
  [提交前 6 h 审校], fill[是/否], fill[【】], fill[T?], fill[是/否],
)

= 情景全清单（直接勾选 · 未发生的删行）

#note[下面按「可能用到 AI 的全部常见情景」列全。赛后：发生的勾「是」并填右侧；未发生的整行删除或标否。这是本模板「可直接替换」的主干。]

== A. 读题与任务分解

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("拆小问交付物（表/图/数值形态）"),
  ..yn-row("歧义句对照题面逐字核对"),
  ..yn-row("数据字段字典整理"),
  ..yn-row("禁止事项/评分关注点提醒"),
  ..yn-row("与往年同类型题的方法对照（不涉当届题解检索）"),
)

== B. 文献与公开资料

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("方法名/关键词建议"),
  ..yn-row("英文摘要翻译对照"),
  ..yn-row("参考文献格式整理"),
  ..yn-row("DOI/题名真实性核对协助"),
  ..yn-row("（禁止）检索当届题解或他人答卷"),
)

== C. 数据理解、清洗与预处理

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("缺失/异常处理策略讨论"),
  ..yn-row("对齐、重采样、单位换算建议"),
  ..yn-row("清洗代码草稿"),
  ..yn-row("清洗前后样本量/分布核对话术"),
  ..yn-row("是否把附件原文粘贴给 AI"),
)

== D. 模型思路与数学推导（核心区）

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("候选模型列表头脑风暴"),
  ..yn-row("假设是否必要的讨论"),
  ..yn-row("目标函数/约束写法建议"),
  ..yn-row("公式符号整理 / LaTeX 公式"),
  ..yn-row("推导查错（非替你推导结论）"),
  ..yn-row("灵敏度/验证方案建议"),
  ..yn-row("（拒绝）黑箱端到端替做全题"),
)

== E. 算法实现与代码（核心区）

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("函数骨架 / boilerplate"),
  ..yn-row("报错栈解读与定位"),
  ..yn-row("向量化/性能小改"),
  ..yn-row("交叉验证划分是否泄漏检查"),
  ..yn-row("指标公式实现核对"),
  ..yn-row("随机种子与可复现"),
  ..yn-row("单元小例手算对照"),
  ..yn-row("IDE Agent 多文件改动"),
  ..yn-row("（拒绝）不可复现的「直接给答案」"),
)

== F. 作图、表头与可视化

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("matplotlib/ggplot 代码草稿"),
  ..yn-row("配色/线型建议"),
  ..yn-row("图题/表题措辞"),
  ..yn-row("流程图/框架图草稿（非数据图）"),
  ..yn-row("（若用）文生图/示意图 AI"),
)

== G. 论文结构、标题与章节

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("目录/章节提纲"),
  ..yn-row("摘要压缩与信息密度"),
  ..yn-row("结果节题表对应检查清单"),
  ..yn-row("贡献句是否 overclaim 审查"),
)

== H. 语言润色与去 AI 味

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("中文病句/翻译腔修改"),
  ..yn-row("英文摘要润色"),
  ..yn-row("humanizer / 说人话 / stop-slop 等 skill"),
  ..yn-row("自有 prose 门禁（banned-prose）复查"),
  ..yn-row("确认润色未改任何数字与结论方向"),
)

== I. 格式、LaTeX/Typst、编译排错

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("xeLaTeX/tectonic 报错解读"),
  ..yn-row("表格三线表/跨页 longtable"),
  ..yn-row("字体/字号/页眉页脚合规核对"),
  ..yn-row("参考文献 bibitem 整理"),
  ..yn-row("AI 详情本 Typst 编译"),
)

== J. Agent / 工作流 / Skill（若使用）

#table(
  columns: (1.6fr, auto, 1.4fr, auto, 1.4fr),
  stroke: 0.5pt,
  inset: 4pt,
  [*情景*], [*用?*], [*用途*], [*工具*], [*核验*],
  ..yn-row("Claude Code / Codex / Cursor Agent"),
  ..yn-row("数模编排 skill（建模/论文）"),
  ..yn-row("model-fitness / claim-coverage 类检查"),
  ..yn-row("自动改多文件后的 diff 人工审"),
  ..yn-row("禁止把 Agent 日志含身份路径提交"),
)

== K. 明确禁止或本队未做的情景（默认否）

#table(
  columns: (1fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 4.5pt,
  [*情景*], [*发生?*], [*说明*],
  [竞赛期间公开平台讨论当届题], fill[否], fill[【确认】],
  [向队外/导师求题解或改论文], fill[否], fill[【确认】],
  [让 AI 编造文献/DOI/数值], fill[否], fill[【确认】],
  [把未运行代码的「结果」写入论文], fill[否], fill[【确认】],
  [用 AI 检索当届题解/答卷], fill[否], fill[【确认】],
  [上传可识别身份的数据或文件名], fill[否], fill[【确认】],
)

#pagebreak()

= 所用 AI 工具清单

#note[对应国赛第 4 条（1）与五一「名称和版本」。一行一种工具/模型；未用的删行。]

#table(
  columns: (auto, 1.2fr, 1.3fr, 1fr, auto),
  stroke: 0.5pt,
  inset: 4.5pt,
  [*编号*], [*工具名称*], [*版本 / 型号 / 模型*], [*提供方*], [*使用日期*],
  [T1], fill[【ChatGPT / Claude / Grok / Gemini / 文心 / 通义 / DeepSeek / …】], fill[【】], fill[【】], fill[【】],
  [T2], fill[【Cursor / Copilot / Continue / Windsurf】], fill[【内嵌模型名】], fill[【】], fill[【】],
  [T3], fill[【Claude Code / Codex / 其他 CLI Agent】], fill[【】], fill[【】], fill[【】],
  [T4], fill[【本地模型：Ollama / LM Studio 等】], fill[【】], fill[【】], fill[【】],
  [T5], fill[【数学/符号：Wolfram / Symbolab 等（若算 AI）】], fill[【】], fill[【】], fill[【】],
  [T6], fill[【翻译：DeepL 等】], fill[【】], fill[【】], fill[【】],
  [T7], fill[【其他】], fill[【】], fill[【】], fill[【】],
)

== 访问方式与环境

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 5pt,
  [*项目*], [*内容*],
  [访问方式], fill[【网页 / API / IDE 插件 / CLI Agent / 本地】],
  [是否联网], fill[【是/否；联网时未检索当届题解】],
  [账号管理], fill[【队内如何共用；勿写密码】],
  [代码助手范围], fill[【仅本机仓库；否写身份路径】],
  [代理/网络], fill[【仅写「经队内合规网络」类，勿写敏感配置】],
)

== 五一参考文献 AI 条目（可复制改写）

#note[五一示例格式：\[编号\] 工具名称，版本/型号，开发机构/公司，使用日期。]

#block(width: 100%, inset: 8pt, fill: rgb("#f7f7f7"))[
  #set par(first-line-indent: 0em)
  #set text(size: 9.5pt)
  #fill[
  \[A1\] DeepSeek，DeepSeek-Vx，深度求索（DeepSeek），YYYY-MM-DD。\
  \[A2\] Claude，Claude x，Anthropic，YYYY-MM-DD。\
  \[A3\] ChatGPT，GPT-x，OpenAI，YYYY-MM-DD。\
  \[A4\] Cursor（模型：…），Anysphere，YYYY-MM-DD。
  ]
]

= 分环节详述（发生则展开；未发生标「本节无」）

== 环节 1：赛题理解与任务分解

+ 目的：#fill[【】]
+ 工具：#fill[【T?】]
+ 是否影响主路线：#fill[【否 / 仅备选，最终队员确认】]
+ 队内否决的 AI 误解：#fill[【】]
+ 对照题面核验：#fill[【】]

== 环节 2：数据与预处理

+ 目的：#fill[【】]
+ 工具：#fill[【】]
+ AI 是否接触附件原文：#fill[【字段名/统计摘要/片段/否】]
+ 最终规则制定人与脚本路径：#fill[【】]
+ 核验（样本量、分布、可复现）：#fill[【】]

== 环节 3：建模与算法（核心）

#boxnote("核心区纪律")[
  模型选择理由、关键假设、目标/约束、主结果数值，必须能回答：「若去掉 AI，队伍仍能独立复述并复算」。
]

+ 目的：#fill[【】]
+ 工具：#fill[【】]
+ 对应小问：#fill[【Q1–Q5】]
+ AI 建议摘要：#fill[【】]
+ 采纳：#fill[【】]
+ 修改/否决：#fill[【】]
+ 数值核验：#fill[【手算小例 / 基线交叉 / 独立重跑】]
+ 结果路径：#fill[【如 runs/…/metrics.csv】]

== 环节 4：作图与表

+ 目的：#fill[【】]
+ 工具：#fill[【】]
+ 图中数据是否全部来自队内脚本：#fill[【是】]
+ 核验：#fill[【】]

== 环节 5：论文写作、润色、去 AI 味

+ 目的：#fill[【】]
+ 工具 / skill：#fill[【】]
+ 是否改动数字或结论方向：#fill[【否；若是必须重核】]
+ prose / banned 检查：#fill[【命令与结果】]

== 环节 6：格式与编译

+ 目的：#fill[【】]
+ 工具：#fill[【】]
+ 最终引擎：#fill[【xelatex / tectonic / typst】]
+ 字体是否按赛规（宋体/黑体/Times）：#fill[【已核】]

== 环节 7：其他

#fill[【无 / 说明】]

#pagebreak()

= 提示策略与典型交互（可附示例）

== 本队提示约定

+ 输入最小化：#fill[【】]
+ 角色设定：#fill[【只协助 debug / 不擅自改模型 …】]
+ 给 AI 的禁止项：#fill[【禁编造文献与数值；禁声称已运行未运行代码】]
+ 输出要求：#fill[【分点、可检验步骤、不确定要标明】]
+ 多轮策略：#fill[【先思路后代码；关键代码必本地跑】]

== 交互示例模板（复制扩到够用；建议至少 3–8 条覆盖核心使用）

#let example(n, default-stage) = [
  === 示例 #n（#fill[#default-stage]）
  #table(
    columns: (auto, 1fr),
    stroke: 0.5pt,
    inset: 6pt,
    [*字段*], [*内容*],
    [工具], fill[【T? · 型号】],
    [时间], fill[【YYYY-MM-DD HH:MM】],
    [小问], fill[【Q?】],
    [提示摘要], fill[【】],
    [回复摘要], fill[【】],
    [队内判断], fill[【采纳 / 部分 / 拒绝】],
    [人工修改], fill[【】],
    [核验], fill[【命令/对照表】],
  )
  「提示原文节选：」
  #block(width: 100%, inset: 7pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
    #set par(first-line-indent: 0em)
    #set text(size: 8.5pt)
    #fill[【脱敏提示；删密钥、姓名、学校、未公开细节】]
  ]
  「回复原文节选：」
  #block(width: 100%, inset: 7pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
    #set par(first-line-indent: 0em)
    #set text(size: 8.5pt)
    #fill[【只留与采纳相关段落】]
  ]
]

#example(1, "读题 / 拆问")
#example(2, "代码报错")
#example(3, "模型实现")
#example(4, "指标/CV 核对")
#example(5, "作图")
#example(6, "润色 / 去 AI 味")
#example(7, "LaTeX 排错")
#example(8, "其他")

== 交互日志索引（完整档在队内）

#table(
  columns: (auto, 1fr, auto),
  stroke: 0.5pt,
  inset: 5pt,
  [*日志 ID*], [*概要*], [*是否纳入本 PDF*],
  [L1], fill[【】], fill[是/否],
  [L2], fill[【】], fill[是/否],
  [L3], fill[【】], fill[是/否],
  [L4], fill[【】], fill[是/否],
  [L5], fill[【】], fill[是/否],
)

#pagebreak()

= 采纳、修改、核验与拒绝

== 采纳总表

#table(
  columns: (auto, auto, 1fr, 1fr, 1fr, auto),
  stroke: 0.5pt,
  inset: 4pt,
  [*ID*], [*类型*], [*AI 要点*], [*采纳*], [*修改/核验*], [*论文位置*],
  [A1], fill[代码], fill[【】], fill[部分], fill[【本地跑通；改了…】], fill[【】],
  [A2], fill[模型思路], fill[【】], fill[拒绝/参考], fill[【】], fill[【】],
  [A3], fill[表述润色], fill[【】], fill[采纳], fill[【未改数字】], fill[【】],
  [A4], fill[公式/LaTeX], fill[【】], fill[【】], fill[【】], fill[【】],
  [A5], fill[作图], fill[【】], fill[【】], fill[【】], fill[【】],
  [A6], fill[【】], fill[【】], fill[【】], fill[【】], fill[【】],
  [A7], fill[【】], fill[【】], fill[【】], fill[【】], fill[【】],
  [A8], fill[【】], fill[【】], fill[【】], fill[【】], fill[【】],
)

== 明确未采纳（防隐性依赖）

#table(
  columns: (auto, 1fr, 1fr),
  stroke: 0.5pt,
  inset: 5pt,
  [*ID*], [*AI 建议*], [*拒绝原因*],
  [R1], fill[【】], fill[【样本/可解释/不可验证】],
  [R2], fill[【】], fill[【】],
  [R3], fill[【】], fill[【】],
  [R4], fill[【】], fill[【】],
)

== 数值与结论核验清单

#table(
  columns: (auto, 1fr, auto, auto),
  stroke: 0.5pt,
  inset: 5pt,
  [*检查项*], [*做法*], [*执行人*], [*通过*],
  [关键指标可复算], fill[【独立重跑；种子/划分一致】], fill[【】], fill[是/否],
  [正文数字与表图一致], fill[【claim map / 交叉】], fill[【】], fill[是/否],
  [无编造文献], fill[【打开 DOI/题名】], fill[【】], fill[是/否],
  [AI 未改结论方向], fill[【对照建模笔记】], fill[【】], fill[是/否],
  [假设均使用或删除], fill[【】], fill[【】], fill[是/否],
  [折外/全样本口径未混写], fill[【】], fill[【】], fill[是/否],
  [表1.1 等题表与锁版 run 一致], fill[【】], fill[【】], fill[是/否],
)

= 分小问细目（Q1–Q5 · 直接替换）

#let qblock(qid) = [
  == 小问 #qid
  #table(
    columns: (auto, 1fr),
    stroke: 0.5pt,
    inset: 5pt,
    [*项*], [*内容*],
    [任务一句话], fill[【题面要求的答案形态】],
    [AI 是否介入], fill[是/否],
    [介入类型], fill[【读题/代码/公式/润色/作图/其他】],
    [工具], fill[【T?】],
    [AI 贡献边界], fill[【】],
    [队内主导部分], fill[【】],
    [关键数值来源路径], fill[【runs/…】],
    [最终答案完全由队内核验产生], fill[是/否],
    [正文标注位置（五一）], fill[【节/段 / 无】],
    [备注], fill[【】],
  )
]

#qblock("Q1")
#qblock("Q2")
#qblock("Q3")
#qblock("Q4")
#qblock("Q5")

#pagebreak()

= 论文内标注与声明文本（按赛道复制）

== 五一：正文标注策略

#fill[【说明在哪些节做了标注。例：第 x 节脚注「表述经 AI 辅助润色，内容经人工审定」；建模节说明「实现阶段使用代码助手排查报错，算法与结果由队内复算确认」。】]

#table(
  columns: (auto, 1fr, 1fr),
  stroke: 0.5pt,
  inset: 5pt,
  [*位置*], [*标注内容*], [*人工审定*],
  [摘要], fill[【润色/未用】], fill[【数字已核】],
  [问题重述/分析], fill[【】], fill[【】],
  [模型建立], fill[【】], fill[【】],
  [求解与结果], fill[【】], fill[【】],
  [结论], fill[【】], fill[【】],
  [附录代码], fill[【】], fill[【】],
)

== 国赛：参考文献前声明（已使用）

#boxnote("复制到论文")[
  #set par(first-line-indent: 0em)
  「AI 工具使用声明」\
  本参赛队在竞赛过程中使用了 AI 工具，主要用于#fill[【简要用途】]，详细使用情况见支撑材料。
]

== 国赛 / 通用：未使用

#boxnote("复制到论文")[
  #set par(first-line-indent: 0em)
  「AI 工具使用声明」\
  本参赛队在竞赛过程中未使用任何 AI 工具。
]

== LaTeX 插入示例

```latex
\section{AI 工具使用声明}
本参赛队在竞赛过程中使用了 AI 工具，主要用于代码调试与中文表达润色，详细使用情况见支撑材料。
% 五一：可改为附录 \section{AI工具使用详情} 并\input 本说明导出的要点
```

= 纪律确认

+ 竞赛期间未在公开或私人平台浏览、发布、讨论当届赛题（论坛/群/知乎/小红书/CSDN/GitHub 等）——#fill[【确认：是】]
+ 未向队外人员（含指导教师）寻求题意解释、选题、求解、改论文——#fill[【确认：是】]
+ 联网 AI 未上传身份信息、未请求检索当届题解——#fill[【确认】]
+ 外源资料均按引用规范处理——#fill[【确认】]

= 支撑材料包文件表

#table(
  columns: (auto, 1fr, auto),
  stroke: 0.5pt,
  inset: 5pt,
  [*文件名*], [*说明*], [*必选*],
  [`AI 工具使用详情.pdf`], [国赛支撑材料文件名（空格）], [已用 AI 时],
  [`AI工具使用详情.pdf`], [无空格副本，便于系统], [建议],
  fill[【附录并入论文 PDF】], fill[【五一路径】], [按赛规],
  fill[【prompts_redacted/】], fill[【脱敏日志，可选】], [可选],
)

= 提交前自检清单

#table(
  columns: (auto, 1fr, auto),
  stroke: 0.5pt,
  inset: 5pt,
  [*\#*], [*检查项*], [*完成*],
  [1], [声明/标注与真实使用一致], fill[ ],
  [2], [国赛：支撑包内文件名正确；五一：附录标题正确], fill[ ],
  [3], [工具名称与版本写清], fill[ ],
  [4], [目的与环节无隐瞒], fill[ ],
  [5], [含提示方式与典型交互（可摘要）], fill[ ],
  [6], [建模/代码/数值写明采纳、修改、核验], fill[ ],
  [7], [核心结论可独立复述复算], fill[ ],
  [8], [五一：参考文献已列 AI 工具], fill[ ],
  [9], [全文匿名], fill[ ],
  [10], [未用 AI/网络讨论当届题解], fill[ ],
  [11], [润色未改数字与结论], fill[ ],
  [12], [队内交叉阅读本详情], fill[ ],
  [13], [支撑包体积符合当届上限], fill[ ],
  [14], [本 PDF 页数与内容充分（建议实填后 20–30 页量级，按实际裁剪）], fill[ ],
)

= 队内签署（化名）

#table(
  columns: (1fr, 1fr, 1fr),
  stroke: 0.5pt,
  inset: 10pt,
  [*队员 A*], [*队员 B*], [*队员 C*],
  [#v(1.1cm)确认真实], [#v(1.1cm)], [#v(1.1cm)],
)

#align(center)[#note[—— 以下附录按需保留；无内容可删 ——]]

#pagebreak()

= 附录 A：代码助手会话主题列表

#table(
  columns: (auto, 1fr, auto, auto, auto),
  stroke: 0.5pt,
  inset: 4.5pt,
  [*会话*], [*主题*], [*改算法逻辑?*], [*已本地复跑*], [*进论文?*],
  [S1], fill[【】], fill[是/否], fill[是/否], fill[是/否],
  [S2], fill[【】], fill[是/否], fill[是/否], fill[是/否],
  [S3], fill[【】], fill[是/否], fill[是/否], fill[是/否],
  [S4], fill[【】], fill[是/否], fill[是/否], fill[是/否],
  [S5], fill[【】], fill[是/否], fill[是/否], fill[是/否],
  [S6], fill[【】], fill[是/否], fill[是/否], fill[是/否],
)

= 附录 B：Skill / Agent 启用清单

#table(
  columns: (auto, 1fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 4.5pt,
  [*名称*], [*用途*], [*启用*], [*人工复核*],
  [humanizer / humanizer-zh / 说人话 / stop-slop], [去 AI 味], fill[是/否], fill[【】],
  [academic-humanizer / humanize-paper], [学术向润色], fill[是/否], fill[【】],
  [math-modeling / mcm / cumcm-\*], [建模编排], fill[是/否], fill[【】],
  [cumcm-model-fitness], [模型是否对题], fill[是/否], fill[【】],
  [paper-polish], [声明边界], fill[是/否], fill[【】],
  [其他], fill[【】], fill[是/否], fill[【】],
)

= 附录 C：风险与诚信声明

我们确认：

1. 本详情所载 AI 使用情况真实、完整，无故意遗漏。
2. 核心模型、关键推导与主要数值由本队完成并核验，AI 仅辅助。
3. 未将未经审查的 AI 内容直接作为核心建模与分析成果提交。
4. 润色未篡改数据含义或结论。
5. 知悉虚假声明或隐瞒使用可能导致取消评奖/竞赛资格。

#v(1cm)
日期：#report-date

= 附录 D：更多脱敏对话续页

#fill[【粘贴更多交互；控制体积。】]
#v(3.5cm)
#fill[【续页】]
#v(3.5cm)
#fill[【续页】]

#pagebreak()

= 附录 E：空白情景扩写页（不够再复制本页）

=== 自定义情景 1
#fill[【名称 / 目的 / 工具 / 提示摘要 / 回复摘要 / 采纳 / 核验】]
#v(2.2cm)
=== 自定义情景 2
#fill[【】]
#v(2.2cm)
=== 自定义情景 3
#fill[【】]
#v(2.2cm)
=== 自定义情景 4
#fill[【】]
#v(2.2cm)
=== 自定义情景 5
#fill[【】]

#pagebreak()

= 附录 F：锁版 run 与论文数字对照（防 AI 改数）

#table(
  columns: (auto, 1fr, 1fr, auto),
  stroke: 0.5pt,
  inset: 5pt,
  [*数字/表*], [*论文中的值*], [*锁版产物路径*], [*一致?*],
  [表1.1 五点], fill[【】], fill[【】], fill[是/否],
  [Q1 MAE/RMSE/R2], fill[【】], fill[【】], fill[是/否],
  [Q2 节点 t1,t2], fill[【】], fill[【】], fill[是/否],
  [Q3 异常计数], fill[【】], fill[【】], fill[是/否],
  [Q4 题表], fill[【】], fill[【】], fill[是/否],
  [Q5 最优组合], fill[【】], fill[【】], fill[是/否],
)


#pagebreak()

= 附录 G：赛时逐日逐时段记录（直接填）

== 第 1 竞赛日

#table(
  columns: (auto, auto, 1fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 4.5pt,
  [*时段*], [*AI?*], [*做了什么*], [*工具*], [*产物/结论*],
  [08–10], fill[是/否], fill[【】], fill[T?], fill[【】],
  [10–12], fill[是/否], fill[【】], fill[T?], fill[【】],
  [12–14], fill[是/否], fill[【】], fill[T?], fill[【】],
  [14–16], fill[是/否], fill[【】], fill[T?], fill[【】],
  [16–18], fill[是/否], fill[【】], fill[T?], fill[【】],
  [18–20], fill[是/否], fill[【】], fill[T?], fill[【】],
  [20–22], fill[是/否], fill[【】], fill[T?], fill[【】],
  [22–24], fill[是/否], fill[【】], fill[T?], fill[【】],
)

== 第 2 竞赛日

#table(
  columns: (auto, auto, 1fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 4.5pt,
  [*时段*], [*AI?*], [*做了什么*], [*工具*], [*产物/结论*],
  [08–10], fill[是/否], fill[【】], fill[T?], fill[【】],
  [10–12], fill[是/否], fill[【】], fill[T?], fill[【】],
  [12–14], fill[是/否], fill[【】], fill[T?], fill[【】],
  [14–16], fill[是/否], fill[【】], fill[T?], fill[【】],
  [16–18], fill[是/否], fill[【】], fill[T?], fill[【】],
  [18–20], fill[是/否], fill[【】], fill[T?], fill[【】],
  [20–22], fill[是/否], fill[【】], fill[T?], fill[【】],
  [22–24], fill[是/否], fill[【】], fill[T?], fill[【】],
)

== 第 3 竞赛日（含提交前）

#table(
  columns: (auto, auto, 1fr, auto, 1fr),
  stroke: 0.5pt,
  inset: 4.5pt,
  [*时段*], [*AI?*], [*做了什么*], [*工具*], [*产物/结论*],
  [08–10], fill[是/否], fill[【】], fill[T?], fill[【】],
  [10–12], fill[是/否], fill[【】], fill[T?], fill[【】],
  [12–14], fill[是/否], fill[【】], fill[T?], fill[【】],
  [14–16], fill[是/否], fill[【】], fill[T?], fill[【】],
  [16–18], fill[是/否], fill[【】], fill[T?], fill[【】],
  [18–提交], fill[是/否], fill[【】], fill[T?], fill[【】],
)

#pagebreak()

= 附录 H：扩展交互示例 9–16


=== 示例 9（#fill[【环节】]）
#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 5.5pt,
  [*字段*], [*内容*],
  [工具], fill[【】],
  [时间], fill[【】],
  [小问], fill[【】],
  [提示摘要], fill[【】],
  [回复摘要], fill[【】],
  [判断/修改/核验], fill[【】],
)
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【提示原文节选】]
]
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【回复原文节选】]
]

=== 示例 10（#fill[【环节】]）
#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 5.5pt,
  [*字段*], [*内容*],
  [工具], fill[【】],
  [时间], fill[【】],
  [小问], fill[【】],
  [提示摘要], fill[【】],
  [回复摘要], fill[【】],
  [判断/修改/核验], fill[【】],
)
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【提示原文节选】]
]
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【回复原文节选】]
]

=== 示例 11（#fill[【环节】]）
#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 5.5pt,
  [*字段*], [*内容*],
  [工具], fill[【】],
  [时间], fill[【】],
  [小问], fill[【】],
  [提示摘要], fill[【】],
  [回复摘要], fill[【】],
  [判断/修改/核验], fill[【】],
)
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【提示原文节选】]
]
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【回复原文节选】]
]

=== 示例 12（#fill[【环节】]）
#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 5.5pt,
  [*字段*], [*内容*],
  [工具], fill[【】],
  [时间], fill[【】],
  [小问], fill[【】],
  [提示摘要], fill[【】],
  [回复摘要], fill[【】],
  [判断/修改/核验], fill[【】],
)
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【提示原文节选】]
]
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【回复原文节选】]
]

=== 示例 13（#fill[【环节】]）
#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 5.5pt,
  [*字段*], [*内容*],
  [工具], fill[【】],
  [时间], fill[【】],
  [小问], fill[【】],
  [提示摘要], fill[【】],
  [回复摘要], fill[【】],
  [判断/修改/核验], fill[【】],
)
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【提示原文节选】]
]
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【回复原文节选】]
]

=== 示例 14（#fill[【环节】]）
#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 5.5pt,
  [*字段*], [*内容*],
  [工具], fill[【】],
  [时间], fill[【】],
  [小问], fill[【】],
  [提示摘要], fill[【】],
  [回复摘要], fill[【】],
  [判断/修改/核验], fill[【】],
)
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【提示原文节选】]
]
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【回复原文节选】]
]

=== 示例 15（#fill[【环节】]）
#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 5.5pt,
  [*字段*], [*内容*],
  [工具], fill[【】],
  [时间], fill[【】],
  [小问], fill[【】],
  [提示摘要], fill[【】],
  [回复摘要], fill[【】],
  [判断/修改/核验], fill[【】],
)
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【提示原文节选】]
]
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【回复原文节选】]
]

=== 示例 16（#fill[【环节】]）
#table(
  columns: (auto, 1fr),
  stroke: 0.5pt,
  inset: 5.5pt,
  [*字段*], [*内容*],
  [工具], fill[【】],
  [时间], fill[【】],
  [小问], fill[【】],
  [提示摘要], fill[【】],
  [回复摘要], fill[【】],
  [判断/修改/核验], fill[【】],
)
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【提示原文节选】]
]
#block(width: 100%, inset: 6pt, fill: rgb("#f6f6f6"), stroke: 0.4pt + rgb("#ccc"))[
  #set par(first-line-indent: 0em)
  #set text(size: 8.5pt)
  #fill[【回复原文节选】]
]

#pagebreak()

= 附录 I：全文润色段落对照（可选 · 防改数）

对每一处「经 AI 润色」的段落保留对照（只留必要几条）：

#table(
  columns: (auto, 1fr, 1fr, auto),
  stroke: 0.5pt,
  inset: 4.5pt,
  [*ID*], [*润色前要点*], [*润色后要点*], [*数字未变?*],
  [P1], fill[【】], fill[【】], fill[是/否],
  [P2], fill[【】], fill[【】], fill[是/否],
  [P3], fill[【】], fill[【】], fill[是/否],
  [P4], fill[【】], fill[【】], fill[是/否],
  [P5], fill[【】], fill[【】], fill[是/否],
  [P6], fill[【】], fill[【】], fill[是/否],
  [P7], fill[【】], fill[【】], fill[是/否],
  [P8], fill[【】], fill[【】], fill[是/否],
)

#pagebreak()

= 附录 J：大段粘贴区（对话 / diff / 日志）

#note[以下预留约数页空白块；把脱敏材料贴满即接近 20–30 页成稿。无材料则删除本附录以免空洞。]

#for i in range(1, 7) [
  === 粘贴块 #i
  #block(width: 100%, height: 11cm, inset: 8pt, stroke: 0.5pt + rgb("#999"), fill: rgb("#fcfcfc"))[
    #set par(first-line-indent: 0em)
    #set text(size: 8.5pt, fill: rgb("#8B0000"))
    【粘贴脱敏内容；或写「本块无」】
  ]
  #v(0.35cm)
]


#align(center)[
  #set text(size: 8.5pt, fill: rgb("#666"))
  模板版本：2026-AI-Use-Detail-Typst-2.0（详尽情景清单）\
  规范：国赛 2026 试行 + 五一 2026 AI 规定 \
  使用：替换全部红色占位；删除未发生情景；实填后建议 20–30 页量级。
]
