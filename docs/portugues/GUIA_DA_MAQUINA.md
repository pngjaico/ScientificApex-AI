# Guia da máquina científica

**O que faz, como escolher o próximo passo e onde a revisão humana continua obrigatória**  
Estado consultado em 2 de novembro de 2026.

## Em uma frase

A Article Machine organiza projetos científicos, aplica bloqueios de processo, seleciona skills por tarefa e prepara análises e documentos reproduzíveis. Um comando, uma skill disponível, um teste aprovado ou um texto bem escrito não comprova evidência científica validada.

Os componentes têm papéis diferentes:

- **Article Machine:** mantém projetos, contratos, modos, fontes, afirmações factuais, manifestos e verificações locais.
- **Skills:** instruções especializadas selecionadas por intenção. Encontrar uma skill não significa tarefa executada nem serviço conectado.
- **Graphify:** ajuda a navegar código e documentos. O grafo operacional não é evidência científica.
- **Conectores e plugins:** consultam serviços locais/remotos conforme disponibilidade, autorização, privacidade e eventual custo.
- **Modelos em `modelos/`:** pontos de partida em branco; não são protocolos aprovados, registros reais, análises concluídas ou manuscritos prontos.

## Caminho normal, do pedido ao pacote revisável

### 1. Escolha o projeto e entenda os contratos

Todo trabalho com evidência, análise, descoberta, manuscrito ou material de congresso começa em `projects/<id>/`. Selecione ou crie o projeto e leia `project.yaml`, `protocol.yaml`, `standards.yaml` e `compute.yaml`. Eles dizem que tipo de projeto existe, em que modo está, qual protocolo e quais ambientes e padrões foram declarados.

Use `project-entry-navigator` para entrar ou retomar o projeto e `scientific-workflow-orchestrator` para quebrar tarefas complexas em etapas. Antes de mexer em dados ou claims, monte ou atualize um Task Packet. O estado `bootstrap` permite planejar; não autoriza pular direto para análise.

### 2. Formule a pergunta, o desenho e o protocolo

Defina pergunta, população/unidade, desfechos e plano antes dos resultados. Use `experimental-design-planner`, `hypothesis-tournament`, `scientific-novelty-checker` e `deep-thinking-governor` conforme a necessidade.

Planejar e congelar o protocolo nos modos `bootstrap`/`protocol-freeze` é permitido antes do registro final. A política local exige **registro final PROSPERO ou OSF revisado antes do início do trabalho científico**, inclusive busca/corpus formal, triagem, extração, análise, descoberta ou redação científica. Esse gate local é mais estrito que regras editoriais que podem aceitar registros posteriores. Ensaios ainda podem exigir registro público específico e aprovação ética/regulatória.

Use `protocol-registration-governor` e os questionários em `modelos/registro_de_protocolo/`. Para revisões em saúde, verifique a elegibilidade atual do PROSPERO; se não for elegível ou se o desenho estiver fora do escopo, avalie OSF. Uma página de projeto OSF não é um registro. Rascunho ou envio pendente também não basta.

O comando `registry register` **só declara metadados locais** e deixa o estado `declared-unverified`; não envia nada ao PROSPERO/OSF. Antes de `registry verify`, uma pessoa nomeada confere o registro final, URL/ID, estado, snapshot local datado e hash, protocolo congelado e a declaração `scientific_work_not_started_before_registration`. A verificação local valida consistência documental e hashes; **não consulta o provedor para autenticar o conteúdo externo**. Nunca invente IDs, timestamps ou atestações.

> Os três modelos científicos foram atualizados para exigir registro antes da execução científica e verificação documental. Continuam em `bootstrap`, com protocolo em rascunho; nenhum está registrado por estar no repositório.

### 3. Busque e preserve as fontes

Com registro e gate apropriados, compile a busca com `query-string-governor` e planeje cache, limites, hashes e replay com `database-retrieval-governor`. Skills por fonte incluem `pubmed-database`, `literature-search-europepmc`, `literature-search-openalex`, `crossref-unpaywall-resolver`, `clinical-trials-database`, `semantic-scholar-citation-graph` e `opencitations-citation-audit`.

Guarde strings completas, base/plataforma, datas, filtros, resultados e identificadores em `sources/` e nos manifests do projeto. PubMed, Europe PMC, Crossref e outras bases fornecem registros e metadados; isso, sozinho, não prova uma afirmação do manuscrito. Registros públicos de ensaio ajudam a verificar o ensaio, mas não substituem evidência publicada ou revisão de método.

Para bibliografia, arquivos RIS/BibTeX, `references.bib` e anexos, use `zotero-reference-manager`. Ele não deve ser usado para contornar paywall. A documentação do workspace já registrou a API local do Zotero indisponível; verifique readiness de novo antes de depender dela. Deduplicação exata por DOI/PMID precisa de checagem manual de versões, títulos e relatos do mesmo estudo; a deduplicação semântica não está comprovada.

