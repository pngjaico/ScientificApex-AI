# AGENTS: ARTICLE MACHINE OPERATIONS

## 1. Operação 100% Automática Machine-First
Toda e qualquer conversa neste workspace é automaticamente uma sessão da Article Machine:
1. Identifique imediatamente o projeto ativo em `.machine/handoff_sessao.json` ou o projeto citado pelo usuário.
2. Todo o trabalho deve ocorrer estritamente contido em `projects/<project_id>/`.
3. Nunca execute scripts improvisados soltos: use os comandos canônicos `.\.venv\Scripts\python.exe -m article_machine <command>`.

## 2. Lean Context Protocol (Máximo Raciocínio, Zero Context Rot)
Para manter o modelo operando no topo de sua capacidade cognitiva sem estourar tokens:
- **Pointer-over-Dump**: NUNCA imprima tabelas brutas, CSVs completos ou textos extensos no chat. Execute scripts em Python/R que salvem os dados em `evidence/` ou `analysis/` e imprimam apenas um resumo de 5 a 10 linhas.
- **Grafo Operacional Enxuto**: Para navegação no workspace, utilize `.\.venv\Scripts\python.exe -m graphify query "<pergunta>" --budget 800`.
- **Respostas Diretas**: Use links no formato `file:///...` para apontar arquivos gerados. Não re-sumarize artefatos já exibidos na interface.

## 3. Menu Rápido de Roteamento de Skills (7 Intenções)
1. **Ideação, Hipóteses & Inovação**: `hypothesis-tournament`, `scientific-novelty-checker`.
2. **Bancada, Validação & Pré-Clínico**: `article-machine bench template`, `analytical-method-validation`, `relsa-severity-assessment`, `pkpd-modeling`, `uncertainty-and-units`, `ontology-term-resolution`, `iso-standards-readiness`, `experimental-design-planner`.
3. **Literatura Seminal & Corpus Landmark**: `article-machine landmark search/dissect/corpus-atlas`, Atlas dos 1000 Artigos (JAMA/Lancet/NEJM), `pubmed-database`.
4. **Revisões Sistemáticas & Meta-Análise**: `meta-analise-medica`, `asreview-screening-bridge`, `risk-of-bias-assistant`, `grade-sof-table-builder`.
5. **Machine Learning Clínico & IA**: `metodos-ml-clinico`, ambiente Python em `modelos/aprendizado_de_maquina_clinico/`.
6. **Redação Bilíngue & Publicação 9 Pastas**: `.\.venv\Scripts\python.exe -m article_machine publish prepare <dir> --journal <revista>`, `bilingual-scientific-writing`, `anti-ai-writing-governor`.
7. **Revisão Crítica, Auditoria Hostil & Aprendizado Contínuo**: `scientific-red-team-reviewer`, `manuscript-integrity-response-governor`, `machine-continuous-learner` (`/learn`), `.\.venv\Scripts\python.exe -m article_machine machine audit --strict`.


## Start Here
- Read `.AGENTES` for the current five-catalog, bilingual, publication and mandatory protocol-registration policy; English counterpart: `docs/ingles/AGENTES_DA_MAQUINA.md`.
- Read `docs/HANDOFF_ENTRE_AGENTES.md` and `.machine/handoff_sessao.json` for sequential multi-agent handoff state across Antigravity, Codex, and OpenCode.
- Workspace root: `D:\Usuario-pc\Projetos\Doutorado`.
- First read `docs/AGENT_START_HERE.md` when entering a new conversation.
- Use `.\.venv\Scripts\python.exe -m article_machine ...` as the reliable CLI path.
- Use `python scripts\generate_workspace_graph.py` to refresh the operational graph.
- Open/read `graphify-out/GRAPH_REPORT.md` before broad workspace navigation.
- Do not assume `article-machine` is on PATH unless you have installed the package in editable mode.
- Graphifyy 0.9.23 is pinned in the workspace dev dependencies and available through the local venv after `uv sync --locked --all-extras --dev`; global Python remains a diagnosed fallback.

## Intercâmbio Multiagente (Antigravity / Codex / OpenCode)
- **Operação Estritamente Sequencial:** os três agentes (Google Antigravity, OpenAI Codex, OpenCode CLI/Desktop) operam a máquina de forma alternada, nunca concorrente ("um agente por vez").
- **Protocolo de Entrada:**
  1. Verificar `git status` e `git log -1 --stat` para ver o último commit do agente anterior.
  2. Ler `.machine/handoff_sessao.json` e a última transição em `docs/HANDOFF_ENTRE_AGENTES.md`.
  3. Rodar `.\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict`.
  4. Manter o trabalho contido em `projects/<project_id>/`.
