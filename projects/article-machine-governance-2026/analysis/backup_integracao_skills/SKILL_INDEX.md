# Global Skill Index - Article Machine

## Layer 0: Navigation and Content Preservation
- `workspace-graph-navigator`: use `graphify-out/GRAPH_REPORT.md`, `graphify-out/graph.html`, and `python -m graphify query` before broad workspace navigation.
- `project-entry-navigator`: select or create the active `projects/<project_id>/`, read the four contract files, and build context before evidence, analysis, discovery, or drafting.
- `content-preservation-guardian`: protect raw scientific content, legacy folders, full text, patient/source dumps, and generated caches during cleanup, staging, graphing, or reorganization.

## Layer 1 and 2: Review and Evidence
- Use literature, citation, peer-review, and evidence skills for search, screening, extraction, synthesis, and claim validation.
- `zotero-reference-manager`: bridge Zotero Desktop/Web API to Article Machine projects for library search, BibTeX export, `drafts/references.bib`, citation keys, local attachments, and requested indexed full text.
- `deep-thinking-governor`: force assumption, alternative-hypothesis, premortem, steelman, and verification checks before strong decisions or claims.

## Layer 3: Modeling and Bench Work
- Use statistical, R/Python, computational discovery, RDKit, DiffDock, DeepChem, molecular dynamics, and scientific visualization skills for analysis.

## Layer 4: Synthesis and Dissemination
- `scientific-writing`: abstracts and manuscripts.
- `anti-ai-writing-governor`: scientific article structure, anti-generic prose audit, and evidence-preserving naturalization without detector bypass.
- `scientific-slides`: legacy slide narrative support.
- `latex-posters`: print-first poster fallback.
- `pptx-posters`: legacy PPTX poster fallback.
- `scientific-visualization`: camera-ready data figures.
- `scientific-schematics`: technical diagrams and study flowcharts.
- `conference-deliverable-router`: official entry point for deck, poster, abstract, handout, and submission pack.
- `conference-requirements-importer`: normalizes congress rules into `conference.yaml`.
- `conference-slides-html`: HTML-first deck generation with QA and PDF/PPTX export.
- `conference-posters-html`: HTML-first vertical/horizontal poster generation with QA and export.
- `visual-backend-router`: chooses diagram, chart, hero image, and asset backends.
- `playwright-layout-qa`: browser QA for screenshots, overflow, thumbnails, and PDF.
- `pptx-export-bridge`: editable PPTX fallback without making PPTX canonical.
- `submission-ops-playwright`: dry-run and confirmed portal submission operations.
- `speaker-notes-timing`: talk timing and speaker notes for 3/5/10/15 minute profiles.
- `paper-to-talk`: converts manuscripts or claim maps into oral narratives.
- `paper-to-poster`: converts manuscripts or claim maps into poster storyboards.
- `life-science-router`: routes biomedical discovery and evidence questions through the Life Science Research plugin inside Article Machine projects.
- `ngs-analysis-router`: routes BCL, FASTQ, BAM/CRAM, VCF, count matrices, and sequencing assays through the Life Sciences NGS Analysis plugin with preflight-first provenance.

## Congress Mode
When the user asks to prepare for a congress:
1. Import rules with `conference-requirements-importer` and `article-machine congress import`.
2. Route the output with `conference-deliverable-router`.
3. Build decks with `conference-slides-html`, `paper-to-talk`, and `speaker-notes-timing`.
4. Build posters with `conference-posters-html` and `paper-to-poster`.
5. Route visuals with `visual-backend-router`.
6. Validate layouts with `playwright-layout-qa`.
7. Export editable fallback files with `pptx-export-bridge`.
8. Use `submission-ops-playwright` for dry-run and explicitly confirmed submissions.

