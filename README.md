# Article Machine

October 2026: version 0.3.0 adds Sol medium/Luna coordination and scientific
workflows in English and PT-BR. Start with [the workflow guide](docs/SCIENTIFIC_WORKFLOWS.md)
and [migration notes](docs/MIGRATION_0_3.md). `workflow plan`, `workflow audit-language`
and `plugins audit` expose the new operational layer. Project-specific scientific
acceptance and independent review remain required for final results.

Scientific OS for agent-native research, evidence synthesis, meta-analysis, thesis drafting, and computational discovery.

## Start here for agents

This checkout should be operated from `D:\Usuario-pc\Projetos\Doutorado`.
Use the local venv for Article Machine:

```powershell
.\.venv\Scripts\python.exe -m article_machine --help
.\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict
.\.venv\Scripts\python.exe -m pytest
```

Do not assume the `article-machine` console script is on PATH. It exists only
after an editable install; `python -m article_machine` is the reliable command.

For the workspace map, the generated project dashboard, and the no-deletion
policy, read `docs/INDICE_DO_WORKSPACE.md`, `docs/ESTADO_DOS_PROJETOS.md` and
`docs/ORGANIZACAO_E_LIMPEZA.md`.

For workspace navigation, generate the operational graph:

```powershell
.\.venv\Scripts\python.exe scripts\generate_workspace_graph.py
```

Then open `graphify-out/graph.html` or read `graphify-out/GRAPH_REPORT.md`.
For a deterministic handoff, read `docs/AGENT_OPERATION_MAP.md` before changing
evidence, analysis, discovery, or drafts.

Also read `.agents/AGENTS.md`. It is the local control plane that tells agents
to query the graph first for workspace navigation, architecture, file
relationships, project selection, skill routing, cleanup, staging, unknown
paths, and handoff even when the user does not explicitly mention the graph.
Read `.codex/README.md` for the project-scoped model and subagent policy. It
keeps Ultra as an explicit session choice and assigns bounded read-only work to
cheaper roles; model capability never bypasses scientific or reproducibility
gates.

## What this implements
- Project-scoped scientific runtime in `article_machine/`
- Agent-facing CLI via `article-machine`
- Standards router for international reporting/checklist baselines
- Evidence Lock for claim-to-source-to-reference validation
- R Bridge with preflight, run manifests, logs, and `sessionInfo()`
- Review Trinity with methodological, quantitative, and editorial gates
- Task Packets and project briefs for compact context handoff
- Conference deliverables for HTML-first slides, posters, abstracts, handouts, submission packs, QA, PDF/PPTX export, and Playwright hooks
- Life Science Research integration for biomedical skill routing across targets, variants, omics, structures, compounds, clinical trials, literature, and public datasets
- Natural skill routing for hypothesis tournaments, novelty checks, deep-thinking gates, Zotero reference management, Life Science Research plugin routing, NGS analysis routing, experimental design, provenance, workflow engines, active-learning screening, risk of bias, GRADE, source-specific retrieval APIs, protocol registration, extraction schemas, living searches, drug-target evidence, chemistry mining, structure routing, in silico validation, benchmarking, and scientific red-team review

## Project layout
Each project lives under `projects/<project_id>/` and includes:

- `project.yaml`
- `protocol.yaml`
- `standards.yaml`
- `compute.yaml`
- `sources/`
- `context/`
- `evidence/`
- `analysis/`
- `drafts/`
- `reviews/`
- `figures/`
- `deliverables/<slug>/`
- `.machine/runs/<run_id>/manifest.json`

## CLI
```bash
article-machine init "Gut Twin Discovery" --type intestinal-digital-twin
article-machine preflight projects/gut-twin-discovery
article-machine context build projects/gut-twin-discovery --mode discovery --hypothesis "Model perfusion collapse under ischemia."
article-machine draft projects/gut-twin-discovery
article-machine review projects/gut-twin-discovery
```

## Life Science Research
```bash
article-machine life-science catalog
article-machine life-science plan projects/gut-twin-discovery --question "Map microbiome, metabolite, and epithelial datasets for an in silico intestine model."
```

The command writes `context/life_science/retrieval_plan.yaml`, `context/life_science/agent_retrieval_packet.md`, and `evidence/life_science/README.md`. Use these artifacts to guide Life Science Research plugin lookups before promoting checked findings into `evidence/claim_map.jsonl`.

## Skill Routing
```bash
article-machine skills catalog
article-machine skills route --query "Discover drug targets with ChEMBL, AlphaFold, docking, and no in silico overclaiming."
article-machine skills audit
```

For navigation and safe handoff, route through `workspace-graph-navigator`, `project-entry-navigator`, and `content-preservation-guardian` before exploring the root, choosing a project, staging files, moving legacy material, or indexing raw content.

