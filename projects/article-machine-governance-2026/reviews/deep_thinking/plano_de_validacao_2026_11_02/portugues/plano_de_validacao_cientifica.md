# Plano de validação científica e preparação editorial

Data: 2026-11-02. Estado: **PROPOSTO; implementação e validação ainda pendentes**. Projeto ativo: `article-machine-governance-2026`. Escopo: infraestrutura e validação de métodos; nenhuma conclusão clínica nova, publicação, cadastro externo ou chamada paga autorizada por este documento.

## Decisão

Consolidar a arquitetura existente com bloqueios comuns, testes independentes dos cálculos e revisão científica documentada. O objetivo verificável é satisfazer todos os critérios aplicáveis de um escopo declarado e expor suas incertezas. Perfeição universal, ausência de vieses e aceitação editorial não podem ser garantidas.

Alternativas consideradas: manter a versão atual preserva funções, mas deixa falhas críticas abertas; adicionar mais skills amplia cobertura nominal, mas não valida os métodos; reescrever tudo perde trabalho funcional e introduz novos riscos. A opção preferida é corrigir e validar a arquitetura atual por famílias de métodos, preservando as capacidades solicitadas.

## Evidência de partida e falhas prioritárias

A inspeção local confirmou serviços de metodologia, corpus, datasets, extração documental, métricas e síntese. A auditoria estrita passou e 11 testes focados passaram na leitura anterior. Isso não constitui validação de todas as análises nem nova execução da suíte completa.

- `clinical_datasets.fetch_open_dataset` alcança a função de download sem chamar o gate de registro; a reprodução foi simulada, sem rede ou escrita. `ingest_and_verify_dataset` deixa a exigência desligada por padrão.
- `study_and_synthesis.synthesize_from_r_outputs` insere uma declaração de verificação humana integral sem comprovar essa revisão. Ler linhas do claim map não comprova aprovação dos claims.
- `results_ledger.evaluate_clinical_prediction_metrics` calcula limiar conformal e cobertura sobre os mesmos pares de resultados. O teste final precisa de avaliação separada. Identificadores de paciente ausentes não podem virar certificação de ausência de vazamento.
- Handoff e contrato divergem quanto ao modo ativo; há modificações posteriores ao checkpoint e documentos com contagens antigas. Os testes de extração incluem dependências de Tesseract instalado e de um certificado pessoal fora do pacote portátil.

## Ordem de execução e critérios de aceitação

### P0 — Integridade e bloqueios de execução

Aplicar a mesma política de registro final revisado a todas as entradas científicas pertinentes: CLI, serviços, importação/download, extração, análise e síntese. Separar preparação de protocolo de execução. Registro de ensaio e ética continuam exigências adicionais quando aplicáveis.

Revisar estado científico, validade temporal do protocolo, verificação de registro, provenance e aprovação das afirmações antes de qualquer exportação final. Declarações de execução, ética, autoria, revisão humana e IA devem vir de registros reais, com responsável, data e artefato; campos ausentes permanecem pendentes. Rascunhos devem ser identificados como tal e não sobrescrever resultados/manuscritos anteriores.

Aceitação: chamadas por todas as rotas pertinentes bloqueiam antes de rede/escrita/execução quando faltam requisitos; testes adversos demonstram cada bloqueio; nenhum texto declara trabalho não realizado; ausência de achado não é aprovação automática.

### P1 — Desenho e plano estatístico por projeto

Antes dos resultados, registrar pergunta, população, unidade, cenário, datas, estimando, desfechos e janelas, comparadores, tamanho amostral, critérios, confundimento, dados ausentes, multiplicidade e sensibilidades. Justificar a amostra com base no desenho, eventos e precisão pretendida; rejeitar regras numéricas universais. Distinguir confirmatório, exploratório, causal e preditivo.

Usar diretrizes de relato e instrumentos de avaliação em funções distintas: TRIPOD+AI e PROBAST+AI em predição; PRISMA 2020 e extensões nas revisões; QUADAS-3 nos estudos primários de acurácia dentro de revisões; SPIRIT 2025 e CONSORT 2025 em protocolos e resultados de ensaios. Aplicar RoB/GRADE conforme pergunta e desenho, com justificativas humanas, sem preencher itens automaticamente por presença de palavras.

Aceitação: protocolo completo e revisado, registro final conferido antes da execução científica, desvios/emendas rastreados e cada item aplicável ligado a uma decisão metodológica concreta.

### P2 — R e estatística validados numericamente

Comparar resultados com exemplos publicados, cálculos analíticos ou implementação independente. Fixar métodos e tolerâncias antes de comparar; diferenças entre pacotes só são defeitos quando estimando, dados e opções coincidem. Não escolher o programa que produz o resultado desejado.

Cobrir medidas de efeito, variâncias, intervalos, heterogeneidade, dependência/multi-braço, regressões, sobrevivência, dados ausentes e pressupostos conforme as famílias ativadas. Testar erros de denominador, valores não finitos, separação, poucos estudos, eventos raros e falhas de convergência. Para NMA, verificar conectividade, transividade e incoerência; para DTA, a estrutura conjunta de sensibilidade/especificidade. Ranking não substitui magnitude e certeza.

Aceitação: casos de referência reproduzidos, desvios explicados, resultados inválidos bloqueados, warnings classificados e todos os números de tabelas/figuras/manuscrito derivados de um resultado canônico.

### P3 — ML e DL com avaliação apropriada

