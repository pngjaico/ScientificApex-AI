# Parecer crítico interno do pacote OSA/IVF do professor Nivaldo Alonso

Data: 03/11/2026. Material-alvo: documentos JCS produzidos em 02/11/2026. Rascunho de avaliação para conferência e decisão dos autores; não é parecer de revista nem decisão editorial.

## Conclusão da avaliação

**Eu não considero este pacote pronto para submissão. A revisão necessária é metodológica e documental, além da redação.** Há erros demonstráveis na descrição de um estudo primário, inconsistências entre estudos e braços, lacunas importantes de cobertura bibliográfica e conclusões sobre subdetecção que o desenho não estima. A revisão hostil anterior identificou problemas reais, mas encerrou com segurança injustificada e recomendou alterações que introduziram ou preservaram afirmações incorretas.

O trabalho tem uma pergunta pertinente e uma organização aproveitável. Separar PSG, questionários e códigos administrativos; excluir uma coorte de resgate; reconhecer a imprecisão de Furlow; e abandonar rankings causais são decisões defensáveis. Essas escolhas não demonstram que o corpus esteja completo nem que os resultados estejam suficientemente sustentados.

## Escopo e evidência efetivamente examinada

Li o manuscrito inglês completo, o pacote textual português do orientador, a revisão hostil, contratos, claim map, referências, tabelas, código de geração e sumário R existente. Inspecionei o XML dos cinco DOCX JCS, incluindo o manuscrito cego e o pacote do professor. Conferi fontes públicas específicas em PubMed/PMC, editora e registro de ensaio. A auditoria local está em `../verificacao_local.json`, com hashes e localizadores por parágrafo dos DOCX; o script está em `../auditar_pacote.py`.

Não refiz extração dos PDFs de todos os estudos nem executei uma nova metanálise. Não inspecionei Google Docs ao vivo, prontuários ou dados identificáveis. Não realizei QA visual das páginas Word. Portanto, contagens de arquivos foram verificadas; exatidão integral da extração e completude do corpus não foram certificadas. O uso da IA nesta avaliação interna foi solicitado pelo usuário; a participação prévia de assistentes impede chamar esta avaliação de independente ou cega. A página atual de instruções JCS não pôde ser recuperada, e não declaro conformidade editorial atual.

Os localizadores `M:linha` abaixo se referem a `drafts/ingles/manuscrito_completo.md`, preservado nesta execução. Os demais caminhos são relativos ao projeto.

## Comentários maiores e bloqueios

### P01. Cobertura do corpus não está sustentada; a afirmação de ausência de ensaios randomizados é falsa

**Localização:** M:15,24,29,40; `evidence/claim_map.jsonl`, claim `design_not_nma`; carta JCS; `analysis/primary_psg_dataset.csv` e `corrected_extraction.csv`.

