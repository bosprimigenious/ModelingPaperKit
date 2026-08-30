# 写作 / 去 AI 味 Skills 军火库

本目录是**符号链接**（真源：`~/Projects/FullStack/math_modeling_skills_catalog/writing/`），不覆盖自有 `skills/cumcm-sentence-polish`、`check_prose_style`、`banned-prose`。

```bash
bash scripts/install_writing_skills.sh   # 重装/修链接（同时修 math_modeling2026）
```

前缀约定：

| 前缀 | 含义 | 典型触发 |
|------|------|----------|
| **H-** | English **H**umanize / stop-slop / de-slop | humanize、de-AI、stop slop、sounds like ChatGPT |
| **Z-** | 中文去 AI 味（**Z**h / Humanizer-zh / 说人话） | 去AI味、说人话、翻译腔、润色成母语 |
| **A-** | **A**cademic / 顶会或工程稿写作管线 | 写 intro/abstract、学术润色、IEEE/Nature 腔 |

---

## 推荐用法（建模论文 vs 学术论文）

### 国赛 / 校赛建模稿（默认中文）

1. **先写内容，后去味**：数字、表号、模型式、结论方向以 `runs/` + `claim_map` 为准，不要边写边 humanize。
2. **中文去味选一条主链**（不要叠开 4 个）：
   - 日常/说明/章节叙述 → `Z-MrGeDiao-shuorenhua` 或 `Z-zhi-ai-lab-shuorenhua`
   - 更偏「维基百科 AI 痕迹清单」汉化 → `Z-op7418-Humanizer-zh` / `Z-ai-zixun-humanizer-zh`
   - 要中文特有 pattern 加强 → `Z-RobinZorro86-humanizer-zh-plus`
3. **终裁永远是自有门禁**：
   ```bash
   python scripts/check_prose_style.py …
   # + skills/cumcm-sentence-polish + banned-prose
   ```
4. 英文摘要 / 英文小节再开 **一条** H-（优先 `H-blader-humanizer` 或 `H-stop-slop`）。

### 英文学术 / 顶会向（含你以后投 arXiv、IEEE）

| 阶段 | 用哪个 | 作用 |
|------|--------|------|
| 论证骨架 / 章节修辞 | `A-SNL-UCSB-paper-writing` | Brainstorm→Draft→Evaluate→Write→Compress |
| Nature 系故事线 | `A-SyntaxSmith-nature-writing` | 中文研究者写 NMI/NC 语料提炼 |
| IEEE/ACM 证据边界 | `A-huguryildiz-ieee-acm` | draft/rewrite/humanize **不许越证据** |
| 审稿模拟 / 句级 sharpen | `A-borgr-paper-sharpener` | multi-reviewer + writing assistant |
| 全稿证据系统 | `A-WenyuChiou-academic-writing` | outline↔draft↔review 同步 |
| 学术去 AI 味（保声明强度） | `A-AIScientists-academic-humanizer` | 不去掉 hedging、不改 citation |
| 论文段 humanize | `A-SyntaxSmith-humanize-paper` / `A-celestialdust-humanize-prose` | 学术散文向 |

本机已有全局 **`paper-polish`**（中枢 skill）：顶会摘要/引言/实验/limitation、防 overclaim —— **与 A- 系列互补，声明边界以 paper-polish + 证据账本为准**。

### 明确不要做的事

- 把 blog 向 humanize（加口头禅、故意残缺句）直接套进 **国赛正式稿**。
- 用 detector-bypass 类 skill（如部分「过 GPTZero」宣传）当目标；国赛要的是**像学生写的、过你们 prose 规则**，不是骗检测器。
- 一次会话同时启用 5+ 写作 skill（互相抢触发，文风会碎）。

---

## 目录一览（安装脚本会链这些）

### H — English humanize

