# Graph Report - C:\Users\Usuario-pc\Desktop\Doutorado  (2026-06-29)

## Corpus Check
- Root semantic graph was not run: the workspace is too broad and detection timed out. This is an operational navigation graph.

## Summary
- 145 nodes · 244 edges · 8 communities detected
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.75)
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
1. `Runtime And Commands` - 40 edges
2. `article_machine.cli` - 36 edges
3. `Article Machine Package` - 31 edges
4. `Critical Scientific Skills` - 27 edges
5. `Article Machine Projects` - 17 edges
6. `lane: evidence-writing` - 12 edges
7. `Legacy And Raw Sources` - 9 edges
8. `mode: bootstrap` - 9 edges
9. `Doutorado Workspace` - 8 edges
10. `Agent Documentation` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Runtime And Commands` --exposes--> `article-machine analyze`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine check`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine compile`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine congress`  [EXTRACTED]
  . → article_machine/cli.py
- `Runtime And Commands` --exposes--> `article-machine context`  [EXTRACTED]
  . → article_machine/cli.py

## Communities

### Community 0 - "Runtime Commands"
Cohesion: 0.33
Nodes (6): Doutorado Workspace, Runtime And Commands, .venv python -m article_machine, global python -m graphify, .venv python -m pytest, article_machine machine audit

### Community 1 - "Article Machine"
Cohesion: 0.03
Nodes (60): Article Machine Package, article_machine.__init__, article_machine.__main__, article_machine.agent_skills, article_machine.analysis, article_machine.cli, article_machine.congress_profiles, article_machine.context (+52 more)

### Community 2 - "Projects And Modes"
Cohesion: 0.12
Nodes (33): Article Machine Projects, Article Machine Upgrade 2026, lane: evidence-writing, mode: bootstrap, type: thesis-chapter, CBCP Cosmiatria Idea Tournament 2026, type: evidence-synthesis, CBCP Top1 Idea Tournament 2026 (+25 more)

### Community 3 - "Scientific Skills"
Cohesion: 0.07
Nodes (27): Critical Scientific Skills, hypothesis-tournament, scientific-novelty-checker, experimental-design-planner, ro-crate-provenance-export, nextflow-pipeline-runner, snakemake-pipeline-runner, cwl-workflow-bridge (+19 more)

### Community 4 - "Agent Docs"
Cohesion: 0.29
Nodes (4): Agent Documentation, docs/AGENT_START_HERE.md, docs/ARTICLE_MACHINE_AGENT_PLAYBOOK.md, docs/WORKSPACE_REORG_PLAN.md

### Community 5 - "Legacy Sources"
Cohesion: 0.22
Nodes (1): Legacy And Raw Sources

### Community 6 - "Graphify Map"
Cohesion: 1.0
Nodes (2): Graphify Operational Map, graphify-out graph.json graph.html GRAPH_REPORT.md

### Community 7 - "Git Hygiene"
Cohesion: 1.0
Nodes (1): Git Hygiene

## Knowledge Gaps
- **35 isolated node(s):** `.venv python -m article_machine`, `global python -m graphify`, `.venv python -m pytest`, `article_machine machine audit`, `article_machine.__init__` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Graphify Map`** (2 nodes): `Graphify Operational Map`, `graphify-out graph.json graph.html GRAPH_REPORT.md`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Git Hygiene`** (1 nodes): `Git Hygiene`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **How should a new agent choose an active Article Machine project?**
  _Connects runtime commands, project modes, and required project files._
- **Which parts of the workspace are hygiene risks before committing?**
  _Highlights untracked/generated areas, legacy folders, and nested projects._
- **How do Graphify and Article Machine runtimes differ in this checkout?**
  _Shows the split between global graphify and the local Article Machine venv._
- **Which skills are mandatory before strong scientific claims?**
  _Bridges critical scientific skills to the Article Machine gates._

## Operational Limitations
- Operational graph only; full root semantic graph timed out and would mix caches, PDFs, and raw data.
- Edges marked INFERRED are navigation/risk inferences, not scientific evidence.
- Use project-specific graphify runs for manuscript evidence graphs.