**Observação e evidência:** Liao 2002 e Liao 2004 não aparecem na extração corrigida. O primeiro estudou PSG após retalho em fissurados; o segundo comparou Furlow e retalho com PSG pós-operatória em 48 crianças. São candidatos aparentemente pertinentes, cuja elegibilidade precisa ser adjudicada com texto completo e critérios explícitos. O ensaio multicêntrico randomizado de Åbyholm/VPI Surgical Trial Group, 2005, comparou retalho e esfincteroplastia em 97 participantes e incluiu avaliação de apneia. Sua existência contradiz a declaração categórica de inexistência de comparações randomizadas, independentemente da elegibilidade do seu desfecho para a primária estrita. [Liao 2002](https://pubmed.ncbi.nlm.nih.gov/12019007/), [Liao 2004](https://pubmed.ncbi.nlm.nih.gov/14989690/), [ensaio 2005](https://journals.sagepub.com/doi/10.1597/03-148.1), [registro](https://www.isrctn.com/ISRCTN14864864).

**Impacto:** a primária atual pode omitir informação que altera as estimativas. A justificativa científica do desenho contém uma premissa factual errada. A existência desses estudos também não demonstra, por si, viabilidade de NMA: conectividade, comparabilidade e transitividade continuam necessárias. [Cochrane, capítulo 11](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-11).

**Ação solicitada:** localizar esses registros na busca/triagem, documentar inclusão ou exclusão e verificar sobreposição de pacientes antes de qualquer nova síntese. Corrigir a alegação no manuscrito, carta e claim map. Não simplesmente acrescentar estudos sem adjudicação. **Prioridade: bloqueio científico.**

### P02. Tempo de seguimento e limiar diagnóstico foram descritos incorretamente

**Localização:** M:31,96-108; DOCX inglês, Métodos; tabela 1 do texto para Google Docs.

**Observação e evidência:** o texto generaliza PSG aos 6 a 12 meses e atribui IAH pediátrico ≥1,5 a Zhao 2021. O original informa seguimento mínimo de 1,2 ano, média de 6 anos, e limiar pediátrico ≥1. Os grupos foram definidos pela idade na cirurgia; dez operados na infância já eram adultos na avaliação. [Zhao 2021, Métodos e tabelas 1-2](https://pmc.ncbi.nlm.nih.gov/articles/PMC8548231/).

**Impacto:** erro confirmado de extração/relato; muda a interpretação de idade, horizonte e comparabilidade. Não implica que os numeradores 6/30 e 16/52 estejam errados.

**Ação solicitada:** conferir definição, idade na cirurgia e na PSG, critério e janela de cada estudo, sem impor um padrão único retrospectivamente. Reconciliar tabela, texto, DOCX e extração. **Prioridade: bloqueio científico.**

### P03. PRISMA e resumo misturam registros, artigos, estudos e braços

**Localização:** M:16,40; `analysis/PRISMA_counts.md`; script R:74-95.

**Observação e evidência:** a primária possui 5 linhas/braços de 3 DOI, N=129 e 53 eventos. A sensibilidade tem 10 braços de 5 DOI, N=1.274 e 138 eventos. A extração total tem 20 linhas de 13 DOI. O resumo declara 10 estudos e 20 braços com N=1.274. O fluxograma codifica 100 textos completos e 80 exclusões, sem reconciliar os 20 restantes com os estudos efetivamente incluídos. DOI identifica relatório, não prova coorte independente.

**Impacto:** o leitor não consegue reconstruir a seleção ou saber quantos estudos sustentam cada resultado.

**Ação solicitada:** reconstruir o fluxo a partir das decisões individuais; criar correspondência registro → relatório → estudo/coorte → braço. Corrigir todos os números derivados. As somas dos CSV conferem, mas não validam o fluxo bibliográfico. **Prioridade: bloqueio de relato e rastreabilidade.**

### P04. O efeito de subdetecção de quatro a oito vezes não foi estimado

**Localização:** M:16-17,63,73,82; tabela 4; carta JCS.

**Observação e evidência:** a comparação usa coortes, técnicas, populações e horizontes distintos, sem aplicação pareada de PSG e códigos/questionários nas mesmas pessoas. O próprio conjunto inclui pacientes não fissurados nos claims e técnica de bucinador no screening. Não há estimativa de sensibilidade nem razão ajustada de subdetecção. A explicação por adaptação comportamental também não foi testada.

**Impacto:** o argumento central transforma diferença entre estudos em desempenho diagnóstico demonstrado. A revisão hostil anterior endossou esse salto.

**Ação solicitada:** remover a magnitude causal/diagnóstica e a explicação mecanística afirmativa. Uma formulação proporcional seria: “As frequências diferiram entre fontes de aferição; diferenças de população, técnica e seguimento impedem atribuir a discrepância exclusivamente ao método diagnóstico.” **Prioridade: bloqueio de interpretação.**

### P05. Cinco braços não representam cinco estudos independentes

**Localização:** M:47-57; `analysis/r_metaprop_summary.txt`; script R:42-52; tabela 2.

**Observação:** Orticochea provém de um relatório com dois subgrupos etários; retalho, de outro; Furlow, de um terceiro. Não demonstrei duplicação de pessoas. Subgrupos disjuntos podem ter independência amostral condicional, mas não constituem replicações independentes entre centros/estudos. I² entre faixas etárias não estima heterogeneidade entre vários estudos de cada técnica. Técnica e estudo/centro ficam confundidos neste conjunto.

**Impacto:** o Q entre técnicas não estabelece superioridade cirúrgica, mesmo chamado exploratório; a linguagem de estimativa “agrupada” pode exagerar a replicação disponível.

**Ação solicitada:** distinguir `k_estudos` de `k_braços`, apresentar resultados por estudo e definir o estimando. Se o corpus elegível continuar com um estudo por técnica, considerar síntese descritiva por estudo em vez de enquadrar subgrupos etários como metanálise de estudos. Não escolher um modelo mais complexo apenas para preservar a aparência de síntese.

### P06. Código, figuras e intervalos não derivam de uma única saída estatística

**Localização:** script R:50,60-63,129-146; `analysis/r_metaprop_summary.txt`; M:15,35; tabela 2.

**Observação:** o R usa `method.ci="CP"`; o sumário registra 0,25% a 44,50% para a linha individual Furlow e 1,39% a 46,72% no resultado de subgrupo. O valor publicado 1,8% a 40,4% é Wilson e está escrito manualmente no sumário complementar e no forest plot. Wilson é intervalo de escore, não intervalo exato; não é sinônimo de Clopper-Pearson. O forest e a matriz ROBINS-I são preenchidos com constantes no script.

**Impacto:** há números reconhecíveis e plausíveis, mas executar o script não garante que tabelas/figuras representem o objeto calculado. Não afirmei que 1,8% a 40,4% seja numericamente errado.

**Ação solicitada:** declarar separadamente os métodos para intervalos individuais, proporções combinadas e braço único. Alimentar gráficos/tabelas de resultados computados e julgamentos rastreáveis; bloquear divergências. Reexecutar somente após resolver corpus e autorização de execução pelo protocolo.

### P07. Avaliações ROBINS-I não são auditáveis por domínio

**Localização:** M:35,57; `analysis/ROBINS_I_support.md`; `evidence/risk_of_bias/ROBINS_I_support.csv`; script R:206-223.

**Observação:** os “support excerpts” visíveis são sínteses gerais, sem localização no texto original ou respostas às perguntas de sinalização. O gráfico contém matriz fixa. Desenho observacional não determina automaticamente risco moderado; exclusão por PICO/resgate não equivale a risco crítico de viés. Para proporção pós-operatória sem efeito comparativo, a escolha e adaptação do instrumento precisam ser justificadas.

**Impacto:** não é possível auditar ou reproduzir os julgamentos exibidos.

**Ação solicitada:** definir unidade e estimando da avaliação, justificar ferramenta adequada e documentar trechos/localizadores e julgamentos por domínio, com revisão humana. Separar inelegibilidade de risco de viés; não interpretar silêncio como baixo risco.

### P08. GRADE contém trajetória de classificação e população de linha pouco claras

**Localização:** `analysis/table3_grade_sof_certainty_en.csv`, linhas 2-5; M:57 e tabela 3.

**Observação:** a tabela marca risco grave (-1) e imprecisão grave (-1), chegando a baixa (2/4), sem explicar o ponto inicial e a abordagem GRADE adotada. A linha “claims and screening”, N=1.145/5 braços, também inclui o braço PSG misto de 10 pacientes. “Undetected” não demonstra ausência de viés de publicação, sobretudo com tão poucos estudos.

**Impacto:** a aritmética pode corresponder a uma abordagem explícita que começa alto, mas não há justificativa suficiente para presumir essa abordagem nem para manter a classificação atual.

**Ação solicitada:** definir abordagem para este estimando, justificar cada domínio e separar os subconjuntos. Não rebaixar mecanicamente nem promover recomendações com base apenas no rótulo GRADE.

### P09. Busca e checklist PRISMA afirmam mais do que documentam

**Localização:** M:15,29; `context/retrieval/compiled_queries.json`; `evidence/retrieval/pubmed_offline_replay_manifest.json`; checklist JCS CSV.

**Observação:** a evidência operacional inspecionada registra replay offline PubMed datado de 14/05/2026, não execução atual nas cinco bases declaradas “through 2026”. Isso não prova que as outras buscas nunca ocorreram. O manuscrito não traz datas exatas, estratégias por base, processo de revisão independente ou resolução de discordâncias. O checklist aponta seções 2.1-2.3 inexistentes nessa versão e usa numeração incompatível com a checklist oficial, inclusive registro como item 25 em vez de 24. [PRISMA 2020](https://www.prisma-statement.org/prisma-2020).

**Ação solicitada:** recuperar logs/exportações de cada base, identificar a última busca real e corrigir o checklist linha por linha. Se o material faltar, declarar a limitação; não reconstruir retrospectivamente uma busca como se tivesse sido executada.

### P10. As versões chamadas finais não estão sincronizadas

**Localização:** `publicacoes/journal-of-craniofacial-surgery/v01/07_manuscrito/ingles/`; `scripts/build_submission_docx_jcs.py`; DOCX JCS e pacote do orientador.

**Observação:** `manuscript_journal_of_craniofacial_surgery_en.md` mantém incidência e PSG rotineira universal; `manuscript_jcs_gdocs_en.md` e o draft completo têm correções posteriores. O gerador DOCX mantém prosa própria codificada no Python e tabelas CSV diferentes da tabela expandida no Markdown. A limitação de centro único explicitada no inglês não está explicitada da mesma forma no pacote textual português; o pacote português reconhece a amostra pequena de Furlow, mas isso não equivale à ressalva de centro único. O DOCX cego não elimina sozinho identificadores indiretos como o projeto FMUSP e referências departamentais.

**Ação solicitada:** definir fonte canônica, sincronizar PT/EN e gerar todos os artefatos dela. Conferir cada correção no DOCX efetivo. Aplicar anonimização somente conforme a política real da revista. Não afirmei que o Google Docs ao vivo esteja divergente, pois não o abri.

### P11. Referências apresentam erro de DOI e apoio temático inadequado

**Localização:** M:24,71,151,157; referência 2 nos DOCX; `drafts/references.bib`.

**Observação:** a referência Prada-Madrid 2011 nos textos/DOCX JCS usa `10.1597/09-082`; o registro correspondente ao título é `10.1597/09-178`. O BibTeX mantém “Chen” onde o artigo de 2021 é de Zhao e metadados divergentes. A referência 8, sobre posição nasal após reparo primário da fissura, não sustenta diretamente a frase sobre estabilidade respiratória noturna após cirurgia velofaríngea. [Prada-Madrid 2011](https://pubmed.ncbi.nlm.nih.gov/20500068/), [Zhao 2021](https://pubmed.ncbi.nlm.nih.gov/34636205/).

**Ação solicitada:** reconciliar DOI, autores, título, volume e páginas e verificar suporte de cada citação. “Erros de revisões anteriores” deve identificar a revisão e a passagem; erro da própria extração local não pode ser atribuído automaticamente à literatura publicada.

### P12. Registro e declarações de autoria/IA exigem conferência real

**Localização:** `protocol.yaml`, registro `prepared-not-submitted`; M:85-87; carta e title page; `.machine/handoff_sessao.json`.

**Observação:** não há ID de registro final no contrato inspecionado. O claim “protocol-driven” e o checklist não substituem registro. A regra local exige registro final antes de nova execução científica. Ausência de registro prospectivo, por si, não invalida automaticamente uma revisão, mas precisa ser declarada com cronologia honesta. A declaração de IA diz exclusivamente polimento/layout com Claude Opus 5.5; o handoff documenta uso de agente em revisão e mudanças científicas. Não verifiquei qual modelo foi efetivamente usado ontem. Apresentação no SIICUSP, aprovação dos autores, vínculos, financiamento e conflitos também precisam de confirmação documental.

**Ação solicitada:** reconciliar status do projeto e cronologia; não inventar registro retrospectivamente prospectivo. Registrar ferramentas e usos reais de IA, incluindo revisão/alterações substantivas quando aplicável, e obter conferência humana. Não copiar uma declaração fixa da skill como prova do histórico de uso.

### P13. Algoritmo clínico ultrapassa a evidência avaliada

**Localização:** M:17,79,82; `clinical_implication` no claim map.

**Observação:** a revisão não compara estratégias de vigilância, validade de oximetria/triagem, custos nem intervalo ideal. Logo, não estabelece PSG “mandatória” por técnica nem comprova segurança da triagem nos demais pacientes. A revisão hostil anterior propôs esse algoritmo sem demonstrar a base externa.

**Ação solicitada:** separar implicação de pesquisa, opinião clínica dos autores e recomendação sustentada por diretriz externa. Identificar explicitamente o suporte externo antes de usar linguagem mandatória. Não usar a frequência observada como validação de um protocolo assistencial.

## Conferência das sete correções da revisão hostil de ontem

| Pedido anterior | Situação verificada em 03/11 | Problema residual |
|---|---|---|
| Trocar incidência por frequência/detecção | Parcial | Título mais recente corrigido; versões antigas e implicações generalizantes persistem. |
| Remover estilo inflado | Parcial | Permanecem “confirms”, “remarkably high” e promessas fortes; estilo não valida ciência nem identifica autoria por IA. |
| Inserir limiares e tempo de PSG | Falhou na verificação factual | Zhao foi descrito com corte e janela incorretos. |
| Ressalvar Furlow N=10 | Parcial | Ressalva existe; ranking e conclusão clínica continuam fortes. |
| Ressalvar centro único de Orticochea | Parcial | Presente no draft inglês; propagação incompleta e ausência de novos estudos elegíveis não resolvida. |
| Estratificar recomendação clínica | Texto alterado, validade não demonstrada | Algoritmo não foi avaliado nem sustentado por diretriz identificada. |
| Sincronizar DOCX/Google Docs | Não demonstrado integralmente | DOCX inspecionados; fontes locais divergem; Docs ao vivo não verificado. |

## Avaliação da própria revisão hostil

Ela acertou ao questionar incidência sem basal, pequeno N e generalização de centro único. Falhou ao endossar a subdetecção “oito vezes”, prescrever um algoritmo sem apoio demonstrado e propor limiares sem checar cada estudo. Sobreposição de IC não demonstra equivalência ou ausência de diferença. “Wilson exato” é terminologia incorreta. A promessa de artigo “inatacável para aceitação” não é conclusão científica nem previsão editorial defensável. Foco em travessões e palavras não substitui verificação de corpus, fontes e estatística.

## Decisão prática e sequência de correção

Considerei três opções: manter o pacote como pronto; fazer apenas correção textual; suspender a prontidão e reparar a cadeia científica. A terceira é a recomendada. A melhor defesa do pacote é seu enquadramento descritivo e a separação de métodos diagnósticos, mas isso não supera erros confirmados e candidatos ausentes do corpus.

1. Corrigir imediatamente os erros factuais confirmados e retirar os claims de subdetecção quantificada e recomendações mandatórias não sustentadas.
2. Resolver registro/contratos para nova execução, rastrear os estudos candidatos e reconstruir seleção/extração com verificação independente. Não executar nova síntese antes disso.
3. Reavaliar unidade de síntese, RoB e certeza; gerar resultados, tabelas e figuras da mesma cadeia computacional.
4. Sincronizar fontes PT/EN, DOCX e checklist; conferir declarações e referências; repetir Evidence Lock e revisão metodológica/quantitativa/editorial sobre hashes finais.

**Condição para reconsiderar prontidão:** corpus rastreável, extração corrigida, resultado reproduzível a partir do corpus adjudicado e conclusões compatíveis com o desenho. O tema permanece aproveitável; o valor das estimativas atuais ainda precisa ser demonstrado após essa reparação.

## Resultado dos controles desta sessão

- **PASS:** inventário/hashes dos cinco DOCX JCS; soma dos CSV existentes; verificação das divergências textuais citadas; auditoria operacional `machine audit --strict` executada e retornou pass.
- **BLOCK:** planejador `workflow plan` recusou os quatro contratos legados por não serem V2. A própria configuração de registro permanece preparada/não submetida.
- **BLOCK na checagem bilíngue lexical:** `workflow audit-language` identificou assinaturas numéricas diferentes entre os relatos, que usam formatos distintos de data, números e localizadores e condensação de frases. Os 13 IDs e os valores clínicos centrais foram conferidos na revisão das duas versões; isso não transforma a checagem automática em pass nem certifica equivalência integral.
- **SKIPPED:** nova busca sistemática, extração integral independente, execução R, reprodução integral, verificação de Docs ao vivo, renderização Word/PDF e submissão.
- **Não inferido:** o pass operacional, o Evidence Lock existente e a suíte de 400 testes descrita no handoff não demonstram validade científica. A suíte não foi reexecutada nesta avaliação documental.

## Método e assistência

Avaliação assistida por OpenAI Codex nesta sessão. Skills utilizadas como estruturas de revisão, sem considerar seus rótulos de aprovação como evidência científica. Referência metodológica da biblioteca `peer-review`, conferida no arXiv e acrescentada somente a este parecer: Kassis T, Agarwal V, He Y, Patel D, Brueckner AM. Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. 2026. [doi:10.48550/arXiv.2609.00065](https://arxiv.org/abs/2609.00065). O artigo descreve a biblioteca, sem demonstrar validade desta revisão específica.
