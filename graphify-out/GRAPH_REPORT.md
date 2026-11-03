# Graph Report - D:\Usuario-pc\Projetos\Doutorado  (2026-11-03)

> **Start here:** [`graphify-out/LEIA-ME.md`](LEIA-ME.md) maps every generated file.
> The agent quickstart and query recipes are at the end of this report.

## Corpus Check
- Root semantic graph was not run: the workspace is too broad and detection timed out. This is an operational navigation graph.

## Summary
- 1343 nodes · 2700 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 273 edges (avg confidence: 0.75)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Runtime Commands
- Article Machine
- Projects And Modes
- Scientific Skills
- Agent Docs
- Legacy Sources
- Graphify Map
- Git Hygiene

## God Nodes (most connected - your core abstractions)
1. `Build context Task Packet` - 155 edges
2. `Article Machine Package` - 102 edges
3. `Runtime And Commands` - 95 edges
4. `Read project protocol standards compute files` - 83 edges
5. `article_machine.cli` - 82 edges
6. `Critical Scientific Skills` - 73 edges
7. `article_machine.agent_skills` - 72 edges
8. `Agent Documentation` - 56 edges
9. `Article Machine Projects` - 47 edges
10. `Graphify Operational Map` - 38 edges

## Surprising Connections (you probably didn't know these)
- `Runtime And Commands` --exposes--> `article-machine aggregate`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine analyze`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine anti-ai-audit`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine anti-ai-naturalize`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine audit-equator`  [EXTRACTED]
  . → article_machine/cli.py

## Import Cycles
- None detected.

## Communities (8 total, 1 thin omitted)

### Community 0 - "Runtime Commands"
Cohesion: 0.11
Nodes (20): Doutorado Workspace, Runtime And Commands, .venv python -m article_machine, .venv python -m graphify, global python -m graphify, .venv python -m pytest, article_machine machine audit --strict, article_machine benchmark validate (+12 more)

### Community 1 - "Article Machine"
Cohesion: 0.02
Nodes (141): Article Machine Package, article_machine.__init__, Article Machine entrypoints and CLI, article_machine.__main__, article_machine.adapters.__init__, article_machine.adapters.runtime, article_machine.agent_skills, Skill routing and PT-BR style gates (+133 more)

### Community 2 - "Projects And Modes"
Cohesion: 0.01
Nodes (196): Article Machine Projects, Article Machine Governance 2026, lane: machine-governance, mode: bootstrap, type: machine-governance, article-machine-governance-2026/context (5 direct items), article-machine-governance-2026/analysis (7 direct items), article-machine-governance-2026/reviews (3 direct items) (+188 more)

### Community 3 - "Scientific Skills"
Cohesion: 0.01
Nodes (533): Critical Scientific Skills, hypothesis-tournament, hypothesis-tournament :: Hypothesis Tournament, hypothesis-tournament :: Workflow, hypothesis-tournament :: Output Contract, hypothesis-tournament :: Gates, scientific-novelty-checker, scientific-novelty-checker :: Scientific Novelty Checker (+525 more)

### Community 4 - "Agent Docs"
Cohesion: 0.01
Nodes (292): Agent Documentation, Workspace Navigation Index, .AGENTES :: Operação permanente da máquina científica, docs/ingles/AGENTES_DA_MAQUINA.md :: Permanent scientific-machine operations, docs/portugues/GUIA_DA_MAQUINA.md :: Guia da máquina científica, docs/portugues/GUIA_DA_MAQUINA.md :: Em uma frase, docs/portugues/GUIA_DA_MAQUINA.md :: Caminho normal, do pedido ao pacote revisável, docs/portugues/GUIA_DA_MAQUINA.md :: 1. Escolha o projeto e entenda os contratos (+284 more)

### Community 6 - "Graphify Map"
Cohesion: 0.07
Nodes (33): Graphify Operational Map, Área / Area: .agents, Área / Area: .codex, Área / Area: .git, Área / Area: .github, Área / Area: .machine, Área / Area: .mypy_cache, Área / Area: .pytest_cache (+25 more)

### Community 7 - "Git Hygiene"
Cohesion: 0.33
Nodes (6): Git Hygiene, local agent control plane; track only policy files and selected navigation skills, local virtual environment; never stage, pytest cache; generated, shared source intake; review before staging raw data, generated operational graph outputs