Cinco catálogos sob demanda: K-Dense (biomedicina), DenDen047 (computação/física), Orchestra-Research (engenharia/IA), Imbad0202 (planejamento/redação) e InternScience (fontes). `catalogos-cientificos-sob-demanda` seleciona por necessidade; confira origem/licença. Não instala nem autoriza upload ou gasto.

### 4. Faça triagem, extração e avaliação crítica

Para revisões, `asreview-screening-bridge` prioriza triagem sem substituir dois revisores. `extraction-schema-governor` estrutura extração; `risk-of-bias-assistant` apoia RoB por desenho e `grade-sof-table-builder` organiza certeza por desfecho. A equipe decide, registra conflitos e fundamenta julgamentos.

### 5. Analise sem perder unidade, dependência ou incerteza

Para meta-análise clínica em R, use a skill local ativa `meta-analise-medica` junto às skills de risco de viés, GRADE e `statistical-analysis`. Confirme população, comparador, desfecho, escala, direção e horizonte compatíveis antes de combinar. Não misture efeitos comparativos com proporções brutas. Meta-análise de proporções exige pergunta e denominadores/tempos compatíveis. Não trate múltiplos braços, tempos ou desfechos de um estudo como independentes.

Defina o modelo pela pergunta, não por p de heterogeneidade/I². Justifique REML e HKSJ, sobretudo com poucos estudos; k pequeno torna heterogeneidade, τ² e intervalos imprecisos. Faça sensibilidade e GRADE por desfecho.

Para outros dados quantitativos, `statistical-analysis` ajuda na escolha de testes, pressupostos, tamanhos de efeito e intervalos; `scientific-visualization` apoia figuras. Declare unidade experimental, desenho, estimando, missingness, multiplicidade e análise antes dos resultados. Use R/`renv` e `run-r` quando os contratos declararem R; Quarto renderiza o relatório, mas não revisa a validade científica.

Para predição clínica, use `metodos-ml-clinico` e `in-silico-validation-governor`. Compare com regressão/baselines simples. Mantenha cada paciente em uma única partição; use validação cruzada aninhada para seleção nos folds internos e avaliação nos folds externos, que continuam sendo validação interna, e divisões temporais ou por centro quando a pergunta for transporte. Ajuste imputação, seleção, balanceamento, hiperparâmetros e calibração somente no treino. Relate discriminação, calibração, intervalos e composição da amostra. AUC isolada não comprova utilidade clínica. Validação externa deve usar dados realmente independentes. PyTorch é opcional e sob demanda.

**TRIPOD+AI é guia de relato. PROBAST+AI avalia qualidade, risco de viés e aplicabilidade.** Nenhum dos dois transforma um modelo em seguro para decisão clínica. Desempenho preditivo não demonstra causalidade, benefício ou segurança.

### 6. Faça descoberta biomédica com rótulos prudentes

Para alvos, ômicas, variantes, proteínas, vias, ensaios ou datasets públicos, use `life-science-router` e primeiro rode o plano local de Life Science Research. Skills de busca e descoberta, como Open Targets, ChEMBL/BindingDB, AlphaFold e ToolUniverse, oferecem pistas e metadados para investigação. Guarde saídas em `evidence/life_science/`, confira fontes originais e rótulos de validação, e só depois promova claims para `evidence/claim_map.jsonl`.

Resultados computacionais, docking, modelos, consultas a bancos ou saídas de plugin começam como **geradores de hipótese** até validação independente. Para FASTQ/BAM/VCF e pipelines NGS, use `ngs-analysis-router` e faça preflight; dado humano não vai para nuvem sem permissão explícita e governança apropriada.

### 7. Redija claims rastreáveis em PT-BR e EN

Toda entrega científica/editorial nova tem pares em subpastas `portugues/` e `ingles/`, com mesmo nome-base em português. Escreva em português brasileiro natural com `ptbr-article-writing`; use `bilingual-scientific-writing` para redigir nativamente cada idioma e `workflow audit-language` como verificação lexical. Uma pessoa ainda precisa conferir equivalência de sentido, números, IDs, citações, incerteza e força das afirmações.

Use `anti-ai-writing-governor` para naturalizar o texto sem retirar limitações, citações ou declaração de uso de IA. Afirmações factuais pertencem a `evidence/claim_map.jsonl` e usam `{{claim:claim-id}}`; mantenha `drafts/references.bib` sincronizado. Um plano não comprova trabalho concluído.

### 8. Organize a publicação por revista e passe por revisão

`publicacao-medica-organizada` organiza uma versão em `projects/<id>/publicacoes/<revista>/<identificador>/`, com nove áreas numeradas: protocolo, busca/referências, dados autorizados, análises, tabelas, figuras, manuscrito, revisão e submissão. `organizar_publicacoes.py` roda em dry-run por padrão; `--criar` cria pastas vazias e manifesto, sem mover arquivos. Exemplo de prévia: `.\.venv\Scripts\python.exe projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/organizar_publicacoes.py --projeto <id> --revista <slug> --identificador v01 --raiz . --dry-run`. Modelos ficam em `modelos/publicacao_em_revistas/`; `venue-templates` e perfis ajudam a conferir instruções oficiais atuais da revista, que mudam.

