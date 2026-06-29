# OncoMetabolic CRC NMA Publication Pack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `projects/OncoMetabolic_CRC_NMA` into an indexed-journal submission package with updated retrieval, methodological audit, rerun quantitative outputs, figures, congress abstract, cover letters, and explicit red-team limitations.

**Architecture:** Keep all scientific work inside `projects/OncoMetabolic_CRC_NMA`. Use Article Machine contracts for retrieval, screening, extraction, evidence lock, Review Trinity, and guard checks. Generate final publication outputs from scripts so manuscripts, figures, tables, and letters are reproducible.

**Tech Stack:** Article Machine CLI (`.venv\Scripts\article-machine.exe`), Python, R/netmeta/meta/ggplot2, PubMed E-utilities, Scopus API if available, python-docx for DOCX deliverables, local markdown/CSV/JSON manifests.

---

### Task 1: Baseline Audit And Plan Lock

**Files:**
- Read: `projects/OncoMetabolic_CRC_NMA/project.yaml`
- Read: `projects/OncoMetabolic_CRC_NMA/protocol.yaml`
- Read: `projects/OncoMetabolic_CRC_NMA/standards.yaml`
- Read: `projects/OncoMetabolic_CRC_NMA/context/query_plan.yaml`
- Create: `projects/OncoMetabolic_CRC_NMA/reviews/PUBLISHABILITY_AUDIT_20260526.md`

- [ ] **Step 1: Verify Article Machine baseline**

Run:
```powershell
.\.venv\Scripts\article-machine.exe preflight .\projects\OncoMetabolic_CRC_NMA
.\.venv\Scripts\article-machine.exe guard check .\projects\OncoMetabolic_CRC_NMA
.\.venv\Scripts\article-machine.exe retrieval plan .\projects\OncoMetabolic_CRC_NMA
.\.venv\Scripts\article-machine.exe retrieval audit .\projects\OncoMetabolic_CRC_NMA
```

Expected: preflight and guard pass; retrieval plan shows PubMed provider; retrieval audit passes existing manifests.

- [ ] **Step 2: Write the publishability audit**

Create `reviews/PUBLISHABILITY_AUDIT_20260526.md` with:
- Current status.
- Blocking issues for indexed-journal submission.
- Fixes performed in this run.
- Items that require human/professor action.
- Whether the work is publishable as exploratory observational NMA, not causal efficacy evidence.

### Task 2: Updated Literature Retrieval

**Files:**
- Modify: `projects/OncoMetabolic_CRC_NMA/context/query_plan.yaml`
- Create: `projects/OncoMetabolic_CRC_NMA/evidence/retrieval/raw/pubmed_esearch_20260526.json`
- Create: `projects/OncoMetabolic_CRC_NMA/evidence/retrieval/raw/pubmed_esummary_20260526.json`
- Create: `projects/OncoMetabolic_CRC_NMA/evidence/retrieval/pubmed_manifest_20260526.json`
- Create: `projects/OncoMetabolic_CRC_NMA/evidence/scopus_retrieval/raw/scopus_gap_20260526.json` if Scopus API responds.
- Create: `projects/OncoMetabolic_CRC_NMA/evidence/scopus_retrieval/scopus_manifest_20260526.json` if Scopus API responds.
- Create: `projects/OncoMetabolic_CRC_NMA/analysis/literature_gap_screen_20260526.csv`
- Create: `projects/OncoMetabolic_CRC_NMA/reviews/LITERATURE_UPDATE_20260526.md`

- [ ] **Step 1: Extend query date**

Update `context/query_plan.yaml` date range to end at `2026-05-26`.

- [ ] **Step 2: Run PubMed E-utilities with manifest**

Use the compiled query from `article-machine retrieval plan`, retrieve PubMed records up to `2026-05-26`, save raw JSON, calculate `records_sha256`, and write a manifest with:
```json
{
  "provider": "pubmed",
  "query_hash": "<sha256 of query>",
  "retrieved_at": "<UTC ISO timestamp>",
  "record_count": 0,
  "records_sha256": "<sha256 of esummary payload>"
}
```

- [ ] **Step 3: Attempt Scopus API retrieval**

Use the local Scopus query pattern from `scripts/fetch_scopus_full.py`, but do not hard-code or expose any API key in newly written code. If no usable key is available or the API rejects the request, write the failure into `reviews/LITERATURE_UPDATE_20260526.md` and do not fabricate Scopus results.

- [ ] **Step 4: Screen candidate additions**

Compare updated PubMed/Scopus records with base NMA source files and write `analysis/literature_gap_screen_20260526.csv` with columns:
`source,identifier,title,year,intervention,outcome,design,screen_decision,reason,network_action`.

