# Repository Map

Use this file when locating the right files in `ModelingPaperKit`.

## Core Engine

- `core/paperkit-base.sty`: layout, geometry, captions, lists, figures, tables, code listings.
- `core/paperkit-math.sty`: math packages, theorem environments, vector/matrix shortcuts.
- `core/paperkit-utils.sty`: algorithms, writing markers, keywords, anonymization helpers, hyperref/cleveref.
- `core/paperkit-cref-zh.tex`: Chinese cleveref names.

Avoid putting contest-specific content in `core/`.

## Templates

- `templates/cumcm/main_cumcm.tex`: CUMCM Chinese paper.
- `templates/mcm/main_mcm.tex`: MCM/ICM English paper.
- `templates/wuyi/main_wuyi.tex`: Wuyi Cup Chinese paper.
- `templates/beijing/main_beijing.tex`: Beijing contest Chinese paper.

Each template has a `sections/` directory. Edit sections rather than core packages unless the task is explicitly about shared style.

## Scripts

- `scripts/build.py`: compile targets with XeLaTeX.
- `scripts/verify_build.py`: compile all targets and inspect logs.
- `scripts/clean.py`: remove auxiliary files.
- `scripts/new_contest.py`: scaffold a new contest template.
- `scripts/generate_dummy_data.py`: generate example CSV data.

Planned checkers:

- `scripts/summarize_build_log.py`
- `scripts/inspect_template.py`
- `scripts/check_tex_links.py`
- `scripts/check_submission.py`

If a planned checker does not exist yet, fall back to direct file/log inspection and mention the gap.

## Examples

- `examples/cumcm_walkthrough/main.tex`: example paper.
- `examples/cumcm_walkthrough/generate_figures.py`: example figure generation.
- `examples/dummy_data/`: non-sensitive sample CSV files.

## Docs

- `README.md`: overview and commands.
- `docs/getting-started.md`: installation and first compile.
- `docs/template-guide.md`: writing guidance.
- `docs/faq.md`: troubleshooting.
- `tasks.md`: implementation backlog.

