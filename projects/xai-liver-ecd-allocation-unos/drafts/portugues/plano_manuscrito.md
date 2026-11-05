# Estrutura do Manuscrito — Candidato 3 (Gastrão 2027)

## Título Provisório
**Machine Learning Explicável (XAI) e Predição Conformal de Incerteza para Alocação de Órgãos com Critérios Expandidos (ECD) no Transplante Hepático: Superando o Donor Risk Index (DRI) no Registro UNOS/OPTN**

## Seções Canônicas (TRIPOD+AI)
1. **Resumo Estruturado** (Contexto, Objetivos, Métodos, Resultados, Conclusões)
2. **Introdução** (Crise de escassez de enxertos, limitações do DRI/ET-DRI/BAR/D-MELD, aprendizado não-linear e predição conformal)
3. **Métodos**
   - Fonte de Dados e Coorte UNOS/OPTN (2010–2025)
   - Critérios de Elegibilidade e Definição de ECD
   - Preditores Clínicos de Doador, Receptor e Matching (Zero Data Leakage)
   - Desfechos Primários (Perda de Enxerto em 90 dias e 1 ano) e Secundários
   - Partição Temporal (Holdout 2021–2025) e Geográfica (11 Regiões UNOS)
   - Algoritmos (ElasticNet, LightGBM, XGBoost) e Otimização Bayesiana Aninhada (Optuna)
   - Interpretabilidade Biológica (TreeSHAP e Interações de 2ª Ordem)
   - Calibração Flexível (Curvas Loess/Spline, Slope, Intercepto, Brier e ICI)
   - Predição Conformal de Incerteza (MAPIE a 95% de Cobertura)
   - Análise de Curva de Decisão (DCA) e Resgate de Órgãos Descartados
4. **Resultados**
   - Fluxograma de Participantes e Tabela 1 (Características Basais)
   - Discriminação e Calibração Comparativa (DRI vs ET-DRI vs BAR vs D-MELD vs ML)
   - Transporte Geográfico e Validação Temporal Prospectiva
   - Padrões de Interação SHAP e Fatores de Proteção
   - Conjuntos Conformais de Decisão e Distribuição de Incerteza
   - Benefício Líquido Clínico e Potencial de Resgate de Fígados Marginais
5. **Discussão**
   - Interpretação Fisiopatológica e Clínica
   - Comparação com a Literatura Internacional
   - Limitações Inerentes a Registros Observacionais Retrospectivos
   - Implicações para Políticas de Alocação de Órgãos
6. **Declarações**
   - Registro de Protocolo (OSF)
   - Declaração de Disponibilidade de Código e Dados
   - Conflitos de Interesse e Financiamento
   - Declaração Canônica de Uso de IA: Claude Opus 5.5
