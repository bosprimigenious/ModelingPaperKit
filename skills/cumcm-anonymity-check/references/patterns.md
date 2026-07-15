# Identity Leak Patterns

## Text Patterns

- `@` email addresses.
- Chinese mobile numbers: 11 digits starting with `1`.
- Student number-like digit strings, especially 8-14 digits near "学号".
- School, college, lab, team, advisor, or member names.
- Absolute paths: `/Users/...`, `C:\Users\...`, `/home/...`.
- Local usernames in logs or notebook metadata.

## File Surfaces

- LaTeX source and auxiliary files.
- Bibliography files.
- Python, MATLAB, R, notebooks.
- CSV headers and comments.
- Figure text labels.
- PDF metadata and image EXIF when tools are available.

## Electronic Submission Red Flags

- Commitment page appears in electronic PDF.
- Numbering page appears in electronic PDF.
- Paper-only fields are filled in source used for electronic build.
- Supporting package includes raw screenshots with user account names.
