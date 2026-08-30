# Deliverable Match Patterns

## Quick classifier (from problem verbs)

| Verb / ask | Default form | Model family to try first |
| --- | --- | --- |
| 预测 / 预报 / 估计未来 | prediction table | baseline lag → regression/TS → residual fix |
| 评价 / 排序 / 优选 | ranking scores | weighted sum / TOPSIS / DEA + sensitivity on weights |
| 优化 / 调度 / 分配 | feasible scheme + objective | LP/MILP/heuristic + constraint report |
| 分类 / 识别 / 判别 | labels + confusion | simple rules → logistic/tree |
| 影响因素 / 归因 | ranked factors + effect size | correlation/regression/SHAP *after* predictive validity |
| 机理 / 过程解释 | equations + calibrated params | ODE/mechanistic + residual check |
| 预警 / 阈值 | threshold rule + alerts | distribution + cost-sensitive threshold |

## Mapping test (must pass before coding sprint)

Write three lines:

```text
题目要的答案对象 = …
模型直接输出 = …
二者差一步转换 = …（必须可脚本化，禁止“肉眼看看”）
```

If the third line is “再人工体会一下”, the model is **not yet contest-ready**.

## Examples

### Good

```text
题目要的答案对象 = 未来7天站点A日均浓度预测表
模型直接输出 = y_hat[t+1..t+7]
二者差一步转换 = 导出 csv 列 date,y_hat 并写入表3
```

### Bad

```text
题目要的答案对象 = 维护方案（哪天修、修什么）
模型直接输出 = LSTM 损失曲线
二者差一步转换 = 根据曲线可知应加强维护
```

## Judge one-liner templates (fill numbers later)

- 预测：`在…范围内，…方法的…指标为…，相对基线…。`
- 排序：`按…规则，前三为…，得分分别为…。`
- 方案：`在约束…下，最优目标值为…，关键决策为…。`
- 归因：`在控制…后，对…影响最大的三个因素为…（效应…）。`
