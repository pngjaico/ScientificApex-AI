# Frozen Protocol Registration Packet (OSF / PROSPERO)

- **Title:** Machine Learning Explicavel (XAI) e Predicao Conformal para Alocacao de Orgaos Marginais (ECD) no Transplante Hepatico: Superando o Donor Risk Index (DRI) com Bases Populacionais (UNOS/OPTN)
- **Study Design:** `prediction-model`
- **EQUATOR Guidelines:** TRIPOD+AI, PROBAST+AI
- **Primary Recommended Registry:** `OSF` (Design 'prediction-model': prospective final registration should use OSF Preregistration (plus applicable clinical trial registry and ethics approval).)
- **Protocol Fingerprint SHA-256 (`protocol_sha256`):** `5f21b98281f13a6162fb5cf85b7ab40dab8c5e450624ff0dda6a666a2b5a4d01`
- **Submission Payload SHA-256:** `fdae140cd88198911422633a8b181d9758a62faaccb9326e158b7506c3b7e87e`

## 1. Research Question

Pode um algoritmo de aprendizado de maquina explicavel (LightGBM/XGBoost com TreeSHAP) e predicao conformal de incerteza (MAPIE), treinado no registro nacional UNOS/OPTN com particao temporal e geografica aninhada, superar os escores lineares classicos de risco (DRI, ET-DRI, BAR e D-MELD) na predicao de perda de enxerto em 90 dias e 1 ano para receptores de figados de doadores com criterios expandidos (ECD), oferecendo maior beneficio liquido clinico e potencial de resgate de orgaos descartados?

## 2. Complete Methodological Specification

