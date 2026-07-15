# CUMCM Data Code Pipeline Checklist

Recommended layout:

```text
data/raw/
data/processed/
code/
outputs/figures/
outputs/tables/
logs/
```

- Preserve raw data unchanged.
- Make preprocessing reproducible.
- Use relative paths.
- Save final figures/tables from scripts.
- Record package versions when feasible.
- Remove secrets, local usernames, and identity information.
- Keep appendix file list aligned with actual support package.
