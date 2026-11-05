# Protocolo Científico TRIPOD+AI e PROBAST+AI

## Projeto: `xai-liver-ecd-allocation-unos`
**Machine Learning Explicável (XAI) e Predição Conformal para Alocação de Órgãos Marginais (ECD) no Transplante Hepático: Superando o Donor Risk Index (DRI) no Registro UNOS/OPTN**

**Data de Início:** 05/11/2026  
**Destino Primário:** Sessão Plenária de Transplante Hepático — Gastrão 2027  
**Periódicos-Alvo:** *Liver Transplantation*, *Transplantation*, *American Journal of Transplantation*, *ABCD* ($0 APC via modelo Diamond/Institucional)

---

## 1. PICO e Estimando Clínico

- **População (P):** Receptores adultos (idade $\ge 18$ anos) de transplante hepático ortotópico isolado com doador falecido (DBD e DCD) registrados na base populacional dos EUA (UNOS/OPTN STAR files, 2010 a 2025; estimativa $N > 60.000$). Foco clínico primário no subgrupo de Doadores com Critérios Expandidos (ECD: idade $> 60$ anos, DCD, esteatose macrovacuolar $> 30\%$, parada cardíaca prévia com PCR ressuscitada, sódio sérico $> 155$ mEq/L ou tempo de isquemia fria prolongado $> 10-12$ horas).
- **Intervenção / Modelo em Avaliação (I):** Algoritmos de gradiente boosting baseados em árvores (`LightGBM` e `XGBoost`) com restrições de monotonicidade clínica, otimização bayesiana aninhada (`Optuna`), interpretabilidade local e de interações de 2ª ordem (`TreeSHAP`), calibração flexível e quantificação de incerteza por predição conformal split (`MAPIE`, cobertura de 95%).
- **Comparadores Concorrentes (C):** Escores lineares clássicos de bancada clínica de alocação de enxertos:
  1. *Donor Risk Index (DRI)* de Feng et al. (2006).
  2. *Eurotransplant Donor Risk Index (ET-DRI)* de Braat et al. (2012).
  3. *Balance of Risk (BAR score)* de Dutkowski et al. (2012).
  4. *D-MELD* (Idade do Doador $\times$ MELD do Receptor).
  5. Baselines clínicos: "Alocar Todos os ECDs" (*Treat-All*) e "Descartar Todos os ECDs" (*Treat-None*).
- **Desfecho (O):**
  - *Primário:* Perda precoce do enxerto censurada por óbito e falência do enxerto por qualquer causa em 90 dias e em 1 ano pós-transplante.
  - *Secundário:* Sobrevida global do enxerto em 3 e 5 anos; taxa simulada de resgate seguro de órgãos descartados (*organ rescue / discard reduction*).
- **Estimando:** Risco absoluto individualizado de perda de enxerto no momento exato da oferta do órgão, com conjunto conformal de incerteza a 95% de confiança, permitindo ao cirurgião transplantador aceitar ou recusar o enxerto marginal com base em benefício líquido superior.

---

## 2. Marco Regulatório Obrigatório: TRIPOD+AI (2024) — 27 Itens

