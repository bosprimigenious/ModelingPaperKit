# MCM/ICM

Target: `mcm`

Main file:

```text
templates/mcm/main_mcm.tex
```

Build:

```bash
python scripts/build.py --target mcm
```

## Metadata

Set in `main_mcm.tex`:

```latex
\newcommand{\MCMControlNumber}{0000000}
\newcommand{\MCMProblemChoice}{C}
\newcommand{\MCMTitle}{Your Paper Title Here}
```

## Structure

Common sections:

- `sections/summary_sheet.tex`
- `sections/introduction.tex`
- `sections/assumptions.tex`
- `sections/notation.tex`
- `sections/models.tex`
- `sections/results.tex`
- `sections/sensitivity.tex`
- `sections/validation.tex`
- `sections/strengths.tex`
- `sections/conclusion.tex`
- `sections/references.tex`
- `sections/appendix.tex`

## Key Checks

- Summary Sheet is first and strong.
- Control Number is present.
- Identity information is absent.
- Source use is cited.
- AI use report is prepared if AI was used.
- Page limit depends on current year rules; confirm latest official instructions.
- MCM typically does not require submitting extra code/data files with the PDF, but local workspace may keep them for reproducibility.

## Safety

During active MCM/ICM, use public inanimate sources only with proper source logging and citation. Do not ask external people for help or post problem/solution content publicly.

