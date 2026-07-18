# Data Quality Checklist

- File inventory: names, formats, sizes, row counts, column counts.
- Schema: column names, units, types, valid ranges, primary keys.
- Missingness: count, rate, pattern, likely cause.
- Duplicates: exact duplicates and duplicate identifiers.
- Outliers: impossible values and influential rare cases.
- Time fields: timezone, ordering, gaps, repeated timestamps.
- Leakage: target-derived features, future data in training, identifiers that reveal labels.
- Cleaning log: rule, affected rows, rationale, output path.
