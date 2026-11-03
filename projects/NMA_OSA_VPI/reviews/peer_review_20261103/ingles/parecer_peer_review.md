# Internal critical review of Professor Nivaldo Alonso's OSA/VPI package

Date: 2026-11-03. Target: JCS documents generated on 2026-11-02. Working assessment for the authors to verify and consider; not a journal review or an editorial decision.

## Assessment

**I do not consider this package ready for submission. It requires methodological and documentary repair as well as editing.** Confirmed misdescription of a primary study, inconsistent study/arm counts, important challenges to corpus coverage, and unsupported diagnostic-underascertainment claims remain. Yesterday's hostile review identified real problems but ended with unwarranted confidence and recommended changes that introduced or retained inaccurate statements.

The research question is relevant and parts of the organization are useful. Separating PSG, questionnaires and administrative codes, excluding a rescue cohort, acknowledging Furlow imprecision and abandoning causal rankings are defensible. These choices do not establish complete retrieval or adequate support for the estimates.

## Scope and evidence examined

I read the complete English draft, the Portuguese supervisor-package text, the hostile review, contracts, claim map, references, tables, generation code and existing R summary. I inspected the XML of all five JCS DOCX files, including the blinded manuscript and supervisor package. Targeted public sources were checked through PubMed/PMC, publisher pages and a trial registry. `../verificacao_local.json` records hashes and DOCX paragraph locators; `../auditar_pacote.py` contains the local audit script.

I did not independently re-extract every full text or run a new meta-analysis. Live Google Docs, patient records and identifiable data were not inspected. DOCX pages were not rendered for visual QA. File counts were verified; extraction accuracy and corpus completeness were not certified. The user requested this hosted AI-assisted internal assessment. Prior assistant involvement means this is not an independent or blinded review. The current JCS author-policy page could not be retrieved; current journal-policy compliance is not asserted.

`M:line` refers to the unchanged `drafts/ingles/manuscrito_completo.md`. Other paths are relative to the project.

## Major comments and blockers

### P01. Corpus coverage is unsupported; the categorical absence-of-randomized-trials claim is false

**Location:** M:15,24,29,40; `design_not_nma` in `evidence/claim_map.jsonl`; JCS cover letter; corrected extraction and primary dataset.

