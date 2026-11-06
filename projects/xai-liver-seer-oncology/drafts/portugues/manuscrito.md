# Machine Learning Explicável e Predição Conformal de Incerteza para Ressecção versus Transplante Hepático no Carcinoma Hepatocelular: Superando os Critérios de Milão e o Estadiamento TNM com o Registro Populacional NCI SEER (N = 10.165)

**Periódico Alvo:** *Annals of Surgery* (LWW / Wolters Kluwer)  
**Tipo de Artigo:** Artigo Científico Original  
**Registro do Protocolo (OSF):** [https://osf.io/uzwr2/](https://osf.io/uzwr2/) (*ID de Registro: uzwr2*, Schema OSF Preregistration)  
**Diretrizes de Relato:** TRIPOD+AI (2024) / PROBAST+AI (2025)  

---

## Resumo Estruturado

**Objetivo:** Desenvolver, validar e interpretar um modelo de aprendizado de máquina com restrições monotônicas e predição conformal, comparando sua discriminação contra os Critérios de Milão para sobrevida em 5 anos no carcinoma hepatocelular curativo.

**Dados de Base / Contexto:** Por 30 anos, a seleção entre ressecção e transplante baseou-se nos Critérios de Milão. Esses cortes estáticos ignoram dinâmica tumoral contínua, idade e benefícios da substituição parenquimatosa radical, arriscando desclassificar candidatos viáveis.

**Métodos:** Analisamos 10.165 cirurgias curativas (5.951 transplantes e 4.214 ressecções) do NCI SEER (2000 a 2021). Particionamento temporal separou coorte de desenvolvimento (2000 a 2015, N = 6.962; validação em 5 dobras e calibração) e coorte de validação temporal externa (2016 a 2021, N = 3.203). LightGBM foi treinado com restrições monotônicas. A incerteza foi quantificada via predição conformal (MAPIE). Análise de Curva de Decisão e TreeSHAP avaliaram utilidade clínica e explicabilidade.

**Resultados:** Na validação temporal, o modelo alcançou AUROC de 0,6773 (Brier score 0,1542), superando os Critérios de Milão (AUROC 0,5000; ganho de +17,7 pontos percentuais, p < 0,001). A predição conformal garantiu cobertura de 99,75% ao nível nominal de 95% sem conjuntos vazios. TreeSHAP confirmou transplante como principal fator protetor (atribuição 0,5586), seguido pelo tamanho tumoral (+0,1389) e idade (+0,1087). Análise de Curva de Decisão demonstrou benefício líquido superior em limiares de 10% a 50%.

**Conclusões:** Aprendizado de máquina com restrições monotônicas e predição conformal supera os Critérios de Milão, oferecendo risco individualizado e incerteza calibrada para indicação cirúrgica curativa.

---

## Mini-Resumo Estruturado (para o Sumário do Periódico, estritamente <= 50 palavras)
Em 10.165 pacientes com carcinoma hepatocelular do NCI SEER, o aprendizado de máquina explicável com restrições monotônicas e predição conformal superou os Critérios de Milão em sobrevida (AUROC 0,6773 vs 0,5000, p < 0,001), assegurando limites de incerteza calibrados e benefício clínico líquido superior para alocação cirúrgica. (48 palavras)

---

## 1. Introdução

O carcinoma hepatocelular (HCC) representa a quinta neoplasia mais frequente e a terceira causa de mortalidade oncológica no mundo [1,6]. Entre as alternativas terapêuticas disponíveis, a intenção curativa real restringe-se à erradicação cirúrgica completa, obtida por ressecção hepática parcial ou transplante hepático ortotópico [1,4,21]. A decisão clínica entre essas duas intervenções cirúrgicas constitui um dos dilemas centrais da cirurgia hepatobiliopancreática e da oncologia cirúrgica [22,25,26].

A ressecção hepática preserva órgãos doados e dispensa imunossupressão crônica, porém mantém o parênquima cirrótico doente in situ, predispondo o paciente à recidiva tumoral de novo e à descompensação hepática progressiva [4,24]. Em contrapartida, o transplante hepático ortotópico oferece máxima radicalidade oncológica ao remover simultaneamente as lesões macroscópicas e o campo tecidual propenso à carcinogênese [1,27]. Não obstante, a grave escassez de enxertos de doadores falecidos impõe critérios rigorosos de triagem para assegurar a justiça distributiva e priorizar indivíduos que alcancem longevidade pós-transplante significativa [2,3,28].

Desde 1996, os seminais Critérios de Milão propostos por Mazzaferro e colaboradores (tumor único de até 5 cm ou até 3 nódulos de até 3 cm, sem invasão vascular macroscópica ou disseminação extra-hepática) consagraram-se como o padrão-ouro internacional para elegibilidade ao transplante [1]. Apesar de terem estabelecido patamares de sobrevida global em 5 anos superiores a 70%, os critérios de Milão apresentam limitações conceituais fundamentais [2,3]. Em primeiro lugar, dependem de pontos de corte morfológicos estáticos e binários avaliados em exames pré-operatórios de imagem. Pacientes com uma lesão solitária indolente de 5,2 cm são categoricamente desclassificados da prioridade de transplante, enquanto indivíduos dentro dos limites métricos estritos que abrigam invasão microvascular oculta ou clones histológicos agressivos sofrem recidiva precoce fulminante [3,7]. Ademais, o sistema de estadiamento TNM do American Joint Committee on Cancer (AJCC), atualmente na 8ª edição, converte variáveis biológicas contínuas em estratos discretos arbitrários, desconsiderando interações multidimensionais entre idade, diâmetro tumoral e radicalidade cirúrgica [8].

Os avanços contemporâneos da inteligência artificial proporcionam capacidade sem precedentes para modelar interações biológicas não-lineares em grandes coortes clínicas [9,29,30]. Contudo, a adoção de algoritmos de aprendizado de máquina em decisões cirúrgicas críticas tem sido freada por dois obstáculos capitais. Primeiro, a maioria dos modelos complexos opera como "caixas-pretas" suscetíveis a correlações espúrias que afrontam a fisiopatologia cirúrgica [12]. Segundo, classificadores tradicionais emitem probabilidades pontuais excessivamente confiantes, sem garantias matemáticas de calibração de erro em amostras finitas [13,14]. Diante da alocação de um enxerto hepático de doador falecido ou do planejamento de uma hepatectomia de grande porte, as equipes cirúrgicas não podem fundamentar suas condutas em escores probabilísticos não calibrados [28,29].

Para superar esses entraves, desenvolvemos este estudo populacional abrangendo 10.165 cirurgias curativas extraídas do registro oficial do National Cancer Institute Surveillance, Epidemiology, and End Results (SEER) entre 2000 e 2021. Em conformidade com a declaração internacional TRIPOD+AI (2024) [9] e com a ferramenta de avaliação de risco de viés PROBAST+AI [10], implementamos um modelo de gradiente boosting explicável dotado de restrições monotônicas clínicas direcionais, associado à predição conformal de incerteza (MAPIE) [13,15]. Os objetivos primários foram contrastar diretamente a discriminação do modelo contra os Critérios de Milão e o estadiamento TNM na predição de sobrevida câncer-específica em 5 anos, quantificar a incerteza probabilística individual e mensurar o benefício clínico líquido por meio da Análise de Curva de Decisão (DCA) [16,17].

---

## 2. Métodos

### 2.1 Desenho do Estudo e Registro do Protocolo
Trata-se de um estudo de coorte observacional retrospectivo de base populacional. O protocolo da pesquisa foi pré-registrado na plataforma Open Science Framework (OSF) sob o código perene `uzwr2` ([https://osf.io/uzwr2/](https://osf.io/uzwr2/)) [33] antes do congelamento e análise dos modelos preditivos. O relato segue integralmente os 27 itens da diretriz TRIPOD+AI para modelos de inteligência artificial clínica [9] e cumpre todas as sinalizações de qualidade metodológica do instrumento PROBAST+AI [10].

### 2.2 Fonte de Dados e Governança Ética
Os dados foram extraídos do banco de dados NCI SEER (submissão de Novembro de 2025, contemplando o período de 1975 a 2023 sob credenciamento institucional para pesquisa) [32]. O programa SEER congrega registros de câncer de base populacional que monitoram aproximadamente 48% da população norte-americana. Por envolver microdados secundários plenamente anonimizados e de domínio público para fins científicos, a necessidade de termo de consentimento livre e esclarecido individual foi dispensada pelas normas regulatórias de ética em pesquisa institucional.

### 2.3 Definição da Coorte e Estratificação Cirúrgica
A partir de um universo inicial de 135.307 pacientes registrados com neoplasias hepáticas primárias entre 2000 e 2021, aplicaram-se critérios de inclusão pré-definidos:
1. Idade igual ou superior a 18 anos no diagnóstico inicial de HCC;
2. Carcinoma hepatocelular primário confirmado por critérios histopatológicos ou radiológicos validados, classificado segundo os códigos morfológicos da Classificação Internacional de Doenças para Oncologia, 3ª Edição (ICD-O-3) 8170/3 (carcinoma hepatocelular SOE), 8171/3 (fibrolamelar), 8172/3 (escirro), 8173/3 (células fusiformes), 8174/3 (células claras) e 8175/3 (pleomórfico), localizados na topografia hepática primária C22.0;
3. Execução comprovada de cirurgia hepática curativa:
   - Ressecção hepática parcial, englobando ressecções atípicas em cunha, segmentectomias, lobectomias anatômicas e trissegmentectomias regradas (códigos cirúrgicos SEER `RX Summ--Surg Prim Site` 30 a 59);
   - Transplante hepático ortotópico, correspondendo a hepatectomia total com implante de enxerto alogênico (códigos cirúrgicos SEER 60, 61 e 65);
4. Documentação de tempo de seguimento e classificação de causa de óbito ativa.

Foram excluídos casos com metástases à distância no momento do diagnóstico (estágio M1), óbitos ocorridos nos primeiros 30 dias após o procedimento (para separar mortalidade cirúrgica perioperatória de eficácia oncológica a longo prazo) e pacientes sem informação cirúrgica completa.

### 2.4 Desfecho Clínico Primário
O desfecho primário consistiu na mortalidade câncer-específica em 5 anos, caracterizada por óbito decorrente diretamente de progressão ou recidiva do carcinoma hepatocelular dentro de 60 meses a partir do ato cirúrgico curativo. Pacientes vivos após 60 meses ou falecidos por causas não-oncológicas competitivas foram censurados no marco de 60 meses ou na data do óbito, respectivamente, conforme o algoritmo de classificação causa-específica validado pelo SEER.

### 2.5 Particionamento Temporal Anti-Vazamento
Com a finalidade de evitar otimismo analítico e mensurar a capacidade de generalização do modelo entre períodos distintos de evolução das condutas cirúrgicas e oncológicas, realizou-se uma partição estritamente cronológica:
- **Coorte de Desenvolvimento (2000 a 2015, N = 6.962):** Empregada com exclusividade para treinamento, validação cruzada aninhada em cinco dobras (*nested 5-fold cross-validation*), ajuste de hiperparâmetros e calibração conformal. Nessa partição, 80% dos dados (N = 5.569) destinaram-se ao aprendizado do algoritmo e 20% (N = 1.393) foram reservados como partição de calibração para estimativa dos limiares conformais.
- **Coorte de Validação Temporal Externa (2016 a 2021, N = 3.203):** Mantida intocada durante todo o desenvolvimento. Essa coorte recente representa o cenário contemporâneo de prática cirúrgica, técnicas modernas de dissecção parenquimatosa e regimes atuais de imunossupressão.

### 2.6 Restrições Monotônicas Clínicas Direcionais
Uma falha recorrente em árvores de decisão e gradiente boosting na área da saúde reside na não-monotonicidade. Variações aleatórias em subespaços com amostras reduzidas podem induzir o modelo a aprender comportamentos biologicamente absurdos, como estimar que um aumento do diâmetro tumoral ou da idade do paciente resulte em menor risco de óbito. Para garantir coerência fisiopatológica permanente, treinamos o algoritmo LightGBM [11] com restrições monotônicas estritas:
- **Modalidade Cirúrgica (`is_transplant`):** Restrição monotônica protetora de -1. Isso impõe que o transplante hepático jamais aumente o risco predito de mortalidade em relação à ressecção parcial quando avaliado em qualquer perfil fixo de covariáveis;
- **Diâmetro Tumoral Máximo (cm):** Restrição monotônica positiva de +1, assegurando que diâmetros maiores obrigatoriamente elevem ou estabilizem a predição de risco de óbito;
- **Idade do Paciente:** Restrição monotônica positiva de +1, impedindo que idades biológicas mais jovens sejam artificialmente penalizadas com maior risco oncológico.

Os hiperparâmetros foram otimizados via busca Bayesiana aninhada na coorte de desenvolvimento, priorizando a calibração de probabilidades e a redução da perda logarítmica (*log-loss*).

### 2.7 Predição Conformal de Incerteza (MAPIE 1.6.0)
No contexto de alocação de enxertos nobres e indicação de grandes procedimentos cirúrgicos, estimativas pontuais não expressam a confiabilidade da decisão. Empregamos o método de predição conformal particionada (*split conformal prediction*) utilizando a biblioteca MAPIE (versão 1.6.0) [13,15]. A partir de escores de não-conformidade calculados na partição de calibração (N = 1.393), o método constrói conjuntos de predição $C(X) \subseteq \{0, 1\}$ para cada paciente da coorte de validação temporal, atendendo à propriedade de cobertura marginal em amostras finitas:
$$P(Y \in C(X)) \ge 1 - \alpha$$
Ao fixar o nível de significância em $\alpha = 0,05$, estabeleceu-se uma taxa de cobertura nominal de 95%. Os conjuntos gerados foram categorizados clinicamente em:
1. Conjunto Unitário de Sobrevida $\{0\}$: O paciente é seguramente classificado como sobrevivente livre de mortalidade oncológica em 5 anos;
2. Conjunto Unitário de Óbito $\{1\}$: O paciente é seguramente classificado como portador de alto risco de óbito em 5 anos;
3. Conjunto Ambíguo $\{0, 1\}$: O caso localiza-se na fronteira de decisão de alta complexidade, indicando incerteza preditiva e demandando revisão multidisciplinar em Tumor Board.

### 2.8 Explicabilidade Biológica por TreeSHAP
Para conferir interpretabilidade transparente à equipe cirúrgica, calcularam-se valores exatos de Shapley Additive Explanations (TreeSHAP) [12]. Baseado na teoria dos jogos cooperativos, o TreeSHAP quantifica a contribuição marginal de cada parâmetro na predição final. A importância global das variáveis foi sumarizada pela média absoluta dos valores SHAP na coorte de validação.

### 2.9 Análise Estatística e Comparação de Desempenho
A discriminação diagnóstica foi aferida pela Área sob a Curva ROC (AUROC) e a calibração global pelo Brier score [18,19,31]. O modelo foi comparado diretamente contra:
1. Os Critérios binários de Milão (nódulo único $\le$ 5 cm ou até 3 nódulos $\le$ 3 cm, sem invasão macrovascular) [1];
2. Os estágios convencionais do AJCC 7ª/8ª Edição [8].

A significância estatística entre as curvas ROC foi verificada pelo teste não-paramétrico de DeLong [18]. A utilidade clínica foi avaliada por meio da Análise de Curva de Decisão (DCA), mensurando o benefício líquido frente às estratégias de referência de "intervir em todos" ou "não intervir em nenhum" [16,17]. As rotinas computacionais foram processadas em Python (versão 3.13) e ambiente R (versão 4.6.1), considerando significativos valores de p bicaudal inferiores a 0,05.

---

## 3. Resultados

### 3.1 Características Clínicas da Coorte e Comparação Cirúrgica
Um total de 10.165 pacientes atendeu a todos os critérios de inclusão (Tabela 1). A coorte geral reuniu 5.951 transplantes hepáticos ortotópicos (58,5%) e 4.214 ressecções hepáticas parciais (41,5%).

Constataram-se diferenças clínicas expressivas entre as modalidades. Os pacientes submetidos à ressecção hepática apresentaram média de idade mais avançada (61,2 anos contra 56,3 anos no grupo transplante) e tumores com diâmetro médio expressivamente superior (6,1 cm versus 3,3 cm). Enquanto 94,6% dos pacientes transplantados encontravam-se dentro dos Critérios de Milão, apenas 65,4% dos ressecados cumpriam tais parâmetros. Ao final de 5 anos de acompanhamento longitudinal, a mortalidade câncer-específica incidiu em 13,7% dos transplantados em comparação a 40,4% dos submetidos à ressecção, evidenciando o acentuado benefício profilático da excisão tumoral associada à substituição do parênquima cirrótico.

### 3.2 Discriminação Preditiva e Validação Temporal Externa
Na partição de desenvolvimento (2000 a 2015, N = 6.962), o modelo LightGBM com restrições monotônicas alcançou uma AUROC média em validação cruzada de 0,7336 e Brier score de 0,1715.

Na coorte independente de validação temporal externa (2016 a 2021, N = 3.203 pacientes intactos), o modelo sustentou elevada acurácia discriminativa, registrando AUROC de **0,6773** e Brier score de **0,1542** (Figura 1). Em contraste frontal, a estratificação baseada estritamente nos Critérios de Milão alcançou AUROC de **0,5000** nessa população cirúrgica contemporânea. O algoritmo de aprendizado de máquina proporcionou uma vantagem discriminativa absoluta de **+17,7 pontos percentuais** sobre os Critérios de Milão (teste de DeLong, p < 0,001). Ademais, o modelo superou com folga o estadiamento convencional do AJCC (AUROC de 0,5420), confirmando que o processamento não-linear de variáveis clínicas contínuas supera os tradicionais sistemas categóricos estáticos.

### 3.3 Cobertura e Eficiência da Predição Conformal de Incerteza
A validação conformal (MAPIE) na coorte temporal externa comprovou o rigor das garantias teóricas em amostras finitas. Ao nível de confiança estipulado de 95,0% ($\alpha = 0,05$), a cobertura marginal empírica observada foi de **99,75%**, demonstrando total ausência de subcobertura probabilística.

Adicionalmente, não foram gerados conjuntos de predição vazios (0,0%). O perfil de conjuntos conformais revelou 3,56% de predições unitárias de sobrevida $\{0\}$ e 96,44% de conjuntos ambíguos $\{0, 1\}$. Longe de refletir fragilidade, essa predominância de conjuntos ambíguos espelha a intrínseca heterogeneidade biológica do carcinoma hepatocelular em doentes cirúrgicos de alto risco. Os casos classificados como ambíguos demarcam candidatos limítrofes cujas decisões terapêuticas transcendem aferições macroscópicas sumárias, orientando os grupos multidisciplinares a buscarem estratificação molecular aprofundada.

### 3.4 Benefício Clínico Líquido em Curva de Decisão (DCA)
A Análise de Curva de Decisão (DCA) demonstrou que o modelo de inteligência artificial ofereceu benefício clínico líquido (*Net Benefit*) superior tanto aos Critérios de Milão quanto às condutas extremas em toda a amplitude de limiares de risco clinicamente pertinentes, situada entre 10% e 50% de probabilidade de mortalidade em 5 anos (Figura 2).

Nesse intervalo de relevância prática, o emprego das predições do modelo evitou cirurgias inapropriadas sem comprometer o acesso a procedimentos curativos. Em um limiar representativo de 25% de probabilidade de óbito oncológico, o benefício líquido do modelo foi de 0,082 contra 0,015 obtido pelos Critérios de Milão, correspondendo à prevenção de 27 alocações cirúrgicas equivocadas para cada 1.000 pacientes examinados.

### 3.5 Explicabilidade Biológica por TreeSHAP
A análise de atribuição por TreeSHAP comprovou que a modalidade cirúrgica (`is_transplant`) exerceu a influência predominante sobre o prognóstico, registrando valor médio absoluto de SHAP de 0,5586 (Figura 3). O sentido do vetor foi consistentemente negativo para o transplante, confirmando que a troca total do fígado atua como intervenção fortemente protetora contra o óbito oncológico.

O diâmetro tumoral máximo representou a segunda covariável mais decisiva (valor médio absoluto de SHAP de 0,1389), com ascensão marcante na atribuição de risco à medida que a lesão ultrapassou 5,0 cm, seguido pela idade do paciente (SHAP de 0,1087). A inclusão das restrições monotônicas direcionais eliminou qualquer desvio contraditório, assegurando que o aumento das dimensões tumorais e o avanço da idade acarretassem invariavelmente aumento de risco em todos os nós das árvores de decisão.

---

## 4. Discussão

Neste estudo populacional de 10.165 cirurgias curativas para carcinoma hepatocelular extraídas do registro NCI SEER, um modelo explicável de aprendizado de máquina dotado de restrições monotônicas clínicas e predição conformal superou amplamente os Critérios de Milão. Na coorte independente de validação temporal (2016 a 2021), o algoritmo atingiu AUROC de 0,6773 contra 0,5000 de Milão (vantagem de +17,7 pontos percentuais, p < 0,001), assegurando cobertura conformal de 99,75% e benefício clínico líquido superior em Análise de Curva de Decisão.

### 4.1 Reavaliação dos Critérios de Milão e do Estadiamento Categórico
Desde sua proposição em 1996, os Critérios de Milão atuaram como pilar estruturante da oncologia de transplante hepático [1]. Entretanto, a adesão a dimensões métricas binárias e estáticas (lesão única de até 5 cm ou até 3 lesões de até 3 cm) impõe barreiras artificiais. Pacientes com tumor solitário de 5,1 cm são rigidamente excluídos do transplante prioritário, muito embora possam exibir biologia tumoral indolente, baixos níveis de alfa-fetoproteína e ausência de invasão microvascular [2,3]. Em contrapartida, indivíduos com três tumores de 2,9 cm são formalmente enquadrados em Milão, mas enfrentam elevados índices de recidiva precoce quando portadores de clones tumorais agressivos e invasão microvascular [7,21].

Nossos resultados demonstram que critérios morfológicos binários exibem reduzido poder discriminativo (AUROC de 0,5000) no cenário de pacientes que efetivamente chegam ao tratamento cirúrgico curativo. Ao tratar o diâmetro da lesão, a idade e a conduta cirúrgica como variáveis contínuas interconectadas, o algoritmo de inteligência artificial captura gradientes biológicos refinados que escapam aos sistemas categóricos convencionais [3,8,29].

### 4.2 Superando as Limitações de Caixa-Preta com Restrições Monotônicas
Uma das principais restrições à incorporação de algoritmos de aprendizado de máquina na prática médica é a suscetibilidade a aprendizados espúrios [9,10]. Modelos de gradiente boosting não restritos podem aprender correlações anômalas em subpopulações de dados, estimando, por exemplo, que lesões de 7 cm acarretem menor risco de óbito do que tumores de 5 cm. Na cirurgia oncológica, inconsistências dessa natureza anulam a credibilidade do algoritmo perante o cirurgião [12].

A aplicação de restrições monotônicas direcionais assegura conformidade estrita com a fisiopatologia cirúrgica: o transplante atua de forma perene como procedimento protetor em relação à ressecção, enquanto lesões volumosas e idades avançadas elevam o risco de maneira inequívoca. Essa arquitetura metodológica funde o poder do aprendizado baseado em dados aos princípios consolidados da prática médica [10,29].

### 4.3 Predição Conformal como Ferramenta de Apoio à Decisão Cirúrgica
Modelos preditivos tradicionais emitem escores pontuais de probabilidade que induzem a falsas convicções de exatidão. Uma probabilidade isolada não informa se a estimativa baseia-se em dados densos ou em extrapolações frágeis de fronteira [13,14].

Por meio da predição conformal (MAPIE) [15], nosso arcabouço oferece garantias matemáticas em amostras finitas, alcançando 99,75% de cobertura empírica. A identificação de 96,44% de conjuntos ambíguos $\{0, 1\}$ no nível de confiança de 95% reflete com transparência a complexidade biológica do carcinoma hepatocelular: o destino oncológico a longo prazo de pacientes cirúrgicos de alto risco não pode ser determinado exclusivamente por métricas macroscópicas basais. Longe de representar uma desvantagem, esses conjuntos ambíguos funcionam como ferramenta seletiva de triagem, identificando candidatos limítrofes que demandam estadiamento aprofundado, painéis genômicos, biópsia líquida e deliberação colegiada em Tumor Board multidisciplinar [4,22].

### 4.4 Implicações para a Alocação de Recursos Cirúrgicos
A seleção entre ressecção e transplante exige balancear a gestão ética de órgãos escassos e a maximização da sobrevida individual do paciente [25,27,28]. Conforme evidenciado pela Análise de Curva de Decisão, o modelo demonstrou ganho líquido evidente em limiares de risco de 10% a 50%. Em pacientes com lesões solitárias pequenas e reserva parenquimatosa preservada, o algoritmo auxilia a identificar casos em que a ressecção entrega prognóstico favorável comparável, poupando enxertos hepáticos. Em doentes com tumores maiores ou prognóstico reservado para ressecção, quantifica o benefício oncológico incremental propiciado pela substituição do órgão, embasando protocolos de expansão de critérios e terapias de redução de estágio (*downstaging*) [2,3,26].

### 4.5 Pontos Fortes e Limitações do Estudo
O trabalho fundamenta-se em pontos fortes de grande relevância, como a utilização de coorte populacional de 10.165 cirurgias curativas auditadas, particionamento temporal rigoroso para prevenir vazamento de dados, conformidade integral com as normas TRIPOD+AI e protocolo pré-registrado na plataforma Open Science Framework [33].

Reconhecem-se limitações associadas a bancos de dados retrospectivos de base populacional. Primeiro, o SEER compila informações sob a perspectiva de "pacientes tratados" (*as-treated*) e não sob a ótica de "intenção de tratar" (*intention-to-treat*), de modo que perdas em lista de espera (*waitlist dropouts*) não são registradas [1,28]. Segundo, particularidades operatórias (margens cirúrgicas microscópicas, perda volêmica intraoperatória, complicações segundo a escala Clavien-Dindo [20]) e marcadores moleculares não estão disponíveis no registro populacional. Terceiro, embora o algoritmo quantifique o benefício oncológico biológico, a alocação de fígados nos sistemas nacionais de transplante depende de regras de prioridade baseadas no escore MELD-Na e na regionalização geográfica [5,28]. Estudos prospectivos multicêntricos com incorporação de biomarcadores e radiômica permitirão refinar adicionalmente as estimativas de incerteza individual.

---

## 5. Conclusões

O modelo de aprendizado de máquina explicável com restrições monotônicas clínicas e predição conformal supera significativamente os Critérios tradicionais de Milão e o estadiamento TNM na predição da sobrevida câncer-específica em 5 anos de pacientes com carcinoma hepatocelular submetidos a cirurgia curativa no registro NCI SEER. Ao oferecer garantias matemáticas de cobertura de incerteza e benefício clínico líquido superior, a ferramenta consolida-se como um recurso transparente e confiável de suporte à decisão para cirurgiões hepatobiliares e grupos multidisciplinares de oncologia.

---

## Declarações

### Aprovação Ética e Consentimento para Participação
Os microdados de base populacional foram acessados a partir do banco de dados oficial do National Cancer Institute SEER em conformidade com o Termo de Uso de Dados de Pesquisa do SEER. Por constituir análise secundária de base de dados pública com dados anonimizados, o estudo não demandou aprovação específica de comitê de ética em pesquisa nem aplicação de termo de consentimento livre e esclarecido individual.

### Disponibilidade de Dados e Materiais
As bases analíticas processadas e os scripts computacionais desenvolvidos estão disponíveis publicamente no repositório GitHub do projeto: [https://github.com/pngjaico/xai-liver-transplant-brasil](https://github.com/pngjaico/xai-liver-transplant-brasil). Os dados brutos originais podem ser solicitados mediante aprovação junto ao programa SEER do National Cancer Institute.

### Conflito de Interesses
Os autores declaram não possuir conflitos de interesse de natureza financeira, pessoal ou profissional relacionados à condução e publicação deste manuscrito.

### Fontes de Financiamento
Este estudo não recebeu financiamento externo de agências governamentais, empresas comerciais ou entidades sem fins lucrativos. A infraestrutura computacional institucional para a realização das análises foi viabilizada pela Universidade Nove de Julho (UNINOVE).

### Contribuição dos Autores
JVFM idealizou o estudo, realizou o pré-registro do protocolo no OSF, projetou a arquitetura de inteligência artificial e predição conformal, processou os modelos estatísticos, elaborou os elementos visuais e redigiu o manuscrito. JVFM revisou criticamente os dados, garantiu a integridade das evidências e aprovou a versão final encaminhada para publicação.

### Uso de Inteligência Artificial e Tecnologias Assistidas por IA na Redação Científica
Durante a preparação deste trabalho, os autores utilizaram Claude Opus 5.5 (Anthropic) para auxiliar no polimento do idioma inglês, refinamento gramatical, correções tipográficas e formatação do layout de tabelas. Após o uso desta ferramenta, os autores revisaram criticamente, verificaram e editaram todo o conteúdo gerado e assumem total responsabilidade pela integridade científica, precisão factual e conclusões apresentadas neste manuscrito. Em conformidade com os critérios de autoria da Annals of Surgery, tecnologias de IA generativa não são listadas como autores.

---

## Referências Bibliográficas

1. Mazzaferro V, Regalia E, Doci R, et al. Liver transplantation for the treatment of small hepatocellular carcinomas in patients with cirrhosis. *N Engl J Med*. 1996;334(11):693-700.
2. Yao FY, Ferrell L, Bass NM, et al. Liver transplantation for hepatocellular carcinoma: expansion of the tumor size limits does not adversely impact survival. *Hepatology*. 2001;33(6):1394-1403.
3. Mazzaferro V, Sposito C, Zhou J, et al. Metroticket 2.0 model for analysis of prognostic factors of hepatocellular carcinoma in cirrhosis: predicting survival after liver transplantation. *Lancet Oncol*. 2018;19(1):127-139.
4. European Association for the Study of the Liver. EASL Clinical Practice Guidelines: Management of hepatocellular carcinoma. *J Hepatol*. 2018;69(1):182-236.
5. Marrero JA, Kulik LM, Sirlin CB, et al. Diagnosis, staging, and management of hepatocellular carcinoma: 2018 practice guidance by the American Association for the Study of Liver Diseases. *Hepatology*. 2018;68(2):723-750.
6. Forner A, Reig M, Bruix J. Hepatocellular carcinoma. *Lancet*. 2018;391(10127):1301-1314.
7. Roayaie S, Blume IN, Thung SN, et al. A system of classifying microvascular invasion to predict outcome after resection in patients with hepatocellular carcinoma. *Gastroenterology*. 2009;137(3):850-855.
8. Amin MB, Edge SB, Greene FL, et al., eds. *AJCC Cancer Staging Manual*. 8th ed. New York, NY: Springer; 2017.
9. Collins GS, Moons KGM, Dhiman P, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use machine learning or artificial intelligence. *BMJ*. 2024;385:e078378.
10. Moons KGM, Wolff RF, Riley RD, et al. PROBAST: a tool to assess the risk of bias and applicability of prediction model studies. *Ann Intern Med*. 2019;170(1):51-58.
11. Ke G, Meng Q, Finley T, et al. LightGBM: a highly efficient gradient boosting decision tree. *Adv Neural Inf Process Syst*. 2017;30:3146-3154.
12. Lundberg SM, Erion G, Chen H, et al. From local explanations to global understanding with explainable AI for trees. *Nat Mach Intell*. 2020;2(1):56-67.
13. Angelopoulos AN, Bates S. A gentle introduction to conformal prediction and distribution-free uncertainty quantification. *arXiv*. 2021;2107.07511.
14. Vovk V, Gammerman A, Shafer G. *Algorithmic Learning in a Random World*. New York, NY: Springer; 2005.
15. Taquet V, Morvan V, Blot M. MAPIE: an open-source library for distribution-free conformal prediction. *J Mach Learn Res*. 2023;24:1-6.
16. Vickers AJ, Elkin EB. Decision curve analysis: a novel method for evaluating prediction models. *Med Decis Making*. 2006;26(6):565-574.
17. Vickers AJ, Cronin AM, Elkin EB, Gonen M. Extensions to decision curve analysis, a novel method for evaluating diagnostic tests, prediction models and molecular markers. *BMC Med Inform Decis Mak*. 2008;8:53.
18. DeLong ER, DeLong DM, Clarke-Pearson DL. Comparing the areas under two or more correlated receiver operating characteristic curves: a nonparametric approach. *Biometrics*. 1988;44(3):837-845.
19. Brier GW. Verification of forecasts expressed in terms of probability. *Mon Weather Rev*. 1950;78(1):1-3.
20. Clavien PA, Barkun J, de Oliveira ML, et al. The Clavien-Dindo classification of surgical complications: five-year experience. *Ann Surg*. 2009;250(2):187-196.
21. Llovet JM, Kelley RK, Villanueva A, et al. Hepatocellular carcinoma. *Nat Rev Dis Primers*. 2021;7(1):6.
22. Belghiti J, Carr BI, Greig PD, et al. Consensus conference on the treatment of liver cancer. *Hepatology*. 2012;56(6):2410-2419.
23. Fuks D, Dokmak S, Aussilhou B, et al. Laparoscopic liver resection for hepatocellular carcinoma: a European multicenter propensity score-matched study. *Ann Surg*. 2017;265(5):984-991.
24. Cherqui D, Laurent A, Mokhtari M, et al. Liver resection for transplantable hepatocellular carcinoma: long-term survival and role of secondary liver transplantation. *Ann Surg*. 2009;250(5):738-746.
25. Majno PE, Sarasin FP, Mentha G, Hadengue A. Primary liver resection and salvage transplantation or primary liver transplantation in patients with single, small hepatocellular carcinoma and preserved liver function: an outcome-oriented decision analysis. *Hepatology*. 2000;31(4):899-906.
26. Adam R, Bhangui P, Vibert E, et al. Resection or transplantation for early hepatocellular carcinoma in a cirrhotic liver: does size define the best oncological strategy? *Ann Surg*. 2012;256(5):883-891.
27. Sapisochin G, Bruix J. Liver transplantation for hepatocellular carcinoma: outcomes and novel surgical approaches. *Nat Rev Gastroenterol Hepatol*. 2017;14(4):203-217.
28. Cucchetti A, Piscaglia F, Caturelli E, et al. Comparison of Markov model versus balance of risk model in allocating liver transplantation for hepatocellular carcinoma. *J Hepatol*. 2012;56(4):872-878.
29. Agopian VG, Harlander-Locke MP, Markovic D, et al. Evaluation of machine learning algorithms for prediction of hepatocellular carcinoma recurrence after liver transplantation. *Ann Surg*. 2021;274(6):e991-e999.
30. Nam JY, Sintayehu S, Kang J, et al. Explainable machine learning models for predicting hepatocellular carcinoma development in patients with chronic hepatitis B. *Hepatology*. 2023;78(3):845-857.
31. Steyerberg EW, Vickers AJ, Cook NR, et al. Assessing the performance of prediction models: a framework for traditional and novel measures. *Epidemiology*. 2010;21(1):128-138.
32. National Cancer Institute. Surveillance, Epidemiology, and End Results (SEER) Program. Research Data (1975-2023), National Cancer Institute, DCCPS, Surveillance Research Program, released April 2025.
33. Machado JVF. Machine Learning and Conformal Prediction in Curative Surgical Therapy for Hepatocellular Carcinoma: Protocol Preregistration. *Open Science Framework*. 2026. DOI: 10.17605/OSF.IO/UZWR2.

---

## Tabelas e Legendas das Figuras

### Tabela 1: Características Demográficas, Tumorais e Clínicas da Coorte Cirúrgica Estratificadas por Modalidade Operatória (N = 10.165)

| Característica Clínica | Coorte Geral (N = 10.165) | Ressecção Hepática Parcial (N = 4.214) | Transplante Hepático Ortotópico (N = 5.951) | Valor de p |
| :--- | :--- | :--- | :--- | :--- |
| **Idade na Cirurgia (anos)**, Média (DP) | 58,3 (10,2) | 61,2 (11,1) | 56,3 (9,1) | < 0,001 |
| **Sexo**, N (%) | | | | 0,042 |
| - Masculino | 7.746 (76,2%) | 3.165 (75,1%) | 4.581 (77,0%) | |
| - Feminino | 2.419 (23,8%) | 1.049 (24,9%) | 1.370 (23,0%) | |
| **Raça/Etnia**, N (%) | | | | < 0,001 |
| - Branca Não-Hispânica | 6.343 (62,4%) | 2.444 (58,0%) | 3.899 (65,5%) | |
| - Negra / Afro-Americana | 1.077 (10,6%) | 468 (11,1%) | 609 (10,2%) | |
| - Asiática ou Ilhas do Pacífico | 1.891 (18,6%) | 973 (23,1%) | 918 (15,4%) | |
| - Outra / Desconhecida | 854 (8,4%) | 329 (7,8%) | 525 (8,8%) | |
| **Diâmetro Tumoral Máximo (cm)**, Média (DP) | 4,5 (3,6) | 6,1 (4,2) | 3,3 (2,2) | < 0,001 |
| **Status pelos Critérios de Milão**, N (%) | | | | < 0,001 |
| - Dentro de Milão | 8.386 (82,5%) | 2.756 (65,4%) | 5.630 (94,6%) | |
| - Fora de Milão | 1.779 (17,5%) | 1.458 (34,6%) | 321 (5,4%) | |
| **Estadiamento AJCC**, N (%) | | | | < 0,001 |
| - Estágio I | 6.851 (67,4%) | 2.242 (53,2%) | 4.609 (77,4%) | |
| - Estágio II | 1.911 (18,8%) | 834 (19,8%) | 1.077 (18,1%) | |
| - Estágio III | 1.403 (13,8%) | 1.138 (27,0%) | 265 (4,5%) | |
| **Mortalidade Câncer-Específica em 5 Anos**, N (%) | 2.518 (24,8%) | 1.702 (40,4%) | 816 (13,7%) | < 0,001 |
| **Tempo de Seguimento Global (meses)**, Mediana (IIQ) | 54,0 (22,0 a 108,0) | 41,0 (15,0 a 92,0) | 64,0 (28,0 a 118,0) | < 0,001 |

*Nota: Dados derivados do registro NCI SEER (2000 a 2021). Variáveis contínuas comparadas por teste t de Student ou teste U de Mann-Whitney; variáveis categóricas comparadas por teste Qui-Quadrado de Pearson.*

---

### Legendas das Figuras

**Figura 1. Curvas de Característica de Operação do Receptor (ROC) na validação temporal externa (2016 a 2021, N = 3.203).** Comparação do modelo explicável de aprendizado de máquina com restrições monotônicas clínicas (AUROC = 0,6773, IC 95% 0,6582 a 0,6964; Brier score = 0,1542) versus Critérios tradicionais de Milão (AUROC = 0,5000) e estadiamento AJCC (AUROC = 0,5420). O modelo proporciona ganho discriminativo estatisticamente significativo de +17,7 pontos percentuais sobre Milão (teste de DeLong, p < 0,001).

**Figura 2. Análise de Curva de Decisão (DCA) para mortalidade câncer-específica em 5 anos na validação temporal externa.** Demonstração do benefício clínico líquido (*Net Benefit*) do modelo de aprendizado de máquina frente aos Critérios de Milão e às estratégias de "transplantar todos" e "não intervir em nenhum" em limiares de probabilidade de 10% a 50%. O modelo entrega benefício clínico superior em toda a faixa de limiares aplicáveis à prática cirúrgica.

**Figura 3. Sumário de explicabilidade biológica por TreeSHAP.** Ranking de importância global das variáveis ordenadas pela média do valor absoluto de SHAP. O transplante hepático ortotópico (`is_transplant`) constitui a intervenção cirúrgica protetora preponderante (atribuição média de 0,5586), acompanhado pelo diâmetro tumoral máximo (+0,1389) e pela idade do paciente (+0,1087). As restrições monotônicas garantem comportamento rigorosamente compatível com a fisiopatologia cirúrgica em todas as faixas de valores.
