# Validação local e passagem de contexto

03/11/2026. Projeto canônico: `D:/Usuario-pc/Projetos/Doutorado/projects/mandaqui-ifabp-programa-2026`. Os novos relatórios têm pares PT/EN com nomes iguais. Os originais em C: foram preservados.

## PASS

- Suíte completa da máquina em D:: **417 passed, 1 skipped**, 239,66 segundos. Valida software no escopo dos testes; não mérito clínico ou produção.
- Auditoria de skills `--strict --provenance`: **269 skills**, sem issues. Skill FAPESP/CNPq registrada, roteada e exposta por junction apontando para D:; cópia com hashes e backups de controle.
- Validador da skill: válido. Documentação gerada: sem drift. Grafo operacional regenerado, sem extração semântica do corpus bruto.
- Verificador da entrega: **30 linhas C01–C30**, pares de arquivos presentes, protocolo draft, registro pending, nenhum claim promovido e nenhum corpus formal em D:.
- Auditoria bilíngue dos dois documentos principais: PASS para assinaturas numéricas; `gate_eligible: false` e revisão semântica continuam explícitos.
- Preflight passa para o planejamento com Python local. Não houve análise R nem QA visual por navegador. O preflight opcional detectou R 4.5.0 no PATH e navegador sem instalação no cache de D:, portanto não prova o ambiente R/visual pronto.

## BLOCK esperado / SKIPPED

- Avanço a `corpus-build`: **BLOCK esperado** por protocolo não congelado, registro não verificado e plano de busca formal ausente. Nenhum modo foi avançado à força.
- Execução clínica, corpus/triagem/extração, análise de pacientes, manuscrito de resultados, Evidence Lock de claims clínicos e Review Trinity de submissão: **não executados**, pois não há registro final/dados/protocolo pronto. Não tratar a suíte de software como aprovação desses gates.
- FAPESP, ética, OSF/PROSPERO, revista e parceiros: nenhum envio externo, aceite ou cadastro realizado.

## Revisão científica independente final

O revisor leu o programa e a carteira final sem pesquisa ou análise de dados. Não identificou erro fatal novo nem promessa indevida de dezenas de papers; considerou o planejamento coerente **de forma condicional**. As duas pendências principais são demonstrar viabilidade local e operacionalizar o estimando (T0, histologia/adjudicação, eventos e ausentes). Isso não aprova novidade, mérito, protocolo ou execução.

## Próxima ação

Preparar inventário agregado autorizado de fluxo/eventos e compromisso de laboratório/imagem/seguimento, obter cotações e confirmar programa/vínculos. Depois fechar os protocolos, plano amostral e registro final verificável. Priorizar o mestrado analítico e estudos de confiabilidade/fluxo enquanto a tese principal se estrutura, respeitando seus próprios gates.

Arquivos fora deste escopo já existentes no worktree foram preservados. Checkpoint deve incluir apenas os caminhos explicitamente selecionados desta entrega, sem backup de controle, segredos ou dados brutos. O estado global sujo preexistente não deve ser descrito como clone limpo.
