# Reproducibility Rules

- One command or short command sequence should regenerate final results when feasible.
- Fix random seeds for stochastic methods.
- Store parameters in code constants or config files, not scattered notebook cells.
- Save intermediate outputs only when they are needed for speed or audit.
- Record library versions if results depend on numerical packages.
- Ensure table values in the paper can be traced to code outputs.
- Do not depend on absolute local paths.
- Keep notebook outputs clean before packaging.
