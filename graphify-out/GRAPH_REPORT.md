# Graph Report - C:\Users\Usuario-pc\Desktop\Doutorado  (2026-07-22)

## Corpus Check
- Root semantic graph was not run: the workspace is too broad and detection timed out. This is an operational navigation graph.

## Summary
- 979 nodes · 1995 edges · 8 communities
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 237 edges (avg confidence: 0.75)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Runtime Commands|Runtime Commands]]
- [[_COMMUNITY_Article Machine|Article Machine]]
- [[_COMMUNITY_Projects And Modes|Projects And Modes]]
- [[_COMMUNITY_Scientific Skills|Scientific Skills]]
- [[_COMMUNITY_Agent Docs|Agent Docs]]
- [[_COMMUNITY_Legacy Sources|Legacy Sources]]
- [[_COMMUNITY_Graphify Map|Graphify Map]]
- [[_COMMUNITY_Git Hygiene|Git Hygiene]]

## God Nodes (most connected - your core abstractions)
1. `Build context Task Packet` - 134 edges
2. `Read project protocol standards compute files` - 71 edges
3. `Critical Scientific Skills` - 66 edges
4. `article_machine.agent_skills` - 65 edges
5. `Article Machine Package` - 49 edges
6. `Runtime And Commands` - 47 edges
7. `article_machine.cli` - 40 edges
8. `Article Machine Projects` - 36 edges
9. `Agent Documentation` - 30 edges
10. `Git Hygiene` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Runtime And Commands` --exposes--> `article-machine analyze`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine anti-ai-audit`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine anti-ai-naturalize`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine benchmark`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine check`  [EXTRACTED]
  . → article_machine/cli.py

## Import Cycles
- None detected.

## Communities (8 total, 0 thin omitted)

### Community 0 - "Runtime Commands"
Cohesion: 0.20
Nodes (10): Doutorado Workspace, Runtime And Commands, .venv python -m article_machine, .venv python -m graphify, global python -m graphify, .venv python -m pytest, article_machine machine audit --strict, article_machine benchmark validate (+2 more)

### Community 1 - "Article Machine"
Cohesion: 0.04
Nodes (70): Article Machine Package, article_machine.__init__, Article Machine entrypoints and CLI, article_machine.__main__, article_machine.agent_skills, Skill routing and PT-BR style gates, article_machine.analysis, Analysis discovery and life-science planning (+62 more)

### Community 2 - "Projects And Modes"
Cohesion: 0.01
Nodes (234): Article Machine Projects, Article Machine Upgrade 2026, lane: evidence-writing, mode: bootstrap, type: thesis-chapter, article-machine-upgrade-2026/project.yaml, article-machine-upgrade-2026/protocol.yaml, article-machine-upgrade-2026/standards.yaml (+226 more)

### Community 3 - "Scientific Skills"
Cohesion: 0.01
Nodes (498): Critical Scientific Skills, hypothesis-tournament, hypothesis-tournament :: Hypothesis Tournament, hypothesis-tournament :: Workflow, hypothesis-tournament :: Output Contract, hypothesis-tournament :: Gates, scientific-novelty-checker, scientific-novelty-checker :: Scientific Novelty Checker (+490 more)

### Community 4 - "Agent Docs"
Cohesion: 0.03
Nodes (140): Agent Documentation, .agents/AGENTS.md, .agents/AGENTS.md :: Local Agent Control Plane, .agents/AGENTS.md :: Graph-First Rule, .agents/AGENTS.md :: Required Entry Flow, .agents/AGENTS.md :: Local Skills, .agents/AGENTS.md :: Hard Rules, .agents/GRAPH_FIRST.md (+132 more)

### Community 5 - "Legacy Sources"
Cohesion: 0.22
Nodes (9): Legacy And Raw Sources, legacy: Correção Orientador, legacy: Doutorado, legacy: Leitor de Artigos, legacy: PDFS DR ANDRÉ, legacy: REVISÃO LIGA, legacy: Revisões Sistemáticas, legacy: Submissão Final (+1 more)

### Community 6 - "Graphify Map"
Cohesion: 0.60
Nodes (5): Graphify Operational Map, scripts/generate_workspace_graph.py, graphify-out/GRAPH_REPORT.md, graphify-out/graph.html, graphify-out/graph.json

### Community 7 - "Git Hygiene"
Cohesion: 0.25
Nodes (8): Git Hygiene, local agent control plane; track only policy files and selected navigation skills, local virtual environment; never stage, pytest cache; generated, browser automation cache; generated, temporary workspace output, shared source intake; review before staging raw data, generated operational graph outputs

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **How should a new agent choose an active Article Machine project?**
  _Connects runtime commands, project modes, and required project files._
- **Which parts of the workspace are hygiene risks before committing?**
  _Highlights untracked/generated areas, legacy folders, and nested projects._
- **How do Graphify and Article Machine runtimes differ in this checkout?**
  _Shows the reproducible venv runtimes and the diagnosed global Graphify fallback._
- **How should GPT-5.6 Sol Ultra and subagents be used in this workspace?**
  _Routes model orchestration to the project-scoped Codex roles, strict audit, and benchmark gate._
- **Which skills are mandatory before strong scientific claims?**
  _Bridges critical scientific skills to the Article Machine gates._
- **When should a user request route to Zotero, Life Science Research, NGS, or deep-thinking gates?**
  _Shows plugin gateways, expected project artifacts, and the local routing surface._

## Agent Operating Flow
1. Read docs/AGENT_START_HERE.md
2. Read .agents/AGENTS.md
3. Run article_machine machine audit --strict
4. Open graphify-out/GRAPH_REPORT.md
5. Query graph before broad navigation
6. Select or create projects/<project_id>
7. Read project protocol standards compute files
8. Run article_machine skills route
9. Build context Task Packet
10. Validate Evidence Lock before ready claims

## Plugin Gateway Map
- `deep-thinking-governor` -> Decision quality gate for assumptions alternatives premortems -> decision notes residual-risk summaries
- `zotero-reference-manager` -> Zotero plugin local library and attachment API -> project drafts/references.bib
- `life-science-router` -> Life Science Research plugin router -> project evidence/life_science outputs
- `ngs-analysis-router` -> Life Sciences NGS Analysis plugin router -> project analysis/ngs run envelopes

## Installed Navigation Skills
- `workspace-graph-navigator` -> `skills/workspace-graph-navigator/SKILL.md`
- `project-entry-navigator` -> `skills/project-entry-navigator/SKILL.md`
- `content-preservation-guardian` -> `skills/content-preservation-guardian/SKILL.md`

## Detailed Navigation Layers
- Markdown sections indexed: 100
- Project contract files indexed: 68
- Project artifact areas indexed: 131
- Skill instruction sections indexed: 426
- Navigation/preservation skills installed: 3
- Project-scoped Codex agent roles indexed: 3
- Read-only Codex benchmark profiles indexed: 2

## Generation Provenance
- Git HEAD: `50430f080f9d825c7dfab94f0522c9dd4e6ed340`
- Dirty worktree at generation: `true`
- Porcelain status entries at generation: 76

## Natural Language Gateway Phrases
These nodes make Portuguese and operational user phrasing easier for `graphify query` to match.
- `pergunta: agente novo navegar workspace doutorado` -> workspace-graph-navigator, project-entry-navigator, Read docs/AGENT_START_HERE.md, Read .agents/AGENTS.md, Open graphify-out/GRAPH_REPORT.md, Query graph before broad navigation, Select or create projects/<project_id>
- `regra: usar graph mesmo sem usuario pedir quando precisar` -> Read .agents/AGENTS.md, Query graph before broad navigation, workspace-graph-navigator, graphify-out/GRAPH_REPORT.md
- `pedido: atualizar graph melhorar fluidez graph html` -> workspace-graph-navigator, scripts/generate_workspace_graph.py, graphify-out/graph.html, graphify-out/GRAPH_REPORT.md
- `pedido: escolher projeto ativo article machine` -> project-entry-navigator, Select or create projects/<project_id>, Article Machine Projects, .venv python -m article_machine
- `pedido: reorganizar sem comprometer conteudo bruto` -> content-preservation-guardian, Legacy And Raw Sources, Git Hygiene
- `pedido: rotear skill para pergunta cientifica` -> Run article_machine skills route, article_machine skills route, Critical Scientific Skills
- `pedido: validar evidence lock antes de draft pronto` -> Validate Evidence Lock before ready claims, article_machine.evidence, article_machine.zero_trust
- `pedido: zotero referencias bibtex biblioteca local` -> zotero-reference-manager, Zotero plugin local library and attachment API, project drafts/references.bib
- `pedido: life science pesquisa biomedica descoberta` -> life-science-router, Life Science Research plugin router, project evidence/life_science outputs
- `pedido: ngs fastq bam vcf sequenciamento` -> ngs-analysis-router, Life Sciences NGS Analysis plugin router, project analysis/ngs run envelopes
- `pedido: pensamento profundo decisao forte hipotese fragil` -> deep-thinking-governor, Decision quality gate for assumptions alternatives premortems, decision notes residual-risk summaries
- `pedido: artigo pt br abnt vancouver sem cara de ia` -> ptbr-article-writing, anti-ai-writing-governor, article_machine.ptbr_style
- `pedido: melhorar maquina com gpt 5.6 sol ultra multiagente` -> Codex project configuration, Codex role: workspace-explorer, Codex role: scientific-reviewer, Codex role: verification-runner, Codex read-only profile: xhigh-baseline.config, Codex read-only profile: ultra-benchmark.config, skill-upgrade-governor, agent-benchmark-harness, article_machine benchmark validate, article_machine machine audit --strict

## Legacy And Hygiene Map
Legacy folders requiring manual triage before moves or staging:
- `Correção Orientador/`
- `Doutorado/`
- `Leitor de Artigos/`
- `PDFS DR ANDRÉ/`
- `REVISÃO LIGA/`
- `Revisões Sistemáticas/`
- `Submissão Final/`
- `NMA_OSA_VPI/`

Git hygiene targets:
- `.agents/`: local agent control plane; track only policy files and selected navigation skills
- `.venv/`: local virtual environment; never stage
- `.pytest_cache/`: pytest cache; generated
- `.playwright-osf/`: browser automation cache; generated
- `tmp/`: temporary workspace output
- `sources/`: shared source intake; review before staging raw data
- `graphify-out/`: generated operational graph outputs


## Operational Limitations
- Operational graph only; full root semantic graph timed out and would mix caches, PDFs, and raw data.
- Edges marked INFERRED are navigation/risk inferences, not scientific evidence.
- Use project-specific graphify runs for manuscript evidence graphs.

## Graph HTML Fluidity
- `graph.html` uses a fixed community layout with physics off by default, so pan/zoom/search stays responsive.
- Non-hub labels are hidden by default; use the Labels toggle when inspecting a focused area.
- Community filtering is intentional: agents should narrow to the active operating layer instead of scanning every node at once.
