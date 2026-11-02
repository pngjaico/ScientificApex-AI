# Guide to the scientific machine

**What it does, how to choose the next step, and where human review remains mandatory**  
State checked on November 2, 2026.

## In one sentence

Article Machine organizes scientific projects, enforces process gates, routes tasks to local skills, and prepares reproducible analyses and documents. A command, available skill, passing test, or polished text does not by itself establish validated scientific evidence.

The components have different roles:

- **Article Machine** maintains projects, contracts, workflow modes, sources, claims, manifests, and local checks.
- **Skills** are specialized instructions selected by intent. Routing helps find instructions; it does not mean a task was performed or an external service is connected.
- **Graphify** helps navigate code and documents. The operational graph is not scientific evidence.
- **Connectors and plugins** may query local or remote services. Their use depends on availability, authorization, privacy, and sometimes cost.
- **Templates under `modelos/`** are blank starting points. They are not approved protocols, real registrations, completed analyses, or ready manuscripts.

## The usual path from a request to a reviewable package

### 1. Select the project and read its contracts

All work involving evidence, analysis, discovery, manuscripts, or conference material starts under `projects/<id>/`. Select or create the project and read `project.yaml`, `protocol.yaml`, `standards.yaml`, and `compute.yaml`. They describe the project, its current mode, declared protocol, and required environments and standards.

Use `project-entry-navigator` to enter or resume a project and `scientific-workflow-orchestrator` to break complex work into stages. Build or refresh a Task Packet before handling data or claims. `bootstrap` permits planning; it does not permit skipping directly to analysis.

### 2. Define the question, design, and protocol

Define the question, population, unit of analysis, outcomes, horizon, estimand, criteria, and analysis plan before examining results. Use `experimental-design-planner` for design and endpoints; `hypothesis-tournament` for competing hypotheses; `scientific-novelty-checker` for novelty; and `deep-thinking-governor` for high-risk decisions or fragile claims.

Planning and freezing a protocol in `bootstrap`/`protocol-freeze` are allowed before final registration. Local policy requires **a final, human-reviewed PROSPERO or OSF registration before scientific work begins**, including formal searches/corpus building, screening, extraction, analysis, discovery, or scientific drafting. This local gate is stricter than editorial policies that may accept later registration. Trials may also require a specific public trial registry and ethics/regulatory approval.

Use `protocol-registration-governor` and the paired questionnaires under `modelos/registro_de_protocolo/`. For health reviews, check current PROSPERO eligibility; if the review is not eligible or the design is out of scope, consider OSF. An OSF project page is not a registration. A draft or pending submission is also insufficient.

The `registry register` command **only declares metadata locally** and leaves status `declared-unverified`; it does not submit anything to PROSPERO/OSF. Before `registry verify`, a named human reviewer checks the final registry record, URL/ID, state, dated local snapshot and hash, frozen protocol, and the `scientific_work_not_started_before_registration` declaration. Local verification checks document consistency and hashes; **it does not contact the provider to authenticate external content**. Never invent IDs, timestamps, or attestations.

> The three scientific templates were updated to require registration before scientific execution and documentary verification. They remain in `bootstrap` with draft protocols; presence in the repository does not mean any project is registered.

### 3. Search and preserve sources

With the appropriate registration and gate in place, compile the search with `query-string-governor` and plan caching, limits, hashes, and replay with `database-retrieval-governor`. Source-specific skills include `pubmed-database`, `literature-search-europepmc`, `literature-search-openalex`, `crossref-unpaywall-resolver`, `clinical-trials-database`, `semantic-scholar-citation-graph`, and `opencitations-citation-audit`.

Store full search strings, database/platform, dates, filters, results, and identifiers in `sources/` and project manifests. PubMed, Europe PMC, Crossref, and other databases provide records and metadata; that alone does not prove a manuscript claim. Public trial records help verify a trial but do not replace published evidence or methodological review.

For bibliography, RIS/BibTeX files, `references.bib`, and attachments, use `zotero-reference-manager`. Do not use it to bypass paywalls. Workspace documentation has recorded that the local Zotero API was unavailable; check readiness again before relying on it. Exact DOI/PMID deduplication still needs human checks for versions, similar titles, and multiple reports of one study; semantic deduplication has not been demonstrated.