## Life Science Mode
When the user asks a biomedical discovery, target, variant, omics, drug, protein, pathway, microbiome, clinical, or dataset question:
1. Run `article-machine life-science plan <project_dir> --question "<question>"`.
2. Read `context/life_science/retrieval_plan.yaml`.
3. Use the selected Life Science Research plugin skills.
4. Save outputs under `evidence/life_science/`.
5. Promote only verified findings to `evidence/claim_map.jsonl`.

## World-Class Scientific Agent Layer
Use these skills naturally whenever the user's intent matches. Do not attempt the workflow manually first.

### Ideation and Design
- `hypothesis-tournament`: generate, criticize, rank, and evolve scientific hypotheses.
- `scientific-novelty-checker`: verify novelty before claims such as novel, first, or unprecedented.
- `experimental-design-planner`: convert a hypothesis into controls, endpoints, bias controls, and validation design.

### Reproducibility and Workflow Standards
- `ro-crate-provenance-export`: package runs with FAIR-style provenance, hashes, environment, commands, inputs, and outputs.
- `nextflow-pipeline-runner`: use scalable, containerized, HPC/cloud-ready workflows.
- `snakemake-pipeline-runner`: use readable Python/R-friendly rule-based workflows.
- `cwl-workflow-bridge`: export command workflows to vendor-neutral Common Workflow Language.

### Evidence Synthesis Quality
- `asreview-screening-bridge`: active-learning screening with audit trail and human reviewer control.
- `risk-of-bias-assistant`: route and support RoB 2, ROBINS-I, QUADAS-2, PROBAST, ROBIS, AMSTAR 2, and related tools.
- `grade-sof-table-builder`: build GRADE certainty and Summary of Findings tables.
- `protocol-registration-governor`: verify protocol registration, protocol freeze, amendments, and registry-to-manuscript consistency.
- `extraction-schema-governor`: design, pilot, and audit extraction forms before extracted data enters analysis or Evidence Lock.
- `living-review-monitor`: manage evidence freshness, update searches, preprint surveillance, and trial update snapshots.

### Source-Specific Retrieval
- `pubmed-database`: PubMed/NCBI/PMC wrapper for PMIDs, abstracts, full text, and citation matching.
- `clinical-trials-database`: ClinicalTrials.gov API v2 wrapper for NCT records, eligibility, status, phase, sponsor, and recruitment facts.
- `literature-search-europepmc`: Europe PMC open-access full text, citations, references, and PubMed fallback route.
- `literature-search-openalex`: OpenAlex executable wrapper for works, authors, institutions, topics, venues, and bibliometrics.
- `literature-search-arxiv`: arXiv preprint retrieval for non-biomedical preprints.
- `literature-search-biorxiv`: bioRxiv/medRxiv preprint retrieval with narrow date windows and preprint caveats.
- `semantic-scholar-citation-graph`: Semantic Scholar citation-neighborhood and recommendation checks.
- `crossref-unpaywall-resolver`: DOI metadata, Crossref, Crossmark, license, and Unpaywall open-access location checks.
- `opencitations-citation-audit`: open DOI-to-DOI citation checks through OpenCitations/COCI.
- `zotero-reference-manager`: local Zotero library bridge for curated references and full text already present in the user's library.

### Biomedical Discovery
- `openalex-literature-graph`: map scholarly metadata, topics, venues, authors, and citation neighborhoods.
- `open-targets-drug-targeting`: target-disease evidence, tractability, safety, known drugs, and prioritization.
- `chembl-bindingdb-miner`: ChEMBL/BindingDB/PubChem compound, activity, binding, and medchem triage.
- `alphafold-pdb-structure-router`: AlphaFold/PDB/UniProt structure selection, confidence, and docking readiness.
- `in-silico-validation-governor`: assign validation labels and prevent overclaiming for computational results.
- `intestinal-transplant-research`: route intestinal transplantation, intestinal failure, SBS/GLP-2, rejection biomarkers, intestinal machine perfusion, organoids, digital pathology, Brazilian implementation, and translational GI strategy through the right Article Machine gates.
- `datasus-research-engine`: route DATASUS/PySUS extraction, SIH/RD, SIM, SIA, SINASC, CNES, PNI, SIGTAP/CID validation, Parquet/DuckDB caches, cohorts, indicators, reports, and scientific QC.

