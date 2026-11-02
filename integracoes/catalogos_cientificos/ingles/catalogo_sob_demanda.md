# On-demand catalog — five scientific sources

This is a lookup gateway, not an installation. Keep skill names/IDs identical in Portuguese and English so search remains stable. A repository entry alone does not validate a skill.

| PT-BR intent | English intent | Source/IDs to inspect | Local guidance |
|---|---|---|---|
| Análise científica, validação analítica, unidades e incerteza | Scientific analysis, analytical method validation, units and uncertainty | K-Dense: `analytical-method-validation`, `uncertainty-and-units`, `statistical-analysis` | The first two are isolated trial candidates. `statistical-analysis` already exists locally by slug. |
| Pesquisa médica, relatório clínico e suporte à decisão | Medical research, clinical reporting and decision support | K-Dense: `clinical-reports`, `clinical-decision-support`; DenDen: same IDs | Medical slugs already exist locally. Do not add copies. DenDen has high slug overlap and an older snapshot. |
| Revisão sistemática, triagem e meta-análise | Systematic review, screening and meta-analysis | Imbad: `sr-screener`; K-Dense/DenDen: `statistical-analysis`; local: `meta-analise-medica`, `risk-of-bias-assistant`, `extraction-schema-governor`, `grade-sof-table-builder`, `asreview-screening-bridge`, `protocol-registration-governor` | Prefer local contracts. `sr-screener` frontmatter was not read and Imbad’s family is Claude Code–centered. No external increment was confirmed. |
| Aprendizado de máquina e profundo | Machine learning and deep learning | Orchestra: `ml-paper-writing`, `pytorch-lightning`, `rigor-reviewer`; K-Dense: `pytorch-lightning`, `transformers` | The local catalog already has `metodos-ml-clinico`, `scikit-learn`, `pytorch-lightning`, `transformers`, and governance. `ml-paper-writing` is a candidate only for a paper with a defined ML venue. |
| Redação de artigo médico PT-BR/EN, referências e revisão | Medical manuscript drafting, citations and review | Orchestra: `ml-paper-writing`; Imbad: `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`; local: `scientific-writing`, `bilingual-scientific-writing`, `ptbr-article-writing`, `manuscript-integrity-response-governor`, `academic-office-deliverables` | Prefer local skills first. Orchestra can be evaluated for ML papers. Imbad may inform workflow design, subject to license and portability limits. |
| Descoberta de catálogos e fontes de skills | Discovery of skill catalogs and sources | InternScience: index of 30 submodules; DenDen: catalog similar to K-Dense | InternScience has no `SKILL.md` of its own. Follow a link to its upstream, pin that SHA, and check its license before use. |

## Minimum useful set by intent

- **Medical research / Pesquisa médica:** local `clinical-decision-support`, `clinical-reports`, `pubmed-database`, `clinical-trials-database`, and `guideline-router`. Use external retrieval on demand and record provenance in the project.
- **Systematic review and meta-analysis / Revisão sistemática e meta-análise:** local `protocol-registration-governor`, `extraction-schema-governor`, `asreview-screening-bridge`, `risk-of-bias-assistant`, `meta-analise-medica`, and `grade-sof-table-builder`. Database or plugin output is not final proof without Evidence Lock.
- **Clinical ML and deep learning / ML clínico e DL:** local `metodos-ml-clinico`, `scikit-learn`, `pytorch-lightning`, `transformers`, and `statistical-analysis`; cover leakage, calibration, external validation, and utility in the project contracts. Do not start cloud work without ComputeContract/preflight.
- **Bilingual medical drafting / Draft médico bilíngue:** local `scientific-writing`, `bilingual-scientific-writing`, `ptbr-article-writing`, `manuscript-integrity-response-governor`, and `academic-office-deliverables`. Evidence and references remain subject to Evidence Lock.

## How to consult

1. Define the task and an active project; read its contracts.
2. Use [`manifesto_das_fontes.json`](../manifesto_das_fontes.json) for repository, SHA, license, and local path.
3. All names and paths are in [`inventario_de_habilidades.json`](../inventario_de_habilidades.json). Unread content is marked `tree_only`.
4. Before adapting a skill, inspect commands, `allowed-tools`, scripts, APIs/cloud, checkpoints, writes, and per-file terms.
5. Propose integration only after an intent-specific benchmark against the local route, including failures and independent evaluation.
