# AGENTS: ARTICLE MACHINE OPERATIONS

## Start Here
- Workspace root: `C:\Users\Usuario-pc\Desktop\Doutorado`.
- First read `docs/AGENT_START_HERE.md` when entering a new conversation.
- Use `.\.venv\Scripts\python.exe -m article_machine ...` as the reliable CLI path.
- Use `python scripts\generate_workspace_graph.py` to refresh the operational graph.
- Open/read `graphify-out/GRAPH_REPORT.md` before broad workspace navigation.
- Do not assume `article-machine` is on PATH unless you have installed the package in editable mode.
- The graphify package is available through global Python in this checkout; the Codex skill is installed under `C:\Users\Usuario-pc\.codex\skills\graphify`.

## Role
- Você está operando uma máquina científica agent-native.
- Sua unidade de trabalho é sempre um projeto em `projects/<project_id>/`.
- Nunca trabalhe fora de um projeto ativo quando a tarefa envolver evidência, análise, descoberta ou manuscrito.

## Default Flow
1. Identificar ou criar o projeto.
2. Ler `project.yaml`, `protocol.yaml`, `standards.yaml` e `compute.yaml`.
3. Construir ou atualizar um `Task Packet`.
4. Avançar apenas para o próximo modo permitido.
5. Registrar artefatos e manifests.
6. Validar `Evidence Lock` antes de chamar qualquer draft de pronto.
7. Rodar `Review Trinity` antes de submissão.

## Skill Routing
- Antes de tarefas científicas não triviais, consulte as skills disponíveis pela intenção do pedido.
- Se houver uma skill que cobre a tarefa, use a skill antes de improvisar uma solução manual.
- Para roteamento explícito, rode `article-machine skills route --query "<pedido do usuário>"`.
- Para auditoria das skills críticas, rode `article-machine skills audit`.
- Use `hypothesis-tournament` para hipóteses, priorização e debate científico.
- Use `scientific-novelty-checker` antes de afirmar novidade.
- Use `experimental-design-planner` para desenhar validação, controles e endpoints.
- Use `ro-crate-provenance-export`, `nextflow-pipeline-runner`, `snakemake-pipeline-runner` ou `cwl-workflow-bridge` quando reprodutibilidade/workflows forem parte da tarefa.
- Use `asreview-screening-bridge`, `risk-of-bias-assistant` e `grade-sof-table-builder` em revisões sistemáticas e meta-análises.
- Use `openalex-literature-graph`, `open-targets-drug-targeting`, `chembl-bindingdb-miner` e `alphafold-pdb-structure-router` em descoberta biomédica.
- Use `in-silico-validation-governor` para qualquer achado computacional antes de escrever conclusões.
- Use `agent-benchmark-harness` quando avaliar se a máquina está forte, perfeita, melhor, ou pronta para produção.
- Use `scientific-red-team-reviewer` antes de submissão, congresso, tese ou claim forte.

## CLI
- Preferred local form on this machine: `.\.venv\Scripts\python.exe -m article_machine <command>`.
- Equivalent console form only after editable install: `article-machine <command>`.
- `article-machine init "<name>" --type <project_type>`
- `article-machine preflight <project_dir>`
- `article-machine ingest <project_dir> --source <value> --kind <file|url|doi|note>`
- `article-machine context build <project_dir> --mode <mode> --hypothesis "..."`
- `article-machine run-r <project_dir> <script_path>`
- `article-machine draft <project_dir>`
- `article-machine review <project_dir>`
- `article-machine export <project_dir>`
- `article-machine congress import <project_dir> --source <url|text|path> --kind <deck|poster> --slug <slug>`
- `article-machine deck plan|build|qa|export <deliverable_dir>`
- `article-machine poster plan|build|qa|export <deliverable_dir>`
- `article-machine submit dry-run|run <deliverable_dir>`
- `article-machine life-science catalog`
- `article-machine life-science plan <project_dir> --question "..."`
- `article-machine skills catalog`
- `article-machine skills route --query "..."`
- `article-machine skills audit`

## Conference Deliverables
- Deliverables live under `projects/<project_id>/deliverables/<slug>/`.
- HTML is canonical for decks and posters.
- `storyboard.yaml` may only use claims approved by `evidence/claim_map.jsonl`.
- Run `qa` before `export`.
- Final portal submission requires explicit confirmation and a fresh Playwright snapshot.

## Life Science Research Integration
- Use `article-machine life-science plan` before biomedical discovery, target validation, omics lookup, variant interpretation, clinical-trial lookup, or public dataset discovery.
- Read `context/life_science/retrieval_plan.yaml` and `context/life_science/agent_retrieval_packet.md`.
- Save Life Science Research plugin outputs under `evidence/life_science/`.
- Promote only verified findings into `evidence/claim_map.jsonl`.

## Modes
- `bootstrap`
- `protocol-freeze`
- `corpus-build`
- `screening`
- `extraction`
- `analysis`
- `discovery`
- `drafting`
- `review-trinity`
- `submission`

## Hard Rules
- Full-root graphify semantic extraction is not the default. The root has caches, legacy folders, PDFs, and generated output; use the operational graph or graph a specific `projects/<project_id>/` folder.
- Do not move root legacy folders or raw scientific data without a migration manifest.
- Do not stage `.env`, `.venv`, caches, graphify transient files, raw fulltexts, or patient/source dumps.
- If a command fails in global Python, retry with `.\.venv\Scripts\python.exe -m ...` before blaming the code.
- Use `{{claim:claim-id}}` in `drafts/manuscript.md` for factual content.
- Keep `evidence/claim_map.jsonl` and `drafts/references.bib` synchronized.
- Treat `drug-discovery` and `intestinal-digital-twin` outputs as `hypothesis-generating`.
- If `Rscript` is absent and the project requires R, stop and surface the preflight failure clearly.
- Do not create congress slides, posters, abstracts, or submission packs outside the deliverables pipeline.
- Do not use database lookups from Life Science Research as final proof without Evidence Lock and explicit caveats.
- Do not bypass an applicable skill for a task already covered by the skill index.
- Do not claim the system is perfect, world-best, or production-grade without `agent-benchmark-harness` evidence.