### Evaluation and Red Team
- `deep-thinking-governor`: deliberate reasoning gate for high-stakes scientific choices, alternatives, assumptions, and residual risks.
- `agent-benchmark-harness`: benchmark the machine, skills, outputs, and regression cases before claiming quality.
- `scientific-red-team-reviewer`: stress-test claims, manuscripts, protocols, decks, posters, and discovery results.
- `tooluniverse-self-review`: build task-specific success criteria and score work against them.
- `anti-ai-writing-governor`: remove generic LLM style from scientific prose while preserving claims, numbers, limitations, citations, and disclosure duties.
- `manuscript-integrity-response-governor`: reviewer responses, rebuttals, claim-strength calibration, citation/reference integrity, and manuscript-wide consistency repair.
- `academic-office-deliverables`: editable DOCX/PPTX/LaTeX academic deliverables, reading reports, defense/group-meeting slides, Zotero-backed packages, and layout QA.
- `skill-upgrade-governor`: research, select, install, audit, and route new skills without unmanaged catalog bloat.

### Agent Navigation and Preservation
- `workspace-graph-navigator`: query and refresh the operational graph before root-level exploration.
- `project-entry-navigator`: force project selection and contract-file reading before scientific execution.
- `content-preservation-guardian`: require read-only inventory and migration manifests before moving, deleting, staging, or bulk-indexing content.

### Upstream Scientific Agent Skills Sync
- `experimental-design` and `statistical-power`: upstream study design and sample-size planning; use with the local `experimental-design-planner` gate.
- `nextflow`, `bulk-rnaseq`, `pathway-enrichment`, and `pacsomatic`: reproducible omics and workflow execution routes.
- `liteparse`, `paper-lookup`, `research-lookup`, and `exa-search`: document parsing, metadata lookup, and current web retrieval routes; still promote only verified findings into Evidence Lock.
- `arbor` and `autoskill`: optimization and skill-generation helpers; require benchmark evidence before claiming improvement.
- `onekgpd`, `bids`, `hugging-science`, and `tamarind`: specialized biomedical data/model routes; database or platform output is not final proof by itself.

### Curated ToolUniverse Layer
- `tooluniverse-literature-deep-research`: multi-source literature retrieval, disambiguation, citation expansion, and T1-T4 evidence grading.
- `tooluniverse-meta-analysis`: effect-size conversion, fixed/random effects pooling, heterogeneity, and forest-plot workflow.
- `tooluniverse-diagnostic-test-evaluation`: diagnostic accuracy, ROC/AUC, likelihood ratios, and post-test probability.
- `tooluniverse-epidemiological-analysis`: PECO, observational designs, confounding control, propensity scores, and sensitivity analysis.
- `tooluniverse-dataset-discovery`: dataset and cohort discovery across public repositories.
- `tooluniverse-clinical-guidelines`: authoritative clinical guideline retrieval and source hierarchy.
- `tooluniverse-clinical-trial-design`: endpoint, comparator, enrollment, and regulatory precedent feasibility.
- `tooluniverse-pharmacovigilance` and `tooluniverse-clinical-data-integration`: FAERS/FDA label/drug-safety evidence with spontaneous-reporting caveats.
- `tooluniverse-drug-target-validation`, `tooluniverse-variant-interpretation`, `tooluniverse-data-integration-analysis`, and `tooluniverse-drug-repurposing`: biomedical discovery support with hypothesis-generating limits.

### Plugin Gateways
- `life-science-router`: local gateway to the Life Science Research plugin; outputs stay under project evidence/context and require Evidence Lock before claims.
- `ngs-analysis-router`: local gateway to the Life Sciences NGS Analysis plugin; raw data stays read-only, installs/downloads require approval, and run envelopes belong under `analysis/ngs/`.
- `zotero-reference-manager`: local gateway to the Zotero plugin and pyzotero; references synchronize to `drafts/references.bib`, full text is only read when requested and legally/local available.

