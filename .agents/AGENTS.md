# Local Agent Control Plane

This `.agents` directory is the local handoff layer for agents entering
`D:\Usuario-pc\Projetos\Doutorado`.

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

## Tri-Agent Sequential Operation
- Antigravity, Codex, and OpenCode operate sequentially without concurrency.
- Entry: check `git status`, read `.machine/handoff_sessao.json` and `docs/HANDOFF_ENTRE_AGENTES.md`.
- Exit: validate tests/audit, update handoff state, commit changes cleanly.

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

## R Environment (R 4.6.1 / renv 1.3.1)
- Canonical template & lockfile: `modelos/meta_analise_em_r/renv.lock` (69 direct packages, 302 in CRAN closure: `tidymodels`, `xgboost`, `lightgbm`, `glmnet`, `ranger`, `probably`, `dcurves`, `DALEX`, `DALEXtra`, `kernelshap`, `shapviz`, `metafor`, `meta`, `netmeta`, `clubSandwich`, `mada`, `dosresmeta`, `robvis`, `PRISMA2020`, `ggplot2`, `patchwork`, `ggpubr`, `survminer`, `plotly`, `gtsummary`, `gt`, `flextable`, `mice`, `data.table`, `janitor`, `skimr`, `broom`, `parameters`, `performance`, `effectsize`, `emmeans`, `marginaleffects`, `quarto`, `shiny`).
- Verify stack: `"C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe" --vanilla modelos/meta_analise_em_r/analysis/00_pacotes_do_ambiente.R`
- Refresh lockfile: `"C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe" --vanilla scripts/atualizar_ambiente_meta_analise.R`
- Run inside active project: `.\.venv\Scripts\python.exe -m article_machine run-r projects/<project_id> projects/<project_id>/analysis/<script>.R`
