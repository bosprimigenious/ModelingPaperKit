# Workflow

Use this file for standard ModelingPaperKit work.

## Pick Target

Map user intent to build target:

- CUMCM / 国赛 / 高教杯: `cumcm`
- MCM / ICM / 美赛: `mcm`
- 五一杯: `wuyi`
- 北京赛: `beijing`
- Walkthrough example: `example`

## Edit Paper

1. Read the target main file.
2. Identify included sections.
3. Edit only the relevant section files.
4. Use PaperKit macros from `latex-patterns.md`.
5. Keep contest-specific pages in the template folder, not `core/`.

## Build

Use:

```bash
python scripts/build.py --target <target>
```

Common variants:

```bash
python scripts/build.py --target <target> --clean
python scripts/build.py --target <target> --bibtex
python scripts/build.py --target all
python scripts/verify_build.py
```

## Diagnose

If build fails:

1. Read the first actionable LaTeX error from `out/*.log`.
2. Ignore noisy follow-on errors until the first real error is fixed.
3. Fix the smallest local issue.
4. Rebuild.

## Review

Final review should check:

- PDF exists and is reasonably sized.
- Log has no critical LaTeX errors.
- Figures exist and are referenced.
- Labels and references resolve.
- Special pages match the contest mode.
- Identity information is not leaked.
- AI/source/supporting-material expectations are addressed.

