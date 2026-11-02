> Continuação atual, 2026-11-02: o catálogo local tem 268 skills e cinco índices de fontes externas fixadas. O candidato BYOK em D passou em 99 testes offline focados e não foi ativado. Registro final PROSPERO/OSF revisado é obrigatório antes da execução científica. O kit editorial tem 24 DOCX editáveis e seis perfis datados de revistas; não está pronto para submissão. Consulte [o guia atual](portugues/GUIA_DA_MAQUINA.md) e `maquina_canonica.json`; números anteriores abaixo pertencem aos respectivos snapshots.

# Arquitetura final da máquina científica

Workspace canônico local: `D:\Usuario-pc\Projetos\Doutorado`. C: preservado como backup/histórico; K-Dense BYOK separado. Estado: validado localmente apenas no escopo testado, com pendências explícitas. Não há alegação de prontidão clínica, produção, publicação garantida ou CI remoto.

## Camadas

1. Codex coordena requisitos, execução e revisão; configurações não provam modelo/esforço efetivo da sessão. AGENTS.md define projeto ativo e gates.
2. Article Machine 0.3.0 controla contratos, Task Packet, roteamento, Evidence Lock, Review Trinity e exportação condicionada ao modo.
3. Graphify operacional navega código e projetos; não produz evidência científica. Skills são carregadas por intenção, sem biblioteca gigante nova no contexto global.
4. Três skills próprias registradas: meta-analise-medica, metodos-ml-clinico, publicacao-medica-organizada. Três upstream atualizadas em pin verificável, em piloto: scikit-learn, pytorch-lightning, scientific-visualization. Licenças, backups e hashes registrados.
5. Execução isolada: Python principal com uv.lock; ML com scikit-learn 1.9.1; DL com PyTorch 2.15.0+cpu; R 4.6.1 com metafor 5.2-1/renv 1.3.1; Quarto 1.10.20 portátil em ferramentas/. Cada stack tem lock próprio. Não depender do R 4.5.0 encontrado no PATH.
6. Busca e bibliografia: APIs oficiais e ferramentas já expostas, com proveniência por fonte. Zotero tem binding, mas API local indisponível. BYOK recebe apenas pacote local aprovado com manifesto; chaves e dados humanos não entram implicitamente.

## Workflows e publicação

Os quatro fluxos exigidos estão detalhados em [FLUXOS_CIENTIFICOS.md](FLUXOS_CIENTIFICOS.md): A pergunta→busca/deduplicação→Zotero→crítica/extração→manuscrito; B protocolo/dataset→SAP→R→tabelas/figuras→Quarto; C revisão→PRISMA→RoB/GRADE→meta-análise R; D dataset clínico→baseline→ML/DL→validação aninhada/externa/calibração→TRIPOD+AI/PROBAST+AI→artigo.

Entregas novas: projects/<id>/publicacoes/<revista>/<identificador>/ com nove áreas numeradas e subpastas portugues/ingles. Nomes de arquivos em português, duas versões obrigatórias. Código/dados/locks compartilhados; paridade lexical não prova equivalência científica. Modelos reutilizáveis em modelos/aprendizado_de_maquina_clinico, meta_analise_em_r e manuscrito. Congressos continuam em deliverables/ com QA e confirmação de submissão.

## Evidência de capacidade

Suíte completa: 275 passed, 1 skipped. Auditoria estrita da máquina, proveniência de skills e documentação gerada: PASS. Organizador: 9 testes PASS. Demonstrações: meta-análise e regressão em R, concordância numérica independente Python, ML aninhado/calibrado e DL com repetição determinística. Duas versões HTML Quarto renderizadas, 11 pares de arquivos conferidos, números/citações preservados e estilo PT-BR aprovado. Tudo sintético; não é validação clínica nem revisão sistemática concluída.

## Limites restantes

Preflight browser bloqueado: cache e dependências Playwright não foram migrados. QA visual do HTML via UI ficou SKIPPED porque navegador local está desabilitado no Work; gráficos PNG foram inspecionados e HTML conferido estruturalmente. Zotero API e atualização BYOK pendentes. Validação externa, dados agrupados reais, revisões RoB/GRADE, aceitação editorial e submissão dependem de cada estudo. Novos arquivos ainda não commitados; não há prova de clean clone/CI remoto. Não alterar configurações globais nem usar serviços pagos/publicar sem autorização.

Evidência: `projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/verificacao_final/`, locks, manifestos, `resultados_finais/portugues` e `ingles`. A demonstração organizada está no projeto governance/publicacoes/demonstracao-interna/2026-11-02_v01.
