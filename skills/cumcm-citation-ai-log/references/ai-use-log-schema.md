# AI Use Log Schema

Record AI usage only truthfully.

```text
tool_name:
model_or_version:
provider:
use_date:
contest_phase:
used_for:
prompt_summary:
output_summary:
human_verification:
paper_locations:
supporting_file:
```

Examples of `used_for`:

- literature search leads
- code debugging
- language polishing
- formula checking
- figure caption draft

Do not claim "no AI used" if AI assisted any contest work covered by official rules.

## 2026 CUMCM trial rule anchors

Source: 全国大学生数学建模竞赛人工智能工具使用规定（2026年试行）, effective 2026-09-01.

- Paper must place **AI 工具使用声明** *before* the reference list (not only after).
- If AI was used, supporting materials must include PDF named exactly `AI 工具使用详情.pdf`.
- Required detail fields: tool name + version/model; purpose and stages; prompt/process (with examples OK); adoption / human edits / verification (except pure polish may be brief).
- Core modeling/analysis must be team-led; unreviewed AI core content or false “no AI” disclosure can cancel award eligibility.
- Template path: `templates/cumcm/support/AI工具使用详情.typ` → compile to the official PDF filename.