- **Protocolo de Saída:**
  1. Validar testes (`pytest tests/`) e integridade.
  2. Atualizar `.machine/handoff_sessao.json` e registrar o bloco no histórico de `docs/HANDOFF_ENTRE_AGENTES.md`.
  3. Realizar commit checkpoint (`git commit -m "handoff(<agente>): <resumo>"`) para o próximo agente encontrar a árvore limpa.
- **Configurações dos 3 Ambientes:**
  - Antigravity: lê `AGENTS.md`, `.agents/AGENTS.md`, skills em `.agents/skills/`.
  - Codex: lançado via `abrir_codex.cmd`, configurado em `.codex/config.toml` e `.codex/agents/*.toml`.
  - OpenCode: lançado via `abrir_opencode.cmd`, configurado em `opencode.json`.

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
- `article-machine bench template <project_dir> --assay <elisa|western|rt-qpcr|chiu|suzuki|teer|biobank>`
- `article-machine bench sample-manifest <project_dir>`
- `article-machine landmark search "<query>"`
- `article-machine landmark dissect <pdf_path> --venue <nature|nejm|lancet|annals-surgery>`
- `article-machine landmark corpus-plan <project_dir> [--count 1000]`
- `article-machine landmark corpus-mine <project_dir>`
- `article-machine landmark corpus-atlas <project_dir>`
- `article-machine publish prepare <project_dir> --journal <slug>`
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
- `article-machine portal build <project_dir> [--firebase-project pharosreader]`
- `article-machine portal deploy <project_dir>`
- `article-machine portal sync <project_dir>`
- `article-machine portal status <project_dir>`

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


## Política canônica a partir de novembro de 2026
- Workspace operacional: `D:\Usuario-pc\Projetos\Doutorado`. C: é backup/histórico; não reorganizar o antigo.
- Leia `LEIA-ME_PRIMEIRO.md`, `docs/ARQUITETURA_FINAL.md` e `docs/ORGANIZACAO_DAS_PUBLICACOES.md` para trabalhos novos.
- Entregas novas: `projects/<id>/publicacoes/<revista>/<identificador>/`, nove áreas numeradas em português. Use nomes `tipo_assunto_YYYY-MM-DD_vNN.ext`. Contratos técnicos, locks e Evidence Lock preservam nomes exigidos pelo runtime.
- Meta-análises: skill `meta-analise-medica`. ML/DL clínico: `metodos-ml-clinico`. Pacotes editoriais: `publicacao-medica-organizada`. Elas complementam as skills científicas existentes, não substituem revisão humana.
- Português científico natural é padrão; escrever primeiro em pt-BR, preservar números, referências, incerteza e disclosure. Não traduzir molde inglês automaticamente.
- K-Dense continua separado: apenas troca de artefatos aprovados via manifesto, nunca credenciais ou dados humanos por padrão.
- Instalações novas são por projeto com lock e teste. Modelos, esforço e disponibilidade devem ser verificados no runtime; configuração local não transforma sessão já aberta.

## Entregas bilíngues obrigatórias e Políticas de Escrita
- **Paridade Bilíngue:** Toda entrega científica/editorial nova deve existir em português brasileiro e inglês, em subpastas `portugues/` e `ingles/`, com nomes base em português. Isso inclui manuscritos, relatórios, tabelas, figuras e documentos de submissão. Compartilhar código, dados e lockfiles entre as duas versões. Verificar paridade de números/citações/claims e obter revisão semântica humana. Ler `docs/FLUXOS_CIENTIFICOS.md`.
- **Declaração Canônica de Uso de IA Obrigatória nos Manuscritos:**
  Todo manuscrito em inglês e português deve conter sob Declarations a seção oficial de disclosure de IA:
  - *Inglês:* `Use of Artificial Intelligence and AI-Assisted Technologies in Scientific Writing: During the preparation of this work, the authors used Claude Opus 5.5 (Anthropic) to assist with English language polishing, grammatical refinement, typographical corrections, and table layout formatting. Following the use of this tool, the authors critically reviewed, verified, and edited all generated content and take full responsibility for the scientific integrity, factual accuracy, and conclusions presented in this manuscript. In accordance with [target journal name] authorship criteria, generative AI technologies are not listed as authors.`
  - *Português:* `Uso de Inteligência Artificial e Tecnologias Assistidas por IA na Redação Científica: Durante a preparação deste trabalho, os autores utilizaram Claude Opus 5.5 (Anthropic) para auxiliar no polimento do idioma inglês, refinamento gramatical, correções tipográficas e formatação do layout de tabelas. Após o uso desta ferramenta, os autores revisaram criticamente, verificaram e editaram todo o conteúdo gerado e assumem total responsabilidade pela integridade científica, precisão factual e conclusões apresentadas neste manuscrito. Em conformidade com os critérios de autoria da [nome da revista], tecnologias de IA generativa não são listadas como autores.`
