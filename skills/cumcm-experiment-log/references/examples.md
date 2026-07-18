# Examples

```text
run_id: q2-rf-003
script: code/train_q2.py
data_inputs: data/processed/q2_features_v2.csv
model: random forest
parameters: n_estimators=300, max_depth=8, seed=202609
metrics: MAE=1.83 on validation split B
outputs: figures/q2_error_distribution.pdf, tables/q2_metrics.csv
paper_claims: supports "the model reduces MAE by 18% over linear baseline"
```
