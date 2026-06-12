# ModelingPaperKit Tasks

Last updated: 2026-06-09

This task plan combines:

- `docs/math-modeling-skill-market-report.md`
- `docs/real-competition-workflow-research.md`
- `docs/modeling-paperkit-skill-plan.md`
- `docs/modeling-paperkit-upgrade-architecture.md`
- `docs/modeling-paperkit-frontend-plan.md`

The main decision is:

```text
Build deterministic repository capabilities first.
Wrap them as a modeling-paperkit skill.
Then build a lightweight CLI Agent.
Only after that, build the full-stack Studio.
```

## Current Execution Plan

Use this section as the active assignment board. Later phases remain below as the full backlog.

### Roles

Owner:

- Chooses the next task card.
- Approves scope changes.
- Decides whether review findings are accepted or deferred.

Implementer Agent, for example Cursor:

- Implements only the assigned task card.
- Does not start future phases unless explicitly assigned.
- Runs required acceptance commands before reporting completion.
- Reports changed files, command results, risks, and gaps.

Reviewer Agent, for example Codex:

- Reviews the implementation against this file.
- Runs acceptance commands independently.
- Reports findings first, ordered by severity.
- Does not fix code unless explicitly asked.

### Status Labels

Use these labels when coordinating work:

```text
TODO
IN_PROGRESS
BLOCKED
READY_FOR_REVIEW
NEEDS_CHANGES
ACCEPTED
DEFERRED
```

### Finding Severity

```text
P0 Blocker: required command fails, data loss risk, unstable JSON contract, or scope violation.
P1 Required: required feature missing, wrong exit code, or common failure unhandled.
P2 Improvement: robustness, clearer messages, more edge cases.
P3 Nice-to-have: refactor, polish, extra docs.
```

### Sprint 1: Phase 0 Core Checkers

Do these in order. Each task should be a separate implementation handoff and a separate review.

#### Task Card 1: Build Log Summarizer

Status: TODO

Implementer scope:

- Create `scripts/summarize_build_log.py`.
- Optional: add `tests/fixtures/logs/latex_error.log`.

Out of scope:

- Do not implement `inspect_template.py`.
- Do not implement `check_tex_links.py`.
- Do not implement `check_submission.py`.
- Do not create skill, agent, backend, or frontend files.

Required CLI:

```bash
python scripts/summarize_build_log.py --help
python scripts/summarize_build_log.py --target cumcm --format json
python scripts/summarize_build_log.py --log tests/fixtures/logs/latex_error.log --format json
```

Required JSON contract:

```json
{
  "tool": "summarize_build_log",
  "target": "cumcm",
  "status": "warning",
  "summary": {
    "critical": 0,
    "warning": 1,
    "info": 0
  },
  "findings": [
    {
      "severity": "warning",
      "code": "overfull_hbox",
      "message": "Overfull hbox found",
      "path": "templates/cumcm/out/main_cumcm.log",
      "line": null
    }
  ]
}
```

Exit code:

- `0` if no `critical` findings.
- Non-zero if critical compile blockers are found or arguments are invalid.

Reviewer checks:

- `--help` works.
- `--target` and `--log` both work.
- Missing log does not traceback.
- JSON contains `tool`, `target`, `status`, `summary`, `findings`.
- Each finding contains `severity`, `code`, `message`, `path`, `line`.
- Severity is only `critical`, `warning`, or `info`.

#### Task Card 2: Template Inspector

Status: TODO

Implementer scope:

- Create `scripts/inspect_template.py`.
- Reuse target metadata from `scripts/build.py` or centralize a small shared target map if necessary.

Out of scope:

- Do not inspect labels/images deeply; that belongs to Task Card 3.
- Do not run LaTeX builds.
- Do not create `.paperkit/state.json` yet.

Required CLI:

```bash
python scripts/inspect_template.py --help
python scripts/inspect_template.py --target cumcm --format json
python scripts/inspect_template.py --target mcm --format json
python scripts/inspect_template.py --target example --format json
```