- **Estilo de Escrita em Inglês (Proibição de Travessões e Cara de IA):**
  - **Evitar Travessões (`—` / `–` / em-dashes):** O uso frequente de travessões é um dos traços mais reconhecíveis de texto artificial gerado por LLMs. Substitua travessões por parênteses, vírgulas, dois-pontos ou frases divididas.
  - **Roteamento Obrigatório de Skills de Escrita:** Sempre acionar `bilingual-scientific-writing`, `ptbr-article-writing` e `anti-ai-writing-governor` na redação e revisão de manuscritos, mantendo rigor terminológico e sobriedade acadêmica.

## Ambiente R Científico Consolidado (R 4.6.1 / renv 1.3.1)
- **Executável canônico:** `C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe` (resolvido automaticamente por `article_machine` quando `compute.yaml` declara `version: 4.6.1`). Não depender de R antigo no PATH.
- **Modelo e lockfile de referência:** `modelos/meta_analise_em_r/renv.lock` (e cópias sincronizadas em `modelos/estatistica_e_figuras/ambiente/renv.lock` e `modelos/manuscrito/renv.lock`), com **85 pacotes principais** e **342 pacotes no fecho transitivo CRAN** instalados e sincronizados:
  1. **Machine Learning Clínico, Calibração, Decisão e XAI (`metodos-ml-clinico`):** `tidymodels` (`parsnip`, `recipes`, `rsample`, `tune`, `workflows`, `yardstick`, `dials`), `bonsai` (suporte LightGBM nativo), `censored` (sobrevida em tidymodels), `finetune` (tuning avançado racing), `themis` (balanceamento/resampling), `probably` (calibração/Brier), `dcurves` (Decision Curve Analysis), `xgboost`, `lightgbm`, `glmnet`, `ranger`, `pROC`, `rms`, `DALEX`, `DALEXtra`, `ingredients`, `iBreakDown`, `pdp`, `kernelshap`, `shapviz`.
  2. **Meta-Análise Pairwise, Multinível, em Rede (NMA), Diagnóstica (DTA) e Dose-Resposta (`meta-analise-medica`):** `metafor` (REML, HKSJ `test="knha"`, `rma.mv`), `meta`, `netmeta` (NMA frequentista, `decomp.design`, `netsplit`, `netrank`), `clubSandwich` (variância robusta a clusters), `mada` (DTA Reitsma/HSROC), `dosresmeta`, `robvis`, `PRISMA2020`, `metadat`.
  3. **Inferência Causal, Riscos Competitivos e Sobrevida:** `MatchIt`, `WeightIt`, `cobalt` (Love plots e balanço de covariáveis), `tidycmprsk` e `ggsurvfit` (riscos competitivos de Fine-Gray e sobrevida acumulada), `survminer` (`ggsurvplot`).
  4. **Fluxogramas PRISMA 2020 e Visualização Gráfica:** `PRISMA2020`, `DiagrammeR`, `DiagrammeRsvg`, `rsvg`, `webshot2`, `ggplot2`, `patchwork` (`+`, `/`), `ggpubr`, `cowplot`, `ggridges`, `ggrepel`, `viridis`, `scales`, `RColorBrewer`, `ragg` (PNG 300 dpi anti-aliasing), `svglite` (SVG vetorial), `plotly` (HTML interativo MIT via `ggplotly()`).
  5. **Manipulação de Dados, Imputação, Tabelas Clínicas e Relatórios:** `dplyr`, `tidyr`, `readr`, `purrr`, `tibble`, `stringr`, `forcats`, `lubridate`, `data.table`, `janitor`, `skimr`, `readxl`, `writexl`, `mice` (imputação múltipla MAR/MNAR), `gtsummary` (Tabela 1 e modelos), `gt` (HTML), `flextable` + `officer` (DOCX editável), `broom`, `broom.mixed`, `parameters`, `performance`, `effectsize`, `emmeans`, `marginaleffects`, `rmarkdown`, `knitr`, `quarto` (CLI portátil em `ferramentas/quarto-1.10.20`), `shiny`, `DT`, `jsonlite`, `pwr`, `epiR`.
