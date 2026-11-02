> Continuação atual, 2026-11-02: o catálogo local tem 268 skills e cinco índices de fontes externas fixadas. O candidato BYOK em D passou em 99 testes offline focados e não foi ativado. Registro final PROSPERO/OSF revisado é obrigatório antes da execução científica. O kit editorial tem 24 DOCX editáveis e seis perfis datados de revistas; não está pronto para submissão. Consulte [o guia atual](portugues/GUIA_DA_MAQUINA.md) e `maquina_canonica.json`; números anteriores abaixo pertencem aos respectivos snapshots.

# Inventário do Codex científico

Atualizado em 2 de novembro de 2026. Workspace canônico: `D:\Usuario-pc\Projetos\Doutorado`. [Versão inglesa](ingles/INVENTARIO_CODEX.md).

- Codex CLI observado: `0.165.0-alpha.1.2`. Modelo/esforço efetivos da sessão não são comprovados por TOML. Configuração local preservada: Sol/medium/Standard; configuração pessoal tinha outro esforço e não foi alterada.
- Article Machine 0.3.0; 18 projetos encontrados por metadados. Projeto responsável: `article-machine-governance-2026`, bootstrap; smokes não promovem o ciclo científico.
- Registro atual: 267 skills (264 herdadas + 3 locais novas); 65 críticas. Overlay inicial tinha 15 entradas, 12 junctions; três entradas foram acrescentadas. Não somar duplicatas como capacidades independentes.
- Clone amplo herdado tinha 163 skills e HEAD histórico `36d8f13a1e754618794bf42f417884940077b4ae`. Fetch em D: e curadoria seletiva de scikit-learn, pytorch-lightning e scientific-visualization no SHA `5f2bc0341354fd5590aef76a533ada1e1e5b4e62`; status piloto. Nenhum catálogo gigante foi adicionado ao contexto global.
- Três skills próprias: `meta-analise-medica`, `metodos-ml-clinico`, `publicacao-medica-organizada`. Registro, rotas PT/EN, frontmatter e proveniência testados. Novos arquivos ainda não foram commitados.
- Ferramentas instaladas/testadas: Python 3.13.5; scikit-learn 1.9.1; PyTorch 2.15.0+cpu; R 4.6.1; metafor 5.2-1; renv 1.3.1; Quarto 1.10.20. Locks reais nos ambientes isolados em `projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/ambientes`. R 4.5.0 continua no PATH, mas o runner correto é R 4.6.1 em AppData/Local/Programs/R; não usar o PATH sem preflight.
- 78 manifests de plugins em cache no inventário inicial. Há ferramentas de PubMed, ClinicalTrials.gov, openFDA, DailyMed, escrita acadêmica, GitHub e pesquisa disponíveis por metadados da sessão; isso não prova autenticação nem valida cada endpoint. Não foram instalados MCPs redundantes.
- Zotero: binding 0.1.2 existente; readiness reportou API local e connector indisponíveis. Nenhuma biblioteca foi consultada ou alterada.
- K-Dense BYOK permanece em `C:\Users\Usuario-pc\k-dense-byok`, HEAD local `13ba4ad833f8bddd568641e712ead8cfa89b3fd1`, duas alterações rastreadas e uma não rastreada. HEAD remoto observado: `6a55f5ce6f4bd9ac7ff75d01ec20d7f27073a9f0`. Não atualizar por pull sobre essa árvore sem análise própria.

Evidências: `projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/local_audit_correcoes.json`, `fontes_oficiais/heads_verificados_git.json`, `verificacao_final/`, manifestos de migração e locks. O inventário inicial confundiu Python global 3.13.4 com venv 3.13.5 e omitiu o binding Zotero; as correções foram preservadas. Não há auditoria de hardware, exposição de chaves, envio de dados humanos ou prova de produção/aceitação editorial.
