# 外部数模 Skills 军火库

本目录是**符号链接**（真源：`~/Projects/FullStack/math_modeling_skills_catalog/`），不覆盖自有 `skills/cumcm-*`。

```bash
bash scripts/install_external_skills.sh   # 重装/修链接（同时修 math_modeling2026）
```

## 社区检索来源（2026-08）

| 渠道 | 常见点名 / 信号 | 说明 |
|------|-----------------|------|
| **CSDN** | [XiaoMaColtAI 数模 Skill 教程](https://blog.csdn.net/SJbeITenginner/article/details/157361171)、[美赛六题攻略](https://blog.csdn.net/SJbeITenginner/article/details/157584559) | 中文圈传播最广，主推 XiaoMa 三阶段 |
| **掘金** | [XiaoMa 完整指南](https://juejin.cn/post/7616936839875395618)、MathModelAgent 沸点 | 作者自述 + 开源推荐 |
| **编程导航 / 知乎系** | XiaoMa 专栏文 | 安装与角色流介绍 |
| **GitHub topics `math-modeling`** | XiaoMa ★~950、handsomeZR、Lupynow、yushui… | 按 star 与更新活跃度 |
| **Skills 目录站** | SkillsLLM 上 Lupynow 等 | 可安装 skill 列表 |
| **小红书** | 公开检索多为「封面/种草 skill」或 IMO 模型话题，**很少出现可核验的数模 SKILL.md 深评** | 不作主力依据 |
| **百度贴吧** | 几乎无稳定、可复现的 skill 仓库推荐 | 不作主力依据 |

> 公开中文社区对「哪个 skill 最好」高度集中在 **XiaoMaColtAI**；其余多为 GitHub 自述或小范围推荐。**Star/转载 ≠ 国赛能获奖。**

## 完整目录（22 套 + README）

### 第一批（维度表）

| 链接 | 上游 | 社区/维度信号 |
|------|------|----------------|
| `01-xiaoma-math-modeling-skill` | XiaoMaColtAI/math-modeling-skill | **CSDN/掘金主推**；社区热度最高 |
| `02-yushui-MathModel-Skill` | yushui2022/MathModel-Skill | 证据门禁 + Word 正式稿 |
| `03-lupynow-math-modeling-skills` | Lupynow/math-modeling-skills | 算法库 / 150+ 论文提炼自述 |
| `04-handsomeZR-mathmodel-skill` | handsomeZR-netizen/mathmodel-skill | 同行引用；多 harness 状态 |
| `05-xuec699-math-modeling-skills` | xuec699-sudo/math-modeling-skills | 吸收 01+04 的工业门控 |
| `06-automcm-pro` | RealSeaberry/AutoMCM-Pro | 自动化（慎用） |
| `07-ez-math-model` | woodfishhhh/EZ_math_model | 七阶段打包流水线 |
| `08-mathodology` | sweetcornna/mathodology | 多赛事 + subagents |
| `09-wuxinbo-Math-model-skills` | WuXinbo-bo/Math-model-skills | 重型全流程 |
| `10-vectorac-math-modeling-skill` | VectorAC/math-modeling-skill | 教学克制、人选型 |
| `11-ailcs-math-modeling.skill` | ai-lcs/math-modeling.skill | 轻量端到端 |
| `12-gdl1605-MCM.skill` | gdl1605/MCM.skill | 薄工作流 |

### 第二批（社区 / GitHub 补录）

| 链接 | 上游 | 为何装 |
|------|------|--------|
| `13-zhnnky329-MathModeling-skills` | zhnnky329/MathModeling-skills | Claude+Codex 原生插件；硬 gate、人拍板模型 |
| `14-enhanced-mathmodel-codex` | xzwwwwww/Enhanced-mathmodel-Codex-skills | **专为 Codex** 的增强全流程 |
| `15-yoki-math-modeling-single` | Yoki-cmd/math-modeling-single | 国赛四阶段 LaTeX 单会话生成 |
| `16-jihe520-MathModelAgent` | jihe520/MathModelAgent | Typst 多赛模板 + `/1start-mathmodel`；掘金沸点传播 |
| `17-usail-LLM-MM-Agent` | usail-hkust/LLM-MM-Agent | 学术向 MM-Agent（CSDN 报道美赛 F 相关） |
| `18-lixiang-MathModelAgent` | LiXiang106991/MathModelAgent | CUMCM Claude 全流程（小众） |
| `19-skillforCUMCM-pro` | skillforCUMCM/math-modeling-skill-pro | 案例卡/方法库向 Pro |
| `20-y351-route-selection` | y3519712124-ui/math-modeling-contest-route-selection | 选题/路线选择 skill |
| `21-capwitf-My-MathModeling` | capwitf/My-MathModeling-skills | GitHub 话题列表出现 |
| `22-leionel-math-model-skill` | Leionel/math-model-skill | 证据 harness 向 |

## 使用原则

1. **自有终裁**：`check_prose_style` / `check_model_fitness` / `preflight` / `skills/cumcm-*`
2. **赛时只开 1 套外部主编排**（中文社区默认试 `01-xiaoma`；要状态机试 `04`/`05`/`13`；纯 Codex 可试 `14`）
3. 外部只作流程/算法/证据结构参考；**不替代当届官方规则与真实计算结果**
4. 软链不进 git（见 `.gitignore`）；团队各自跑 install 脚本

## 中文社区「最好用」共识（可证伪摘要）

| 排名（传播热度） | Skill | 依据 |
|------------------|-------|------|
| 1 | **XiaoMaColtAI** | CSDN 多文、掘金、美赛攻略转载、GitHub ★ 断层第一 |
| 2 | Lupynow / yushui / handsomeZR | GitHub 与 skill 站；工程/门禁叙事 |
| 3 | jihe520 MathModelAgent、zhnnky329、Codex 增强包 | 掘金/GitHub 专题，体量或插件完整 |
| — | 小红书 / 贴吧 | **缺乏可复核的 skill 仓库深评** |

赛时组合建议：

```text
主编排: 01-xiaoma  或  04/05/13
证据参考: 02-yushui
算法速查: 03-lupynow
Codex 专向: 14-enhanced-mathmodel-codex
教学刹车: 10-vectorac
终裁: 本仓 cumcm-* + check_*.py
```
