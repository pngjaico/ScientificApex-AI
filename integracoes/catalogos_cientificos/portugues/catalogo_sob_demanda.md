# Catálogo sob demanda — cinco fontes científicas

Este é um gateway de consulta, não uma instalação. Use nomes/IDs de skills iguais em português e inglês para manter a busca estável. Nenhum item desta tabela está validado apenas por constar em um repositório.

| Intenção PT-BR | English intent | Fonte/IDs para consulta | Orientação local |
|---|---|---|---|
| Análise científica, validação analítica, unidades e incerteza | Scientific analysis, analytical method validation, units and uncertainty | K-Dense: `analytical-method-validation`, `uncertainty-and-units`, `statistical-analysis` | Os dois primeiros são candidatos a ensaio isolado. `statistical-analysis` já tem slug local. |
| Pesquisa médica, relatório clínico e suporte à decisão | Medical research, clinical reporting and decision support | K-Dense: `clinical-reports`, `clinical-decision-support`; DenDen: mesmos IDs | Os slugs médicos já existem localmente. Não adicionar cópias. DenDen tem grande sobreposição nominal e snapshot mais antigo. |
| Revisão sistemática, triagem e meta-análise | Systematic review, screening and meta-analysis | Imbad: `sr-screener`; K-Dense/DenDen: `statistical-analysis`; local: `meta-analise-medica`, `risk-of-bias-assistant`, `extraction-schema-governor`, `grade-sof-table-builder`, `asreview-screening-bridge`, `protocol-registration-governor` | Preferir contratos locais. `sr-screener` não teve frontmatter lido e a família Imbad é Claude Code–centrada. Nenhum incremento externo foi confirmado. |
| Aprendizado de máquina e profundo | Machine learning and deep learning | Orchestra: `ml-paper-writing`, `pytorch-lightning`, `rigor-reviewer`; K-Dense: `pytorch-lightning`, `transformers` | O catálogo local já tem `metodos-ml-clinico`, `scikit-learn`, `pytorch-lightning`, `transformers` e governança. `ml-paper-writing` é candidato só para paper de ML com venue definido. |
| Redação de artigo médico PT-BR/EN, referências e revisão | Medical manuscript drafting, citations and review | Orchestra: `ml-paper-writing`; Imbad: `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`; local: `scientific-writing`, `bilingual-scientific-writing`, `ptbr-article-writing`, `manuscript-integrity-response-governor`, `academic-office-deliverables` | Priorizar skills locais. Orchestra pode ser avaliado para artigos de ML. Imbad pode informar desenho, com restrições de licença e portabilidade. |
| Descoberta de catálogos e fontes de skills | Discovery of skill catalogs and sources | InternScience: índice de 30 submódulos; DenDen: catálogo próximo de K-Dense | InternScience não tem `SKILL.md` próprio. Siga o link até o upstream, fixe seu SHA e confira sua licença antes de qualquer uso. |

## Conjunto mínimo por intenção

- **Pesquisa médica / Medical research:** local `clinical-decision-support`, `clinical-reports`, `pubmed-database`, `clinical-trials-database`, `guideline-router`. Use retrieval externo sob demanda com proveniência no projeto.
- **Revisão sistemática e meta-análise / Systematic review and meta-analysis:** local `protocol-registration-governor`, `extraction-schema-governor`, `asreview-screening-bridge`, `risk-of-bias-assistant`, `meta-analise-medica`, `grade-sof-table-builder`. Saída de banco ou plugin não é prova final sem Evidence Lock.
- **ML clínico e DL / Clinical ML and deep learning:** local `metodos-ml-clinico`, `scikit-learn`, `pytorch-lightning`, `transformers` e `statistical-analysis`; cobrir leakage, calibração, validação externa e utilidade nos contratos do projeto. Não iniciar cloud sem ComputeContract/preflight.
- **Draft médico bilíngue / Bilingual medical drafting:** local `scientific-writing`, `bilingual-scientific-writing`, `ptbr-article-writing`, `manuscript-integrity-response-governor`, `academic-office-deliverables`. Evidência e referências continuam sujeitas a Evidence Lock.

## Como consultar

1. Defina uma tarefa e um projeto ativo; leia seus contratos.
2. Consulte [`manifesto_das_fontes.json`](../manifesto_das_fontes.json) para repositório, SHA, licença e caminho local.
3. Nomes/caminhos completos estão em [`inventario_de_habilidades.json`](../inventario_de_habilidades.json). Conteúdo não lido aparece como `tree_only`.
4. Antes de adaptar qualquer skill, revise comandos, `allowed-tools`, scripts, APIs/cloud, checkpoints, gravações e termos por arquivo.
5. Só propor integração depois de benchmark por intenção contra a rota local, incluindo falhas e avaliação independente.