Required JSON contract:

```json
{
  "tool": "inspect_template",
  "target": "cumcm",
  "status": "warning",
  "summary": {
    "critical": 0,
    "warning": 1,
    "info": 3
  },
  "template": {
    "dir": "templates/cumcm",
    "main": "main_cumcm.tex",
    "out_dir": "templates/cumcm/out"
  },
  "sections": {
    "present": ["problem.tex"],
    "missing": []
  },
  "artifacts": {
    "pdf": null,
    "log": null
  },
  "findings": []
}
```

Reviewer checks:

- Works for all targets: `cumcm`, `mcm`, `wuyi`, `beijing`, `example`.
- Does not modify files.
- Detects special pages such as `cover`, `ai_declaration`, `summary_sheet`.
- Missing PDF/log is reported as warning or info, not a crash.

#### Task Card 3: TeX Link and Asset Checker

Status: TODO

Implementer scope:

- Create `scripts/check_tex_links.py`.
- Parse main file and included section files.
- Check labels, references, includegraphics, and `\figplot` assets.

Out of scope:

- Do not do identity scanning.
- Do not do contest-specific submission checks.
- Do not compile LaTeX.

Required CLI:

```bash
python scripts/check_tex_links.py --help
python scripts/check_tex_links.py --target cumcm --format json
python scripts/check_tex_links.py --target mcm --format json
python scripts/check_tex_links.py --target example --format json
```

Required JSON contract:

```json
{
  "tool": "check_tex_links",
  "target": "example",
  "status": "warning",
  "summary": {
    "critical": 0,
    "warning": 1,
    "info": 0
  },
  "findings": [
    {
      "severity": "warning",
      "code": "missing_figure",
      "message": "Figure file was not found in configured graphics paths",
      "path": "examples/cumcm_walkthrough/sections/model.tex",
      "line": 42
    }
  ]
}
```

Reviewer checks:

- Does not flag labels inside comments.
- Detects duplicate labels.
- Detects missing figures.
- Supports `\ref`, `\cref`, `\Cref`, and `\eqref`.
- Respects `figures/`, `../02_figures/`, and `\graphicspath`.

#### Task Card 4: Submission Checker

Status: TODO

Implementer scope:

- Create `scripts/check_submission.py`.
- Reuse Task Cards 1-3 checkers.
- Add identity leak scan and contest-mode checks.

Out of scope:

- Do not create AI usage export yet.
- Do not create supporting material package yet.
- Do not modify paper files.

Required CLI:

```bash
python scripts/check_submission.py --help
python scripts/check_submission.py --target cumcm --format json
python scripts/check_submission.py --target cumcm --contest-mode cumcm_active --format json
python scripts/check_submission.py --target mcm --contest-mode mcm_active --format json
```

Required JSON contract:

```json
{
  "tool": "check_submission",
  "target": "cumcm",
  "contest_mode": "cumcm_active",
  "status": "warning",
  "summary": {
    "critical": 0,
    "warning": 2,
    "info": 1
  },
  "findings": [
    {
      "severity": "warning",
      "code": "missing_ai_usage_log",
      "message": "AI usage details are expected when AI assistance was used",
      "path": null,
      "line": null
    }
  ]
}
```

Reviewer checks:

- Calls or imports Phase 0 checkers instead of duplicating all logic.
- Suspected identity findings are phrased as suspected, not proven.
- CUMCM and MCM modes produce different rule checks.
- Missing PDF/log/support files are reported cleanly.

#### Task Card 5: Phase 0 Smoke Test

Status: TODO

Implementer scope:

- Add a minimal smoke test script or pytest tests.
- Include fixtures only if needed.
- Verify Phase 0 commands run on a clean checkout.

Required commands:

```bash
python scripts/summarize_build_log.py --help
python scripts/inspect_template.py --target cumcm --format json
python scripts/inspect_template.py --target mcm --format json
python scripts/check_tex_links.py --target example --format json
python scripts/check_submission.py --target cumcm --format json
```