Use `peer-review`, `manuscript-integrity-response-governor`, `scientific-critical-thinking` e `scientific-red-team-reviewer` conforme a etapa. Antes de chamar um draft pronto, rode Evidence Lock; antes de submissão, Review Trinity. A skill `academic-office-deliverables` pode preparar DOCX/PPTX/LaTeX editável com QA de layout. Template preenchido não é aprovação editorial.

Para congresso, o pipeline usa `deliverables/<slug>/`; HTML é o formato canônico para deck e pôster. O storyboard só pode usar claims aprovados no claim map. `conference-deliverable-router` aparece como `hold` no registry atual e exige revisão de status. Rode QA antes de exportar. A submissão em portal continua manual, exige confirmação explícita e snapshot Playwright recente.

## Funções e limites

A máquina estrutura projetos, valida contratos, prepara buscas, organiza referências, executa scripts autorizados e renderiza documentos. A equipe confirma protocolo e registro, autoriza conectores e transferências, revisa fontes, faz dupla triagem/extração, julga RoB/GRADE, valida análises, aprova claims, ética, autoria e submissão. Avanço bloqueia quando registro final, contratos, dados/ambiente, validação independente ou revisões obrigatórias faltam.

## Comandos disponíveis e confirmados

Use o Python da máquina, na raiz D. Ajuda da CLI e subcomandos abaixo foi consultada nesta versão local. Exemplos com `<...>` são marcadores a substituir; não copie IDs fictícios.

```powershell
.\.venv\Scripts\python.exe -m article_machine --help
.\.venv\Scripts\python.exe -m article_machine skills route --query "meta-análise médica em R"
.\.venv\Scripts\python.exe -m article_machine workflow plan projects/<id> --query "<pergunta>" --language pt-BR
.\.venv\Scripts\python.exe -m article_machine preflight projects/<id>
.\.venv\Scripts\python.exe -m article_machine context build projects/<id> --mode <modo> --hypothesis "<hipótese>"
.\.venv\Scripts\python.exe -m article_machine registry register projects/<id> --registry OSF --id <id-real> --url <url-registro-final> --registered-at <ISO-8601-real>
.\.venv\Scripts\python.exe -m article_machine registry verify projects/<id> --record projects/<id>/evidence/protocol_registration/<registro-revisado>.json
.\.venv\Scripts\python.exe -m article_machine run-r projects/<id> projects/<id>/analysis/<script-aprovado>.R
.\.venv\Scripts\python.exe -m article_machine workflow audit-language projects/<id> --language en --draft drafts/ingles/<arquivo>.md --reference drafts/portugues/<arquivo>.md
.\.venv\Scripts\python.exe -m article_machine submit dry-run projects/<id>/deliverables/<slug>
```

## Evidência local e estado dos exemplos

- Os modelos de meta-análise e ML estão em `bootstrap`, com pergunta vazia e protocolo em rascunho. São scaffolds, não estudos registrados ou dados clínicos executados.
- `modelos/publicacao_em_revistas/registro_renderizacao.json` registra 24 DOCX com `PASS` estrutural. Revisão humana de layout está `SKIPPED` e o conteúdo é template não preenchido.
- A demonstração estatística e de Quarto descrita nos docs é sintética. Ela não prova uma revisão sistemática completa, validação de coorte ou benefício clínico.
- A candidata BYOK em `projects/article-machine-governance-2026/analysis/continuacao-2026-11-02/byok/upstream_ro/` está no SHA `6a55f5ce6f4bd9ac7ff75d01ec20d7f27073a9f0`. Os testes focados passaram (69 server + 30 web), os typechecks passaram e a suíte completa reportou 307 passed/1 skipped (symlink Windows). Não houve chamada a modelo nem início de serviço; houve downloads de pacotes do registry npm, sem APIs pagas. O `npm ci` do frontend atingiu timeout embora a árvore tenha passado em `npm ls --offline` e nos testes. Build Next.js e startup foram omitidos. `launcher_candidato.cmd` só diagnostica; `iniciar_candidato.cmd` requer `--start` e confirmação digitada, usa loopback 8101/3101 e não foi executado. O iniciador pode instalar pacotes, criar configurações locais e baixar skills; revise esses efeitos antes de usá-lo. Isso não atualiza nem substitui a instalação histórica em C.

## Limites que não desaparecem com automação

Credencial existente não é autorização para usar API paga. Skill instalada não prova plugin conectado. Busca planejada não é busca feita. Hash local não autentica registro externo. Renderização DOCX/Quarto não é revisão visual/metodológica. Testes sintéticos não validam pessoas, hospitais ou uso clínico. Detector de IA não autoriza ocultar disclosure. Nenhum texto é aceito ou submetido automaticamente. O responsável pelo estudo continua responsável por ética, privacidade, protocolo, métodos, interpretação e decisão de publicar.
