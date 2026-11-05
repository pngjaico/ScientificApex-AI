# Transportabilidade Transcontinental de Machine Learning e Calibração Conformal de Incerteza no Transplante Hepático: Validação Externa Cruzada entre os Registros do SUS Brasileiro e do SEER Norte-Americano (N > 85.000)

**Autores:** João Vitor Fiches Machado e colaboradores  
**Registro do Protocolo (OSF):** [https://osf.io/w9mnq/](https://osf.io/w9mnq/) (*ID: w9mnq*, Schema OSF Preregistration)  
**Diretriz de Relato:** TRIPOD+AI (2024) / PROBAST+AI (2025)  
**Revistas-Alvo:** *Lancet Digital Health*, *Nature Medicine*, *JAMA Surgery*

---

## Resumo Estruturado

- **Contexto:** A generalização de algoritmos de inteligência artificial em saúde é frequentemente limitada pelo fenômeno do deslocamento de distribuição (*distribution shift*). Modelos preditivos derivados em países de alta renda (ex.: registros dos Estados Unidos) frequentemente falham ao serem aplicados em sistemas universais públicos de países em desenvolvimento (ex.: Sistema Único de Saúde do Brasil - SUS), devido a disparidades estruturais de etiologia (hepatite C e álcool vs esteatoepatite metabólica), tempos de lista e alocação de enxertos.
- **Objetivos:** Avaliar formalmente a transportabilidade geográfica e a degradação de calibração de modelos de Machine Learning (LightGBM/XGBoost) entre os registros norte-americano (NCI SEER, N > 60.000) e brasileiro (Registro de São Paulo e SUS Nacional, N > 25.000), desenvolvendo estratégias de adaptação de domínio (*domain adaptation*) e quantificação de incerteza conformal (MAPIE) com garantia marginal de 95%.
- **Métodos:** Estudo multicêntrico transcontinental de validação externa cruzada (*cross-system transportability benchmark*). Avaliação de calibração (razão O/E, Integrated Calibration Index), discriminação (AUROC, C-index) e análise de curva de decisão (DCA) sob transferência direta (*naive transfer*) versus adaptação de domínio supervisionada e predição conformal.
- **Resultados Planejados:** Mensuração exata da perda de calibração transcontinental, eficácia da recalibração conformal e mapeamento dos subgrupos clínicos mais vulneráveis ao erro de transferência.
- **Conclusões:** A governança por predição conformal e adaptação de domínio viabiliza a cooperação transcontinental em IA clínica, prevenindo danos iatrogênicos decorrentes da importação cega de modelos internacionais no SUS.

---

## 1. Introdução

O avanço de modelos de inteligência artificial na medicina tem sido acompanhado por uma crescente preocupação com a equidade algorítmica e a validade externa entre diferentes sistemas de saúde. A esmagadora maioria dos modelos preditivos publicados na literatura de ponta é desenvolvida a partir de bases de dados de nações de alta renda, notadamente dos Estados Unidos e da Europa Ocidental.

No transplante hepático e na oncologia cirúrgica, os ecossistemas clínicos do Brasil e dos Estados Unidos apresentam contrastes profundos. Enquanto o sistema norte-americano (refletido no NCI SEER e UNOS) opera sob dinâmicas específicas de financiamento e predominância crescente de disfunção metabólica associada à esteatoepatite (MASH), o Sistema Único de Saúde (SUS) brasileiro gerencia o maior sistema público universal de transplantes do mundo, com perfis etiológicos distintos, disparidades regionais de acesso e tempos de espera específicos.

A aplicação direta de modelos treinados em registros internacionais sem avaliação de transportabilidade representa risco grave de subestimação ou superestimação de sobrevida. Neste estudo, estabelecemos o primeiro benchmark transcontinental de validação cruzada entre o NCI SEER e os registros brasileiros, avaliando a perda de acurácia sob deslocamento de domínio e propondo a predição conformal (MAPIE) como barreira de segurança clínica.

---

## 2. Métodos

### 2.1 Registro do Protocolo e Governança
O protocolo completo foi registrado no Open Science Framework sob o identificador imutável [https://osf.io/w9mnq/](https://osf.io/w9mnq/) em conformidade com as diretrizes TRIPOD+AI (2024) e PROBAST+AI (2025).

### 2.2 Coortes de Estudo
- **Coorte Norte-Americana (NCI SEER):** Pacientes submetidos a ressecção hepática ou transplante entre 2000 e 2021 (N > 60.000).
- **Coorte Brasileira (São Paulo + SUS Nacional):** Receptores de transplante hepático e ressecção oncológica no Brasil entre 2007 e 2022 (N > 25.000).

### 2.3 Métricas de Transportabilidade e Adaptação
- Avaliação de deslocamento de covariáveis (*covariate shift*) através de distância de Wasserstein e divergência de Jensen-Shannon;
- Degradação de discriminação (delta C-index e delta AUROC) e calibração (razão O/E, declive e intercepto de calibração);
- Conjuntos de predição conformal (Split Conformal Prediction com MAPIE) para identificação de predições de alta incerteza na transferência entre fronteiras.

---

## Declarações

### Aprovação Ética
Estudo secundário baseado em bases de dados populacionais anonimizadas e desidentificadas de domínio público e registros estaduais sob licenças abertas de pesquisa. Isento de CEP/IRB nos termos da Resolução CNS/CONEP e 45 CFR 46.104(d)(4).

### Uso de Inteligência Artificial e Tecnologias Assistidas por IA na Redação Científica
Uso de Inteligência Artificial e Tecnologias Assistidas por IA na Redação Científica: Durante a preparação deste trabalho, os autores utilizaram Claude Opus 5.5 (Anthropic) para auxiliar no polimento do idioma inglês, refinamento gramatical, correções tipográficas e formatação do layout de tabelas. Após o uso desta ferramenta, os autores revisaram criticamente, verificaram e editaram todo o conteúdo gerado e assumem total responsabilidade pela integridade científica, precisão factual e conclusões apresentadas neste manuscrito. Em conformidade com os critérios de autoria da revista, tecnologias de IA generativa não são listadas como autores.