Five on-demand catalogs: K-Dense (biomedicine), DenDen047 (computing/physics), Orchestra-Research (engineering/AI), Imbad0202 (planning/writing), and InternScience (sources). `catalogos-cientificos-sob-demanda` selects by need; verify origin/license. It does not install or authorize uploads/spending.

### 4. Screen, extract, and critically appraise

For reviews, `asreview-screening-bridge` can prioritize screening but does not replace two reviewers. `extraction-schema-governor` structures extraction; `risk-of-bias-assistant` supports design-specific appraisal and `grade-sof-table-builder` organizes certainty by outcome. The team decides and records conflicts and justifications.

### 5. Analyze without losing units, dependence, or uncertainty

For medical meta-analysis in R, use the active local skill `meta-analise-medica` with risk-of-bias, GRADE, and `statistical-analysis` skills. Confirm compatible population, comparator, outcome, scale, direction, and horizon before pooling. Do not combine comparative effects with raw proportions. Proportion meta-analysis requires a compatible prevalence/incidence question, denominators, and time periods. Do not treat multiple arms, times, or outcomes from one study as independent.

Choose the model based on the question, not heterogeneity p-value/I². Justify REML and HKSJ, especially with few studies; small k makes heterogeneity, τ², and intervals imprecise. Run sensitivity analyses and GRADE by outcome.

For other quantitative data, `statistical-analysis` supports test selection, assumptions, effect sizes, and intervals; `scientific-visualization` supports figures. Define the experimental unit, design, estimand, missingness, multiplicity, and analysis before results. Use R/`renv` and `run-r` when project contracts require R; Quarto renders a report but does not review scientific validity.

For clinical prediction, use `metodos-ml-clinico` and `in-silico-validation-governor`. Compare against simple regression/statistical baselines. Keep each patient in one partition; use nested validation for internal tuning/performance estimation, and temporal or center splits when the question concerns transport. Fit imputation, feature selection, balancing, hyperparameters, and calibration only within training data. Report discrimination, calibration, intervals, and sample composition. AUC alone does not establish clinical utility. External validation must use truly independent data. PyTorch is optional and on demand.

**TRIPOD+AI is a reporting guideline. PROBAST+AI assesses quality, risk of bias, and applicability.** Neither makes a model safe for clinical decisions. Predictive performance does not establish causality, benefit, or safety.

### 6. Discover biomedical evidence with cautious labels

For targets, omics, variants, proteins, pathways, trials, or public datasets, use `life-science-router` and first create the local Life Science Research plan. Discovery skills such as Open Targets, ChEMBL/BindingDB, AlphaFold, and ToolUniverse provide leads and metadata for investigation. Save outputs under `evidence/life_science/`, check original sources and validation labels, and only then promote claims into `evidence/claim_map.jsonl`.

Computational results, docking, models, database queries, or plugin outputs begin as **hypothesis-generating** until independently validated. For FASTQ/BAM/VCF and NGS workflows, use `ngs-analysis-router` and run preflight; human data must not be uploaded to the cloud without explicit permission and appropriate governance.

### 7. Write traceable claims in PT-BR and English

Every new scientific/editorial deliverable has paired versions under `portugues/` and `ingles/`, using the same Portuguese base filename. Write natural Brazilian Portuguese with `ptbr-article-writing`; use `bilingual-scientific-writing` to draft natively in each language and `workflow audit-language` as a lexical check. A human must still review meaning, numbers, IDs, citations, uncertainty, and claim strength across both versions.

Use `anti-ai-writing-governor` without removing limitations, citations, or AI disclosure. Claims belong in `evidence/claim_map.jsonl` and use `{{claim:claim-id}}`; synchronize `drafts/references.bib`. A plan is not completed work.

### 8. Organize the journal package and complete review

`publicacao-medica-organizada` organizes a version under `projects/<id>/publicacoes/<revista>/<identificador>/`, with nine numbered areas: protocol, search/references, authorized data, analyses, tables, figures, manuscript, review, and submission. `organizar_publicacoes.py` defaults to dry-run; `--criar` creates empty folders and a manifest without moving files. Example preview: `.\.venv\Scripts\python.exe projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/organizar_publicacoes.py --projeto <id> --revista <slug> --identificador v01 --raiz . --dry-run`. Templates are under `modelos/publicacao_em_revistas/`; `venue-templates` and journal profiles support checks against current official journal instructions, which can change.

