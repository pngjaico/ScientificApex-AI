# Scientific validation and editorial preparation plan

Date: 2026-11-02. Status: **PROPOSED; implementation and validation remain pending**. Active project: `article-machine-governance-2026`. Scope: infrastructure and method validation; this document authorizes no new clinical conclusion, publication, external registration or paid call.

## Decision

Consolidate the existing architecture using shared execution gates, independently checked calculations and documented scientific review. The verifiable objective is to meet every applicable criterion within a declared scope while exposing uncertainty. Universal perfection, absence of bias and editorial acceptance cannot be guaranteed.

Alternatives considered: retaining the current version preserves functionality but leaves critical defects; adding more skills expands nominal coverage without validating methods; rewriting everything discards working components and introduces new risks. The preferred option is to repair and validate the present architecture by method family, preserving the requested capabilities.

## Starting evidence and priority defects

Local inspection confirmed methodology, corpus, dataset, document-extraction, metric and synthesis services. The strict audit passed and 11 focused tests passed during the preceding inspection. This does not validate all analyses or constitute a new full-suite run.

- `clinical_datasets.fetch_open_dataset` reaches the download function without calling the registration gate; reproduction used mocks without network or writes. `ingest_and_verify_dataset` disables this requirement by default.
- `study_and_synthesis.synthesize_from_r_outputs` inserts a full-human-verification statement without establishing that review. Reading claim-map entries does not establish claim approval.
- `results_ledger.evaluate_clinical_prediction_metrics` computes a conformal threshold and coverage on the same outcome pairs. Final evaluation needs separate data. Missing patient identifiers must not become certification of absent leakage.
- Handoff and project contract disagree on the active mode; post-checkpoint modifications and stale counts remain. Extraction tests depend on installed Tesseract and a personal certificate outside the portable package.

## Execution order and acceptance criteria

### P0 — Integrity and execution gates

Apply the reviewed-final-registration policy to all relevant scientific entrypoints: CLI, services, import/download, extraction, analysis and synthesis. Distinguish protocol preparation from execution. Trial registration and ethics remain additional requirements where applicable.

Check scientific state, protocol chronology, registration verification, provenance and claim approval before any final export. Execution, ethics, authorship, human-review and AI declarations must derive from actual records identifying a responsible person, date and artifact; absent fields remain pending. Label drafts and preserve earlier results/manuscripts rather than overwriting them.

Acceptance: every relevant route blocks before network/write/execution when prerequisites are missing; adversarial tests demonstrate each gate; no text declares unperformed work; absence of a finding is not automatic approval.

### P1 — Project-specific design and statistical plan

Before results, register the question, population, unit, setting, dates, estimand, outcomes/windows, comparators, sample size, eligibility, confounding, missingness, multiplicity and sensitivity analyses. Justify sample size from design, events and intended precision; reject universal numerical rules. Distinguish confirmatory, exploratory, causal and predictive aims.

Use reporting guidelines and appraisal instruments for distinct purposes: TRIPOD+AI and PROBAST+AI for prediction; PRISMA 2020/extensions for reviews; QUADAS-3 for primary accuracy studies within reviews; SPIRIT 2025 and CONSORT 2025 for trial protocols/results. Apply RoB/GRADE according to question/design with human reasoning, not automatic keyword completion.

Acceptance: a complete reviewed protocol, verified final registration before scientific execution, tracked amendments/deviations and each applicable item connected to a concrete methodological decision.

### P2 — Numerically validated R and statistics

Compare results with published examples, analytical calculations or an independent implementation. Fix methods/tolerances before comparison; package differences are defects only when estimands, data and options coincide. Do not select software for a preferred result.

Cover effect measures, variances, intervals, heterogeneity, dependence/multiple arms, regressions, survival, missing data and assumptions for activated families. Test denominator errors, nonfinite values, separation, few studies, rare events and nonconvergence. NMA requires connectivity, transitivity and incoherence assessment; DTA needs the joint sensitivity/specificity structure. Rankings do not replace effect magnitude and certainty.

Acceptance: reference cases reproduced, discrepancies explained, invalid results blocked, warnings classified and all table/figure/manuscript numbers derived from canonical results.

### P3 — Appropriate ML and DL evaluation

Define intended population, prediction time, predictor availability, outcome and baseline. Respect patient/group/site/time partitions as required by design. Keep imputation, selection, transformation, balancing, tuning and calibration within appropriate training partitions. Nested CV remains internal validation; external testing needs independent compatible data.