Reviewer checks:

- Smoke tests do not require TeX installation.
- Tests do not write to template directories except temporary files under a test fixture or temp dir.
- All scripts preserve the shared JSON finding contract.

### Implementer Final Response Template

```text
## Scope
Assigned task card:
Out of scope:

## Changed Files
- ...

## Implemented
- ...

## Acceptance Commands
- `...` PASS
- `...` FAIL: ...

## JSON Contract
Example output:
```json
...
```

## Risks / Gaps
- ...

## Status
READY_FOR_REVIEW
```

### Reviewer Final Response Template

```text
## Verdict
PASS / PASS WITH WARNINGS / NEEDS CHANGES

## Findings
- [P0] path:line - issue
- [P1] path:line - issue

## Commands Run
- `...` PASS
- `...` FAIL

## Contract Check
- CLI flags:
- JSON shape:
- Exit codes:
- Scope control:

## Required Fixes
- ...

## Optional Follow-ups
- ...
```

## Phase 0: Deterministic PaperKit Checks

Goal: make the existing LaTeX repository reliably inspectable, buildable, and reviewable by scripts before adding Agent behavior.

Why this is urgent:

- Real contest users lose time on LaTeX logs, missing figures, unresolved references, identity leaks, and submission rule mistakes.
- Agent output must be grounded in deterministic checks, not only natural language guesses.
- CUMCM/MCM compliance differs, so checks need contest-aware inputs.

### P0.1 Build Log Summarizer

- [ ] Create `scripts/summarize_build_log.py`.
- [ ] Accept `--target <name>` and/or `--log <path>`.
- [ ] Support `--format text` and `--format json`.
- [ ] Detect common LaTeX errors:
  - [ ] `! LaTeX Error`
  - [ ] `Undefined control sequence`
  - [ ] `Missing $ inserted`
  - [ ] `File ... not found`
  - [ ] `Citation ... undefined`
  - [ ] `Reference ... undefined`
  - [ ] `Label(s) may have changed`
  - [ ] `Overfull \hbox`
  - [ ] `Underfull \hbox`
- [ ] Include error severity: `critical`, `warning`, `info`.
- [ ] Include source line hints where log provides them.
- [ ] Return non-zero exit code only for critical compile blockers.

Acceptance:

- [ ] Can summarize logs from `templates/cumcm/out/`, `templates/mcm/out/`, and `examples/cumcm_walkthrough/out/` when present.
- [ ] Missing log path produces a clear message, not a traceback.
- [ ] JSON output is stable enough for an Agent or backend to parse.

### P0.2 Template Inspector

- [ ] Create `scripts/inspect_template.py`.
- [ ] Accept `--target cumcm|mcm|wuyi|beijing|example`.
- [ ] Read target metadata from `scripts/build.py` or a shared target map.
- [ ] Report:
  - [ ] template directory
  - [ ] main tex file
  - [ ] section files
  - [ ] missing expected sections
  - [ ] whether `figures/` exists
  - [ ] whether `out/` exists
  - [ ] latest PDF/log path and size if present
  - [ ] detected special pages, such as `cover`, `ai_declaration`, `summary_sheet`
- [ ] Support `--format text` and `--format json`.

Acceptance:

- [ ] Works for all current targets: `cumcm`, `mcm`, `wuyi`, `beijing`, `example`.
- [ ] Does not modify files.
- [ ] Gives enough information to initialize `.paperkit/state.json` later.

### P0.3 TeX Link and Asset Checker

- [ ] Create `scripts/check_tex_links.py`.
- [ ] Accept `--target <name>`.
- [ ] Parse main file and included `sections/*.tex`.
- [ ] Check duplicate `\label{...}`.
- [ ] Check unresolved `\ref{...}`, `\cref{...}`, `\Cref{...}`, `\eqref{...}` against local labels.
- [ ] Check `\includegraphics{...}` files.
- [ ] Check `\figplot` fifth argument image files.
- [ ] Respect current image search paths:
  - [ ] `figures/`
  - [ ] `../02_figures/`
  - [ ] paths declared by `\graphicspath`