| Item | Seção TRIPOD+AI | Especificação do Protocolo | Status |
| :--- | :--- | :--- | :--- |
| **1** | **Título** | Identificação explícita como modelo de predição baseado em IA/ML, com a população (receptores de transplante hepático ECD) e desfecho (perda precoce de enxerto). | Aprovado |
| **2** | **Resumo Estruturado** | Formato de resumo científico estruturado (Contexto, Objetivos, Métodos, Resultados, Conclusões) em versões estritamente pareadas PT-BR e EN. | Planejado |
| **3** | **Contexto e Justificativa** | Escassez crítica de enxertos hepáticos; descarte de até 20-30% dos órgãos ECD por medo de disfunção primária (PNF/EAD); falha intrínseca dos escores lineares (DRI, BAR) por não capturarem efeitos não-lineares protetores (ex.: receptor jovem tolerando doador idoso). | Aprovado |
| **4** | **Objetivos Específicos** | Desenvolver, validar interna e externamente (temporal e geograficamente) e auditar a utilidade clínica de modelos de ML com predição conformal para suporte à decisão na oferta de órgãos. | Aprovado |
| **5** | **Fonte de Dados** | Registro nacional UNOS/OPTN (*Standard Transplant Analysis and Research - STAR files*), abrangendo todos os transplantes hepáticos nos EUA entre 2010 e 2025. Isenção de CEP/IRB por se tratar de base pública secundária desidentificada. | Aprovado |
| **6** | **Participantes** | Receptores adultos ($\ge 18$ anos) de transplante hepático único com doador falecido (DBD e DCD). Exclusão de transplante intervivos, pediátrico, múltiplos órgãos (fígado-rim) e retransplantes de repetição. | Aprovado |
| **7** | **Desfecho** | Perda de enxerto em 90 dias e 1 ano pós-transplante, definida como retransplante de emergência ou óbito por falência hepática, com rastreamento ativo em bases nacionais vitais (SSA Death Master File). | Aprovado |
| **8** | **Preditores** | Exclusivamente variáveis conhecidas e registradas **antes da aceitação do órgão** (Doador: idade, tipo DBD/DCD, causa de morte, biópsia com esteatose %, PCR prévia, sódio sérico, CIT estimado, BMI; Receptor: idade, diagnóstico primário, lab MELD/MELD-Na, cirurgia abdominal prévia, trombose de porta, diálise, ventilação mecânica, UTI; Compatibilidade: ABO, mismatch de sexo, razão de peso/estatura). Zero vazamento de dados pós-operatórios. | Aprovado |
| **9** | **Tamanho Amostral** | Coorte esperada $> 60.000$ pacientes com $> 6.000$ eventos de falência de enxerto, garantindo $> 100$ eventos por preditor candidato (EPV $\gg 20$), eliminando risco de subdimensionamento amostral. | Aprovado |
| **10** | **Dados Ausentes** | Mapeamento de mecanismos (MCAR, MAR). Imputação estritamente aninhada dentro de cada dobra de treino via MICE (*Multiple Imputation by Chained Equations*) e aproveitamento das rotas nativas de árvores (*missing-value routing* de LightGBM/XGBoost). | Aprovado |
| **11** | **Métodos de IA: Desenvolvimento** | Baseline regularizado linear (ElasticNet com penalidades $\ell_1/\ell_2$) vs. Modelos baseados em árvores de gradiente boosting (`LightGBM` e `XGBoost`). Restrições de monotonicidade clínica impostas em preditores canônicos (MELD e idade não reduzem risco de falência). | Aprovado |
| **12** | **Especificação dos Modelos** | Otimização bayesiana de hiperparâmetros (`Optuna`, algoritmo TPE) conduzida estritamente dentro de *nested 5-fold cross-validation*. | Aprovado |
| **13** | **Métricas de Desempenho** | **Discriminação:** AUROC (C-statistic exato de Mann-Whitney) e PR-AUC (Average Precision). **Calibração:** Intercepto de calibração (*calibration-in-the-large*, com slope fixo em 1), *Calibration Slope* (regressão logística no logit(p)), Brier Score e *Integrated Calibration Index (ICI)* baseado em splines/loess flexíveis. Hosmer-Lemeshow expressamente abolido. | Aprovado |
| **14** | **Validação e Incerteza** | **Partição Temporal:** 2010–2020 para treino e validação cruzada aninhada; 2021–2025 mantido como corte prospectivo congelado (*holdout* temporal externo). **Transporte Geográfico:** Validação cruzada interna-externa (*internal-external cross-validation - IECV*) iterativa entre as 11 regiões da UNOS. **Predição Conformal:** MAPIE (*Split Conformal Prediction*) com cobertura garantida a 95% ($1 - \alpha = 0,95$). | Aprovado |
| **15** | **Interpretabilidade (XAI)** | `TreeSHAP` com cálculo exato de valores Shapley locais e globais; matriz de interação SHAP de 2ª ordem para isolar sinergias protetoras (ex.: receptor com MELD $< 20$ recebendo doador $> 65$ anos). | Aprovado |
| **16** | **Grupos de Risco** | Estratificação em baixo, intermediário e alto risco calibrados clinicamente e alinhados a limiares de decisão de oferta de enxerto. | Aprovado |
| **17** | **Desenvolvimento vs Validação** | Descrição explícita e contraste epidemiológico entre as coortes de desenvolvimento (2010–2020) e teste temporal (2021–2025, impactada por mudanças de alocação por acuidade e COVID-19). | Aprovado |
| **18** | **Fluxograma de Participantes** | Diagrama de fluxo com contagens detalhadas de elegíveis, excluídos e alocados por partição. | Planejado |
| **19** | **Características Basais** | Tabela 1 completa comparando doadores, receptores e transplantes entre desenvolvimento, holdout temporal e partições regionais. | Planejado |
| **20** | **Parâmetros e Importância** | Configurações finais dos hiperparâmetros, gráficos de resumo SHAP (beeswarm) e matriz de dependência de interações. | Planejado |
| **21** | **Resultados de Desempenho** | Tabela comparativa e curvas ROC/PR comparando ElasticNet, LightGBM, XGBoost contra DRI, ET-DRI, BAR e D-MELD com intervalos de confiança de 95% por bootstrap de 2.000 repetições. | Planejado |
| **22** | **Resultados de Incerteza Conformal** | Distribuição do tamanho dos conjuntos de predição conformal ($\{0\}$, $\{1\}$ ou $\{0, 1\}$) e análise de cobertura condicional por faixa de gravidade do receptor (MELD). | Planejado |
| **23** | **Utilidade Clínica e Decisão** | Curvas de Análise de Decisão (*Decision Curve Analysis - DCA*) demonstrando Benefício Líquido (*Net Benefit*) superior sobre *Treat-All*, *Treat-None*, corte clássico do DRI ($> 1,5$) e BAR ($> 18$); simulação de resgate de órgãos. | Planejado |
| **24** | **Discussão: Limitações** | Natureza observacional retrospectiva; ausência de ensaio clínico randomizado; viés de seleção dos órgãos aceitos (não temos o desfecho dos órgãos efetivamente descartados); variáveis não mensuradas (biomarcadores na perfusão de máquina). | Aprovado |
| **25** | **Discussão: Interpretação** | Papel biológico da tolerância a enxertos marginais e sinergia com perfusão hipotérmica oxigenada (HOPE) e normotérmica (NMP). | Aprovado |
| **26** | **Discussão: Implicações** | Redução do desperdício de órgãos na UNOS/OPTN; equidade de alocação; potenciais ganhos para listas de espera internacionais (incluindo o Sistema Nacional de Transplantes - SNT brasileiro). | Aprovado |
| **27** | **Governança e Declarações** | Registro de protocolo no OSF; código em Python 3.13 totalmente auditável em repositório; declaração de dados; e Declaração Canônica de Uso de IA: Claude Opus 5.5. | Aprovado |