Use `peer-review`, `manuscript-integrity-response-governor`, `scientific-critical-thinking`, and `scientific-red-team-reviewer` as appropriate. Run Evidence Lock before calling a draft ready and Review Trinity before submission. `academic-office-deliverables` can prepare editable DOCX/PPTX/LaTeX with layout QA. A filled template is not editorial approval.

For conferences, the pipeline stores deliverables under `deliverables/<slug>/`; HTML is canonical for decks and posters. A storyboard may only use claims approved in the claim map. `conference-deliverable-router` is currently `hold` in the registry and requires a status review. Run QA before export. Portal submission remains manual and requires explicit confirmation and a fresh Playwright snapshot.

## Functions and limits

The machine structures projects, validates contracts, prepares searches, organizes references, runs authorized scripts, and renders documents. The team confirms protocol and registration, authorizes connectors/transfers, checks sources, performs duplicate screening/extraction, judges RoB/GRADE, validates analyses, approves claims, ethics, authorship, and submission. Progress stops when final registration, contracts, data/environment, independent validation, or required reviews are missing.

## Available and verified commands

Use the machine's Python from D. CLI and subcommand help was checked in this local version. Values in `<...>` are placeholders; do not copy fake IDs.

```powershell
.\.venv\Scripts\python.exe -m article_machine --help
.\.venv\Scripts\python.exe -m article_machine skills route --query "meta-análise médica em R"
.\.venv\Scripts\python.exe -m article_machine workflow plan projects/<id> --query "<question>" --language pt-BR
.\.venv\Scripts\python.exe -m article_machine preflight projects/<id>
.\.venv\Scripts\python.exe -m article_machine context build projects/<id> --mode <mode> --hypothesis "<hypothesis>"
.\.venv\Scripts\python.exe -m article_machine registry register projects/<id> --registry OSF --id <real-id> --url <final-registration-url> --registered-at <real-ISO-8601>
.\.venv\Scripts\python.exe -m article_machine registry verify projects/<id> --record projects/<id>/evidence/protocol_registration/<reviewed-record>.json
.\.venv\Scripts\python.exe -m article_machine run-r projects/<id> projects/<id>/analysis/<script-aprovado>.R
.\.venv\Scripts\python.exe -m article_machine workflow audit-language projects/<id> --language en --draft drafts/ingles/<file>.md --reference drafts/portugues/<file>.md
.\.venv\Scripts\python.exe -m article_machine submit dry-run projects/<id>/deliverables/<slug>
```

## Local evidence checked

- Meta-analysis/ML models are in `bootstrap`, with an empty question and draft protocol. They are scaffolds, not registered studies or executed clinical data.
- `modelos/publicacao_em_revistas/registro_renderizacao.json` records 24 structurally valid DOCX files. Human layout review is SKIPPED and content remains unfilled template material.
- Statistics/Quarto demonstrations are synthetic, not a complete systematic review, cohort validation or proof of clinical benefit.
- The BYOK candidate at `projects/article-machine-governance-2026/analysis/continuacao-2026-11-02/byok/upstream_ro/` is pinned to `6a55f5ce6f4bd9ac7ff75d01ec20d7f27073a9f0`. Focused tests (69 server + 30 web) and typechecks passed; the complete workspace suite reported 307 passed/1 skipped (Windows symlink). No model call or service startup occurred; npm downloaded dependencies without paid API use. Frontend `npm ci` timed out although its offline dependency inventory/tests subsequently passed. Next.js build and startup were omitted. `launcher_candidato.cmd` only diagnoses dependencies; `iniciar_candidato.cmd` requires `--start` and typed confirmation, uses loopback 8101/3101, and its startup branch was not executed. The starter may install packages, create local settings and download skills; review those effects before use. It does not update or replace the historical C: installation.

## Limits that automation does not remove

An existing credential is not permission to call a paid API. An installed skill does not prove a plugin is connected. A planned search is not a completed search. A local hash does not authenticate an external registration. DOCX/Quarto rendering is not visual or methodological review. Synthetic tests do not validate patients, hospitals, or clinical use. An AI detector does not authorize hiding disclosure. Nothing is accepted or submitted automatically. The study team remains responsible for ethics, privacy, protocol, methods, interpretation, and publication decisions.