- [ ] Report unused section files not included by main.
- [ ] Support `--format text` and `--format json`.

Acceptance:

- [ ] Can detect missing image files without compiling.
- [ ] Can detect duplicate labels.
- [ ] Does not flag labels in comments.
- [ ] Produces `critical` findings only for issues that likely break compilation or final PDF integrity.

### P0.4 Submission Checker

- [ ] Create `scripts/check_submission.py`.
- [ ] Accept `--target <name>`.
- [ ] Accept `--contest-mode off|cumcm_active|mcm_active`.
- [ ] Run or reuse:
  - [ ] `inspect_template.py`
  - [ ] `summarize_build_log.py`
  - [ ] `check_tex_links.py`
- [ ] Check PDF presence and size.
- [ ] Check log has no critical LaTeX errors.
- [ ] Scan `.tex`, `.bib`, and supporting files for likely identity leaks:
  - [ ] email
  - [ ] phone number
  - [ ] student number-like sequences
  - [ ] ID card-like sequences
  - [ ] obvious placeholders replaced with real names
- [ ] Contest-specific checks:
  - [ ] CUMCM: summary page expectation for electronic version.
  - [ ] CUMCM: support package expectation.
  - [ ] CUMCM: AI usage details expectation.
  - [ ] MCM: Summary Sheet first page expectation.
  - [ ] MCM: Control Number presence.
  - [ ] MCM: no extra submitted files expectation.
  - [ ] MCM: AI use report expectation.
- [ ] Support `--format text` and `--format json`.

Acceptance:

- [ ] Produces a grouped report: `Critical`, `Warning`, `Info`.
- [ ] Avoids declaring uncertain identity findings as facts; uses "suspected".
- [ ] Gives file paths and line numbers where possible.
- [ ] Does not modify files.

### P0.5 Script Smoke Tests

- [ ] Add a small test or smoke-test script for all Phase 0 checkers.
- [ ] Include at least one synthetic LaTeX log sample with common errors.
- [ ] Include at least one synthetic tex sample with duplicate labels and missing images.
- [ ] Ensure scripts can run without TeX installed, except actual build commands.

Acceptance:

- [ ] `python scripts/summarize_build_log.py --help` works.
- [ ] `python scripts/inspect_template.py --target cumcm --format json` works.
- [ ] `python scripts/check_tex_links.py --target example --format json` works.
- [ ] `python scripts/check_submission.py --target cumcm --format json` works, even if it reports missing PDF.

## Phase 1: ModelingPaperKit Skill

Goal: create a real `modeling-paperkit` skill that teaches Codex/Agent how to use this repository without loading too much context.

Why this matters:

- Market research shows successful skills separate `SKILL.md`, `references/`, `scripts/`, and `assets/`.
- The skill should be a capability layer, not a giant prompt.
- It should encode real contest workflows and repository conventions.

### P1.1 Skill Directory

- [ ] Create `skills/modeling-paperkit/`.
- [ ] Create `skills/modeling-paperkit/SKILL.md`.
- [ ] Create `skills/modeling-paperkit/agents/openai.yaml`.
- [ ] Create `skills/modeling-paperkit/references/`.
- [ ] Create `skills/modeling-paperkit/scripts/`.
- [ ] Create `skills/modeling-paperkit/assets/checklists/`.

Acceptance:

- [ ] `SKILL.md` has valid YAML frontmatter with `name` and `description`.
- [ ] `SKILL.md` body stays concise and points to references by need.
- [ ] No extra `README.md` inside skill folder unless required by packaging.

### P1.2 Core Skill Instructions

- [ ] Define trigger conditions:
  - [ ] user wants to use `ModelingPaperKit`
  - [ ] user edits math modeling paper templates
  - [ ] user compiles or fixes LaTeX
  - [ ] user checks CUMCM/MCM/Wuyi/Beijing submission
  - [ ] user asks for final review of a math modeling paper