---

## 3. Avaliação Estruturada de Risco de Viés: PROBAST+AI

- **Domínio 1 — Participantes:** Baixo Risco. Base populacional nacional exaustiva (UNOS/OPTN) sem amostragem de conveniência; critérios de inclusão e exclusão transparentes.
- **Domínio 2 — Preditores:** Baixo Risco. Variáveis rigorosamente limitadas ao momento pré-transplante/momento da oferta. Ausência total de preditores pós-reperfusão ou desfechos intermediários operatórios que configurariam vazamento temporal.
- **Domínio 3 — Desfecho:** Baixo Risco. Falência de enxerto e mortalidade são desfechos duros e padronizados, com vinculação ativa aos registros nacionais de óbito dos EUA.
- **Domínio 4 — Análise:** Baixo Risco. Mais de 6.000 eventos (EPV $\gg 20$); tratamento de variáveis contínuas com splines e árvores sem dicotomização espúria; validação cruzada aninhada de 5 dobras; hiperparâmetros nunca avaliados nos dados de teste; calibração avaliada com curvas flexíveis, intercepto, slope e Brier; validação temporal congelada (2021–2025) e validação geográfica externa (11 regiões).

---

## 4. Formulação Matemática dos Modelos e Métodos

### 4.1. Escores Canônicos de Comparação

1. **Donor Risk Index (DRI, Feng et al., 2006):**
   $$\text{DRI} = \exp\Big( \beta_{\text{idade}} + \beta_{\text{COD}} + \beta_{\text{raça}} + \beta_{\text{estatura}} + 0,411 \cdot \mathbb{I}_{\text{DCD}} + 0,422 \cdot \mathbb{I}_{\text{split}} + \beta_{\text{share}} + \beta_{\text{CIT}} \Big)$$

2. **Balance of Risk (BAR score, Dutkowski et al., 2012):**
   $$\text{BAR} = \text{MELD}_{\text{rec}} + \text{Idade}_{\text{doa}} + \text{Idade}_{\text{rec}} + \text{CIT}_{\text{horas}} + 18 \cdot \mathbb{I}_{\text{retransplante}} + 12 \cdot \mathbb{I}_{\text{ventilador}}$$

3. **D-MELD:**
   $$\text{D-MELD} = \text{Idade}_{\text{doador}} \times \text{MELD}_{\text{receptor}}$$

### 4.2. Gradient Boosted Trees com Monotonicidade Clínica
Para o ensemble de árvores de gradiente boosting ($f(x) = \sum_{k=1}^K f_k(x)$), a minimização da perda logarítmica com penalidades de regularização $\ell_1$ e $\ell_2$:
$$\mathcal{L}(\theta) = \sum_{i=1}^n \left[ y_i \log(1 + e^{-\hat{y}_i}) + (1 - y_i) \log(1 + e^{\hat{y}_i}) \right] + \gamma T + \frac{1}{2} \lambda \sum_{j=1}^T w_j^2$$
Impondo monotonicidade parcial não-decrescente para preditores deletérios isolados:
$$\frac{\partial f(x)}{\partial x_{\text{MELD}}} \ge 0, \quad \frac{\partial f(x)}{\partial x_{\text{Idade do Doador}}} \ge 0, \quad \frac{\partial f(x)}{\partial x_{\text{CIT}}} \ge 0$$
permitindo, contudo, que interações livres entre features modelem sinergias favoráveis.