## Knowledge Gaps
- **38 isolated node(s):** `.AGENTES :: Operação permanente da máquina científica`, `docs/ingles/AGENTES_DA_MAQUINA.md :: Permanent scientific-machine operations`, `docs/portugues/ESTADO_E_LIMITES_DA_MAQUINA.md :: Estado atual e limites verificáveis`, `docs/ingles/ESTADO_E_LIMITES_DA_MAQUINA.md :: Current state and verifiable limitations`, `LEIA-ME_PRIMEIRO.md :: Comece aqui — fábrica científica` (+33 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **How should a new agent choose an active Article Machine project?**
  _Connects runtime commands, project modes, and required project files._
- **Which parts of the workspace are hygiene risks before committing?**
  _Highlights untracked/generated areas, legacy folders, and nested projects._
- **How do Graphify and Article Machine runtimes differ in this checkout?**
  _Shows the reproducible venv runtimes and the diagnosed global Graphify fallback._
- **How should GPT-6.1 Sol medium and GPT-6 Luna coordinate bilingual scientific work?**
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
5. Read graphify-out/LEIA-ME.md for the generated file map
6. Query graph before broad navigation
7. Select or create projects/<project_id>
8. Read project protocol standards compute files
9. Run article_machine skills route
10. Build context Task Packet
11. Validate Evidence Lock before ready claims

## Agent Quickstart By Intent
- **Open the operational graph**: graphify-out/LEIA-ME.md -> graphify-out/GRAPH_REPORT.md -> graphify-out/graph.html
- **New agent entering the workspace**: docs/INDICE_DO_WORKSPACE.md -> docs/AGENT_START_HERE.md -> .agents/AGENTS.md
- **Choose or resume a project**: docs/ESTADO_DOS_PROJETOS.md -> projects/<project_id>/project.yaml
- **Restore an environment**: docs/AMBIENTES_E_LOCKS.md -> uv.lock or renv.lock
- **Organize or clean without deleting**: docs/ORGANIZACAO_E_LIMPEZA.md
- **Check Git or worktrees**: docs/GIT_E_WORKTREES.md
- **Migrate or audit the C: legacy**: docs/MIGRACAO_PARA_D_STATUS.md -> archive/legado_C_2026-11/LEIA-ME.md
- **Claim something as ready**: evidence/claim_map.jsonl -> Review Trinity

## Agent Query Recipes
- `graphify query "onde esta o painel de projetos" --budget 1200`
- `graphify query "como restaurar o ambiente R" --budget 1200`
- `graphify query "como organizar sem excluir conteudo bruto" --budget 1200`
- `graphify query "qual projeto esta no modo analysis" --budget 1200`

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
- Markdown sections indexed: 250
- Project contract files indexed: 80
- Project artifact areas indexed: 152
- Skill instruction sections indexed: 454
- Navigation/preservation skills installed: 3
- Project-scoped Codex agent roles indexed: 5
- Read-only Codex benchmark profiles indexed: 2

## Generation Provenance
- Git HEAD: `416250a795a47f088cc9850fc6718d674e9f2957`
- Dirty worktree at generation: `true`
- Porcelain status entries at generation: 17

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
- `pedido: melhorar maquina sol medio luna trabalhos cientificos complexos ingles portugues` -> Codex project configuration, Codex role: workspace-explorer, Codex role: scientific-reviewer, Codex role: verification-runner, Codex read-only profile: xhigh-baseline.config, Codex read-only profile: ultra-benchmark.config, skill-upgrade-governor, agent-benchmark-harness, article_machine benchmark validate, article_machine machine audit --strict
- `pedido: indice do workspace painel de projetos estado atual` -> Workspace Navigation Index, docs/INDICE_DO_WORKSPACE.md, docs/ESTADO_DOS_PROJETOS.md, Article Machine Projects
- `pedido: restaurar ambiente r renv python uv lock quarto playwright` -> R 4.6.1 renv scientific environment, Python 3.13 root uv environment, Clinical ML Python uv environments, Quarto 1.10.20 portable toolchain, Playwright 1.61.1 browser tooling, docs/AMBIENTES_E_LOCKS.md
- `pedido: organizar limpar workspace sem excluir conteudo bruto` -> content-preservation-guardian, docs/ORGANIZACAO_E_LIMPEZA.md, docs/GIT_E_WORKTREES.md, Git Hygiene
- `pedido: migracao c para d backup legado archive` -> docs/MIGRACAO_PARA_D.md, docs/MIGRACAO_PARA_D_STATUS.md, Legacy And Raw Sources, docs/ORGANIZACAO_E_LIMPEZA.md
- `pedido: worktree sujo git status antes de commit` -> Git Hygiene, docs/GIT_E_WORKTREES.md, docs/ORGANIZACAO_E_LIMPEZA.md
- `pedido: abrir grafo operacional graph html graph report` -> graphify-out/LEIA-ME.md, graphify-out/GRAPH_REPORT.md, graphify-out/graph.html, scripts/generate_workspace_graph.py, Graphify Operational Map

## Legacy And Hygiene Map

Git hygiene targets:
- `.agents/`: local agent control plane; track only policy files and selected navigation skills
- `.venv/`: local virtual environment; never stage
- `.pytest_cache/`: pytest cache; generated
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
