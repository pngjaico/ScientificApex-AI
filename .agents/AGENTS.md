# Local Agent Control Plane

This `.agents` directory is the local handoff layer for agents entering
`C:\Users\Usuario-pc\Desktop\Doutorado`.

## Graph-First Rule
- If the task involves workspace navigation, architecture, code/file
  relationships, project selection, skill routing, cleanup, staging, unknown
  paths, or "where/what should I use", query the graph first even when the user
  did not explicitly ask for the graph.
- Use:

```powershell
.\.venv\Scripts\python.exe -m graphify query "<task or navigation question>" --budget 1200
```

- If the graph may be stale, refresh it first:

```powershell
.\.venv\Scripts\python.exe scripts\generate_workspace_graph.py
```

## Required Entry Flow
1. Read `docs/AGENT_START_HERE.md`.
2. Run `.\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict`.
3. Read `graphify-out/GRAPH_REPORT.md`.
4. Query the graph for navigation or routing questions.
5. Select or create one active `projects/<project_id>/` before evidence,
   analysis, discovery, drafting, or deliverables.
6. Run `.\.venv\Scripts\python.exe -m article_machine skills route --query "<task>"`
   before non-trivial scientific work.

## Local Skills
- `workspace-graph-navigator`: graph-first navigation.
- `project-entry-navigator`: project selection and contract-file entry.
- `content-preservation-guardian`: source/content protection during cleanup,
  staging, graphing, and reorganization.

## Hard Rules
- Do not run full-root semantic graph extraction by default.
- Do not move, delete, deduplicate, rewrite, upload, or stage raw scientific
  content without an explicit reviewed manifest.
- Do not treat graph edges as scientific evidence.
- Evidence, analysis, discovery, and manuscript work must happen inside
  `projects/<project_id>/`.
