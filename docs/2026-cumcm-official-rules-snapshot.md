# 2026 CUMCM Official Rules Snapshot

Access date: 2026-07-16

This snapshot records rule-sensitive facts from official CUMCM pages. Use it as
the current baseline for ModelingPaperKit checks and template decisions. Re-check
the official pages before making final submission decisions.

## Official Sources Checked

| Area | Official source | Published/updated | Repository impact |
| --- | --- | --- | --- |
| Contest homepage and problem release | https://www.mcm.edu.cn/ | homepage accessed 2026-07-16 | 2026 problems are scheduled for release at 2026-09-10 18:00. Registration and paper submission go through CNKI. |
| First 2026 notice | https://www.mcm.edu.cn/html_cn/node/d6fd7a0ee8f3a3d525e30af1c365fcec.html | 2026-03-24 02:42 | Keep as a tracked notice; page points to a PDF attachment. |
| Paper format specification | https://www.mcm.edu.cn/html_cn/node/4cd596519c9eb9fbd866398f6df0caa3.html | 2026-03-03 04:31 | Drives CUMCM template page order, appendix, PDF, support-material and anonymity checks. |
| Participation rules | https://www.mcm.edu.cn/html_cn/node/9d8e511fe7a1447b35f53a82c908e2e0.html | 2026-03-03 04:27 | Drives contest-safety, plagiarism, outside-discussion, instructor-contact and AI-policy guardrails. |
| AI tool rules | https://www.mcm.edu.cn/html_cn/node/eebcfb6dc37fd2de9603dc16026fdf01.html | 2025-08-12 09:38, effective 2025-09-01 | Drives citation and supporting-material requirements for AI use until superseded by a newer 2026 AI rule. |

## Template-Critical Rules

- Paper pages use A4 with at least 2.5 cm margins on all sides.
- Paper copy page order is:
  1. commitment page,
  2. numbering page,
  3. abstract page,
  4. main text,
  5. appendix.
- Page numbering starts on the abstract page as page 1, centered in the footer.
- The main text starts after the abstract page and must not include a table of contents.
- The main text must not exceed 30 pages. Appendix pages are not limited.
- The appendix must include the support-material file list and all complete runnable source code used for modeling, including software interaction commands when applicable.
- If no program was used, the appendix must explicitly state that no program was used.
- The abstract page, main text and appendix must not contain participant, school or contest-area identity information.
- References must list external or public sources and mark their use in the main text.

## Electronic Submission Rules

- The paper file must be a single PDF or Word file. PDF is recommended.
- The paper file must be no larger than 20 MB.
- The electronic paper must match the paper-copy content and format, including appendix content.
- The electronic paper must not include the commitment page or numbering page. Its first page must be the abstract page.
- Supporting materials must contain all necessary files supporting the model, results and conclusions.
- Supporting materials should include runnable source code, self-collected or externally obtained data, and large intermediate result tables/figures when needed.
- Supporting materials are packaged as one RAR or ZIP file no larger than 20 MB.
- Commitment and numbering pages must not be included in supporting materials.
- All supporting-material files must also avoid participant, school and contest-area identity information.

## Discipline and AI Rules

- During the contest, instructors must not guide students on problem explanation, topic selection, solution suggestions, references, paper editing or similar competition work.
- Teams must independently solve the problem and must not discuss contest-problem content with anyone outside the team.
- Teams must not browse, publish or discuss contest-problem content on public or private platforms during the contest, including forums, QQ/WeChat groups, livestreams, Zhihu, Xiaohongshu, CSDN and GitHub.
- Public or external sources must be cited according to scientific-paper conventions; large copied passages are treated as academic misconduct.
- AI tools may be used as assistance, but teams remain responsible for originality, truthfulness and accuracy.
- If AI tools are used, AI-generated content must be marked at the relevant paper locations, AI tools must be listed in references, and supporting materials must include a PDF named `AI 工具使用详情`.
- The AI-use details PDF should record tool name/version, usage purpose and stage, important prompts and responses, adopted content, and manual modifications.
- If no AI tool is used, the paper must state after the references that no AI tools were used.

## Repository Follow-Ups

- `templates/cumcm/main_cumcm.tex` should keep electronic mode as the safe default.
- `templates/cumcm/sections/cover.tex` and `numbering_page.tex` should remain paper-mode only.
- `scripts/preflight.py` and `scripts/check_submission.py` should continue to detect paper-mode leakage, table-of-contents usage, paper-only front-page leakage, identity terms, missing support-material lists, and AI-use record requirements.
- `skills/cumcm-citation-ai-log` should keep the AI-use-detail PDF and reference-entry workflow aligned with the 2025 trial AI rules until a newer official rule appears.
- Re-check the first 2026 notice PDF before freezing the final submission checklist, because the HTML page only states that the notice is in the attachment.