- [ ] Define non-goals:
  - [ ] no automatic contest participation
  - [ ] no fabricated results
  - [ ] no automatic file submission
  - [ ] no contest-period unsafe browsing
- [ ] Define required workflow:
  - [ ] inspect target
  - [ ] load contest reference if needed
  - [ ] edit minimal files
  - [ ] build or check
  - [ ] report findings

Acceptance:

- [ ] A user request like "帮我修国赛模板编译错误" clearly triggers this skill.
- [ ] A user request like "解释 ARIMA 原理" does not require this skill unless paper integration is involved.

### P1.3 Repository References

- [ ] Create `references/workflow.md`.
- [ ] Create `references/repository-map.md`.
- [ ] Create `references/latex-patterns.md`.
- [ ] Create `references/final-review.md`.

Acceptance:

- [ ] `repository-map.md` maps `core/`, `templates/`, `scripts/`, `examples/`, `docs/`.
- [ ] `latex-patterns.md` covers:
  - [ ] `\figplot`
  - [ ] `\keywords`
  - [ ] `\vb`
  - [ ] `\mat`
  - [ ] `\topline`, `\midline`, `\bottomline`
  - [ ] `algorithm` / `algpseudocode`
  - [ ] `\cref`
  - [ ] `\email`, `\phone`
- [ ] `final-review.md` separates `Critical`, `Warning`, `Info`.

### P1.4 Contest References

- [ ] Create `references/cumcm.md`.
- [ ] Create `references/mcm.md`.
- [ ] Create `references/wuyi.md`.
- [ ] Create `references/beijing.md`.

Acceptance:

- [ ] Each file records main tex path, build target, language, required/special pages, expected section order, and submission risks.
- [ ] CUMCM reference includes electronic submission distinction: summary-only first page vs full template pages.
- [ ] MCM reference includes Summary Sheet, Control Number, page limit, AI report, and source citation expectations.

### P1.5 Contest Safety Mode Reference

- [ ] Add `contest_safety_mode` guidance to `references/workflow.md` or a separate `references/contest-safety.md`.
- [ ] Define modes:
  - [ ] `off`
  - [ ] `cumcm_active`
  - [ ] `mcm_active`
- [ ] CUMCM active mode:
  - [ ] no proactive search for current contest solution discussions
  - [ ] no browsing GitHub/CSDN/Zhihu/Xiaohongshu/forums for live problem discussion
  - [ ] only local files and official rules unless user explicitly confirms safe source
- [ ] MCM active mode:
  - [ ] public inanimate sources allowed
  - [ ] all sources must be logged
  - [ ] no interactive external help

Acceptance:

- [ ] Skill instructions make contest-period behavior safer than default open browsing.
- [ ] Skill requires explicit user confirmation before external search in active contest contexts.

### P1.6 Skill Script Integration

- [ ] Copy or reference Phase 0 scripts under skill scripts as appropriate.
- [ ] Document whether scripts live in root `scripts/` or skill `scripts/`.
- [ ] Avoid duplicate script logic if possible.

Acceptance:

- [ ] Skill can tell Codex exactly which script to run for inspect/build-log/review.
- [ ] Script paths are correct from repository root.

## Phase 2: Competition Project State and Logs

Goal: support real contest workflows with persistent project metadata, AI usage records, source records, and result manifests.

Why this matters:

- Real users switch between reading, coding, writing, plotting, compiling, and final review.
- CUMCM/MCM both require careful AI/source handling.
- Agent and Web UI need state to resume work.

### P2.1 `.paperkit/state.json`

- [ ] Define `.paperkit/state.schema.json`.
- [ ] Generate `.paperkit/state.json` for a project.
- [ ] Track:
  - [ ] project id
  - [ ] contest
  - [ ] target
  - [ ] problem id
  - [ ] paper title
  - [ ] workspace
  - [ ] main tex
  - [ ] sections status
  - [ ] figures
  - [ ] references
  - [ ] last build
  - [ ] last review
  - [ ] contest safety mode
  - [ ] deadline/timeline