### Task 3: Analysis Rerun And Figure Package

**Files:**
- Read/Modify if needed: `projects/OncoMetabolic_CRC_NMA/sources/cleaned/nma_clean_crc_base.csv`
- Read/Modify if needed: `projects/OncoMetabolic_CRC_NMA/sources/cleaned/nma_clean_crc_sensitivity.csv`
- Run: `projects/OncoMetabolic_CRC_NMA/scripts/run_nma_clean_crc.R`
- Create/Update: `projects/OncoMetabolic_CRC_NMA/sources/cleaned/nma_clean_crc_results.xlsx`
- Create/Update: `projects/OncoMetabolic_CRC_NMA/sources/cleaned/nma_clean_crc_forest.png`
- Create/Update: `projects/OncoMetabolic_CRC_NMA/sources/cleaned/nma_clean_crc_hub_inflated_forest.png`
- Create/Update: `projects/OncoMetabolic_CRC_NMA/sources/cleaned/nma_clean_crc_network.png`
- Create/Update: `projects/OncoMetabolic_CRC_NMA/sources/cleaned/nma_clean_crc_pscore.png`
- Create/Update: `projects/OncoMetabolic_CRC_NMA/sources/cleaned/nma_clean_crc_bariatric_pairwise_forest.png`
- Create: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/figures/`

- [ ] **Step 1: Decide whether new articles change the network**

If gap screening finds a new eligible active-comparator CRC HR/aHR study, add it to the base dataset with source evidence and rerun the NMA. If new articles are reviews, adenoma-only, non-user comparator, pharmacovigilance, MR-only, overlapping database, or non-CRC, keep them in narrative/gap notes and do not change the primary network.

- [ ] **Step 2: Rerun NMA**

Run:
```powershell
.\.venv\Scripts\article-machine.exe run-r .\projects\OncoMetabolic_CRC_NMA scripts\run_nma_clean_crc.R
```

Expected: output ranking CSVs, network plot, forest plots, P-score plot, bariatric forest plot, and Excel workbook.

- [ ] **Step 3: Copy figure package**

Copy final figure files into `deliverables/publication_pack_20260526/figures/` and write a figure manifest listing source path, caption, and intended manuscript location.

### Task 4: Manuscript, Congress Abstract, And Submission Letters

**Files:**
- Create: `projects/OncoMetabolic_CRC_NMA/scripts/build_publication_pack.py`
- Create: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/manuscript.md`
- Create: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/cover_letter.md`
- Create: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/editor_inquiry_letter.md`
- Create: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/congress_abstract_pt.md`
- Create: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/congress_abstract_en.md`
- Create: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/title_page.md`
- Create: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/highlights.md`

- [ ] **Step 1: Generate manuscript**

Write an English indexed-journal manuscript with structured abstract, introduction, methods, results, discussion, limitations, conclusions, references, tables, and figure callouts.

- [ ] **Step 2: Preserve scientific caveats**

Manuscript must explicitly say:
- Evidence is observational and exploratory.
- All base studies have serious ROBINS-I concerns.
- GLP1-RA ranking is hub-dependent.
- Bariatric surgery has numerically lower HR but is not pooled with pharmacologic NMA.
- PROSPERO identifier must be inserted before external submission.

- [ ] **Step 3: Generate congress abstracts and letters**

Produce PT and EN congress abstracts plus cover letter and editor inquiry letter. Do not state that the work is definitive, causal, or ready for a top-tier journal without caveats.

### Task 5: Evidence Lock, Red Team, And Final Gate

**Files:**
- Create: `projects/OncoMetabolic_CRC_NMA/reviews/SCIENTIFIC_RED_TEAM_20260526.md`
- Create/Update: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/manifest.json`
- Create/Update: `projects/OncoMetabolic_CRC_NMA/deliverables/publication_pack_20260526/qa_report.json`

- [ ] **Step 1: Run Article Machine review and guard**

Run:
```powershell
.\.venv\Scripts\article-machine.exe review .\projects\OncoMetabolic_CRC_NMA
.\.venv\Scripts\article-machine.exe guard check .\projects\OncoMetabolic_CRC_NMA
```

Expected: pass or explicit blocking issues.

- [ ] **Step 2: Red-team submission claims**

Write `reviews/SCIENTIFIC_RED_TEAM_20260526.md` attacking novelty, causal inference, transitivity, overlap, screening, GRADE, risk of bias, and dissemination language.

- [ ] **Step 3: Final status**

Report exactly:
- What was changed.
- Which figures/deliverables exist.
- Whether new articles were added or not.
- Which validations passed.
- Which issues still block real external submission.
