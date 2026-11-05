# Machine Learning Explicável (XAI) e Predição Conformal de Incerteza para Alocação de Órgãos com Critérios Expandidos no Transplante Hepático: Superando o Donor Risk Index com o Registro Populacional UNOS/OPTN

**Autores:** João Vitor Fiches Machado et al.  
**Conformidade de Relato:** Diretrizes TRIPOD+AI (2024) e PROBAST+AI  
**Registro de Protocolo:** Open Science Framework (OSF Preregistration: `https://osf.io/wq2f7/`, projeto base `https://osf.io/ejw2v/`)

---

## Resumo Estruturado

- **Contexto:** A escassez crítica de enxertos no transplante hepático resulta no descarte frequente de fígados de doadores com critérios expandidos (ECD) e doação após parada circulatória (DCD). Os escores clínicos tradicionais, como o *Donor Risk Index (DRI)* e o *Balance of Risk (BAR score)*, baseiam-se em modelos lineares aditivos que não capturam interações biológicas não-lineares protetoras entre doador e receptor, provocando recusa excessiva de órgãos viáveis.
- **Objetivos:** Desenvolver e validar prospectivamente um modelo explicável de aprendizado de máquina (*gradient boosted trees*) com quantificação conformal de incerteza (MAPIE) para predizer a falência do enxerto em 1 ano e quantificar o benefício líquido clínico no resgate de órgãos descartados.
- **Métodos:** Estudo de coorte observacional nacional baseado nos registros oficiais UNOS/OPTN STAR (2010 a 2025). O particionamento anti-vazamento divide a coorte em desenvolvimento interno (2010 a 2020) com validação cruzada aninhada de 5 dobras (*nested CV* via Optuna) e corte prospectivo temporal externo (2021 a 2025), além de validação cruzada interna-externa (IECV) entre as 11 regiões geográficas da UNOS. Os modelos avaliados incluem regressão logística regularizada (ElasticNet), LightGBM e XGBoost com restrições clínicas de monotonicidade, comparados ao DRI de Feng et al. (2006) e ao escore BAR de Dutkowski et al. (2012). A interpretabilidade foi mapeada via TreeSHAP e matrizes de interação de segunda ordem. A incerteza individual foi calculada via predição conformal split (MAPIE) com garantia matemática de 95% de cobertura. A utilidade clínica foi avaliada por Análise de Curva de Decisão (DCA).
- **Resultados:** Aguardando processamento da extração autorizada dos STAR files da UNOS/OPTN.
- **Conclusões:** Aguardando liberação dos microdados oficiais.

---

## 1. Introdução

O transplante hepático ortotópico permanece como a única terapia curativa definitiva para a insuficiência hepática terminal e para o carcinoma hepatocelular selecionado. No entanto, o descompasso crônico entre a oferta e a demanda de órgãos impõe uma mortalidade significativa em lista de espera. Como resposta a essa crise, a comunidade transplantadora expandiu a utilização de enxertos marginais, denominados Doadores com Critérios Expandidos (ECD: idade avançada, esteatose macrovacuolar, hipernatremia grave, parada cardiorrespiratória prévia e tempo de isquemia fria prolongado) e doadores após parada circulatória (DCD).

A decisão de aceitar ou recusar uma oferta de enxerto marginal ocorre em um ambiente de alta pressão temporal, no qual o cirurgião transplantador deve equilibrar o risco de disfunção primária grave do enxerto contra a probabilidade de o paciente falecer aguardando uma oferta ideal. Historicamente, essa tomada de decisão é subsidiada por escores estatísticos lineares de risco do doador, destacando-se o *Donor Risk Index (DRI)* de Feng et al. (2006) e, subsequentemente, escores de compatibilidade como o *Balance of Risk (BAR score)* de Dutkowski et al. (2012) e o *Eurotransplant DRI (ET-DRI)* de Braat et al. (2012).

Contudo, tais escores lineares tradicionais apresentam limitações metodológicas intrínsecas graves. Por serem baseados em modelos de riscos proporcionais de Cox univariados ou aditivos simples, assumem que o impacto deletério de cada fator do doador atua de forma constante em qualquer receptor. Na prática clínica, a biologia do transplante hepático é governada por complexas interações não-lineares. Um receptor jovem, ambulatorial, com MELD laboratorial baixo (< 18), frequentemente tolera com segurança um enxerto de doador idoso ou esteatótico, ao passo que a mesma oferta implantada em um receptor em choque, intubado e com MELD > 35 precipita falência primária catastrófica. Ao ignorar essas sinergias protetoras e deletérias, o DRI e o BAR score superestimam sistematicamente o risco em receptores de baixa acuidade, induzindo o descarte desnecessário de órgãos viáveis.