Acceptance:

- [ ] Can initialize state for `cumcm` and `mcm`.
- [ ] State file can be updated after inspect/build/review.
- [ ] Schema validation catches invalid target names.

### P2.2 AI Usage Log

- [ ] Define `.paperkit/ai_usage_log.json`.
- [ ] Track:
  - [ ] tool name
  - [ ] model/version
  - [ ] timestamp
  - [ ] purpose
  - [ ] prompt summary
  - [ ] adopted content summary
  - [ ] human modification note
- [ ] Add export command or script:
  - [ ] CUMCM AI usage details Markdown
  - [ ] MCM Report on Use of AI Markdown

Acceptance:

- [ ] Agent can append entries.
- [ ] Final review warns if AI usage exists but no report/export exists.
- [ ] Log avoids storing sensitive full prompts by default; summaries are enough.

### P2.3 Supporting Materials Manifest

- [ ] Define `.paperkit/supporting_materials.json`.
- [ ] Create optional `supporting/` structure:
  - [ ] `supporting/code/`
  - [ ] `supporting/data/`
  - [ ] `supporting/results/`
  - [ ] `supporting/README.md`
- [ ] Track file purpose and whether it should be submitted.
- [ ] Add identity scan for supporting materials.

Acceptance:

- [ ] CUMCM final review checks supporting materials.
- [ ] MCM final review warns that extra files generally should not be submitted.
- [ ] Manifest distinguishes local workspace files from submission files.

### P2.4 Result Manifest

- [ ] Define `.paperkit/result_manifest.json`.
- [ ] Track figures and tables:
  - [ ] generated file path
  - [ ] source script
  - [ ] source data
  - [ ] generation timestamp
  - [ ] paper section
  - [ ] LaTeX label
- [ ] Add checker to compare manifest with actual files and TeX references.

Acceptance:

- [ ] Missing figure files are detected.
- [ ] Figures in paper but not in manifest are reported.
- [ ] Manifest helps verify code-result-paper consistency.

### P2.5 Source and Reference Log

- [ ] Define `.paperkit/source_log.json`.
- [ ] Track external sources:
  - [ ] title/name
  - [ ] URL or citation
  - [ ] access date
  - [ ] usage purpose
  - [ ] whether cited in paper
- [ ] Integrate with MCM active mode.

Acceptance:

- [ ] Final review warns if source log entries are not cited.
- [ ] MCM mode encourages source logging for all external materials.

## Phase 3: CLI Agent MVP

Goal: build a lightweight Agent that orchestrates existing scripts and skill knowledge without becoming a broad autonomous modeling system.

### P3.1 CLI Skeleton

- [ ] Create `agent/` package or `scripts/agent_cli.py`.
- [ ] Choose CLI library: `argparse` first, `Typer` if dependencies are acceptable.
- [ ] Implement commands:
  - [ ] `paperkit-agent init --target <target>`
  - [ ] `paperkit-agent inspect --target <target>`
  - [ ] `paperkit-agent build --target <target>`
  - [ ] `paperkit-agent review --target <target>`
  - [ ] `paperkit-agent fix-log --target <target>`

Acceptance:

- [ ] Commands can run without Web UI.
- [ ] Commands call existing repository scripts.
- [ ] Commands update `.paperkit/state.json` where appropriate.

### P3.2 Agent Tool Wrappers

- [ ] Implement safe wrappers:
  - [ ] `build_target`
  - [ ] `inspect_template`
  - [ ] `summarize_log`
  - [ ] `check_submission`
  - [ ] `check_tex_links`
  - [ ] `read_section`
  - [ ] `update_section`
  - [ ] `list_figures`
- [ ] Centralize path resolution and target validation.

Acceptance:

- [ ] Agent does not call arbitrary shell for known PaperKit operations.
- [ ] Tool wrappers return structured results.

### P3.3 Build-Fix Mode

