# Model Fitness Rubric (three layers)

Use this to separate three different questions people mix up.

## Layer A — Problem answer form（题目想要的结果形态）

| Deliverable type | What “done” looks like | Common false done |
| --- | --- | --- |
| Scalar / table of metrics | Named metric + value + unit + condition | Only training curves |
| Ranking / ordering | Ordered list with scores and rule | Unsorted feature importance plot |
| Prediction | Values on the **asked** horizon/objects | In-sample fit only |
| Classification / labels | Label set + rule + counts/errors | Cluster plot without labels tied to task |
| Scheme / policy / schedule | Implementable decisions + objective value | Algorithm description without a scheme |
| Explanation / attribution | Factors + direction + magnitude on this data | Generic SHAP essay |
| Optimization design | Feasible point + objective + constraints status | Solver log only |

**Rule:** If the official wording says “给出…方案/排序/预测值”, the model output must become that object, not a related visualization.

## Layer B — Model usable on this data（能不能用）

| Check | Pass | Fail |
| --- | --- | --- |
| Fields | All inputs exist in attachments | Needs external labels not given |
| Granularity | Model grain = data grain or explicit aggregation | Daily model on undated rows |
| Size | n, p, missingness allow identification | 5 samples for 20-param DL |
| Split | Time/order/group split matches task | Random split on time series delivery |
| Baseline | Same deliverable, weaker method | No baseline |
| Compute | Finishes in contest budget | Overnight hypersearch as only path |
| Stability | Seed/param small change OK or explained | Answers flip under tiny noise |

## Layer C — Judge-facing answer（评委想看到的答案）

Judges/instructors usually scan for:

1. **One-sentence answer per subproblem** early (abstract + section end).
2. **Why this model** linked to the task type, not a brand name.
3. **Assumptions that are actually used** in derivation or cleaning.
4. **Baseline vs main** on the same metric and sample.
5. **Validation or sensitivity** that could have falsified the claim.
6. **Limitations** that are specific (not “模型仍有不足”).
7. **Reproducible path** code → table → sentence.

### Award vs participate (honest)

| Pattern | Likely ceiling |
| --- | --- |
| Correct form + baseline + validation + clear answers | Competitive |
| Fancy model, wrong form or no direct answer | Participate |
| Everyone’s shallow method, weak paper | Paper war only |
| Deep stack, no baseline, beautiful prose | High risk of soft reject by careful judges |

### What judges are *not* primarily scoring

- Number of acronyms
- 3D decorative plots
- Length of formula appendix unused in results
- Claims of “SOTA” without this-problem evidence
