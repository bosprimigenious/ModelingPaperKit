# Model Fitness Checklist

## Per subproblem (Qi)

- [ ] Required answer form written in one phrase
- [ ] Direct answer sentence template exists (no 可知/However)
- [ ] Candidate model output type matches that form (or scripted transform exists)
- [ ] Real data fields listed and verified present
- [ ] Split / leakage rule written
- [ ] Baseline defined on **same** deliverable
- [ ] Smoke run artifact path exists
- [ ] Validation or sensitivity planned or done
- [ ] Assumptions list; each tagged used-in-math / used-in-data / unused
- [ ] Reject criteria: when would we abandon this model?
- [ ] Verdict: PASS / REFINE / REJECT with one-line reason

## Whole paper risk

- [ ] Every Qi has PASS or time-boxed REFINE plan
- [ ] No Qi is “advanced model” without direct answer
- [ ] Interfaces between Qi share units and symbols
- [ ] `artifacts/model_fitness.md` filled
- [ ] `python3 scripts/check_model_fitness.py --artifacts artifacts` clean enough to proceed