O aprendizado de máquina moderno (*Machine Learning*) oferece algoritmos baseados em árvores de gradiente boosting capazes de aprender interações não-lineares multidimensionais. Todavia, a adoção clínica de modelos de inteligência artificial em transplante enfrenta dois obstáculos principais: a falta de interpretabilidade das predições ("caixa-preta") e a emissão de probabilidades pontuais que transmitem uma falsa sensação de certeza cirúrgica. 

Este estudo aborda diretamente essas lacunas fundamentais por meio de uma abordagem metodológica tripartite:
1. **Modelagem Não-Linear com Monotonicidade:** Emprego de árvores de gradiente boosting com restrições formais de monotonicidade clínica, garantindo que preditores sabidamente deletérios (como acuidade do MELD e isquemia fria) nunca recebam pesos contraditórios;
2. **Interpretabilidade Biológica Explicável (XAI):** Mapeamento exato de valores Shapley locais e matrizes de interação de segunda ordem via TreeSHAP, isolando as combinações específicas doador-receptor que viabilizam o resgate seguro de enxertos;
3. **Predição Conformal de Incerteza (MAPIE):** Implementação de predição conformal split para fornecer conjuntos de predição com cobertura de probabilidade matematicamente garantida a 95%, distinguindo com precisão enxertos seguros em preservação estática daqueles que necessitam de perfusão hipotérmica oxigenada (HOPE/NMP).

Conduzido em estrita conformidade com as diretrizes internacionais TRIPOD+AI (2024) e com o instrumento PROBAST+AI, este estudo utiliza o registro populacional nacional UNOS/OPTN para demonstrar a superioridade estatística e clínica dos modelos explicáveis sobre o DRI, BAR score e D-MELD.

---

## 2. Métodos

### 2.1. Desenho do Estudo e Governança Ética
Trata-se de um estudo de coorte retrospectivo observacional de base populacional nacional, desenhado para desenvolvimento e validação prospectiva temporal de modelos preditivos multivariáveis com inteligência artificial, segundo os 27 itens do checklist TRIPOD+AI (2024) e critérios de qualidade do PROBAST+AI.

O protocolo do estudo foi pré-registrado de forma imutável e transparente na plataforma Open Science Framework (OSF Preregistration: `https://osf.io/wq2f7/`, repositório base `https://osf.io/ejw2v/`). Por utilizar microdados desidentificados e anonimizados de registro nacional secundário sem possibilidade de reidentificação de doadores, receptores ou equipes médicas, o estudo é qualificado como isento de aprovação presencial por Comitê de Ética em Pesquisa nos termos da regulamentação federal norte-americana 45 CFR 46.104(d)(4) e das resoluções éticas vigentes no Brasil para bases públicas desidentificadas. O acesso aos dados cumpre integralmente os requisitos do *OPTN Data Use Agreement*.

### 2.2. Fonte de Dados e População Elegível
Os dados brutos provêm dos arquivos oficiais *Standard Transplant Analysis and Research (STAR files)* da *Organ Procurement and Transplantation Network (OPTN)* e do *Scientific Registry of Transplant Recipients (SRTR)*, que consolidam os dados de todos os transplantes hepáticos realizados nos Estados Unidos.

**Critérios de Inclusão:**
- Receptores adultos (idade $\ge 18$ anos na data do transplante);
- Transplante hepático ortotópico com enxerto de doador falecido (Doação após Morte Encefálica - DBD ou Doação após Parada Circulatória - DCD);
- Transplantes realizados entre 1º de janeiro de 2010 e 31 de dezembro de 2025, com seguimento pós-operatório documentado.

**Critérios de Exclusão:**
- Receptores pediátricos (< 18 anos);
- Transplante com doador vivo (LDLT) ou transplante dominó;
- Transplantes multiviscerais ou combinados de múltiplos órgãos (ex.: fígado-rim, fígado-coração, fígado-pulmão);
- Retransplantes de repetição (> 2º transplante);
- Casos com ausência de registro do status do enxerto ou sobrevida em 1 ano.