Repair conformal evaluation using separate conformalization/test data and explicit assumptions. Marginal coverage does not guarantee subgroup coverage or validity under distribution shift. Report discrimination, calibration, Brier, uncertainty, errors, sufficiently precise subgroup results and utility within the evaluation's actual scope. For DL/images, audit duplicates, origin, labels, acquisition, pretraining and patient-level separation; explanation maps do not establish causation.

Acceptance: manifests/tests support absence of leakage, a comparable baseline, evaluation free of final-test-driven selection and documented external validation when performed. Without external validation, explicitly limit claims; never fabricate a universal performance threshold or require DL to beat a baseline.

### P4 — Verifiable reviews and meta-analyses

Select review/synthesis methods from the question. Preserve full searches, platforms/dates and exports; reconcile deduplication, selection and PRISMA flow. Document reviewers, conflicts, exclusions, checked extraction, multiple reports of a study and RoB/GRADE judgments. OCR and AI prioritization remain assistance requiring checking.

Acceptance: reconciled counts; extracted values traceable to pages/tables; compatible measures/populations before synthesis; justified primary/sensitivity analyses; conclusions limited by evidence certainty.

### P5 — Reproducibility and portability

Restore environments from `uv.lock`/`renv.lock` into clean directories. Rerun analysis/rendering without accidental dependence on personal files, global libraries or old paths. Separate portable tests from optional integrations such as OCR/browser; an absent mandatory requirement blocks that capability rather than becoming PASS. Preserve hashes of inputs, scripts, results and versions.

Acceptance: documented third-party reconstruction or independent execution, actual CI on the corresponding commit when authorized and numerical agreement within specified tolerances. Code coverage/security audits complement scientific validation; they do not replace it.

### P6 — PT-BR/EN documentation and editorial package

Each project must provide protocol/registration/amendments; statistical plan; dictionary/provenance; code/locks; logs/canonical results; figures/tables; applicable checklist with page locations; relevant RoB/GRADE assessments; manuscript, supplements, cover letter, CRediT, conflicts, funding, ethics, consent and actual AI disclosure; reviewer responses when available.

Pair natural Portuguese and English with Portuguese filenames, shared code/data and numerical, bibliographic, semantic and visual audits. Verify current journal scope, indexing, category, limits and fees. Relevance, design and contribution precede formatting; do not promise acceptance.

Acceptance: no unresolved field in a package presented as final; supported claims; author approval of declarations; checked layout/references; external submission requires specific authorization.

### P7 — Benchmarks and independent review

Create reference cases per family and deliberately erroneous tests. Proposed initial panel: binary, continuous and dependent meta-analysis; DTA; NMA; observational regression; survival; tabular ML; DL/images; conformal; document extraction; editorial integrity. Each case has licensed/synthetic inputs, reference answers, tolerances, limitations and a predefined evaluator. Software fixtures never become clinical findings.

Acceptance: all defined critical criteria pass with no open critical defect; capability-level failures/SKIPPED remain visible. A methodologist/statistician and clinical specialist review relevant parts of real studies; repeated AI opinions do not equal independent human review. Validation of one family does not certify the others.

## Recommended first milestone

Complete P0; validate metrics and a meta-analysis workflow numerically; reproduce environments; run a complete demonstration using synthetic data or published methodological references; then conduct a prospectively registered real study with independent review and a complete editorial package. Promote only capabilities supported by obtained evidence. This plan declares none of those steps complete.

## Official sources consulted

- [TRIPOD+AI and TRIPOD-LLM](https://www.tripod-statement.org/) and [PROBAST+AI](https://www.probast.org/).
- [PRISMA 2020](https://www.prisma-statement.org/prisma-2020), [current Cochrane Handbook](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current), [QUADAS-3](https://www.bristol.ac.uk/population-health-sciences/projects/quadas/quadas-3/) and [SPIRIT/CONSORT](https://www.consort-spirit.org/).
- [scikit-learn: leakage and good practices](https://scikit-learn.org/stable/common_pitfalls.html), [MAPIE: conformal separation](https://github.com/scikit-learn-contrib/MAPIE/blob/master/doc/content/conformal-prediction/split-cross-conformal.md).
- [metafor: reproduced analyses](https://www.metafor-project.org/doku.php/analyses), [renv](https://rstudio.github.io/renv/articles/renv.html), [ICMJE: AI use](https://www.icmje.org/recommendations/browse/artificial-intelligence/).