- **Exclusões deliberadas de governança (não instalar no lock base):**
  - `dmetar`: pacote fora do CRAN (apenas GitHub); usar funções nativas de `metafor` e `meta`.
  - `gemtc` / `BUGSnet`: exigem binário externo JAGS/Stan no SO (`rjags`); usar `netmeta` e `metafor::rma.mv` por padrão.
  - `highcharter`: licença comercial proprietária; usar `plotly` (MIT).
  - `chattr` / `ellmer`: proibidos dentro de scripts R de execução científica batch.
  - `keras` / `tensorflow` / `torch`: Deep Learning roda no ambiente Python isolado (`PyTorch 2.15.0+cpu` em `modelos/aprendizado_de_maquina_clinico/ambientes/aprendizado_profundo/`).
- **Comandos operacionais do ambiente R:**
  - Verificar os 85 pacotes principais: `"C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe" --vanilla modelos/meta_analise_em_r/analysis/00_pacotes_do_ambiente.R`
  - Sincronizar/atualizar o ambiente e lockfile: `"C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe" --vanilla scripts/atualizar_ambiente_meta_analise.R`
  - Executar script R em projeto ativo: `.\.venv\Scripts\python.exe -m article_machine run-r projects/<project_id> projects/<project_id>/analysis/<script>.R`

## Ambiente Python de Machine Learning Clínico e IA Médica (Python 3.13 / uv)
- **Diretório canônico:** `modelos/aprendizado_de_maquina_clinico/` (e subambiente `ambientes/aprendizado_profundo/`).
- **Executável canônico:** `modelos/aprendizado_de_maquina_clinico/.venv/Scripts/python.exe`.
- **Stack Consolidado (54 pacotes instalados com lockfile `uv.lock` sincronizado):**
  1. **Modelos Supervisionados e Ensembles:** `scikit-learn` (1.9.1), `xgboost` (3.4.1), `lightgbm` (4.7.0).
  2. **Predição Conformal e Incerteza Finita (MAPIE):** `mapie` (1.6.0) com `SplitConformalClassifier` e `CrossConformalClassifier` para conjuntos preditivos com garantia marginal finita (ex: 90% ou 95% de cobertura).
  3. **Análise de Sobrevida e Riscos Proporcionais:** `lifelines` (0.30.3) para curvas de Kaplan-Meier, testes de log-rank e modelos multivariáveis de Cox (`CoxPHFitter`).
  4. **Otimização de Hiperparâmetros:** `optuna` (4.9.0) para busca Bayesiana e pruning de experimentos.
  5. **Explicabilidade e Interpretabilidade (XAI):** `shap` (0.54.1) com `TreeExplainer` para valores de Shapley locais e gráficos globais (beeswarm e importância).
  6. **Contratos e Validação de Dados:** `pandera` (0.35.0) para validação de esquemas e limites fisiológicos.
  7. **Processamento e Gráficos:** `pandas` (2.3.3), `numpy` (2.5.4), `scipy` (1.18.1), `statsmodels` (0.15.0), `matplotlib` (3.11.2), `seaborn` (0.13.2), `plotly` (6.9.0), `openpyxl` (3.1.5).
  8. **Deep Learning Clínico (`ambientes/aprendizado_profundo`):** `torch` (2.15.0+cpu), `torchvision`, `torchmetrics` com `uv.lock` próprio.
- **Restauração e Execução:**
  - Restaurar ambiente ML tabular: `uv sync --directory modelos/aprendizado_de_maquina_clinico`
  - Restaurar ambiente Deep Learning: `uv sync --directory modelos/aprendizado_de_maquina_clinico/ambientes/aprendizado_profundo`
  - Executar script de ML no projeto: `modelos/aprendizado_de_maquina_clinico/.venv/Scripts/python.exe projects/<project_id>/analysis/<script>.py`