### 2.3. Particionamento Anti-Vazamento (Zero Data Leakage)
A coorte nacional foi particionada estritamente pelo identificador único do paciente (`patient_id`), impedindo qualquer vazamento entre partições de treino, calibração e teste:
1. **Coorte de Desenvolvimento (2010 a 2020):** Dedicada à harmonização de variáveis, imputação de dados ausentes, validação cruzada aninhada de 5 dobras (*nested 5-fold cross-validation*), ajuste de hiperparâmetros com Optuna e determinação dos quantis conformais na partição de calibração independente (subdivisão 80/20);
2. **Corte Prospectivo Temporal Congelado (2021 a 2025):** Mantido intacto como partição externa de validação temporal. Este corte temporal funciona como um teste de estresse rigoroso sobre a transportabilidade temporal do algoritmo, visto que opera inteiramente sob a nova política nacional de alocação por *Acuity Circles* (implementada em fevereiro de 2020) e do MELD 3.0 (2023);
3. **Validação Geográfica Externa (IECV):** Validação cruzada interna-externa iterativa entre as 11 regiões geográficas da UNOS, avaliando a robustez do algoritmo a variações regionais de prática cirúrgica e logística de transporte.

### 2.4. Preditores Clínicos Candidatos
Todos os preditores foram estritamente restritos a variáveis conhecidas e registradas **antes da aceitação do órgão** pelo centro transplantador (ponto zero da decisão clínica). Nenhuma variável transoperatória posterior à revascularização ou pós-operatória precoce foi incluída, blindando o modelo contra viés de incorporação temporal.

- **Doador:** Idade contínua (anos), tipo de doador (DBD vs. DCD), causa do óbito (anóxia, trauma encefálico, acidente vascular encefálico, outros), percentual de esteatose macrovacuolar em biópsia hepática, indicador binário de realização de biópsia (*indication biopsy flag*), histórico de parada cardiorrespiratória com ressuscitação prévia, pico sérico terminal de sódio (mEq/L), tempo de isquemia fria (CIT, horas), tempo de isquemia morna do doador (WIT, minutos, para DCD), índice de massa corporal do doador (BMI, kg/m²), transaminases séricas (AST/ALT) e contagem de drogas vasoativas inotrópicas;
- **Receptor:** Idade na data do transplante (anos), diagnóstico etiológico primário (MASH/esteato-hepatite dismetabólica, hepatopatia alcoólica, infecção crônica por vírus C, vírus B, doenças colestáticas, carcinoma hepatocelular isolado), MELD laboratorial no transplante, MELD-Na laboratorial no transplante, cirurgia abdominal prévia, trombose de veia porta e seu grau, dependência de ventilação mecânica no transplante, suporte dialítico / hemodiálise pré-transplante nos 7 dias anteriores, internação prévia em UTI no transplante, BMI do receptor, grau de ascite e presença de encefalopatia hepática clínica;
- **Matching Doador-Receptor:** Compatibilidade do sistema ABO (idêntico, compatível, incompatível), compatibilidade de sexo biológico (mismatch de gênero), razão entre peso do receptor e peso do doador, razão de estaturas e tipo de alocação geográfica (local, regional ou nacional).

### 2.5. Tratamento de Dados Ausentes
O mecanismo de dados ausentes foi investigado sistematicamente (MCAR, MAR, MNAR). Para preditores com ausência explicável por covariáveis basais (MAR), utilizou-se imputação múltipla por equações encadeadas (MICE) executada estritamente dentro das dobras de treinamento da validação aninhada, sem vazamento para as dobras de validação ou teste temporal. Para a biópsia de doador, cuja ausência obedece a um viés seletivo de indicação clínica (*Missing Not at Random* - MNAR, pois fígados de aparência macroscópica homogênea raramente são biopsiados), incluiu-se a covariável binária de realização de biópsia combinada ao roteamento nativo de *missing values* das árvores de gradiente boosting.

### 2.6. Desfechos Clínicos
- **Desfecho Primário:** Perda precoce do enxerto em 1 ano pós-transplante, definida como desfecho composto de falência primária ou secundária do enxerto demandando retransplante de emergência ou óbito do receptor por qualquer causa dentro de 365 dias do implante (desfecho canônico mandatário da OPTN/UNOS), associado à perda em 90 dias pós-transplante;
- **Desfechos Secundários:** Falência do enxerto censurada por óbito (*death-censored graft loss*), modelada formalmente sob riscos competitivos (Fine-Gray, tratando óbito com enxerto funcionante como evento concorrente); sobrevida global do enxerto aos 3 e 5 anos; e taxa simulada de resgate seguro de enxertos marginais descartados.