## Natural Skill Routing
- Use `article-machine skills route --query "<user request>"` when unsure which skills apply.
- Use `article-machine skills audit` after adding or editing skills.
- If a routed skill applies, read and use that skill before solving the task directly.

<!-- ARTICLE_MACHINE_REGISTRY_START -->
# Skill Registry

Generated from `skills/registry.json`; do not edit this section manually.

- `ab-test-setup` — hold — local unverified skill tree — `local-unverified`
- `academic-office-deliverables` — active — Article Machine curated layer — `workspace-2026-10-12`
- `ad-creative` — hold — local unverified skill tree — `local-unverified`
- `adaptyv` — hold — local unverified skill tree — `local-unverified`
- `aeon` — hold — local unverified skill tree — `local-unverified`
- `agent-benchmark-harness` — active — Article Machine curated layer — `workspace-2026-10-12`
- `ai-seo` — hold — local unverified skill tree — `local-unverified`
- `alphafold-pdb-structure-router` — active — Article Machine curated layer — `workspace-2026-10-12`
- `analytics-tracking` — hold — local unverified skill tree — `local-unverified`
- `anndata` — hold — local unverified skill tree — `local-unverified`
- `anti-ai-writing-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `arbor` — hold — local unverified skill tree — `local-unverified`
- `arboreto` — hold — local unverified skill tree — `local-unverified`
- `asreview-screening-bridge` — active — Article Machine curated layer — `workspace-2026-10-12`
- `astropy` — hold — local unverified skill tree — `local-unverified`
- `author-identity-resolver` — active — Article Machine curated layer — `workspace-2026-10-12`
- `autoskill` — hold — local unverified skill tree — `local-unverified`
- `benchling-integration` — hold — local unverified skill tree — `local-unverified`
- `bgpt-paper-search` — hold — local unverified skill tree — `local-unverified`
- `bids` — hold — local unverified skill tree — `local-unverified`
- `bilingual-scientific-writing` — active — Article Machine curated layer — `workspace-2026-10-12`
- `biopython` — hold — local unverified skill tree — `local-unverified`
- `bioservices` — hold — local unverified skill tree — `local-unverified`
- `bulk-rnaseq` — hold — local unverified skill tree — `local-unverified`
- `cellxgene-census` — hold — local unverified skill tree — `local-unverified`
- `chembl-bindingdb-miner` — active — Article Machine curated layer — `workspace-2026-10-12`
- `churn-prevention` — hold — local unverified skill tree — `local-unverified`
- `cirq` — hold — local unverified skill tree — `local-unverified`
- `citation-management` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `clinical-decision-support` — hold — local unverified skill tree — `local-unverified`
- `clinical-reports` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `clinical-trials-database` — active — Article Machine curated layer — `workspace-2026-10-12`
- `cobrapy` — hold — local unverified skill tree — `local-unverified`
- `cold-email` — hold — local unverified skill tree — `local-unverified`
- `competitor-alternatives` — hold — local unverified skill tree — `local-unverified`
- `conference-deliverable-router` — hold — local unverified skill tree — `local-unverified`
- `conference-posters-html` — hold — local unverified skill tree — `local-unverified`
- `conference-requirements-importer` — hold — local unverified skill tree — `local-unverified`
- `conference-slides-html` — hold — local unverified skill tree — `local-unverified`
- `consciousness-council` — hold — local unverified skill tree — `local-unverified`
- `content-preservation-guardian` — active — Article Machine curated layer — `workspace-2026-10-12`
- `content-strategy` — hold — local unverified skill tree — `local-unverified`
- `copy-editing` — hold — local unverified skill tree — `local-unverified`
- `copywriting` — hold — local unverified skill tree — `local-unverified`
- `crossref-unpaywall-resolver` — active — Article Machine curated layer — `workspace-2026-10-12`
- `customer-research` — hold — local unverified skill tree — `local-unverified`
- `cwl-workflow-bridge` — active — Article Machine curated layer — `workspace-2026-10-12`
- `dask` — hold — local unverified skill tree — `local-unverified`
- `database-lookup` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `database-retrieval-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `datamol` — hold — local unverified skill tree — `local-unverified`
- `datasus-research-engine` — hold — local unverified skill tree — `local-unverified`
- `deep-thinking-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `deepchem` — hold — local unverified skill tree — `local-unverified`
- `deeptools` — hold — local unverified skill tree — `local-unverified`
- `depmap` — hold — local unverified skill tree — `local-unverified`
- `dhdna-profiler` — hold — local unverified skill tree — `local-unverified`
- `diffdock` — hold — local unverified skill tree — `local-unverified`
- `dnanexus-integration` — hold — local unverified skill tree — `local-unverified`
- `docx` — hold — local unverified skill tree — `local-unverified`
- `email-sequence` — hold — local unverified skill tree — `local-unverified`
- `esm` — hold — local unverified skill tree — `local-unverified`
- `etetoolkit` — hold — local unverified skill tree — `local-unverified`
- `evidence-lock-hardener` — active — Article Machine curated layer — `workspace-2026-10-12`
- `exa-search` — hold — local unverified skill tree — `local-unverified`
- `experimental-design` — hold — local unverified skill tree — `local-unverified`
- `experimental-design-planner` — active — Article Machine curated layer — `workspace-2026-10-12`
- `exploratory-data-analysis` — hold — local unverified skill tree — `local-unverified`
- `extraction-schema-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `flowio` — hold — local unverified skill tree — `local-unverified`
- `fluidsim` — hold — local unverified skill tree — `local-unverified`
- `form-cro` — hold — local unverified skill tree — `local-unverified`
- `free-tool-strategy` — hold — local unverified skill tree — `local-unverified`
- `generate-image` — hold — local unverified skill tree — `local-unverified`
- `geniml` — hold — local unverified skill tree — `local-unverified`
- `geomaster` — hold — local unverified skill tree — `local-unverified`
- `geopandas` — hold — local unverified skill tree — `local-unverified`
- `get-available-resources` — hold — local unverified skill tree — `local-unverified`
- `gget` — hold — local unverified skill tree — `local-unverified`
- `ginkgo-cloud-lab` — hold — local unverified skill tree — `local-unverified`
- `glycoengineering` — hold — local unverified skill tree — `local-unverified`
- `grade-sof-table-builder` — active — Article Machine curated layer — `workspace-2026-10-12`
- `gtars` — hold — local unverified skill tree — `local-unverified`
- `guideline-router` — active — Article Machine curated layer — `workspace-2026-10-12`
- `histolab` — hold — local unverified skill tree — `local-unverified`
- `hugging-science` — hold — local unverified skill tree — `local-unverified`
- `hypogenic` — hold — local unverified skill tree — `local-unverified`
- `hypothesis-generation` — hold — local unverified skill tree — `local-unverified`
- `hypothesis-tournament` — active — Article Machine curated layer — `workspace-2026-10-12`
- `imaging-data-commons` — hold — local unverified skill tree — `local-unverified`
- `in-silico-validation-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `infographics` — hold — local unverified skill tree — `local-unverified`
- `intestinal-transplant-research` — hold — local unverified skill tree — `local-unverified`
- `iso-13485-certification` — hold — local unverified skill tree — `local-unverified`
- `labarchive-integration` — hold — local unverified skill tree — `local-unverified`
- `lamindb` — hold — local unverified skill tree — `local-unverified`
- `latchbio-integration` — hold — local unverified skill tree — `local-unverified`
- `latex-posters` — hold — local unverified skill tree — `local-unverified`
- `launch-strategy` — hold — local unverified skill tree — `local-unverified`
- `lead-magnets` — hold — local unverified skill tree — `local-unverified`
- `life-science-router` — active — Article Machine plugin bridge — `workspace-2026-10-12`
- `liteparse` — hold — local unverified skill tree — `local-unverified`
- `literature-review` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `literature-search-arxiv` — active — Article Machine curated layer — `workspace-2026-10-12`
- `literature-search-biorxiv` — active — Article Machine curated layer — `workspace-2026-10-12`
- `literature-search-europepmc` — active — Article Machine curated layer — `workspace-2026-10-12`
- `literature-search-openalex` — active — Article Machine curated layer — `workspace-2026-10-12`
- `living-review-monitor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `manuscript-integrity-response-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `markdown-mermaid-writing` — hold — local unverified skill tree — `local-unverified`
- `market-research-reports` — hold — local unverified skill tree — `local-unverified`
- `marketing-ideas` — hold — local unverified skill tree — `local-unverified`
- `marketing-psychology` — hold — local unverified skill tree — `local-unverified`
- `markitdown` — hold — local unverified skill tree — `local-unverified`
- `matchms` — hold — local unverified skill tree — `local-unverified`
- `matlab` — hold — local unverified skill tree — `local-unverified`
- `matplotlib` — hold — local unverified skill tree — `local-unverified`
- `medchem` — hold — local unverified skill tree — `local-unverified`
- `modal` — hold — local unverified skill tree — `local-unverified`
- `molecular-dynamics` — hold — local unverified skill tree — `local-unverified`
- `molfeat` — hold — local unverified skill tree — `local-unverified`
- `networkx` — hold — local unverified skill tree — `local-unverified`
- `neurokit2` — hold — local unverified skill tree — `local-unverified`
- `neuropixels-analysis` — hold — local unverified skill tree — `local-unverified`
- `nextflow` — hold — local unverified skill tree — `local-unverified`
- `nextflow-pipeline-runner` — active — Article Machine curated layer — `workspace-2026-10-12`
- `ngs-analysis-router` — active — Article Machine plugin bridge — `workspace-2026-10-12`
- `omero-integration` — hold — local unverified skill tree — `local-unverified`
- `onboarding-cro` — hold — local unverified skill tree — `local-unverified`
- `onekgpd` — hold — local unverified skill tree — `local-unverified`
- `open-notebook` — hold — local unverified skill tree — `local-unverified`
- `open-targets-drug-targeting` — active — Article Machine curated layer — `workspace-2026-10-12`
- `openalex-literature-graph` — active — Article Machine curated layer — `workspace-2026-10-12`
- `opencitations-citation-audit` — active — Article Machine curated layer — `workspace-2026-10-12`
- `opentrons-integration` — hold — local unverified skill tree — `local-unverified`
- `optimize-for-gpu` — hold — local unverified skill tree — `local-unverified`
- `pacsomatic` — hold — local unverified skill tree — `local-unverified`
- `page-cro` — hold — local unverified skill tree — `local-unverified`
- `paid-ads` — hold — local unverified skill tree — `local-unverified`
- `paper-lookup` — hold — local unverified skill tree — `local-unverified`
- `paper-to-poster` — hold — local unverified skill tree — `local-unverified`
- `paper-to-talk` — hold — local unverified skill tree — `local-unverified`
- `paperzilla` — hold — local unverified skill tree — `local-unverified`
- `parallel-web` — hold — local unverified skill tree — `local-unverified`
- `pathml` — hold — local unverified skill tree — `local-unverified`
- `pathway-enrichment` — hold — local unverified skill tree — `local-unverified`
- `paywall-upgrade-cro` — hold — local unverified skill tree — `local-unverified`
- `pdf` — hold — local unverified skill tree — `local-unverified`
- `peer-review` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `pennylane` — hold — local unverified skill tree — `local-unverified`
- `perplexity-search` — hold — local unverified skill tree — `local-unverified`
- `phylogenetics` — hold — local unverified skill tree — `local-unverified`
- `pi-agent` — hold — local unverified skill tree — `local-unverified`
- `playwright-layout-qa` — hold — local unverified skill tree — `local-unverified`
- `polars` — hold — local unverified skill tree — `local-unverified`
- `polars-bio` — hold — local unverified skill tree — `local-unverified`
- `popup-cro` — hold — local unverified skill tree — `local-unverified`
- `pptx` — hold — local unverified skill tree — `local-unverified`
- `pptx-export-bridge` — hold — local unverified skill tree — `local-unverified`
- `pptx-posters` — hold — local unverified skill tree — `local-unverified`
- `pricing-strategy` — hold — local unverified skill tree — `local-unverified`
- `primekg` — hold — local unverified skill tree — `local-unverified`
- `product-marketing-context` — hold — local unverified skill tree — `local-unverified`
- `programmatic-seo` — hold — local unverified skill tree — `local-unverified`
- `project-entry-navigator` — active — Article Machine curated layer — `workspace-2026-10-12`
- `protocol-registration-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `protocolsio-integration` — hold — local unverified skill tree — `local-unverified`
- `ptbr-article-writing` — active — Article Machine curated layer — `workspace-2026-10-12`
- `pubmed-database` — active — Article Machine curated layer — `workspace-2026-10-12`
- `pufferlib` — hold — local unverified skill tree — `local-unverified`
- `pydeseq2` — hold — local unverified skill tree — `local-unverified`
- `pydicom` — hold — local unverified skill tree — `local-unverified`
- `pyhealth` — hold — local unverified skill tree — `local-unverified`
- `pylabrobot` — hold — local unverified skill tree — `local-unverified`
- `pymatgen` — hold — local unverified skill tree — `local-unverified`
- `pymc` — hold — local unverified skill tree — `local-unverified`
- `pymoo` — hold — local unverified skill tree — `local-unverified`
- `pyopenms` — hold — local unverified skill tree — `local-unverified`
- `pysam` — hold — local unverified skill tree — `local-unverified`
- `pytdc` — hold — local unverified skill tree — `local-unverified`
- `pytorch-lightning` — hold — local unverified skill tree — `local-unverified`
- `pyzotero` — hold — local unverified skill tree — `local-unverified`
- `qiskit` — hold — local unverified skill tree — `local-unverified`
- `query-string-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `qutip` — hold — local unverified skill tree — `local-unverified`
- `rdkit` — hold — local unverified skill tree — `local-unverified`
- `referral-program` — hold — local unverified skill tree — `local-unverified`
- `research-grants` — hold — local unverified skill tree — `local-unverified`
- `research-lookup` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `retraction-integrity-checker` — active — Article Machine curated layer — `workspace-2026-10-12`
- `revops` — hold — local unverified skill tree — `local-unverified`
- `risk-of-bias-assistant` — active — Article Machine curated layer — `workspace-2026-10-12`
- `ro-crate-provenance-export` — active — Article Machine curated layer — `workspace-2026-10-12`
- `rowan` — hold — local unverified skill tree — `local-unverified`
- `sales-enablement` — hold — local unverified skill tree — `local-unverified`
- `scanpy` — hold — local unverified skill tree — `local-unverified`
- `schema-markup` — hold — local unverified skill tree — `local-unverified`
- `scholar-evaluation` — hold — local unverified skill tree — `local-unverified`
- `scienceskillscommon` — hold — local unverified skill tree — `local-unverified`
- `scientific-brainstorming` — hold — local unverified skill tree — `local-unverified`
- `scientific-critical-thinking` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `scientific-novelty-checker` — active — Article Machine curated layer — `workspace-2026-10-12`
- `scientific-red-team-reviewer` — active — Article Machine curated layer — `workspace-2026-10-12`
- `scientific-schematics` — hold — local unverified skill tree — `local-unverified`
- `scientific-slides` — hold — local unverified skill tree — `local-unverified`
- `scientific-visualization` — hold — local unverified skill tree — `local-unverified`
- `scientific-workflow-orchestrator` — active — Article Machine curated layer — `workspace-2026-10-12`
- `scientific-writing` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `scikit-bio` — hold — local unverified skill tree — `local-unverified`
- `scikit-learn` — hold — local unverified skill tree — `local-unverified`
- `scikit-survival` — hold — local unverified skill tree — `local-unverified`
- `scvelo` — hold — local unverified skill tree — `local-unverified`
- `scvi-tools` — hold — local unverified skill tree — `local-unverified`
- `seaborn` — hold — local unverified skill tree — `local-unverified`
- `semantic-scholar-citation-graph` — active — Article Machine curated layer — `workspace-2026-10-12`
- `seo-audit` — hold — local unverified skill tree — `local-unverified`
- `shap` — hold — local unverified skill tree — `local-unverified`
- `signup-flow-cro` — hold — local unverified skill tree — `local-unverified`
- `simpy` — hold — local unverified skill tree — `local-unverified`
- `site-architecture` — hold — local unverified skill tree — `local-unverified`
- `skill-upgrade-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `snakemake-pipeline-runner` — active — Article Machine curated layer — `workspace-2026-10-12`
- `social-content` — hold — local unverified skill tree — `local-unverified`
- `speaker-notes-timing` — hold — local unverified skill tree — `local-unverified`
- `stable-baselines3` — hold — local unverified skill tree — `local-unverified`
- `stage-audit-governor` — active — Article Machine curated layer — `workspace-2026-10-12`
- `statistical-analysis` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `statistical-power` — hold — local unverified skill tree — `local-unverified`
- `statsmodels` — hold — local unverified skill tree — `local-unverified`
- `submission-ops-playwright` — hold — local unverified skill tree — `local-unverified`
- `sympy` — hold — local unverified skill tree — `local-unverified`
- `tamarind` — hold — local unverified skill tree — `local-unverified`
- `tiledbvcf` — hold — local unverified skill tree — `local-unverified`
- `timesfm-forecasting` — hold — local unverified skill tree — `local-unverified`
- `tooluniverse-clinical-data-integration` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-clinical-guidelines` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-clinical-trial-design` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-data-integration-analysis` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-dataset-discovery` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-diagnostic-test-evaluation` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-drug-repurposing` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-drug-target-validation` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-epidemiological-analysis` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-literature-deep-research` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-meta-analysis` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-pharmacovigilance` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-self-review` — hold — ToolUniverse — `v1.3.1`
- `tooluniverse-variant-interpretation` — hold — ToolUniverse — `v1.3.1`
- `topic-ideation-tournament` — active — Article Machine curated layer — `workspace-2026-10-12`
- `torch-geometric` — hold — local unverified skill tree — `local-unverified`
- `torchdrug` — hold — local unverified skill tree — `local-unverified`
- `transformers` — hold — local unverified skill tree — `local-unverified`
- `treatment-plans` — hold — local unverified skill tree — `local-unverified`
- `umap-learn` — hold — local unverified skill tree — `local-unverified`
- `usfiscaldata` — hold — local unverified skill tree — `local-unverified`
- `uv` — hold — local unverified skill tree — `local-unverified`
- `vaex` — hold — local unverified skill tree — `local-unverified`
- `venue-templates` — active — K-Dense AI — `a1043ef544e3a100c28e70a736b6cf32554d0677`
- `visual-backend-router` — hold — local unverified skill tree — `local-unverified`
- `what-if-oracle` — hold — local unverified skill tree — `local-unverified`
- `workspace-graph-navigator` — active — Article Machine curated layer — `workspace-2026-10-12`
- `xlsx` — hold — local unverified skill tree — `local-unverified`
- `zarr-python` — hold — local unverified skill tree — `local-unverified`
- `zotero-reference-manager` — active — Article Machine plugin bridge — `workspace-2026-10-12`
<!-- ARTICLE_MACHINE_REGISTRY_END -->