```json
{
  "contract_version": 2,
  "exclusion_criteria": [
    "Receptores pediatricos (idade < 18 anos).",
    "Transplante intervivos (LDLT) ou domino.",
    "Transplantes combinados de multiplos orgaos (ex.: figado-rim, multivisceral).",
    "Retransplantes de repeticao (> 2o retransplante).",
    "Casos sem dados de desfecho vital ou status do enxerto em 90 dias / 1 ano."
  ],
  "hypothesis": "Modelos baseados em arvores de gradiente boosting com interacoes nao-lineares aprendidas combinados a calibracao flexivel e conjuntos de predicao conformal (MAPIE) superam significativamente o DRI, ET-DRI, BAR e D-MELD em discriminacao, calibracao e beneficio liquido clinico em DCA, permitindo reclassificar e resgatar com seguranca 15-20% dos enxertos ECD atualmente descartados sem comprometer a sobrevida.",
  "inclusion_criteria": [
    "Receptores com idade >= 18 anos no momento do transplante.",
    "Transplante hepatico ortotopico com enxerto de doador falecido (DBD ou DCD).",
    "Transplante realizado entre 01/01/2010 e 31/12/2025 com dados de seguimento documentados."
  ],
  "missing_data_plan": "Avaliacao formal de padroes de dados ausentes (MCAR, MAR, MNAR); flag explicita de indicacao para biopsia de doador; imputacao multipla encadeada (MICE) estritamente contida dentro das dobras de treinamento da validacao aninhada, combinada ao roteamento nativo de missing values dos algoritmos de arvore (LightGBM e XGBoost).",
  "notes": "Operacao 100% contida em projects/xai-liver-ecd-allocation-unos/. Paridade bilingue estrita em drafts/portugues/ e drafts/ingles/. Proibicao de travessoes na redacao em ingles. Declaracao canonica de IA Claude Opus 5.5 obrigatoria.",
  "objectives": [
    {
      "description": "Harmonizar e auditar a coorte de receptores adultos de transplante hepatico de doador falecido (DBD e DCD) do registro UNOS/OPTN (2010-2025, N > 60.000).",
      "id": "obj_1_cohort"
    },
    {
      "description": "Desenvolver modelos preditivos com restricoes de monotonicidade e hiperparametros otimizados por validacao cruzada aninhada de 5 dobras (nested 5-fold CV com Optuna) no periodo 2010-2020.",
      "id": "obj_2_development"
    },
    {
      "description": "Comparar formalmente o desempenho do modelo contra os 4 escores canonicos de bancada clinica (DRI de Feng et al., ET-DRI de Braat et al., BAR score de Dutkowski et al. e D-MELD).",
      "id": "obj_3_benchmarking"
    },
    {
      "description": "Realizar validacao externa prospectiva temporal no corte congelado 2021-2025 e validacao cruzada interna-externa (IECV) nas 11 regioes geograficas da UNOS.",
      "id": "obj_4_temporal_geographic_validation"
    },
    {
      "description": "Mapear valores TreeSHAP locais e globais e matriz de interacao de 2a ordem para isolar efeitos protetores e deleterios de matching doador-receptor.",
      "id": "obj_5_xai_interpretability"
    },
    {
      "description": "Implementar predicao conformal split via MAPIE com nivel de confianca garantido de 95% para quantificar incerteza individual em cada oferta de orgao.",
      "id": "obj_6_conformal_uncertainty"
    },
    {
      "description": "Executar Analise de Curva de Decisao (DCA) e simulacao de beneficio liquido para quantificar resgate de enxertos marginais e reducao de descarte.",
      "id": "obj_7_decision_curve_utility"
    },
    {
      "description": "Produzir manuscrito bilingue integral e pacote de apresentacao para a Sessao Plenaria de Transplante Hepatico do Gastrao 2027.",
      "id": "obj_8_bilingual_gastrao_pack"
    }
  ],
  "population": {
    "setting": "Receptores adultos de transplante hepatico ortotopico nos Estados Unidos (registro nacional UNOS/OPTN).",
    "target_subgroup": "Doadores com Criterios Expandidos (ECD: idade > 60 anos, doacao apos parada circulatoria DCD, esteatose macrovacuolar > 30%, parada cardiaca previa com ressuscitacao, sodio serico > 155 mEq/L ou tempo de isquemia fria > 10-12 horas)."
  },
  "prediction_spec": {
    "candidate_predictors": [
      "donor_age",
      "donor_type_dcd_dbd",
      "donor_cause_of_death",
      "donor_macrosteatosis_percentage",
      "donor_biopsy_performed_flag",
      "donor_cardiac_arrest_history",
      "donor_peak_sodium",
      "cold_ischemia_time_hours",
      "dcd_warm_ischemia_time_minutes",
      "donor_bmi",
      "donor_transaminases_sgot_sgpt",
      "donor_inotropic_support_count",
      "recipient_age",
      "recipient_primary_diagnosis",
      "recipient_lab_meld_at_transplant",
      "recipient_meld_na_at_transplant",
      "recipient_prior_abdominal_surgery",
      "recipient_portal_vein_thrombosis",
      "recipient_mechanical_ventilation",
      "recipient_dialysis_pretransplant",
      "recipient_icu_status",
      "recipient_bmi",
      "recipient_ascites_grade",
      "recipient_encephalopathy_grade",
      "abo_compatibility",
      "gender_mismatch",
      "recipient_donor_weight_ratio",
      "recipient_donor_height_ratio",
      "allocation_share_type"
    ],
    "outcome_definition": "Perda precoce do enxerto censurada por obito e falencia global do enxerto por qualquer causa (retransplante ou morte) em 90 dias e 1 ano pos-transplante, com rastreamento ativo em registros vitais nacionais (SSA Death Master File).",
    "prediction_horizon": "90 dias e 1 ano pos-transplante hepatico (desfechos primarios); seguimento longitudinal estendido para 3 e 5 anos (desfechos secundarios).",
    "target_population": "Receptores adultos (idade >= 18 anos) de transplante hepatico ortotopico isolado com enxerto de doador falecido (DBD e DCD) registrados no UNOS/OPTN STAR files (2010-2025), com foco em doadores com criterios expandidos (ECD).",
    "time_zero": "Momento exato da decisao clinica de oferta e aceitacao do enxerto hepatico pelo cirurgiao transplantador, imediatamente anterior ao implante cirurgico (preservacao estatica ou hipotermica oxigenada)."
  },
  "project_type": "prediction-model",
  "research_question": "Pode um algoritmo de aprendizado de maquina explicavel (LightGBM/XGBoost com TreeSHAP) e predicao conformal de incerteza (MAPIE), treinado no registro nacional UNOS/OPTN com particao temporal e geografica aninhada, superar os escores lineares classicos de risco (DRI, ET-DRI, BAR e D-MELD) na predicao de perda de enxerto em 90 dias e 1 ano para receptores de figados de doadores com criterios expandidos (ECD), oferecendo maior beneficio liquido clinico e potencial de resgate de orgaos descartados?",
  "target_venues": {
    "congress": "Gastrao 2027 (Sessao Plenaria de Transplante Hepatico)",
    "journal": "Liver Transplantation / Transplantation / American Journal of Transplantation / ABCD"
  },
  "title": "Machine Learning Explicavel (XAI) e Predicao Conformal para Alocacao de Orgaos Marginais (ECD) no Transplante Hepatico: Superando o Donor Risk Index (DRI) com Bases Populacionais (UNOS/OPTN)",
  "title_en": "Explainable Machine Learning (XAI) and Conformal Prediction for Expanded Criteria Donor (ECD) Allocation in Liver Transplantation: Outperforming the Donor Risk Index (DRI) using UNOS/OPTN Population Registry",
  "validation_plan": {
    "baseline_comparator": [
      "Donor Risk Index (DRI) de Feng et al. (2006)",
      "Eurotransplant Donor Risk Index (ET-DRI) de Braat et al. (2012)",
      "Balance of Risk (BAR score) de Dutkowski et al. (2012)",
      "D-MELD (Donor Age x Recipient Lab MELD)",
      "Treat-All (Alocar todos os enxertos ECD)",
      "Treat-None (Descartar todos os enxertos ECD)"
    ],
    "calibration_metrics": [
      "Brier Score",
      "Calibration-in-the-large (intercepto com slope fixo em 1,0)",
      "Calibration Slope (regressao logistica no logit da probabilidade)",
      "Integrated Calibration Index (ICI) baseado em suavizacao loess flexivel",
      "Estimated Calibration Error (ECE)"
    ],
    "clinical_utility_dca": "Decision Curve Analysis (DCA) com calculo de Beneficio Liquido (Net Benefit) para limiares de probabilidade de decisao clinica entre 0,05 e 0,40, com estimativa da taxa de resgate seguro de orgaos descartados.",
    "partition_unit": "patient",
    "strategy": "Nested 5-fold cross-validation com Optuna no corte 2010-2020 para desenvolvimento interno; validacao cruzada interna-externa (IECV) iterativa nas 11 regioes geograficas da UNOS; e holdout prospectivo temporal congelado no periodo 2021-2025 para validacao externa."
  }
}
```

## 3. Next Steps for Official Registration

1. Submit this frozen protocol to **OSF** (or **PROSPERO**).
2. Once finalized on OSF, run:
   `python -m article_machine registry fetch-osf D:/Usuario-pc/Projetos/Doutorado/projects/xai-liver-ecd-allocation-unos --id <OSF_ID> --reviewer "<Name>"`
3. Verify the finalized registration with:
   `python -m article_machine registry verify D:/Usuario-pc/Projetos/Doutorado/projects/xai-liver-ecd-allocation-unos --record <REVIEWED_JSON_PATH>`
