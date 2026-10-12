# Agent Start Here

This workspace is not a single clean manuscript repository. It is an Article
Machine workspace containing a Python package, many project folders, local
skills, legacy source folders, generated outputs, and old graphify leftovers.
Treat it like an operating workspace, not a flat corpus.

## First Commands

Run from `C:\Users\Usuario-pc\Desktop\Doutorado`.

```powershell
.\.venv\Scripts\python.exe -m article_machine --help
.\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe scripts\generate_workspace_graph.py
```

Use `python -m article_machine ...` or `.\.venv\Scripts\python.exe -m article_machine ...`
unless you have explicitly installed the package in editable mode. Do not assume
the `article-machine` console script is on PATH.

Graphifyy 0.9.23 is pinned in the workspace development dependencies and is
available through the local venv after `uv sync --locked --all-extras --dev`. The global
Python also has Graphify in this checkout. Prefer the venv for reproducible
audits and generation; use global Python only as a diagnosed fallback.

Graph-first rule: for workspace navigation, architecture, file relationships,
project selection, skill routing, cleanup, staging, unknown paths, or handoff,
query the graph even if the user did not explicitly ask for it.

```powershell
.\.venv\Scripts\python.exe -m graphify query "<operational question>" --budget 1200
```

## Operating Rules

The October 2026 operating policy uses GPT-6.1 Sol medium for coordination,
GPT-6 Luna low/medium/high for bounded tasks, and Sol high for scientific review.
Read `.codex/README.md` and `docs/SCIENTIFIC_WORKFLOWS.md`. Runtime settings must
be observed in each execution; configuration files do not change an open session.

Plan complex tasks with `workflow plan <project> --query "..." --language en|pt-BR`.
Inspect installed providers with `plugins audit`. Use `workflow audit-language`
to check numeric, citation and claim-marker preservation between drafts.

- Pick or create one active project under `projects/<project_id>/` before doing
  evidence, analysis, discovery, drafting, slides, posters, or submission work.
- Read `project.yaml`, `protocol.yaml`, `standards.yaml`, and `compute.yaml`
  before touching claims or analysis.
- Build or update a Task Packet before advancing work.
- Promote claims only through `evidence/claim_map.jsonl`; factual manuscript
  text must use `{{claim:claim-id}}`.
- Run Evidence Lock before calling a draft ready.
- Run Review Trinity before submission.
- Do not treat Life Science database outputs as final proof.
- Do not call the machine production-ready, perfect, or best without benchmark
  evidence and residual-risk notes.

## July 2026 Baseline Defects (historical snapshot)

- The current branch has three commits and is two commits ahead of `origin/main`,
  but the worktree is heavily mixed with pre-existing modified and untracked
  files. A green local test is not clean-clone proof.
- `machine audit --strict` currently blocks because 37 of 63 required critical
  skill entrypoints are present locally but absent from the Git index. Review an
  explicit staging manifest before versioning them; do not bulk-stage the root.
- The root contains legacy folders and generated artifacts. A full graphify
  detect on the root timed out; use the generated operational graph or graph a
  specific project subfolder.
- The active upgrade project still reports `bootstrap` while its protocol and
  older review artifacts imply later states. Treat those reports as stale until
  the lifecycle and benchmark provenance are rebuilt.
- The local venv is managed with uv and may intentionally omit `pip`; use
  `uv sync --locked --dev` instead of ad hoc installs.

## Useful Files

- `AGENTS.md`: hard operating rules for agents.
- `.agents/AGENTS.md`: local graph-first control plane for coding agents.
- `.agents/GRAPH_FIRST.md`: short rule for when to query the graph without being asked.
- `.codex/README.md`: project-scoped model and subagent control plane.
- `README.md`: Article Machine overview and commands.
- `SKILL_INDEX.md`: local scientific skill routing.
- `workspace-graph-navigator`, `project-entry-navigator`, and
  `content-preservation-guardian`: first-line local skills for graph navigation,
  project entry, and safe cleanup/reorganization.
- `docs/AGENT_OPERATION_MAP.md`: shortest safe operating flow for agents.
- `docs/ARTICLE_MACHINE_AGENT_PLAYBOOK.md`: prompt and usage guide for agents.
- `docs/WORKSPACE_REORG_PLAN.md`: non-destructive reorganization plan.
- `graphify-out/graph.html`: interactive operational graph.
- `graphify-out/GRAPH_REPORT.md`: graph audit report.
