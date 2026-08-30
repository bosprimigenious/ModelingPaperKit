# 数模双仓 Loop 管理

开发手册。一次唤醒**只做一刀**，不要凭记忆猜下一刀。

根目录：`math_modeling2026`（赛题实战）  
工具真源仍是 `ModelingPaperKit`；本 loop 的状态与验收产物落在竞赛仓。

停机：创建 `iterator/STOP`。锁：`iterator/lock.json` 未满 12 分钟则本轮退出。

## 七轨轮转

```text
fonts → ai_use → writing → prose → model → lock → paper
```

| 轨 | 做什么 | 不是什么 |
|----|--------|----------|
| `fonts` | 宋/黑/Times/字号/无页眉对照赛规 | 不是改正文论点 |
| `ai_use` | AI 详情 Typ 编译与页数/文件名 | 不是编造使用记录 |
| `writing` | writing-skills / Grok humanize 可加载 | 不是一次开齐 34 个 skill |
| `prose` | `check_prose_style --strict-prose` | 不是只扫模板占位 |
| `model` | e2e / fitness / claim；诚实记 CV 风险 | 不是全样本 R² 即 PASS |
| `lock` | 论文题表 vs 锁版 run | 不是用演示 e2e 覆盖定稿 |
| `paper` | 编译 PDF；对照五一≤30 页建议 | 不是清零 overfull 才算过 |

## 命令

```bash
cd ~/Projects/FullStack/math_modeling2026

python3 scripts/modeling_loop_manager.py status
python3 scripts/modeling_loop_manager.py next
# 可自动验收的刀：
python3 scripts/modeling_loop_manager.py verify --id <slice_id>
# 或一键：next + verify + finish
python3 scripts/modeling_loop_manager.py run-once

# 硬阻塞暂时挪到队尾（不装完成）：
python3 scripts/modeling_loop_manager.py defer --id <slice_id> --note '等锁版 run'

# 做完（含人工刀）：
python3 scripts/modeling_loop_manager.py finish --id <slice_id> --status ok|partial|fail --note '一句话'
```

退出码：`0` 正常 / `2` STOP / `3` 锁 / `4` 队列空 / `5` verify 失败。

`ok` / `partial` 都会推进队列；`fail` 不推进（硬阻塞）。`defer` 把刀挪到队尾继续别的。

产物：`runs/loop/<slice_id>/*_report.json`  
流水：`iterator/ITERATION_LOG.md`

## 唤醒步骤

1. `status` 看下一刀  
2. `next` 领刀（或 `run-once`）  
3. 只改该刀 `goal` 范围  
4. `verify` 有证据再 `finish`  
5. 聚合门没过就报 **NOT READY**，不要口头 ok  

## 当前队列在迭代什么

见 `iterator/queue.json`：字体、AI Typ、writing-skills、prose、e2e/fitness、表1.1 锁版、编译页数、模板占位、真实 AI 填写、砍页。

## 明确不做

- 不在 loop 里静默改口径或编数字  
- 不 `commit`/`push`，除非用户点名  
- 人工刀（`manual: true`）verify 只提示，不假装完成  