Definir população de uso, momento da predição, disponibilidade dos preditores, desfecho e baseline. Preservar paciente/grupo/centro/tempo nas partições conforme o desenho. Executar imputação, seleção, transformação, balanceamento, tuning e calibração dentro das partições de treinamento apropriadas. A CV aninhada continua validação interna; teste externo precisa de dados independentes e compatíveis.

Corrigir a rotina conformal com dados de conformalização e teste separados e pressupostos explícitos. Cobertura marginal não garante cobertura por subgrupo ou sob mudança de distribuição. Relatar discriminação, calibração, Brier, incerteza, erros, subgrupos com precisão suficiente e utilidade apenas no alcance da avaliação realizada. Em DL/imagens, auditar duplicatas, origem, rótulos, aquisição, pré-treinamento e separação por paciente; mapas de explicação não demonstram causalidade.

Aceitação: ausência de vazamento sustentada por manifests e testes, baseline comparável, avaliação sem seleção pelo teste final e validação externa documentada quando realizada. Sem externa, limitar explicitamente a alegação; não fabricar desempenho mínimo universal nem exigir que DL vença um baseline.

### P4 — Revisões e meta-análises com processo verificável

Escolher tipo de revisão e método de síntese pela pergunta. Preservar buscas completas, plataformas/datas e exportações; reconciliar deduplicação, seleção e fluxo PRISMA. Documentar revisores, conflitos, exclusões, extrações verificadas, múltiplos relatos do mesmo estudo e julgamentos RoB/GRADE. OCR e priorização por IA são assistência sujeita a conferência.

Aceitação: contagens reconciliadas; números extraídos rastreáveis à página/tabela; medidas e populações compatíveis antes da síntese; análises e sensibilidades justificadas; conclusões limitadas pela certeza da evidência.

### P5 — Reprodutibilidade e portabilidade

Restaurar os ambientes a partir de `uv.lock`/`renv.lock` em diretórios limpos. Reexecutar análise e renderização sem dependência acidental de arquivos pessoais, bibliotecas globais ou caminhos antigos. Separar testes portáteis de integrações opcionais como OCR/navegador; um requisito obrigatório ausente bloqueia aquela função, e não vira PASS. Preservar hashes de entradas, scripts, resultados e versões.

Aceitação: reconstrução documentada por terceiro ou execução independente, CI real no commit correspondente quando autorizada e igualdade numérica dentro das tolerâncias especificadas. Cobertura de código e auditorias de segurança são evidências complementares, não validação científica.

### P6 — Documentação e pacote editorial PT-BR/EN

Cada projeto deve entregar: protocolo/registro/emendas; plano estatístico; dicionário e proveniência; código e locks; logs e resultados canônicos; figuras/tabelas; checklist aplicável preenchido com páginas; avaliações RoB/GRADE quando pertinentes; manuscrito, suplementos, carta, CRediT, conflitos, financiamento, ética, consentimento e declaração real de IA; respostas a pareceristas quando houver.

Parear português natural e inglês com nomes PT-BR, código/dados compartilhados e auditoria numérica, bibliográfica, semântica e visual. Conferir escopo, indexação, categoria, limites e taxas atuais da revista. Relevância, desenho e contribuição precedem formatação; não prometer aceitação.

Aceitação: nenhum campo pendente em pacote apresentado como final; toda afirmação sustentada; todos os autores aprovam suas declarações; layout e referências conferidos; submissão externa depende de autorização específica.

### P7 — Benchmarks e revisão independente

Criar casos de referência por família e testes com erros deliberados. Painel inicial proposto: meta-análise binária, contínua e dependente; DTA; NMA; regressão observacional; sobrevivência; ML tabular; DL/imagens; conformal; extração documental; integridade editorial. Cada caso tem entrada licenciada/sintética, resposta de referência, tolerância, limites e avaliador definido previamente. Fixtures de software não viram resultados clínicos.

Aceitação: todos os critérios críticos definidos passam, sem defeito crítico aberto; falhas e SKIPPED aparecem por capacidade. Um metodologista/estatístico e um especialista clínico revisam as partes relevantes de estudos reais; repetir parecer por IA não equivale a revisão humana independente. A validação de uma família não certifica todas as outras.

## Primeiro marco recomendável

Concluir P0; validar numericamente as métricas e um fluxo de meta-análise; reproduzir os ambientes; executar um projeto demonstrativo completo com dados sintéticos ou referências metodológicas publicadas; depois conduzir um estudo real previamente registrado, com revisão independente e pacote editorial completo. Só promover capacidades cobertas pela evidência obtida. Este plano não declara nenhuma dessas etapas concluída.

## Fontes oficiais consultadas

- [TRIPOD+AI e TRIPOD-LLM](https://www.tripod-statement.org/) e [PROBAST+AI](https://www.probast.org/).
- [PRISMA 2020](https://www.prisma-statement.org/prisma-2020), [Cochrane Handbook atual](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current), [QUADAS-3](https://www.bristol.ac.uk/population-health-sciences/projects/quadas/quadas-3/) e [SPIRIT/CONSORT](https://www.consort-spirit.org/).
- [scikit-learn: vazamento e boas práticas](https://scikit-learn.org/stable/common_pitfalls.html), [MAPIE: separação conformal](https://github.com/scikit-learn-contrib/MAPIE/blob/master/doc/content/conformal-prediction/split-cross-conformal.md).
- [metafor: reproduções de análises](https://www.metafor-project.org/doku.php/analyses), [renv](https://rstudio.github.io/renv/articles/renv.html), [ICMJE: uso de IA](https://www.icmje.org/recommendations/browse/artificial-intelligence/).