| 链接 | 上游 | 备注 |
|------|------|------|
| `H-blader-humanizer` | blader/humanizer | ★ 最高；Wikipedia Signs of AI Writing |
| `H-stop-slop` | hardikpandya/stop-slop | installs 高；英文 slop 清理 |
| `H-jpeggdev-humanize-writing` | jpeggdev/humanize-writing | 8-pass + ai-tells |
| `H-YKehinde-humaniser` | YKehinde/humaniser | 25 patterns + 自审 |
| `H-aihxp-humanizer` | aihxp/humanizer | 多 harness；voice matching |
| `H-WhimseyAI-humanizer` | WhimseyAI/humanizer-skill | 9 rules |
| `H-Skillproofdev-text-humanizer` | Skillproofdev/text-humanizer | 强调保事实 |
| `H-199-humanise-text` | 199-biotechnologies/humanise-text-skill | 大 banned 词表 |
| `H-timolabs-humanize` | timolabs-ai/claude-humanize-skill | 五层编辑 |
| `H-lguz-humanize-writing` | lguz/humanize-writing-skill | 3-pass |
| `H-gregorymm-humanize-text` | gregorymm/humanize-text | 7 类打分（偏 UX copy） |
| `H-isatimur-de-slop` | isatimur/de-slop | de-slop |
| `H-kimhons-humanize` / `H-harshaneel-humanize` / `H-lakshitha-ai-humanizer` | 各作者 | 检测/改写变体 |
| `H-glebis-de-ai` | glebis/claude-skills `de-ai/` | 单目录 de-ai |

### Z — 中文去 AI 味

| 链接 | 上游 | 备注 |
|------|------|------|
| `Z-op7418-Humanizer-zh` | op7418/Humanizer-zh | blader 汉化经典 |
| `Z-ai-zixun-humanizer-zh` | ai-zixun/humanizer-zh | 长文非虚构 / 翻译腔 |
| `Z-syw2039-humanizer-zh` | syw2039/humanizer-zh | 文风校准 |
| `Z-RobinZorro86-humanizer-zh-plus` | RobinZorro86/humanizer-zh-plus | 中文特有 pattern+ |
| `Z-MrGeDiao-shuorenhua` | MrGeDiao/shuorenhua | **说人话**；有评测；开发者中文场景强 |
| `Z-zhi-ai-lab-shuorenhua` | zhi-ai-lab/shuorenhua | 说人话另一实现 |

### A — 学术 / 论文管线

| 链接 | 上游 | 备注 |
|------|------|------|
| `A-AIScientists-academic-humanizer` | AIScientists-Dev/academic-humanizer | 学术腔 + claim↔evidence |
| `A-SyntaxSmith-humanize-paper` | SyntaxSmith/humanize-paper | 论文 humanize |
| `A-celestialdust-humanize-prose` | celestialdust/humanize-prose | 实证六步（偏砍字） |
| `A-momo2young-humanize-academic` | momo2young/humanize-academic-writing | 社科英文学术 |
| `A-crabin-paper-humanizer` | crabin/paper-humanizer-skill | 论文向 |
| `A-SNL-UCSB-paper-writing` | SNL-UCSB/paper-writing-skill | 系统/ML 论文全流程 |
| `A-SyntaxSmith-nature-writing` | SyntaxSmith/nature-writing-skill | Nature 系 |
| `A-huguryildiz-ieee-acm` | huguryildiz/ieee-acm-paper-writing | IEEE/ACM + 证据门 |
| `A-borgr-paper-sharpener` | borgr/paper-sharpener | 审稿模拟 + 写作 sharpen |
| `A-WenyuChiou-academic-writing` | WenyuChiou/academic-writing-skills | 成稿系统 + paper-review |
| `A-kgraph57-paper-writer` | kgraph57/paper-writer-skill | IMRAD / 医学向也可借鉴结构 |
| `A-lishix520-academic-paper` | lishix520/academic-paper-skills | strategist + composer |

完整镜像与检索笔记：`math_modeling_skills_catalog/writing/README.md`。

---

## 与自有栈的关系

```text
内容真源:     runs/ + claim_map + check_model_fitness
结构真源:     skills/cumcm-paper-structure + templates
句级禁令:     banned-prose + check_prose_style + cumcm-sentence-polish
顶会声明:     ~/.grok/skills/paper-polish（中枢）
外部去味:     本目录 H-/Z-/A-（参考改写，不终裁）
```

软链不进 git（见 `.gitignore`）；团队各自跑 `install_writing_skills.sh`。