Agents should use the routed skills before doing the task manually. The world-class layer includes skills for hypothesis generation, novelty checks, experimental design, FAIR/RO-Crate provenance, Nextflow/Snakemake/CWL, active-learning screening, risk of bias, GRADE SoF tables, provider-specific literature and registry APIs, protocol registration, extraction schemas, living-review monitoring, OpenAlex, Open Targets, ChEMBL/BindingDB, AlphaFold/PDB, in silico validation, anti-AI-style manuscript naturalization without detector bypass, benchmarking, and red-team review.

The local catalog also syncs selected upstream Scientific Agent Skills for article creation and scientific computing: `experimental-design`, `statistical-power`, `liteparse`, `paper-lookup`, `research-lookup`, `nextflow`, `bulk-rnaseq`, `pathway-enrichment`, `bids`, `onekgpd`, `tamarind`, `arbor`, and `autoskill`. These skills expand execution coverage; they do not weaken Article Machine gates. Evidence Lock, benchmark evidence, stage audit, and Review Trinity remain the authority before a manuscript, report, deck, or submission is called ready.

The external-provider layer adds Google DeepMind Science Skills wrappers for `pubmed-database`, `clinical-trials-database`, `literature-search-europepmc`, `literature-search-openalex`, `literature-search-arxiv`, and `literature-search-biorxiv`; curated ToolUniverse workflows for deep literature research, meta-analysis, diagnostic accuracy, epidemiology, datasets, clinical guidelines, trial design, pharmacovigilance, target validation, variant interpretation, clinical data integration, biological annotation, drug repurposing, and self-review; plus local governors for Crossref/Unpaywall, Semantic Scholar, OpenCitations, protocol registration, extraction schemas, living reviews, reviewer-response/manuscript-integrity work, academic Office/LaTeX deliverables, and skill upgrades. These are execution aids, not final proof: source excerpts, manifests, Evidence Lock, and Review Trinity still decide readiness.

The plugin gateway layer adds `zotero-reference-manager` for local Zotero/BibTeX/reference syncing and requested indexed full text, `life-science-router` for Life Science Research plugin orchestration, `ngs-analysis-router` for Life Sciences NGS Analysis routing and preflight-first sequencing workflows, and `deep-thinking-governor` for assumptions, alternatives, premortem/steelman/red-team checks, and decision summaries before strong claims. These gateways do not make the system perfect; benchmark evidence, Evidence Lock, preflight artifacts, and residual-risk notes still decide readiness.

For scientific prose that sounds AI-generated, use:

```bash
article-machine style anti-ai-audit drafts/manuscript.md --output reviews/anti_ai_style.md --json-output reviews/anti_ai_style.json --strict
article-machine style anti-ai-naturalize drafts/manuscript.md --output drafts/manuscript.naturalized.md --json-output reviews/anti_ai_naturalize.json
```

These commands are for accountable authorship and structure, not detector evasion.

## Conference Deliverables
```bash
article-machine congress import projects/gut-twin-discovery --source "Oral presentation. Duration: 5 minutes. Maximum 6 slides." --kind deck --slug congress-oral
article-machine deck plan projects/gut-twin-discovery/deliverables/congress-oral
article-machine deck build projects/gut-twin-discovery/deliverables/congress-oral
article-machine deck qa projects/gut-twin-discovery/deliverables/congress-oral
article-machine deck export projects/gut-twin-discovery/deliverables/congress-oral
```

Each deliverable includes `conference.yaml`, `storyboard.yaml`, `theme.yaml`, `qa_report.json`, `manifest.json`, `layouts/`, `exports/`, `qa/`, and `submission/`. HTML is the canonical source; PDF and PPTX are exports.

## Standards routing
- `systematic-review` -> `PRISMA`, `GRADE`, `ROBIS`, `AMSTAR 2`
- `network-meta-analysis` -> `PRISMA-NMA`, `GRADE`
- `diagnostic-study` -> `STARD`, `QUADAS-2`
- `clinical-trial` -> `CONSORT`
- `observational-study` -> `STROBE`
- `animal-study` -> `ARRIVE`
- `prediction-model` -> `TRIPOD`
- `health-economics` -> `CHEERS`

## Notes
- `drug-discovery` and `intestinal-digital-twin` are explicitly treated as `hypothesis-generating`.
- If `Rscript` is not available, the preflight gate blocks R-dependent execution early with a setup message.
- For prompt-level operating rules, read `AGENTS.md` and `docs/ARTICLE_MACHINE_AGENT_PLAYBOOK.md` before doing scientific work.
- For workspace cleanup policy, read `docs/WORKSPACE_REORG_PLAN.md`; do not move legacy source folders without a migration manifest.
