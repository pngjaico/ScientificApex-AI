# AGENTS: ARTICLE MACHINE OPERATIONS

## Start Here
- Workspace root: `C:\Users\Usuario-pc\Desktop\Doutorado`.
- First read `docs/AGENT_START_HERE.md` when entering a new conversation.
- Use `.\.venv\Scripts\python.exe -m article_machine ...` as the reliable CLI path.
- Use `python scripts\generate_workspace_graph.py` to refresh the operational graph.
- Open/read `graphify-out/GRAPH_REPORT.md` before broad workspace navigation.
- Do not assume `article-machine` is on PATH unless you have installed the package in editable mode.
- Graphifyy 0.9.23 is pinned in the workspace dev dependencies and available through the local venv after `uv sync --locked --all-extras --dev`; global Python remains a diagnosed fallback.

## Graph-First Rule
- Quando a tarefa envolver navegação, arquitetura, relações entre arquivos/código, seleção de projeto, roteamento de skills, limpeza, staging, caminho desconhecido ou handoff, use o grafo primeiro mesmo que o usuário não peça.
- Comando padrão: `.\.venv\Scripts\python.exe -m graphify query "<pergunta operacional>" --budget 1200`.
- Se o grafo parecer desatualizado, rode `.\.venv\Scripts\python.exe scripts\generate_workspace_graph.py` antes da consulta.
- Use `.agents/AGENTS.md` e `.agents/GRAPH_FIRST.md` como política local curta para novos agentes.
- O grafo operacional não é prova científica; Evidence Lock continua obrigatório para claims.

## Model-Aware Orchestration
- Herde a política global: GPT-6.1 Sol medium como coordenador e revisor final; Luna low para exploração simples, medium para execução delimitada e high para análise delimitada. A revisão científica crítica usa Sol high. Respeite escolhas explícitas da sessão.
- Paralelismo não exige Ultra. Use o menor esforço que passe nos testes e gates; Sol high para problemas difíceis, xhigh para evidências conflitantes, e não use max/ultra automaticamente.
- A configuração local em `.codex/` limita o trabalho paralelo a três subagentes e oferece papéis read-only para exploração, revisão científica e verificação.
- Dê a cada subagente um escopo delimitado e, se houver escrita, uma superfície de arquivos não sobreposta. O agente principal lê as skills e contratos aplicáveis, integra os resultados e executa a validação final.
- Contexto longo e multiagente não autorizam varredura ampla do root, ingestão de dados brutos nem promoção de achados sem Evidence Lock. Capacidade do modelo não é evidência.

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
- Use `scientific-workflow-orchestrator` to plan complex scientific tasks with bounded Sol/Luna assignments.
- Use `bilingual-scientific-writing` for English/PT-BR manuscript drafting and translation fidelity audits.
- Antes de tarefas científicas não triviais, consulte as skills disponíveis pela intenção do pedido.
- Se houver uma skill que cobre a tarefa, use a skill antes de improvisar uma solução manual.
- Para roteamento explícito, rode `article-machine skills route --query "<pedido do usuário>"`.
- Para auditoria das skills críticas, rode `article-machine skills audit`.
- Use `workspace-graph-navigator` para navegar o grafo operacional e evitar varredura ampla do root.
- Use `project-entry-navigator` para escolher/criar/retomar o projeto ativo antes de evidência, análise, descoberta ou manuscrito.
- Use `content-preservation-guardian` antes de reorganizar, limpar, mover, stagear, deletar, indexar ou graphar áreas com risco a conteúdo bruto.
- Use `hypothesis-tournament` para hipóteses, priorização e debate científico.
- Use `scientific-novelty-checker` antes de afirmar novidade.
- Use `experimental-design-planner` para desenhar validação, controles e endpoints.
- Use `ro-crate-provenance-export`, `nextflow-pipeline-runner`, `snakemake-pipeline-runner` ou `cwl-workflow-bridge` quando reprodutibilidade/workflows forem parte da tarefa.
- Use `asreview-screening-bridge`, `risk-of-bias-assistant` e `grade-sof-table-builder` em revisões sistemáticas e meta-análises.
- Use `protocol-registration-governor`, `extraction-schema-governor` e `living-review-monitor` para preregistro/protocolo, extração estruturada e revisões vivas.
- Use `pubmed-database`, `clinical-trials-database`, `literature-search-europepmc`, `literature-search-openalex`, `literature-search-arxiv`, `literature-search-biorxiv`, `crossref-unpaywall-resolver`, `semantic-scholar-citation-graph` e `opencitations-citation-audit` quando a tarefa depender de fonte/provedor específico.
- Use `zotero-reference-manager` para biblioteca Zotero, BibTeX, `drafts/references.bib`, chaves de citação, anexos e full text local/indexado; não use Zotero para burlar paywall ou como prova sem Evidence Lock.
- Use `openalex-literature-graph`, `open-targets-drug-targeting`, `chembl-bindingdb-miner` e `alphafold-pdb-structure-router` em descoberta biomédica.
- Use `life-science-router` para orquestrar o plugin Life Science Research em perguntas biomédicas amplas antes de promover achados para claims.
- Use `ngs-analysis-router` para BCL/FASTQ/BAM/VCF/count matrices e workflows de sequenciamento; rode preflight antes de instalação/execução e peça permissão antes de cloud upload de dados humanos.
- Use `deep-thinking-governor` antes de decisões fortes, hipóteses concorrentes, claims frágeis ou pedidos de "perfeito"; não chame nada de perfeito sem benchmark.
- Use as skills `tooluniverse-*` instaladas para literatura profunda, meta-análise, diagnóstico, epidemiologia, datasets, diretrizes clínicas, desenho de ensaios, farmacovigilância, validação de alvo, interpretação de variantes e integração biológica; trate saídas como suporte, não como prova final.
- Use `anti-ai-writing-governor` para tirar cara de IA, polir estrutura de artigo e naturalizar manuscritos sem burlar detector, apagar disclosure ou enfraquecer Evidence Lock.
- Use `skill-upgrade-governor` antes de pesquisar, instalar ou promover novas skills para a camada crítica da Article Machine.
- Use `in-silico-validation-governor` para qualquer achado computacional antes de escrever conclusões.
- Use `agent-benchmark-harness` quando avaliar se a máquina está forte, perfeita, melhor, ou pronta para produção.
- Use `scientific-red-team-reviewer` antes de submissão, congresso, tese ou claim forte.

- Use `manuscript-integrity-response-governor` para resposta a pareceristas, rebuttal, integridade de referencias/citacoes, consistencia entre texto-tabelas-figuras e calibracao de forca dos claims.
- Use `academic-office-deliverables` para DOCX/PPTX/LaTeX editaveis, relatorios de leitura, slides de defesa/reuniao, pacotes com Zotero e QA de layout; congressos continuam usando `conference-deliverable-router`.

## CLI
- `article-machine workflow plan <project_dir> --query "..." --language en|pt-BR`
- `article-machine workflow audit-language <project_dir> --language en|pt-BR --draft drafts/pt.md --reference drafts/en.md`
- `article-machine plugins audit`
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