- [ ] Run build.
- [ ] If build fails, summarize log.
- [ ] Identify minimal likely fix.
- [ ] Apply fix only when high confidence.
- [ ] Rebuild.
- [ ] Stop after a bounded number of attempts.

Acceptance:

- [ ] Does not loop forever.
- [ ] Does not rewrite unrelated sections.
- [ ] Reports unresolved errors clearly.

### P3.4 Final Review Mode

- [ ] Run inspect/check/log/link checks.
- [ ] Produce final report grouped by severity.
- [ ] Respect contest safety mode.
- [ ] Do not modify paper automatically.

Acceptance:

- [ ] Usable in the last 6-12 hours before submission.
- [ ] Clearly separates must-fix issues from suggestions.

## Phase 4: Skill-Driven Writing Support

Goal: add writing assistance that reflects real contest workflows without fabricating results.

### P4.1 Section Progress Checker

- [ ] Detect empty or placeholder-heavy sections.
- [ ] Detect missing assumptions, notation, results, validation, conclusion.
- [ ] Map sections to contest-specific expected structure.

Acceptance:

- [ ] Can tell a user what remains to write.
- [ ] Does not judge mathematical quality as if certain.

### P4.2 Result-to-Paper Helper

- [ ] Accept user-provided result tables, metrics, and figure paths.
- [ ] Draft result explanation text.
- [ ] Generate captions.
- [ ] Suggest where to insert in `sections/*.tex`.
- [ ] Update result manifest.

Acceptance:

- [ ] Requires user-provided data/results.
- [ ] Does not invent metrics.
- [ ] Inserts labels and references consistently.

### P4.3 Abstract/Summary Review

- [ ] Check whether abstract or Summary Sheet mentions:
  - [ ] problem context
  - [ ] method
  - [ ] major results
  - [ ] conclusions
  - [ ] limitations if needed
- [ ] For MCM, emphasize Summary Sheet quality.
- [ ] For CUMCM, check one-page abstract pressure.

Acceptance:

- [ ] Produces actionable rewrite suggestions.
- [ ] Does not overwrite user abstract unless asked.

### P4.4 Contest Timeline Assistant

- [ ] Add timeline fields to state.
- [ ] Support phase labels:
  - [ ] pre_contest
  - [ ] day_1_problem_selection
  - [ ] day_2_modeling
  - [ ] day_3_paper
  - [ ] final_review
  - [ ] post_contest
- [ ] Produce next-milestone suggestions.

Acceptance:

- [ ] Helps users prioritize under time pressure.
- [ ] Does not force a rigid linear workflow.

## Phase 5: Full-stack Studio MVP

Goal: expose the CLI Agent and repository checks through a visual workspace after scripts/skill/CLI are stable.

Frontend product details are specified in `docs/modeling-paperkit-frontend-plan.md`. The frontend should be a math modeling paper delivery workbench, not a landing page or generic chat UI.

### P5.1 Backend

- [ ] Create `backend/`.
- [ ] Add FastAPI app.
- [ ] Add API routes:
  - [ ] `POST /api/projects`
  - [ ] `GET /api/projects`
  - [ ] `GET /api/projects/{id}`
  - [ ] `GET /api/projects/{id}/files`
  - [ ] `GET /api/projects/{id}/files/{path}`
  - [ ] `PATCH /api/projects/{id}/files/{path}`
  - [ ] `POST /api/projects/{id}/build`
  - [ ] `GET /api/projects/{id}/builds/{run_id}`
  - [ ] `POST /api/projects/{id}/review`
  - [ ] `GET /api/projects/{id}/reviews/{run_id}`
  - [ ] `POST /api/projects/{id}/agent/run`
- [ ] Add SQLite persistence.
- [ ] Add background task support for build/review.

Acceptance:

- [ ] Can create a project and run review through API.
- [ ] Build/review runs are persisted and retrievable.

### P5.2 Frontend