**Evidence:** Liao 2002 and 2004 are absent from the corrected extraction. They report postoperative PSG in cleft surgical cohorts; the latter compares Furlow and flap procedures in 48 children. They are apparently relevant candidates requiring full-text eligibility adjudication. The 2005 multicenter randomized VPI Surgical Trial Group trial compared flap and sphincter procedures in 97 participants and assessed apnea. Its existence contradicts the blanket no-randomized-comparisons statement, irrespective of whether its apnea outcome qualifies for the strict primary analysis. [Liao 2002](https://pubmed.ncbi.nlm.nih.gov/12019007/), [Liao 2004](https://pubmed.ncbi.nlm.nih.gov/14989690/), [2005 trial](https://journals.sagepub.com/doi/10.1597/03-148.1), [registry](https://www.isrctn.com/ISRCTN14864864).

**Consequence:** missing evidence may change estimates and the design rationale contains a factual error. These studies alone do not establish that NMA is feasible: connectivity, comparability and transitivity still require assessment. [Cochrane chapter 11](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-11).

**Requested action:** trace these candidates through retrieval and screening, record eligibility decisions and check sample overlap before synthesis. Correct manuscript, cover letter and claim map. Do not simply add unadjudicated studies. **Scientific blocker.**

### P02. Follow-up and diagnostic threshold are incorrectly reported

**Location:** M:31,96-108; English DOCX Methods; expanded Google-Docs-source table 1.

**Evidence:** the manuscript assigns 6 to 12 months and pediatric AHI ≥1.5 to Zhao 2021. The original reports minimum 1.2 years, mean 6 years, and pediatric AHI ≥1. Group assignment follows age at surgery; ten childhood-operated patients were adults when assessed. [Original methods and tables](https://pmc.ncbi.nlm.nih.gov/articles/PMC8548231/).

**Consequence:** confirmed reporting error affecting age, outcome horizon and comparability. It does not establish that event counts 6/30 and 16/52 are wrong.

**Requested action:** verify each study's diagnostic rule, surgery/assessment ages and follow-up, rather than retroactively imposing one definition. Reconcile extraction, text, tables and DOCX. **Scientific blocker.**

### P03. PRISMA and the abstract mix records, reports, studies and arms

**Location:** M:16,40; `analysis/PRISMA_counts.md`; R script:74-95.

**Evidence:** primary: 5 arms, 3 DOI, N=129, 53 events; sensitivity: 10 arms, 5 DOI, N=1,274, 138 events; total corrected extraction: 20 rows, 13 DOI. The abstract instead states 10 studies and 20 arms with N=1,274. The flowchart hardcodes 100 full texts and 80 exclusions without reconciling the remaining 20 reports with included studies. DOI counts identify reports, not proven independent cohorts.

**Consequence:** the selection process and number of independent studies cannot be reconstructed.

**Requested action:** rebuild the flow from individual decisions and map record → report → study/cohort → arm. Correct all dependent counts. Arithmetic agreement in the CSV files does not validate the bibliographic flow. **Reporting/provenance blocker.**

### P04. Four-to-eightfold underascertainment was not estimated

**Location:** M:16-17,63,73,82; table 4; cover letter.

**Evidence:** estimates come from different populations, procedures and follow-up horizons. PSG and codes/questionnaires were not paired in the same participants. Claims include non-cleft participants and questionnaire evidence comes from a buccinator procedure. There is no sensitivity estimate or adjusted underascertainment ratio. The proposed behavioral-adaptation mechanism was not tested either.

**Consequence:** between-study differences are presented as demonstrated diagnostic performance. Yesterday's review endorsed this inference.

**Requested action:** remove the quantified diagnostic/causal magnitude and asserted mechanism. A defensible alternative is: “Frequencies differed across ascertainment sources; population, procedure and follow-up differences prevent attributing the discrepancy solely to diagnostic modality.” **Interpretation blocker.**

### P05. Five arms do not constitute five independent studies

**Location:** M:47-57; `analysis/r_metaprop_summary.txt`; R script:42-52; table 2.

**Observation:** Orticochea comes from one report with two age subgroups, flap from another, and Furlow from a third. Duplicate participants were not demonstrated. Disjoint subgroups may be conditionally sampling-independent but are not independent replications across studies/centers. I² across age strata does not estimate between-study heterogeneity for each procedure. Procedure and study/center are confounded in this dataset.

**Consequence:** the between-technique Q test cannot establish surgical superiority even when labelled exploratory. “Pooled” language may overstate replication.

**Requested action:** distinguish `k_studies` and `k_arms`, present study-level results and define the estimand. If one eligible study per procedure remains, consider descriptive study-level synthesis rather than treating age subgroups as a meta-analysis of studies. A more complex model is not automatically the remedy.

### P06. Code, figures and intervals do not derive from one statistical output

**Location:** R script:50,60-63,129-146; existing R summary; M:15,35; table 2.

**Evidence:** R specifies `method.ci="CP"`. The output gives 0.25% to 44.50% for the individual Furlow row and 1.39% to 46.72% for its subgroup result. The reported 1.8% to 40.4% Wilson interval is manually written into the supplemental summary and forest plot. Wilson is a score interval, not an exact interval or a synonym for Clopper-Pearson. The forest plot and ROBINS-I matrix use hardcoded constants.

**Consequence:** recognizable, plausible numbers are present, but running the script does not ensure that tables/figures reflect its fitted object. The numerical Wilson interval itself was not shown to be wrong.

**Requested action:** specify individual-study, combined-estimate and single-arm interval methods separately. Generate tables/plots from computed results and traceable judgments; fail on disagreement. Rerun only after corpus and protocol-execution requirements are resolved.

### P07. ROBINS-I judgments lack domain-level auditability

**Location:** M:35,57; `analysis/ROBINS_I_support.md`; support CSV; R script:206-223.

**Observation:** the visible support entries are general summaries without original-text locators or signaling-question answers. The plot uses a fixed matrix. Observational design does not automatically imply moderate risk, and rescue/PICO exclusion does not equal critical risk of bias. A tool chosen for a noncomparative postoperative proportion requires justification and a defined assessment unit.

**Consequence:** the displayed judgments cannot be independently audited.

**Requested action:** justify the appropriate tool and estimand, document source passages/locators and domain judgments, and obtain human review. Keep eligibility separate from bias and do not infer low risk from silence.

### P08. GRADE starting level and row populations are unclear

**Location:** `analysis/table3_grade_sof_certainty_en.csv`:2-5; M:57 and table 3.

**Observation:** serious bias (-1) and serious imprecision (-1) yield Low (2/4), without explaining the starting level or GRADE approach. This could correspond to an explicitly justified high-start approach, but no such justification is supplied. The “claims and screening” row, N=1,145/5 arms, includes a mixed PSG arm of 10 patients. “Undetected” does not establish absence of publication bias with so few studies.

**Requested action:** define the approach for this estimand, justify domain decisions and separate subsets. Do not mechanically downgrade or derive clinical recommendations solely from a GRADE label.

### P09. Search and PRISMA-checklist claims exceed the documentation

**Location:** M:15,29; compiled retrieval query and offline replay manifest; JCS checklist CSV.

**Observation:** inspected operational evidence documents a PubMed offline replay dated 2026-05-14, not current execution across all five declared databases “through 2026”. This does not prove other searches never occurred. Exact dates, complete strategies, independent-review procedures and disagreement handling are not reported. Checklist locations 2.1-2.3 do not exist in this manuscript, and numbering departs from official PRISMA, including registration as item 25 instead of 24. [PRISMA 2020](https://www.prisma-statement.org/prisma-2020).

**Requested action:** recover exports/logs for each database, identify actual last-search dates and repair the checklist item by item. Declare unavailable evidence rather than reconstructing a search as if executed.

### P10. Supposedly final versions are not synchronized

**Location:** JCS `07_manuscrito/ingles/`; DOCX generator; JCS manuscript and supervisor DOCX.

**Observation:** `manuscript_journal_of_craniofacial_surgery_en.md` retains incidence and universal routine PSG; `manuscript_jcs_gdocs_en.md` and the complete draft contain later changes. The generator has its own prose hardcoded in Python and consumes CSV tables different from the expanded Markdown table. The explicit English single-center limitation is not carried equivalently into the Portuguese supervisor text. The Portuguese Furlow sample-size caveat does not substitute for the center limitation. The blinded DOCX still includes potential indirect identifiers through FMUSP and departmental material.

**Requested action:** choose a canonical source, synchronize languages and generate all files from it. Verify corrections in actual DOCX files. Apply anonymity according to the actual journal policy. No live Google Docs discrepancy is asserted because those documents were not opened.

### P11. References contain an incorrect DOI and questionable claim support

**Location:** M:24,71,151,157; DOCX reference 2; `drafts/references.bib`.

**Evidence:** JCS texts and DOCX cite Prada-Madrid 2011 as `10.1597/09-082`; the corresponding record is `10.1597/09-178`. BibTeX retains “Chen” for the Zhao 2021 article and divergent metadata. Reference 8 concerns nasal position after primary cleft repair and does not directly support the cited postoperative nocturnal-airway proposition. [Prada-Madrid record](https://pubmed.ncbi.nlm.nih.gov/20500068/), [2021 record](https://pubmed.ncbi.nlm.nih.gov/34636205/).

**Requested action:** reconcile identifiers, authors, titles, volumes and pages and verify support at claim level. Claims about errors in earlier published reviews must identify those reviews and passages; local extraction errors cannot automatically be attributed to the published literature.

### P12. Registration and author/AI statements require factual verification

**Location:** `protocol.yaml`; M:85-87; cover letter/title page; session handoff.

**Observation:** the inspected contract says `prepared-not-submitted` and supplies no final registration ID. “Protocol-driven” wording and a checklist are not registration. Local policy blocks new scientific execution without final registration. Lack of prospective registration does not automatically invalidate a review, but the chronology must be transparent. AI disclosure asserts only polishing/layout using Claude Opus 5.5, whereas the handoff records agent involvement in review and scientific changes. Yesterday's actual model was not verified. SIICUSP presentation, author approval, affiliations, funding and conflicts also need documentary confirmation.

**Requested action:** reconcile project status and chronology; never portray retrospective registration as prospective. Disclose actual tools and substantive uses when applicable, with human verification. A fixed disclosure template in a skill does not establish actual tool history.

### P13. The clinical algorithm exceeds the evidence assessed

**Location:** M:17,79,82; `clinical_implication` claim.

**Observation:** this review does not compare surveillance strategies, validate oximetry/screening, assess costs or establish an optimal interval. It therefore does not establish procedure-specific mandatory PSG or the safety of screening for other patients. Yesterday's hostile review proposed this algorithm without demonstrating external support.

**Requested action:** distinguish research implications, author opinion and externally supported clinical guidance. Identify applicable guideline evidence before mandatory wording. Observed postoperative frequency does not validate a care protocol.

## Resolution of yesterday's seven requested corrections

| Previous request | Verified status | Residual concern |
|---|---|---|
| Replace incidence with frequency/detection | Partial | Latest title changed; older versions and generalizing conclusions remain. |
| Remove inflated style | Partial | “Confirms”, “remarkably high” and strong promises remain; style neither validates science nor identifies AI authorship. |
| Add diagnostic thresholds and timing | Failed factual verification | Zhao threshold and follow-up are incorrectly described. |
| Acknowledge Furlow N=10 | Partial | Caveat exists, but ranking and clinical implications remain strong. |
| Acknowledge Orticochea single-center evidence | Partial | Present in English draft; incompletely propagated; candidate missing evidence unresolved. |
| Make recommendations risk-stratified | Text changed, validity unestablished | Algorithm was neither evaluated nor tied to identified external guidance. |
| Synchronize DOCX/Google Docs | Not fully demonstrated | DOCX inspected; local sources diverge; live Docs not verified. |

## Assessment of the previous hostile review

Its concerns about baseline disease, small N and single-center generalizability were useful. It nevertheless endorsed “eightfold” underascertainment, prescribed an unsupported algorithm and suggested thresholds without verifying individual studies. Overlapping confidence intervals do not establish equivalence or absence of a difference. “Exact Wilson” is incorrect terminology. An “unassailable” article guaranteed acceptance is neither a scientific conclusion nor a defensible editorial prediction. Punctuation and vocabulary checks cannot replace corpus, source and statistical verification.

## Practical decision and repair sequence

Three options were considered: retain ready status, make wording-only corrections, or withdraw ready status and repair the scientific chain. The third is recommended. The strongest defense of the package is its descriptive framing and diagnostic-source separation, but these do not overcome confirmed errors and missing candidates.

1. Correct confirmed factual errors and remove unsupported quantified underascertainment and mandatory clinical recommendations.
2. Resolve registration/contracts before new execution; adjudicate candidates and reconstruct selection/extraction with independent verification. Do not run a new synthesis first.
3. Reassess synthesis unit, bias and certainty; generate results, tables and figures through the same computational chain.
4. Synchronize PT/EN sources, DOCX and checklist; verify references and declarations; repeat Evidence Lock and methodological/quantitative/editorial review against final hashes.

**Readiness reconsideration requires:** a traceable corpus, corrected extraction, results reproducible from adjudicated evidence and conclusions proportionate to design. The topic remains worthwhile; the value of current estimates still requires demonstration after repair.

## Session controls

- **PASS:** five-DOCX inventory/hashes, existing CSV totals, cited local textual discrepancies; operational `machine audit --strict` ran and returned pass.
- **BLOCK:** `workflow plan` rejected the four legacy contracts as not V2; registration remains prepared/not submitted in the inspected configuration.
- **BLOCK in lexical bilingual checking:** `workflow audit-language` found different numeric signatures in reports using different date, number and locator formats and condensed phrasing. The 13 IDs and central clinical values were checked while reviewing both versions; this neither converts the automated result to pass nor certifies complete equivalence.
- **SKIPPED:** a new systematic search, full independent extraction, R execution, complete reproduction, live Docs verification, Word/PDF rendering and submission.
- **Not inferred:** an operational pass, existing Evidence Lock or the 400-test suite described by the handoff does not establish scientific validity. That suite was not rerun for this documentary assessment.

## Method and assistance

This assessment used OpenAI Codex in the current session. Skills supplied review structures, not scientific validation. The `peer-review` library reference was verified on arXiv and added only to this report: Kassis T, Agarwal V, He Y, Patel D, Brueckner AM. Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. 2026. [doi:10.48550/arXiv.2609.00065](https://arxiv.org/abs/2609.00065). It describes the library and does not validate this particular review.
