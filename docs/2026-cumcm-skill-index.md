# 2026 CUMCM Skill Index

This index maps common 2026 CUMCM preparation tasks to repository skills and machine gates.

**Status legend**

- **gated**: has a deterministic script or hard acceptance command
- **guidance-only**: agent skill + checklist; human/LLM still executes judgment

Passing gates means lower submission risk. It does **not** guarantee an award.

## Skill Map

| Need | Skill | Trigger | Required output | Acceptance / gate | Status |
|---|---|---|---|---|---|
| Track official notices | `cumcm-2026-rules-watch` | Before contest / rule changes | Updated rules notes | `acceptance.md` + official snapshot | guidance-only |
| Audit LaTeX template | `cumcm-template-audit` | Template edits | Format findings | `inspect_template` / `check_submission` | gated |
| Decompose problem | `cumcm-problem-reading` | New problem, before methods | `artifacts/task_matrix.md` | `check_claim_coverage` | guidance + coverage gate |
| Paper structure | `cumcm-paper-structure` | Drafting sections | Section skeleton review | checklist in skill | guidance-only |
| Modeling strategy | `cumcm-modeling-plan` | After reading, before lock | `artifacts/modeling_decision_card.md` | decision-card + acceptance | guidance-only |
| Model usable vs problem/judge answer | `cumcm-model-fitness` | Before lock / after first runs | `artifacts/model_fitness.md` | **`check_model_fitness`** | **gated** |
| Baseline models | `cumcm-baseline-models` | Before complex models | Baseline metrics | checklist | guidance-only |
| Data quality | `cumcm-data-quality-audit` | Raw/processed data ready | Issue list | checklist | guidance-only |
| Code/data layout | `cumcm-data-code-pipeline` | Workspace setup | Reproducible tree | directory-layout ref | guidance-only |
| Experiment log | `cumcm-experiment-log` | While running models | Run log | schema ref | guidance-only |
| Figures/tables | `cumcm-figures-tables` | Result presentation | Captions + assets | tex-links / manual | guidance-only |
| Validation/sensitivity | `cumcm-validation-sensitivity` | After main results | Validation notes | checklist | guidance-only |
| Paper–result consistency | `cumcm-result-consistency` | Numbers in draft | `artifacts/claim_map.md` | `check_claim_coverage` | guidance + coverage gate |
| Sentence polish / de-AI | `cumcm-sentence-polish` | Stable facts, AI-heavy prose | Polished tex + removal report | **`check_prose_style`** | **gated** |
| References + AI log | `cumcm-citation-ai-log` | Continuous | Source/AI logs | checklist | guidance-only |
| Identity leaks | `cumcm-anonymity-check` | Before submit | Leak findings | **`check_identity_leaks`** | **gated** |
| Support materials | `cumcm-support-material-audit` | Before pack | Risk list | checklist | guidance-only |
| Submission package | `cumcm-submission-pack` | Final package | Package tree | **`check_submission`** | **gated** |
| Contest safety | `cumcm-contest-safety-mode` | Live contest window | Red-line adherence | policy only | guidance-only |
| Final review | `cumcm-final-review` | Last pass | Severity-ordered findings | **`preflight`** | **gated** |
| PaperKit delivery | `modeling-paperkit` | Working in this repo | Build/diagnose path | build + preflight | gated |

## Suggested Preparation Loop

1. `cumcm-2026-rules-watch` — confirm current rules.
2. `cumcm-template-audit` — keep `templates/cumcm` safe.
3. `cumcm-contest-safety-mode` — during the active window.
4. `cumcm-problem-reading` → write `artifacts/task_matrix.md`.
5. `cumcm-modeling-plan` → write `artifacts/modeling_decision_card.md`.
5b. `cumcm-model-fitness` → write `artifacts/model_fitness.md` and gate PASS/REFINE/REJECT.
6. `cumcm-baseline-models` + data skills before trusting results.
7. Produce results → `cumcm-result-consistency` → `artifacts/claim_map.md`.
8. `cumcm-sentence-polish` then **`check_prose_style`** (clear AI filler / meta-language).
9. `cumcm-citation-ai-log` continuously.
10. `preflight` + anonymity + submission + final review.

## Machine validation bundle

Baseline (official sources): `docs/2026-cumcm-official-rules-snapshot.md`.

```bash
# Structure + contracts
python3 scripts/check_skills.py skills
python3 scripts/check_skill_contract.py skills --require-fixtures

# Prose: AI filler + "不要/Do not" meta-language
python3 scripts/check_prose_style.py --target cumcm
python3 scripts/check_prose_style.py --path tests/fixtures/prose_bad.tex   # must go red
python3 scripts/check_prose_style.py --path tests/fixtures/prose_good.tex  # must stay clean

# Optional coverage (when artifacts exist)
python3 scripts/check_claim_coverage.py --artifacts artifacts

# One-shot
python3 scripts/preflight.py --target cumcm --strict-prose --strict-placeholders --skip-git-diff-check
python3 scripts/preflight.py --target cumcm --artifacts artifacts --skip-git-diff-check

# Template / identity / links / submission
python3 scripts/inspect_template.py --target cumcm
python3 scripts/check_identity_leaks.py templates/cumcm
python3 scripts/check_tex_links.py --target cumcm
python3 scripts/check_submission.py --target cumcm
```

Build when `xelatex` is installed:

```bash
python3 scripts/build.py --target cumcm
```

## Dual-repo sync

Tooling changes land in **ModelingPaperKit** first, then:

```bash
python3 scripts/sync_to_contest_repo.py --dest ../math_modeling2026
```

See `docs/repo-sync.md`.
