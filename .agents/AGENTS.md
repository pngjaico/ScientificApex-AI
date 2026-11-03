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
- Canonical template & lockfile: `modelos/meta_analise_em_r/renv.lock` (85 direct packages, 342 in CRAN closure: `tidymodels`, `bonsai`, `censored`, `finetune`, `themis`, `xgboost`, `lightgbm`, `glmnet`, `ranger`, `probably`, `dcurves`, `DALEX`, `DALEXtra`, `kernelshap`, `shapviz`, `metafor`, `meta`, `netmeta`, `clubSandwich`, `mada`, `dosresmeta`, `robvis`, `PRISMA2020`, `MatchIt`, `WeightIt`, `cobalt`, `tidycmprsk`, `ggsurvfit`, `ggplot2`, `patchwork`, `ggpubr`, `survminer`, `plotly`, `gtsummary`, `gt`, `flextable`, `mice`, `data.table`, `janitor`, `skimr`, `broom`, `parameters`, `performance`, `effectsize`, `emmeans`, `marginaleffects`, `quarto`, `shiny`, `pwr`, `epiR`).
- Verify stack: `"C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe" --vanilla modelos/meta_analise_em_r/analysis/00_pacotes_do_ambiente.R`
- Refresh lockfile: `"C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe" --vanilla scripts/atualizar_ambiente_meta_analise.R`
- Run inside active project: `.\.venv\Scripts\python.exe -m article_machine run-r projects/<project_id> projects/<project_id>/analysis/<script>.R`

## Python Clinical Machine Learning & AI (Python 3.13 / uv)
- Canonical environment: `modelos/aprendizado_de_maquina_clinico/`
- Direct python: `modelos/aprendizado_de_maquina_clinico/.venv/Scripts/python.exe`
- Stack: `scikit-learn` (1.9.1), `xgboost` (3.4.1), `lightgbm` (4.7.0), `mapie` (1.6.0), `lifelines` (0.30.3), `optuna` (4.9.0), `shap` (0.54.1), `pandera` (0.35.0), `pandas` (2.3.3), `statsmodels` (0.15.0), `matplotlib` (3.11.2), `seaborn` (0.13.2), `plotly` (6.9.0).
- Deep Learning: `modelos/aprendizado_de_maquina_clinico/ambientes/aprendizado_profundo/` (`torch 2.15.0+cpu`, `torchvision`, `torchmetrics`).
- Restore: `uv sync --directory modelos/aprendizado_de_maquina_clinico`
- Run ML script: `modelos/aprendizado_de_maquina_clinico/.venv/Scripts/python.exe projects/<project_id>/analysis/<script>.py`

## Writing Quality & AI Disclosure Policy
- **Mandatory AI Disclosure:** All manuscripts must include the canonical Claude Opus 5.5 AI disclosure under Declarations (in both EN and PT-BR).
- **Prohibition of Em-Dashes (`—`):** In English academic writing, avoid conversational em-dashes (`—`); use parentheses, commas, or direct declarative sentences to maintain natural scientific style.
- **Mandatory Writing Skills:** Always route text preparation through `bilingual-scientific-writing`, `ptbr-article-writing`, and `anti-ai-writing-governor`.
