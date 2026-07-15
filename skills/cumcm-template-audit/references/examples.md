# Example Uses

## Electronic Submission Audit

User asks: "检查电子版国赛模板是不是安全。"

Do:

- Inspect `main_cumcm.tex`.
- Verify commitment and numbering pages are not included by default.
- Check title/abstract starts page 1.
- Check references, appendix, and AI details placement.

## Paper Version Audit

User asks: "纸质版要打印，模板前两页对吗？"

Do:

- Enable reasoning around `\cumcmPaperSubmissiontrue`.
- Inspect `cover.tex` and `numbering_page.tex`.
- Check registration fields and page order.