- [ ] Create `frontend/`.
- [ ] Use React + Vite + TypeScript.
- [ ] Start with mock JSON if backend APIs are not ready.
- [ ] Build pages/components:
  - [ ] Dashboard
  - [ ] Project Overview
  - [ ] Project page
  - [ ] Section editor
  - [ ] Agent panel
  - [ ] Build status
  - [ ] Review checklist
  - [ ] Log summary
- [ ] Add contest-specific views when backend data exists:
  - [ ] Figures & Tables
  - [ ] AI Usage
  - [ ] Supporting Materials
  - [ ] Source Log
- [ ] Keep UI workbench-like, not landing-page-like.

Acceptance:

- [ ] User can view project status.
- [ ] User can trigger build/review.
- [ ] User can inspect findings and logs.
- [ ] User can confirm or reject Agent changes.
- [ ] User can distinguish CUMCM and MCM submission risks.

### P5.3 PDF and Artifact View

- [ ] Show latest PDF path/status.
- [ ] Show log summary.
- [ ] Show generated reports:
  - [ ] submission review
  - [ ] AI usage report
  - [ ] supporting materials report

Acceptance:

- [ ] User can understand submission readiness without reading raw logs.

## Phase 6: Advanced Competition Assistance

Goal: add selective higher-level modeling support after the delivery system is reliable.

### P6.1 Problem Analysis Mode

- [ ] Support user-provided problem text.
- [ ] Extract subproblems, inputs, outputs, constraints.
- [ ] Suggest candidate models with assumptions and risks.
- [ ] Respect contest safety mode.

Acceptance:

- [ ] Does not browse unsafe live contest discussion sources in active CUMCM mode.
- [ ] Produces a decision matrix, not a fake final solution.

### P6.2 Data and Modeling Skill Integration

- [ ] Add separate data-analysis skill or integration.
- [ ] Add separate visualization skill or integration.
- [ ] Keep modeling support independent from PaperKit delivery skill.

Acceptance:

- [ ] PaperKit skill remains focused on paper delivery.
- [ ] Modeling/data skills can be used only when task requires them.

### P6.3 Optional Web Enhancements

- [ ] Timeline view.
- [ ] Team task board.
- [ ] Figure/table manifest view.
- [ ] Source/AI usage log view.
- [ ] PDF preview.

Acceptance:

- [ ] Enhancements improve real contest workflow, not just visual polish.

## Cross-Phase Rules

### Safety and Compliance

- [ ] Never encourage live contest rule violations.
- [ ] In active CUMCM mode, do not proactively search public discussion platforms for current problem solutions.
- [ ] In active MCM mode, log external sources and AI usage.
- [ ] Never fabricate data, model results, citations, or awards.
- [ ] Never automatically submit contest files.

### Engineering

- [ ] Keep `core/` free of contest-specific content.
- [ ] Keep `templates/` focused on contest differences.
- [ ] Keep `SKILL.md` concise; move details to references.
- [ ] Prefer deterministic scripts for fragile checks.
- [ ] Provide JSON output for scripts intended for Agent/backend use.
- [ ] Keep scripts runnable without unnecessary external dependencies.

### Documentation

- [ ] Update `README.md` after Phase 0/1 with new check scripts and skill usage.
- [ ] Keep docs linked:
  - [ ] market research
  - [ ] real competition workflow
  - [ ] skill plan
  - [ ] upgrade architecture
  - [ ] tasks
- [ ] Avoid adding more architecture documents unless implementation reveals a real gap.

## Immediate Next Steps

Start here:

1. [ ] Implement `scripts/summarize_build_log.py`.
2. [ ] Implement `scripts/inspect_template.py`.
3. [ ] Implement `scripts/check_tex_links.py`.
4. [ ] Implement `scripts/check_submission.py`.
5. [ ] Add smoke tests or sample fixtures.
6. [ ] Create `skills/modeling-paperkit/SKILL.md`.
7. [ ] Create `skills/modeling-paperkit/references/latex-patterns.md`.

Do not start these yet:

- [ ] Web UI.
- [ ] Full autonomous modeling Agent.
- [ ] RAG model database.
- [ ] Auto-submission workflow.
