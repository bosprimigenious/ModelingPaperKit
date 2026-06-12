# Final Review

Use this reference for final submission checks.

## Critical

- PDF missing or too small.
- Build log contains critical LaTeX errors.
- Required first page or summary sheet missing for the selected contest.
- Suspected identity information in paper or supporting materials.
- Missing figure files used by the paper.
- Unresolved labels or citations that affect the final PDF.

## Warning

- Overfull/Underfull boxes.
- Placeholder text remains.
- Sections are empty or very thin.
- Figures/tables are not referenced in text.
- AI usage exists but no AI usage report/log is prepared.
- Supporting materials are incomplete for contests that require them.
- Source log entries are not cited.

## Info

- PDF exists.
- Build completed.
- Optional special pages are present or intentionally omitted.
- Review report generated.

## Report Format

```text
Critical
- [code] message (path:line)

Warning
- [code] message (path:line)

Info
- [code] message
```

When uncertain, say "suspected" and ask the user to confirm.