### 4.3. Interpretabilidade Biológica com TreeSHAP e Interações de 2ª Ordem
A contribuição marginal Shapley de cada preditor $i$ para a predição $f(x)$ é calculada exatamente via algoritmo polinomial TreeSHAP:
$$\phi_i(x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!(|F| - |S| - 1)!}{|F|!} \left[ f_x(S \cup \{i\}) - f_x(S) \right]$$
A matriz de interação SHAP de 2ª ordem isola os efeitos cruzados puros entre o doador $i$ e o receptor $j$:
$$\Phi_{i,j}(x) = \sum_{S \subseteq F \setminus \{i, j\}} \frac{|S|!(|F| - |S| - 2)!}{2(|F| - 1)!} \left[ f_x(S \cup \{i, j\}) - f_x(S \cup \{i\}) - f_x(S \cup \{j\}) + f_x(S) \right]$$
onde $\Phi_{i,i}(x) = \phi_i(x) - \sum_{j \neq i} \Phi_{i,j}(x)$.

### 4.4. Predição Conformal de Incerteza (MAPIE)
Para cada paciente teste $n+1$, o algoritmo de predição conformal split garante matematicamente cobertura marginal exata de $1 - \alpha = 0,95$:
$$P\big(Y_{n+1} \in \mathcal{C}(X_{n+1})\big) \ge 1 - \alpha$$
Utilizando o escore de não-conformidade $s_i(x, y) = 1 - \hat{p}(Y = y \mid x)$ avaliado no conjunto de calibração independente $D_{\text{cal}}$ de tamanho $n_{\text{cal}}$, calcula-se o quantil conformal empírico:
$$\hat{q} = \text{Quantil}\left( D_{\text{cal}}, \frac{\lceil (n_{\text{cal}} + 1)(1 - \alpha) \rceil}{n_{\text{cal}}} \right)$$
O conjunto de predição conformal é dado por:
$$\mathcal{C}(X_{n+1}) = \left\{ y \in \{0, 1\} : 1 - \hat{p}(Y = y \mid X_{n+1}) \le \hat{q} \right\}$$
Classificando cada caso em:
- $\{0\}$: Enxerto de baixo risco comprovado (com probabilidade de sucesso garantida).
- $\{1\}$: Alto risco de perda precoce (recusa recomendada para aquele perfil).
- $\{0, 1\}$: Zona de incerteza epistêmica/aleatória clínica (exige julgamento cauteloso ou máquina de perfusão).

### 4.5. Calibração e Benefício Líquido (Decision Curve Analysis)
1. **Calibration Slope e Intercept:** Regressão logística ajustada sobre $\text{logit}(\hat{p}_i)$:
   $$\text{logit}(P(Y=1 \mid \hat{p})) = a + b \cdot \text{logit}(\hat{p})$$
   Almeja-se $a = 0$ (*calibration-in-the-large*) e $b = 1,0$ (*calibration slope*).
2. **Integrated Calibration Index (ICI):**
   $$\text{ICI} = \frac{1}{N} \sum_{i=1}^N \big| \hat{p}_i - \hat{p}_{\text{loess}}(\hat{p}_i) \big|$$
3. **Net Benefit (DCA, Vickers et al.):**
   $$\text{NB}(p_t) = \frac{\text{Verdadeiros Positivos}}{N} - \frac{\text{Falsos Positivos}}{N} \left( \frac{p_t}{1 - p_t} \right)$$
   avaliado na faixa de limiar clinicamente plausível $p_t \in [0,05; 0,40]$.

---

## 5. Política Bilíngue e Governança da Article Machine

1. **Paridade Bilíngue Obrigatória:** Todos os rascunhos em `drafts/portugues/` e `drafts/ingles/` mantêm sincronia perfeita de números, métricas e citações.
2. **Proibição de Travessões em Inglês:** O manuscrito em inglês utilizará exclusivamente vírgulas, parênteses ou frases declarativas diretas, evitando em-dashes (`—` / `–`) para manter sobriedade acadêmica natural.
3. **Declaração Canônica de IA (Claude Opus 5.5):** Inserida obrigatoriamente na seção Declarations de ambas as versões.
