# Agent Start Here

This workspace is not a single clean manuscript repository. It is an Article
Machine workspace containing a Python package, many project folders, local
skills, legacy source folders, generated outputs, and old graphify leftovers.
Treat it like an operating workspace, not a flat corpus.

## First Commands

Run from `C:\Users\Usuario-pc\Desktop\Doutorado`.

```powershell
.\.venv\Scripts\python.exe -m article_machine --help
.\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root .
.\.venv\Scripts\python.exe -m pytest
python scripts\generate_workspace_graph.py
```

Use `python -m article_machine ...` or `.\.venv\Scripts\python.exe -m article_machine ...`
unless you have explicitly installed the package in editable mode. Do not assume
the `article-machine` console script is on PATH.

Graphify is currently available through the global Python, not the local venv.
The Codex skill was installed in `C:\Users\Usuario-pc\.codex\skills\graphify`;
restart Codex to load it natively.

## Operating Rules

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

## Known Workspace Defects

- The root Git repo has no local commits on the current branch and most files are
  untracked. This is not a clean branch history.
- The root contains legacy folders and generated artifacts. A full graphify
  detect on the root timed out; use the generated operational graph or graph a
  specific project subfolder.
- `projects/projects/` exists and is probably accidental nesting. Do not move it
  without a deliberate migration note.
- The local venv can run tests and Article Machine, but does not have `pip` or
  `graphify`.

## Useful Files

- `AGENTS.md`: hard operating rules for agents.
- `README.md`: Article Machine overview and commands.
- `SKILL_INDEX.md`: local scientific skill routing.
- `docs/ARTICLE_MACHINE_AGENT_PLAYBOOK.md`: prompt and usage guide for agents.
- `docs/WORKSPACE_REORG_PLAN.md`: non-destructive reorganization plan.
- `graphify-out/graph.html`: interactive operational graph.
- `graphify-out/GRAPH_REPORT.md`: graph audit report.
