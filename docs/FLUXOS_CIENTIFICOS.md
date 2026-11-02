> Continuação atual, 2026-11-02: o catálogo local tem 268 skills e cinco índices de fontes externas fixadas. O candidato BYOK em D passou em 99 testes offline focados e não foi ativado. Registro final PROSPERO/OSF revisado é obrigatório antes da execução científica. O kit editorial tem 24 DOCX editáveis e seis perfis datados de revistas; não está pronto para submissão. Consulte [o guia atual](portugues/GUIA_DA_MAQUINA.md) e `maquina_canonica.json`; números anteriores abaixo pertencem aos respectivos snapshots.

# Fluxos científicos A–D

Todos os fluxos começam em `projects/<id>/`, lendo project.yaml, protocol.yaml, standards.yaml e compute.yaml. Crie o Task Packet e respeite o modo permitido. Toda entrega tem pares portugues/ingles, com nomes de arquivo em português. Código/dados/locks são compartilhados. A demonstração interna não autoriza análise clínica ou submissão.

## A — Pergunta, busca, Zotero, crítica e manuscrito

1. Defina PICO/PECO, objetivo e critérios antes de buscar. Rode `python -m article_machine workflow plan projects/<id> --query "<pergunta>" --language pt-BR`; gere também o plano en em arquivo separado para não sobrescrever o primeiro.
2. Use as skills query-string-governor, database-retrieval-governor, pubmed-database e literature-search-europepmc. Congele bases, strings completas, datas, filtros e limites; preserve respostas e IDs em sources/. PubMed/Europe PMC e Crossref são fontes de metadados, não prova do claim.
3. Deduplicate por DOI/PMID exato; confira manualmente títulos semelhantes, versões e múltiplas publicações do mesmo estudo. O teste atual cobre só normalização exata de DOI (3 registros viram 2); deduplicação semântica não foi validada.
4. Via zotero-reference-manager, cheque readiness antes de exportar/importar. O binding local existe, mas a API estava indisponível: etapa Zotero PENDENTE. Escrita/importação requer instrução explícita. Não contornar paywalls.
5. Dois revisores verificam elegibilidade e extração; registrar discordâncias, fontes e locators. Revisão crítica com scientific-critical-thinking e peer-review; claims entram no claim_map somente após suporte checado.
6. Manuscrito bilíngue com ptbr-article-writing, bilingual-scientific-writing e anti-ai-writing-governor. Conferir referências, Evidence Lock e Review Trinity. Não chamar busca/triagem executadas só porque há um plano.

## B — Protocolo, dataset, estatística R e Quarto

Defina estimando, unidade experimental, desfechos, missingness, multiplicidade e sensibilidades no SAP antes de resultados. Registre permissão/hash/dicionário do dataset. Execute preflight, use R declarado e renv.lock. Scripts aprovados rodam por `python -m article_machine run-r projects/<id> analysis/<script.R>` no modo permitido. Inspecione pressupostos, estimativas e intervalos, tabelas e gráficos. Gere Quarto nos dois idiomas; renderização não é revisão científica. Exemplo executado: executar_demonstracoes.R em R 4.6.1; validação numérica independente em Python; duas versões HTML renderizadas com Quarto 1.10.20. Verifique idioma com `workflow audit-language` e revisão semântica humana.

## C — Revisão sistemática, PRISMA, RoB/GRADE e meta-análise

Use meta-analise-medica; protocolo registrado/congelado antes da triagem, buscas auditáveis, deduplicação, dupla triagem e extração independente. Separe estudos de relatos; reconcilie PRISMA e motivos de exclusão. Escolha RoB adequado ao desenho, GRADE por desfecho com justificativas e estimando/medida compatível. A síntese R depende de independência, efeito e variância corretos; REML/HKSJ não é escolha universal. Defina sensibilidades para poucos estudos, dependência, heterogeneidade e viés de publicação. Não inventar estudos nem preencher RoB por omissão. O exemplo de quatro efeitos sintéticos testa a mecânica REML/Knapp–Hartung; não representa uma revisão realizada. Texto, tabelas e figuras bilíngues passam Evidence Lock/revisão antes de uso editorial.

## D — Dataset clínico, baseline, ML/DL e artigo

Use metodos-ml-clinico e in-silico-validation-governor. Defina tempo zero/horizonte, preditores disponíveis e desfecho antes de treino. Separe pacientes/grupos/tempo/centros conforme objetivo. Ajuste imputação, seleção, balanceamento, hiperparâmetros e calibração somente no treino; validação interna aninhada e conjunto externo independente. Compare modelo simples, relate AUROC/AUPRC, prevalência, calibração, intervalos e utilidade quando justificável. DL depende da modalidade/pergunta e deve ser comparado com baseline, ablações e análise de erro. TRIPOD+AI é relato; PROBAST+AI julga qualidade/viés/aplicabilidade. Os smokes atuais cobrem 180 linhas independentes para ML e autograd/otimizador determinístico para DL; não validam coortes clínicas, divisão agrupada, benefício assistencial ou validação externa. Manuscrito segue revisão clínica e pacote por revista.

## Pacote para revista

Use organizar_publicacoes.py para criar publicacoes/<revista>/<versao>/ com nove áreas e pares de idioma. Revisar normas oficiais atuais da revista, autoria, ética, disclosure, limites de palavras, arquivos e resolução real das figuras; não presumir aceitação. Congressos continuam em deliverables/ com QA e submissão confirmada. Referências oficiais: https://www.prisma-statement.org/prisma-2020 ; https://www.bmj.com/content/385/bmj-2023-078378 ; https://www.bmj.com/content/388/bmj-2024-082505 ; https://quarto.org/docs/manuscripts/ .