### 2.7. Algoritmos e Otimização de Hiperparâmetros
Foram comparadas três famílias algorítmicas de predição:
1. **Baseline Paramétrico:** Regressão logística com regularização ElasticNet (penalidades $\ell_1$ e $\ell_2$), combinada a splines cúbicas restritas para capturar curvatura básica em preditores contínuos;
2. **LightGBM Classifier:** Ensemble de árvores de gradiente boosting com particionamento histograma-based e suporte nativo a dados categóricos e rotas de missingness;
3. **XGBoost Classifier com Restrições Clínicas de Monotonicidade:** Implementação de gradiente boosting impondo restrições direcionadas não-decrescentes em fatores sabidamente deletérios isolados ($\partial f(x)/\partial x_{\text{MELD}} \ge 0$, $\partial f(x)/\partial x_{\text{Idade do Doador}} \ge 0$ e $\partial f(x)/\partial x_{\text{CIT}} \ge 0$), enquanto as interações de segunda ordem com outros parâmetros permanecem livres para capturar efeitos protetores.

A otimização de hiperparâmetros foi conduzida por validação cruzada aninhada de 5 dobras com o algoritmo bayesiano TPE (*Tree-structured Parzen Estimator*) via biblioteca Optuna, minimizando a perda logarítmica e maximizando a área sob a curva de precisão-revocação (PR-AUC).

### 2.8. Escores Canônicos de Bancada (Benchmarking Clínico)
Todos os modelos foram formalmente comparados contra as quatro ferramentas canônicas utilizadas na prática internacional de alocação hepática:
1. **Donor Risk Index (DRI, Feng et al., 2006):** Calculado a partir da formulação canônica com beta-coeficientes ajustados para idade do doador, causa de óbito, raça, estatura, DCD, fígado dividido, compartilhamento e CIT;
2. **Eurotransplant DRI (ET-DRI, Braat et al., 2012);**
3. **Balance of Risk (BAR score, Dutkowski et al., 2012):** Calculado pela soma ponderada de MELD, idades do receptor e do doador, CIT, suporte ventilatório e retransplante;
4. **D-MELD:** Produto direto entre a idade do doador e o MELD laboratorial do receptor.

### 2.9. Interpretabilidade Biológica com TreeSHAP
A interpretabilidade biológica das predições foi extraída utilizando o framework SHAP (*SHapley Additive exPlanations*). Empregou-se o algoritmo exato TreeSHAP para calcular os valores locais de contribuição Shapley de cada preditor para cada paciente. Além do impacto global, calculou-se a matriz de interações de segunda ordem ($\Phi_{i,j}(x)$), permitindo decompor o efeito conjunto de pares críticos de variáveis (em especial, Idade do Doador $\times$ MELD do Receptor, e CIT $\times$ MELD).

### 2.10. Quantificação Conformal de Incerteza (MAPIE)
Para superar a limitação de emitir probabilidades pontuais que omitem a incerteza epistêmica e aleatória, aplicou-se a teoria de Predição Conformal (*Split Conformal Prediction*) via biblioteca MAPIE:
$$P\big(Y_{n+1} \in \mathcal{C}(X_{n+1})\big) \ge 1 - \alpha$$
com taxa de erro fixada em $\alpha = 0,05$ (garantia matemática de 95% de cobertura marginal no teste temporal). O escore de não-conformidade $s_i = 1 - \hat{p}(Y = y \mid x)$ foi avaliado na partição independente de calibração ($D_{\text{cal}}$, 20% do desenvolvimento), permitindo emitir para cada paciente do teste prospectivo um conjunto conformal:
- $\{0\}$: Enxerto compatível de baixo risco, com probabilidade formal de sucesso em preservação estática a frio (SCS);
- $\{1\}$: Risco proibitivo de perda precoce, indicando recusa justificada para aquele receptor específico;
- $\{0, 1\}$: **Zona de Incerteza Conformal**, identificando os enxertos marginais que não devem ser descartados sumariamente, mas sim encaminhados para teste funcional e recondicionamento em máquina de perfusão hipotérmica oxigenada (HOPE) ou normotérmica (NMP).

