# Machine Learning Explicável (XAI) e Predição Conformal para Ressecção Cirúrgica versus Transplante Hepático no Carcinoma Hepatocelular: Superando os Critérios de Milão e o Estadiamento TNM (AJCC 8ª Edição) com o Registro Populacional SEER (N > 60.000)

**Autores:** João Vitor Fiches Machado e colaboradores  
**Registro do Protocolo (OSF):** [https://osf.io/uzwr2/](https://osf.io/uzwr2/) (*ID: uzwr2*, Schema OSF Preregistration)  
**Diretriz de Relato:** TRIPOD+AI (2024) / PROBAST+AI  

---

## Resumo Estruturado

- **Contexto:** A escolha cirúrgica entre ressecção hepática parcial e transplante hepático ortotópico no carcinoma hepatocelular (HCC) depende historicamente de sistemas lineares rígidos de estadiamento, com destaque para os Critérios de Milão (Mazzaferro et al., 1996) e o estadiamento TNM da AJCC 8ª Edição. Esses sistemas baseiam-se em pontos de corte univariados estáticos de diâmetro tumoral e contagem de nódulos, falhando em capturar a biologia tumoral agressiva ou interações não-lineares protetoras entre alfa-fetoproteína (AFP), invasão microvascular e reserva funcional hepática.
- **Objetivos:** Desenvolver e validar prospectivamente um modelo explicável de aprendizado de máquina em gradiente boosting (LightGBM/XGBoost com restrições monotônicas clínicas) e predição conformal de incerteza (MAPIE), avaliando seu Benefício Líquido Clínico em Análise de Curva de Decisão (DCA) e comparando seu desempenho diretamente contra os Critérios de Milão e o TNM 8ª Edição na predição de sobrevida câncer-específica em 5 anos.
- **Métodos:** Estudo de coorte observacional retrospectivo de base populacional extraído do registro do National Cancer Institute (NCI SEER, 2000–2021). Foram incluídos pacientes adultos com HCC primário submetidos a ressecção hepática ou transplante. O particionamento anti-vazamento dividiu a coorte em partição de desenvolvimento (2000–2015, N > 45.000) para validação cruzada aninhada em 5 dobras e calibração conformal, e partição de validação temporal externa intacta (2016–2021, N > 15.000).
- **Resultados Planejados:** Avaliação de discriminação temporal (C-index, AUROC), calibração com curvas de calibração flexíveis (ICI, Brier Score), garantia marginal empírica de 95% de cobertura conformal e curvas de benefício líquido (DCA) em limiares de decisão de 10% a 50%.
- **Conclusões:** A combinação de inteligência artificial explicável (TreeSHAP) e quantificação de incerteza conformal oferece suporte individualizado à decisão cirúrgica no HCC, identificando subgrupos que se beneficiam de transplante além dos critérios clássicos de Milão.

---

## 1. Introdução

O carcinoma hepatocelular (HCC) é a forma predominante de câncer primário de fígado e representa uma das principais causas de mortalidade oncológica no mundo. A ressecção hepática cirúrgica e o transplante hepático ortotópico constituem as únicas modalidades curativas estabelecidas. Contudo, a alocação terapêutica ótima permanece um dos dilemas mais complexos da cirurgia do aparelho digestivo e da oncologia cirúrgica.

Historicamente, a elegibilidade para transplante hepático tem sido governada pelos Critérios de Milão propostos por Mazzaferro e colaboradores em 1996 (nódulo único <= 5 cm ou até 3 nódulos <= 3 cm, sem invasão vascular macroscópica). Embora os Critérios de Milão tenham consagrado taxas de sobrevida em 5 anos superiores a 70%, sua natureza dicotômica e estritamente morfológica é cada vez mais questionada. Pacientes com tumores ligeiramente superiores a 5 cm, mas com biologia favorável (baixo nível sérico de AFP, ausência de invasão microvascular), são frequentemente excluídos do transplante curativo. Por outro lado, pacientes dentro de Milão com histologia desfavorável sofrem recidiva precoce após o procedimento.

Paralelamente, os escores lineares convencionais de estadiamento oncológico, como a 8ª Edição do TNM/AJCC e o escore CLIP, tratam variáveis contínuas cruciais através de categorizações artificiais e ignoram as sinergias biológicas não-lineares. Recentemente, modelos de aprendizado de máquina (Machine Learning) demonstraram capacidade ímpar de modelar relações não-lineares complexas. Entretanto, a aplicação clínica de modelos de aprendizado de máquina na cirurgia tem sido limitada pelo paradigma de "caixa-preta" e pela ausência de garantias formais de quantificação de incerteza probabilística em nível individual.

Neste trabalho, implementamos uma estrutura metodológica orientada pelo TRIPOD+AI (2024), integrando árvores de gradiente boosting com restrições monotônicas clínicas, explicabilidade biológica exata por TreeSHAP e predição conformal (*Split Conformal Prediction* com MAPIE) para fornecer conjuntos de predição com cobertura marginal matematicamente garantida de 95%. O objetivo primário é superar o estadiamento TNM e os Critérios de Milão na predição de sobrevida câncer-específica em 5 anos e estimar o benefício cirúrgico individualizado da ressecção versus transplante hepático na base populacional do NCI SEER (>60.000 pacientes).

---

## 2. Métodos

### 2.1 Desenho do Estudo e Governança do Protocolo
O estudo foi desenhado como uma coorte observacional retrospectiva de base populacional, com relato rigorosamente aderente aos 27 itens da declaração TRIPOD+AI (2024) e avaliação crítica de risco de viés pela ferramenta PROBAST+AI (2025). O protocolo formal do estudo foi previamente registrado no Open Science Framework (OSF) sob o código imutável [https://osf.io/uzwr2/](https://osf.io/uzwr2/) antes de qualquer ajuste de hiperparâmetros ou modelagem nos dados analíticos.

### 2.2 Fonte de Dados e População do Estudo
Os dados foram extraídos do programa SEER (*Surveillance, Epidemiology, and End Results*) mantido pelo National Cancer Institute (NCI) dos Estados Unidos, abrangendo registros oncológicos de base populacional que cobrem aproximadamente 48% da população norte-americana.

Os critérios formais de inclusão foram:
1. Idade igual ou superior a 18 anos no diagnóstico de HCC;
2. Diagnóstico microscópico confirmado de carcinoma hepatocelular primário (códigos histológicos ICD-O-3: 8170 a 8175) localizado no fígado (código topográfico C22.0);
3. Submissão documentada a tratamento cirúrgico com intenção curativa: ressecção hepática parcial (cunha, segmentectomia, lobectomia ou trissegmentectomia; códigos SEER 30 a 59) ou transplante hepático ortotópico (código SEER 61);
4. Diagnóstico e cirurgia realizados entre 1 de janeiro de 2000 e 31 de dezembro de 2021 com seguimento documentado.

Foram excluídos casos com metástases hepáticas de outros sítios primários, variantes histológicas não-carcinoma (ex.: fibrolamelar, hepatoblastoma, angiossarcoma), tempo de sobrevida desconhecido ou nulo, ou registros sem causa de óbito especificada.

### 2.3 Arquitetura de Particionamento Anti-Vazamento
Para garantir que o desempenho do modelo reflita condições clínicas reais e evitar viés de sobreajuste (*optimism bias*), adotamos uma divisão temporal prospectiva:
- **Coorte de Desenvolvimento (2000–2015, N ~ 45.000):** Utilizada estritamente para engenharia de variáveis, imputação de dados faltantes, validação cruzada aninhada em 5 dobras (*nested cross-validation*), busca bayesiana de hiperparâmetros (Optuna TPE) e calibração de incerteza conformal;
- **Coorte de Validação Temporal Externa (2016–2021, N ~ 15.000):** Mantida intocada e preservada como partição de teste externa independente para mensuração da transportabilidade temporal e calibração em período recente de prática cirúrgica.

### 2.4 Preditores Clínicos e Histopatológicos
Todos os preditores foram definidos com base estrita em informações obtidas no momento da decisão cirúrgica ou na avaliação histopatológica da peça cirúrgica:
- Demografia: idade no diagnóstico (anos contínuos), sexo biológico, raça/etnia e quintil de renda domiciliar mediana;
- Carga tumoral e histopatologia: diâmetro do maior nódulo tumoral (em centímetros contínuos), número de lesões (solitário versus multifocal), invasão vascular (ausente, microvascular ou macrovascular), grau histológico de diferenciação (I a IV) e acometimento linfonodal regional;
- Biomarcadores e parênquima hepático: nível sérico de alfa-fetoproteína (AFP, categorizado como normal <= 20 ng/mL ou elevado > 20 ng/mL), escore de fibrose histológica de Ishak e presença de cirrose hepática;
- Modalidade cirúrgica: ressecção hepática parcial versus transplante hepático ortotópico.

### 2.5 Desfechos Clínicos e Modelagem Estatística
O desfecho primário do estudo é a **Sobrevida Câncer-Específica em 5 anos (CSS)**, definida como o óbito atribuível exclusivamente ao carcinoma hepatocelular dentro de 60 meses a partir do procedimento cirúrgico. Pacientes que faleceram por outras causas concorrentes (ex.: doença cardiovascular, insuficiência hepática não neoplásica) foram censurados ou analisados sob o modelo de riscos competitivos de Fine-Gray (*subdistribution hazard ratio*). O desfecho secundário é a Sobrevida Global (OS) em 5 anos e 3 anos.

### 2.6 Algoritmos de Machine Learning e Explicabilidade
1. **Modelos em Gradiente Boosting:** Implementamos o LightGBM e o XGBoost. Para garantir coerência biológica estrita e prevenir comportamentos contraintuitivos, aplicamos restrições monotônicas crescentes de risco para diâmetro tumoral, multiplicidade e idade.
2. **Explicabilidade Exata por TreeSHAP:** Calculamos as contribuições locais de cada variável (*SHAP values*) e a matriz de interação de segunda ordem de Lundberg $\Phi_{i,j}(x)$, isolando sinergias entre AFP, tamanho tumoral e cirrose subjacente.
3. **Predição Conformal Dividida (MAPIE):** Utilizamos o *Split Conformal Classifier* com escore de não-conformidade $s_i = 1 - \hat{P}(y_i | x_i)$, calibrado em subconjunto independente da coorte de desenvolvimento para garantir cobertura marginal mínima de 95% ($\alpha = 0,05$).
4. **Análise de Curva de Decisão (DCA):** O benefício clínico líquido (*Net Benefit*) do modelo foi comparado diretamente contra estratégias universais ("tratar todos", "tratar nenhum"), contra os Critérios de Milão e contra o TNM 8ª Edição em limiares de probabilidade de decisão clínica variando de 10% a 50%.

---

## Declarações

### Aprovação Ética e Enquadramento Regulatório
Estudo secundário baseado em registros desidentificados de domínio público do programa SEER (NCI/NIH). Enquadrado na isenção formal de consentimento e aprovação ética do Comitê de Ética em Pesquisa (CEP/IRB) nos termos da regulamentação federal norte-americana 45 CFR 46.104(d)(4) e das resoluções éticas da CONEP (Brasil) para bancos de dados anonimizados sem identificação de sujeitos humanos.

### Declaração de Uso de Inteligência Artificial
Uso de Inteligência Artificial e Tecnologias Assistidas por IA na Redação Científica: Durante a preparação deste trabalho, os autores utilizaram Claude Opus 5.5 (Anthropic) para auxiliar no polimento do idioma inglês, refinamento gramatical, correções tipográficas e formatação do layout de tabelas. Após o uso desta ferramenta, os autores revisaram criticamente, verificaram e editaram todo o conteúdo gerado e assumem total responsabilidade pela integridade científica, precisão factual e conclusões apresentadas neste manuscrito. Em conformidade com os critérios de autoria da revista, tecnologias de IA generativa não são listadas como autores.
