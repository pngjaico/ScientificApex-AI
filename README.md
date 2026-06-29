# Article Machine

Scientific OS for agent-native research, evidence synthesis, meta-analysis, thesis drafting, and computational discovery.

## Start here for agents

This checkout should be operated from `C:\Users\Usuario-pc\Desktop\Doutorado`.
Use the local venv for Article Machine:

```powershell
.\.venv\Scripts\python.exe -m article_machine --help
.\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root .
.\.venv\Scripts\python.exe -m pytest
```

Do not assume the `article-machine` console script is on PATH. It exists only
after an editable install; `python -m article_machine` is the reliable command.

For workspace navigation, generate the operational graph:

```powershell
python scripts\generate_workspace_graph.py
```

Then open `graphify-out/graph.html` or read `graphify-out/GRAPH_REPORT.md`.

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
- Natural skill routing for hypothesis tournaments, novelty checks, experimental design, provenance, workflow engines, active-learning screening, risk of bias, GRADE, drug-target evidence, chemistry mining, structure routing, in silico validation, benchmarking, and scientific red-team review

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

Agents should use the routed skills before doing the task manually. The world-class layer includes skills for hypothesis generation, novelty checks, experimental design, FAIR/RO-Crate provenance, Nextflow/Snakemake/CWL, active-learning screening, risk of bias, GRADE SoF tables, OpenAlex, Open Targets, ChEMBL/BindingDB, AlphaFold/PDB, in silico validation, benchmarking, and red-team review.

The local catalog also syncs selected upstream Scientific Agent Skills for article creation and scientific computing: `experimental-design`, `statistical-power`, `liteparse`, `paper-lookup`, `research-lookup`, `nextflow`, `bulk-rnaseq`, `pathway-enrichment`, `bids`, `onekgpd`, `tamarind`, `arbor`, and `autoskill`. These skills expand execution coverage; they do not weaken Article Machine gates. Evidence Lock, benchmark evidence, stage audit, and Review Trinity remain the authority before a manuscript, report, deck, or submission is called ready.

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