### 2.11. Métricas de Avaliação e Análise de Decisão Clínica (DCA)
A avaliação metodológica seguiu as recomendações de Harrell e Steyerberg para modelos preditivos clínicos:
- **Discriminação:** Área sob a Curva ROC (AUROC) com intervalos de confiança de 95% calculados por bootstrap de 2.000 repetições e teste de DeLong para comparação pareada contra o DRI; e Área sob a Curva de Precisão-Revocação (PR-AUC);
- **Calibração:** Calibração gráfica contínua estimada por suavizadores loess/splines; intercepto de calibração (*calibration-in-the-large*, com inclinação fixada em 1,0); inclinação de calibração (*calibration slope*, obtido por regressão logística sobre o logit da probabilidade predita); Brier Score; e o *Integrated Calibration Index (ICI)*. O teste de Hosmer-Lemeshow foi expressamente abolido conforme as diretrizes TRIPOD+AI;
- **Análise de Curva de Decisão (DCA):** Cálculo do Benefício Líquido (*Net Benefit*) de Vickers et al. para avaliar o impacto clínico da alocação baseada no modelo em comparação com as estratégias default ("Alocar Todos os Enxertos", "Descartar Todos os Enxertos Marginais") e com a alocação guiada pelos pontos de corte tradicionais do DRI e do escore BAR, em limiares de decisão clinicamente plausíveis ($p_t \in [0,05; 0,35]$).

---

## 3. Resultados
*(Esta seção aguarda a ingestão e o processamento dos microdados brutos oficiais UNOS/OPTN STAR em sources/unos_star/)*

- **Tabela 1:** Características Basais da Coorte de Desenvolvimento e Teste Temporal: `{{metric:tabela_01_baseline}}`
- **Discriminação Comparativa (AUROC):**
  - XGBoost Monotônico: `{{metric:auroc_xgboost}}`
  - LightGBM: `{{metric:auroc_lightgbm}}`
  - Baseline ElasticNet: `{{metric:auroc_elasticnet}}`
  - Donor Risk Index (DRI): `{{metric:auroc_dri_feng}}`
  - Balance of Risk (BAR score): `{{metric:auroc_bar_dutkowski}}`
- **Calibração e Ajuste Estatístico:**
  - Calibration Slope (XGBoost): `{{metric:calibration_slope_xgboost}}`
  - Calibration Intercept (XGBoost): `{{metric:calibration_intercept_xgboost}}`
  - Brier Score (XGBoost): `{{metric:brier_score_xgboost}}`
  - Brier Score (DRI): `{{metric:brier_score_dri}}`
- **Incerteza Conformal e Utilidade Clínica:**
  - Cobertura Conformal Empírica (Alvo 95%): `{{metric:conformal_empirical_coverage}}%`
  - Tamanho Médio do Conjunto Conformal: `{{metric:conformal_mean_set_size}}`
  - Enxertos na Zona de Incerteza Conformal {0, 1}: `{{metric:conformal_uncertain_zone_pct}}%`
  - Benefício Líquido DCA no Limiar de 15% (ML): `{{metric:dca_net_benefit_thresh_15}}`
  - Benefício Líquido DCA no Limiar de 15% (DRI): `{{metric:dca_net_benefit_dri_thresh_15}}`

---

## 4. Discussão
*(A ser expandida após o fechamento analítico com os dados autorizados da UNOS/OPTN)*

---

## 5. Declarações

- **Registro do Protocolo:** O protocolo deste estudo está registrado no Open Science Framework (OSF Preregistration: `https://osf.io/wq2f7/`, projeto base `https://osf.io/ejw2v/`), submetido sob as diretrizes TRIPOD+AI e PROBAST+AI.
- **Disponibilidade de Dados e Código:** O código-fonte em Python e os pipelines analíticos estão versionados no repositório do estudo. Os dados brutos da UNOS/OPTN são regidos por acordo DUA e podem ser solicitados formalmente ao SRTR/OPTN.
- **Conflitos de Interesse:** Os autores declaram não possuir conflitos de interesse comerciais, financeiros ou políticos relacionados a este trabalho.
- **Financiamento:** Este estudo foi conduzido no âmbito do programa acadêmico de pós-graduação, sem financiamento comercial de entidades farmacêuticas ou fabricantes de máquinas de perfusão.
- **Uso de Inteligência Artificial e Tecnologias Assistidas por IA na Redação Científica:** Durante a preparação deste trabalho, os autores utilizaram Claude Opus 5.5 (Anthropic) para auxiliar no polimento do idioma inglês, refinamento gramatical, correções tipográficas e formatação do layout de tabelas. Após o uso desta ferramenta, os autores revisaram criticamente, verificaram e editaram todo o conteúdo gerado e assumem total responsabilidade pela integridade científica, precisão factual e conclusões apresentadas neste manuscrito. Em conformidade com os critérios de autoria das revistas-alvo, tecnologias de IA generativa não são listadas como autores.
