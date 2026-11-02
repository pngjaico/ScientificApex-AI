> Continuação atual, 2026-11-02: o catálogo local tem 268 skills e cinco índices de fontes externas fixadas. O candidato BYOK em D passou em 99 testes offline focados e não foi ativado. Registro final PROSPERO/OSF revisado é obrigatório antes da execução científica. O kit editorial tem 24 DOCX editáveis e seis perfis datados de revistas; não está pronto para submissão. Consulte [o guia atual](portugues/GUIA_DA_MAQUINA.md) e `maquina_canonica.json`; números anteriores abaixo pertencem aos respectivos snapshots.

# Registro de execução e instalação

Consolidação: 2026-11-02. Escopo: nova máquina científica em D:, sem auditoria de hardware, publicação, uso de chaves ou dados humanos. Configurações globais e BYOK não foram alterados.

| Comando/ação | Escopo | Resultado | Evidência/limite |
|---|---|---|---|
| Ler ZIP README→AGENTS→plano→critérios→legado | Pacote | PASS; Pesquisa Aprofundada ausente | Recomendações de hardware não executadas |
| Inventário sanitizado, graphify query, codex --version | Read-only inicial | PASS | local_audit e correções; CLI 0.165.0-alpha.1.2 |
| Criar D:\Doutorado | Primeiro destino | FAIL: escrita negada pelo Windows | Usuário aprovou D:\Usuario-pc\Projetos\Doutorado |
| migrar_para_d.py | Cópia sem apagar origem | PASS: 12.642 arquivos / 1.528.443.834 bytes | SHA-256 iguais; manifesto antes da cópia |
| Correções da cópia | Apenas D: | PASS | Template rastreado restaurado; projeto NMA_OSA_VPI: 92 arquivos / 1.779.862 bytes com hashes; 12 cópias soltas isoladas por manifesto |
| uv sync --locked --offline --all-extras --dev | Venv operacional | PASS: 95 pacotes | Lock original; ambiente reconstruído |
| uv lock / uv sync --locked --no-build | Ambientes ML/DL separados | PASS | scikit-learn 1.9.1, PyTorch 2.15.0+cpu; locks reais |
| CRAN biblioteca local; renv::snapshot | R 4.6.1 isolado | PASS após duas falhas corrigidas | Dependências completadas; lock 16 pacotes; metafor 5.2-1/renv 1.3.1 |
| Quarto ZIP oficial, SHA, extração | ferramentas/quarto-1.10.20 | PASS | SHA 08a6d026877e5fb2c89e5f7e01c018847412993309cb49056e5427014ea5d868 |
| GitHub API / Crossref | Metadados públicos | FAIL parcial e recuperação | API GH timeout; seis HEADs via git ls-remote. PRISMA Crossref 429, confirmado por web; dois DOIs TRIPOD+AI/PROBAST+AI via Crossref |
| Fetch/curadoria K-Dense | 3 skills / 40 arquivos | PASS estático/proveniência; pilot | SHA 5f2bc0341354fd5590aef76a533ada1e1e5b4e62, licenças e backups |
| Integrar 3 skills próprias / rotas PT/EN | Registro D: | PASS | 267 entradas; 16 testes focados e seis rotas; novas skills fora das 65 críticas até versionamento |
| executar_demonstracoes.R / gerar_entregas_bilingues.R | Sintético | PASS | Meta/regressão em R; tabelas/figuras; estimativa e IC conferidos independentemente em Python para tau2=0 |
| clinical_ml_baseline.py | ML isolado | PASS | 180 linhas sintéticas, nested CV/calibração; grupos/tempo/validação externa pendentes |
| executar_dl_sintetico.py | DL CPU isolado | PASS por assertivas/resultados persistidos | 100 iterações, repetição exata; mecânica de gradientes/otimizador |
| quarto render português e inglês | Dois relatórios | PASS | HTML com imagens incorporadas e bibliografia; 11 pares conferidos |
| workflow audit-language / style ptbr-audit | Relatórios PT/EN | PASS | Números/citações preservados; revisão semântica humana exigida |
| Inspeção PNG / tentativa UI | QA | PNGs inspecionados; HTML visual SKIPPED | Navegador local desabilitado no Work; HTML estrutural PASS |
| test_organizar_publicacoes.py | Temporário | PASS: 9 testes | Dry-run, traversal, colisão, 18 subpastas, pares órfãos |
| python -m pytest | Suíte final D: | PASS: 275 passed, 1 skipped | verificacao_final/testes_completos.log; skip de symlink Windows |
| machine audit --strict / skills audit --provenance --strict / generate_skill_docs --check-workspace | Integração final | PASS | verificacao_final/resultado_verificacao.json |
| Zotero readiness / preflight browser | Serviços | SKIPPED/BLOCKED | API indisponível; Playwright não restaurado; biblioteca não acessada |
| Pacote local BYOK com hashes e tarefas PT/EN | Intercâmbio | PREPARADO; execução SKIPPED | governance/intercambio_kdense/demonstracao_2026-11-02 |

A primeira suíte D: teve 256 pass, 1 skip e 1 fail por template omitido; houve correção byte a byte e rerun completo acima. Os smokes iniciais pularam ML/Quarto antes das instalações novas em D:. Snapshots antigos foram preservados.

Nada foi commitado, enviado ao remoto, submetido a revista ou promovido como resultado clínico. Parte dos ambientes/resultados locais está ignorada pelo Git. C: é backup. Novas entregas são bilíngues, com nomes base em português.

Evidências em projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/. Fontes oficiais: [Quarto](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.10.20), [scikit-learn](https://scikit-learn.org/stable/install.html), [PyTorch](https://docs.pytorch.org/), [metafor](https://wviechtb.github.io/metafor/), [renv](https://rstudio.github.io/renv/).

Complemento final: 140 diretórios estruturais de projetos restaurados por metadados. Grafo reconciliado após conferir que apenas raízes legadas/caches estavam ausentes; backup preservado. Novas skills e documentos incluídos: 1.071 nós/2.157 arestas. Defaults de modelos preditivos atualizados para TRIPOD+AI/PROBAST+AI; três templates gerados pela CLI real com contratos validados e locks. 14 testes focados de templates/grafo passaram após essas mudanças.

Rerun definitivo após defaults/templates: **275 passed, 1 skipped**, 81,23 s. Evidência: verificacao_final/testes_completos_apos_templates.log.
