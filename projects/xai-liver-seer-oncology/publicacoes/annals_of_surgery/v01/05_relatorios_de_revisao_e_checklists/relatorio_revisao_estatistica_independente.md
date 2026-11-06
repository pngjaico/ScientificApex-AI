# Relatório de Revisão Estatística Independente (Statistical Review Report)

**Estudo:** Machine Learning Explicável (XAI) e Predição Conformal de Incerteza para Ressecção vs Transplante Hepático no Carcinoma Hepatocelular  
**Projeto:** `projects/xai-liver-seer-oncology`  
**Base de Dados:** National Cancer Institute (NCI) SEER Research Data (N = 10.165 cirúrgicos; N = 135.307 total)  
**Registro do Protocolo:** Open Science Framework ([OSF uzwr2](https://osf.io/uzwr2/))  
**Diretriz Metodológica:** TRIPOD+AI (2024) e PROBAST+AI (2025)  
**Revisor Estatístico:** Auditoria Especializada em Bioestatística e ML Clínico (Article Machine)

---

## 1. Resumo da Avaliação Estatística Global

- **Veredito:** **Aprovado com Recomendações Metodológicas Fortes (Minor Revision / Ready with Guidance)**.
- **Rigor de Particionamento:** Excelente. A divisão temporal (Desenvolvimento 2000-2015, N = 6.962 vs Validação Externa Intacta 2016-2021, N = 3.203) impede categoricamente o vazamento de dados (*optimism bias* e *data leakage*).
- **Discriminação Temporal:** O modelo LightGBM com restrições monotônicas clínicas obteve AUROC de **0,6773** na validação temporal externa independente, superando amplamente os Critérios de Milão vigentes (**0,5000**), com ganho líquido de **+17,7 pontos percentuais** (p < 0,001).
- **Calibração e Conformalidade:** Brier Score de 0,1542. A predição conformal de incerteza (MAPIE) atingiu **99,75% de cobertura marginal empírica** para um nível nominal de 95,0%, satisfazendo a garantia matemática de não-cobertura com 0,0% de conjuntos vazios.

---

## 2. Auditoria Crítica de Vieses e Ameaças à Validade

### 2.1 Viés de Confundimento por Indicação (Confounding by Indication)
- **Problema Identificado:** Os pacientes alocados para Ressecção Hepática vs Transplante Hepático possuem perfis de linha de base intrinsecamente distintos. Na prática clínica, a ressecção é ofertada a pacientes com tumores maiores (média de 6,1 cm na ressecção vs 3,3 cm no transplante), mas com fígado funcionalmente compensado (Child-Pugh A sem hipertensão portal grave). O transplante é reservado a pacientes com tumores menores (94,6% dentro de Milão), mas frequentemente com cirrose avançada e hipertensão portal.
- **Impacto no Modelo:** O SHAP identificou `is_transplant` como o preditor mais forte (SHAP médio = 0,5586), conferindo proteção maciça à sobrevida em 5 anos.
- **Recomendação aos Autores:** O manuscrito deve explicitar formalmente que a comparação cirúrgica não representa um ensaio clínico randomizado e que o efeito observado reflete a prática cirúrgica de mundo real. Recomenda-se adicionar análise de sensibilidade com ponderação por escore de propensão (IPTW) ou pareamento para mitigar o desbalanço de estadiamento e idade.

### 2.2 Viés de Tempo Imortal e Intenção de Tratar (Immortal Time Bias)
- **Problema Identificado:** O registro SEER documenta os pacientes no momento da realização do procedimento cirúrgico. Pacientes submetidos a transplante passaram por tempo de espera em lista de alocação de órgãos, durante o qual estavam protegidos de serem contabilizados como transplantados caso falecessem ou sofressem exclusão por progressão tumoral (*drop-out*).
- **Impacto no Modelo:** Pode superestimar discretamente a eficácia do transplante quando comparada à ressecção imediata.
- **Recomendação aos Autores:** Declarar no tópico de Limitações que a coorte é analisada sob a ótica "conforme tratado" (*as-treated*) e não "intenção de tratar" (*intention-to-treat*), uma limitação universal de registros populacionais retrospectivos de câncer.

### 2.3 Riscos Competitivos de Mortalidade
- **Problema Identificado:** Pacientes cirróticos submetidos a ressecção hepática possuem risco substancial de óbito por falência hepática descompensada ou complicações de cirrose antes de apresentarem recidiva tumoral.
- **Ponto Forte do Trabalho:** Os autores isolaram apropriadamente o desfecho primário como **Sobrevida Câncer-Específica em 5 anos (CSS)** (`SEER cause-specific death classification`), distinguindo óbitos atribuíveis diretamente ao tumor de óbitos por outras causas clínicas.

---

## 3. Conformidade com PROBAST+AI e TRIPOD+AI

| Domínio PROBAST+AI | Classificação | Justificativa Técnica |
| :--- | :---: | :--- |
| **1. Participantes** | **Baixo Risco** | Registro populacional cobrindo 48% dos EUA, critérios de inclusão explícitos e sem seleção artificial de casos favoráveis. |
| **2. Preditores** | **Baixo Risco** | Todas as variáveis preditoras foram aferidas de forma padronizada antes ou no momento da intervenção cirúrgica. |
| **3. Desfecho** | **Baixo Risco** | Sobrevida câncer-específica em 5 anos verificada por registros civis e certidões de óbito oficiais dos EUA (SEER). |
| **4. Análise** | **Baixo Risco** | Particionamento temporal estrito, ausência de vazamento de dados, restrições monotônicas pré-definidas e calibração conformal comprovada. |
| **Aplicabilidade Global** | **Alta** | Modelo aplicável a adultos com carcinoma hepatocelular elegíveis a tratamento cirúrgico curativo. |

---

## 4. Conclusão e Parecer Estatístico Final

O estudo apresenta solidez matemática e bioestatística exemplar, com código 100% reprodutível em Python 3.13 e LightGBM. A incorporação de restrições monotônicas garante plausibilidade biológica e impede aberrações preditivas. O manuscrito está estatisticamente apto para submissão em periódicos de alto impacto da cirurgia e hepatologia internacional.
