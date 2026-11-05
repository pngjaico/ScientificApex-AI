# Explainable Machine Learning (XAI) and Conformal Uncertainty Prediction for Expanded Criteria Donor Allocation in Liver Transplantation: Outperforming the Donor Risk Index Using the UNOS/OPTN Population Registry

**Authors:** Joao Vitor Fiches Machado et al.  
**Reporting Standards:** TRIPOD+AI (2024) Statement and PROBAST+AI Quality Assessment  
**Protocol Registration:** Open Science Framework (OSF Preregistration: `https://osf.io/wq2f7/`, base repository `https://osf.io/ejw2v/`)

---

## Structured Abstract

- **Background:** Critical graft shortage in liver transplantation forces frequent discard of organs from Expanded Criteria Donors (ECD) and Donation after Circulatory Death (DCD). Conventional clinical scoring tools, such as the Donor Risk Index (DRI) and the Balance of Risk (BAR score), are linear additive models that fail to capture non-linear protective biological interactions between donors and recipients, leading to excessive refusal of viable organs.
- **Objectives:** To develop and prospectively validate an explainable gradient boosted machine learning model with split conformal uncertainty quantification (MAPIE) to predict one-year graft failure, quantify non-linear biological interactions, and measure clinical Net Benefit in organ discard reduction.
- **Methods:** National retrospective observational cohort study utilizing official UNOS/OPTN STAR files from 2010 to 2025. A strict anti-leakage partitioning scheme was implemented: internal development cohort (2010 to 2020) with nested 5-fold cross-validation via Optuna, an untouched prospective temporal holdout cohort (2021 to 2025), and internal-external cross-validation across all 11 UNOS geographic regions. Evaluated architectures included regularized logistic regression (ElasticNet), LightGBM, and XGBoost with clinical monotonicity constraints, benchmarked against the DRI (Feng et al., 2006) and the BAR score (Dutkowski et al., 2012). Explainability was mapped via exact TreeSHAP values and second-order interaction matrices. Individual patient uncertainty was bounded using split conformal prediction (MAPIE) targeting guaranteed 95% marginal coverage. Clinical utility was assessed using Decision Curve Analysis (DCA).
- **Results:** Pending official processing and extraction of authorized UNOS/OPTN STAR dataset files.
- **Conclusions:** Awaiting completion of formal data request and primary model evaluation.

---

## 1. Introduction

Orthotopic liver transplantation remains the definitive life-saving therapy for end-stage liver disease and selected hepatocellular carcinoma. However, persistent organ shortages impose significant waiting list mortality worldwide. To mitigate candidate attrition, transplant centers increasingly utilize marginal allografts, formally categorized as Expanded Criteria Donors (ECD: advanced age, macrovacuolar steatosis, marked hypernatremia, prolonged cold ischemia, and history of cardiac arrest) as well as Donation after Circulatory Death (DCD).

Accepting an offer for an expanded criteria allograft requires complex intraoperative and perioperative judgment under severe time constraints. The transplant team must balance the hazard of severe ischemia-reperfusion injury, early allograft dysfunction, and primary non-function against the competing risk of waitlist death while awaiting an optimal donor offer. Historically, this clinical decision has been guided by linear risk scoring systems, most notably the Donor Risk Index (DRI) introduced by Feng et al. in 2006, followed by matching models such as the Balance of Risk (BAR score, Dutkowski et al., 2012), the Eurotransplant DRI (ET-DRI, Braat et al., 2012), and the D-MELD index.

Despite widespread historical use, classical linear scores carry substantial methodological shortcomings. Built upon univariate or additive multivariable Cox proportional hazards frameworks, they assume that each donor risk factor exerts a constant proportional penalty across every prospective recipient. In clinical reality, liver transplantation biology is driven by multifaceted non-linear interactions. A young, ambulatory recipient with low laboratory MELD (< 18) frequently tolerates an older or moderately steatotic donor allograft with excellent functional recovery, whereas the exact same graft transplanted into an intubated, hemodynamically unstable recipient with MELD > 35 carries catastrophic risk of primary failure. By failing to account for protective and synergistic non-linear matching dynamics, linear scores systematically overestimate risk in low-acuity candidates, provoking unwarranted discard of viable organs.

Modern machine learning techniques, particularly gradient boosted decision trees, can capture complex multi-dimensional non-linear interactions without requiring manual pre-specification of interaction terms. Nevertheless, clinical integration of predictive artificial intelligence in organ allocation has been hampered by two fundamental challenges: the black-box nature of ensemble models, which impairs surgeon trust, and the output of uncalibrated point probabilities that convey an illusion of certainty while ignoring epistemic and aleatoric ambiguity.

This study directly addresses these challenges through a three-pronged methodological framework:
1. **Monotonically Constrained Boosted Ensembles:** Tree-based models incorporating formal clinical monotonicity constraints, preventing mathematically unconstrained algorithms from learning biologically implausible relationships (such as higher MELD or prolonged cold ischemia decreasing graft failure risk);
2. **Explainable Biological Interpretability (XAI):** Exact local Shapley feature attributions and second-order interaction matrices calculated via TreeSHAP, isolating specific protective donor-recipient phenotypes that enable safe graft rescue;
3. **Conformal Uncertainty Quantification (MAPIE):** Split conformal prediction sets delivering guaranteed 95% marginal coverage, effectively stratifying marginal offers into definitive low risk (suitable for conventional cold storage), definitive prohibitive risk, and a distinct conformal uncertainty zone (prime candidates for dynamic hypothermic or normothermic machine perfusion reconditioning).

Conducted in strict compliance with the TRIPOD+AI (2024) statement and appraised through the PROBAST+AI risk of bias instrument, this study leverages the national UNOS/OPTN registry to establish the statistical superiority, calibration fidelity, and clinical decision utility of explainable artificial intelligence over traditional linear allocation metrics.

---

## 2. Methods

### 2.1. Study Design and Ethical Governance
This is a retrospective population-based observational cohort study designed for the development, prospective temporal validation, and geographic transportability assessment of multivariable clinical prediction models, reported according to the 27-item TRIPOD+AI (2024) statement and the PROBAST+AI quality tool.

The study protocol was formally preregistered on the Open Science Framework (OSF Preregistration: `https://osf.io/wq2f7/`, parent project repository `https://osf.io/ejw2v/`). Because the research uses secondary, fully de-identified national registry microdata without direct patient contact or possibility of re-identification, the protocol is qualified as exempt from human subjects institutional review pursuant to United States Federal Regulation 45 CFR 46.104(d)(4) and institutional guidelines. Data handling strictly complies with the OPTN Data Use Agreement.

### 2.2. Data Source and Study Population
The study cohort is derived from the official Standard Transplant Analysis and Research (STAR) files maintained by the Organ Procurement and Transplantation Network (OPTN) and the Scientific Registry of Transplant Recipients (SRTR), which prospectively record all organ transplant procedures in the United States.

**Inclusion Criteria:**
- Adult recipients aged 18 years or older on the day of transplantation;
- Primary or first repeat orthotopic liver transplantation utilizing a deceased donor allograft (Donation after Brain Death [DBD] or Donation after Circulatory Death [DCD]);
- Procedures performed between January 1, 2010, and December 31, 2025, with completed follow-up.

**Exclusion Criteria:**
- Pediatric candidates (< 18 years);
- Living-donor liver transplantations (LDLT) and domino liver procedures;
- Multi-organ or multivisceral procedures (such as simultaneous liver-kidney or liver-heart transplants);
- High-order repeat retransplantations (> 2nd transplant);
- Missing graft survival status or vital status ascertainment during the primary evaluation window.

### 2.3. Anti-Data-Leakage Partitioning Architecture
The national dataset was partitioned strictly at the unique patient level (`patient_id`), preventing overlap across development, calibration, and validation subsets:
1. **Development Cohort (2010 to 2020):** Dedicated to variable harmonization, nested 5-fold cross-validation with Optuna Bayesian optimization, and split conformal calibration quantile calculation on an internal 80/20 holdout;
2. **Prospective Temporal Holdout (2021 to 2025):** Maintained completely untouched as an external temporal validation set. This partition serves as a stringent test of model transportability across national policy shifts, operating entirely under the post-2020 Acuity Circles allocation framework and the MELD 3.0 era;
3. **Geographic Validation (IECV):** Iterative internal-external cross-validation across all 11 UNOS administrative regions, assessing algorithmic transportability across varying regional procurement logistics and clinical practices.

### 2.4. Candidate Predictors (Prespecified at Organ Offer Time Zero)
All predictors were strictly limited to clinical variables documented and accessible prior to donor organ acceptance (the operational decision-point). No post-reperfusion intraoperative variables or post-operative laboratory values were admitted, eliminating temporal incorporation bias.

- **Donor Predictors:** Continuous age (years), donor type (DBD versus DCD), primary cause of death (anoxia, head trauma, cerebrovascular accident, other), biopsy macrovacuolar steatosis percentage, indication biopsy indicator flag, history of pre-procurement cardiac arrest with CPR, terminal peak serum sodium (mEq/L), cold ischemia time (CIT, hours), DCD warm ischemia time (WIT, minutes), donor body mass index (BMI, kg/m2), peak transaminases (AST and ALT, IU/L), and inotropic support count;
- **Recipient Predictors:** Age at transplantation, primary liver disease etiology (MASH, alcohol-associated liver disease, HCV, HBV, cholestatic, hepatocellular carcinoma), laboratory MELD and MELD-Na at allocation, previous abdominal surgery, portal vein thrombosis presence and grade, mechanical ventilation status at transplant, pretransplant dialysis or renal replacement therapy within seven days prior to surgery, ICU admission status at transplant, recipient BMI, ascites severity, and clinical encephalopathy grade;
- **Match Predictors:** ABO compatibility (identical, compatible, incompatible), donor-recipient biological sex match (gender mismatch), recipient-to-donor weight ratio, recipient-to-donor height ratio, and geographic sharing classification (local, regional, national distribution).

### 2.5. Missing Data Handling Strategy
Missingness mechanisms were evaluated across all predictors. Missing-at-random (MAR) covariates were handled using Multiple Imputation by Chained Equations (MICE) executed strictly within the inner training folds of the nested cross-validation without test leakage. For donor liver biopsy, which exhibits indication-driven Missing Not at Random (MNAR) characteristics (procurement surgeons preferentially biopsy visually steatotic organs), a dedicated binary indicator flag was incorporated alongside the continuous fat percentage, combined with the native tree-based missing path routing of LightGBM and XGBoost.

### 2.6. Primary and Secondary Endpoints
- **Primary Endpoint:** 1-year all-cause graft loss, defined as the composite endpoint of graft failure requiring urgent retransplantation or recipient mortality from any cause within 365 days of transplantation (mandatory OPTN primary endpoint), alongside 90-day early graft loss;
- **Secondary Endpoints:** Death-censored graft failure evaluated using Fine-Gray competing risk regression (treating recipient death with functioning graft as a competing event), long-term graft survival at 3 and 5 years, and simulated safe discard reduction rate among marginal ECD organs.

### 2.7. Algorithmic Modeling and Hyperparameter Tuning
Three predictive model paradigms were developed and compared:
1. **Parametric Baseline:** Regularized logistic regression with ElasticNet (combining L1 and L2 penalties), paired with restricted cubic splines for continuous clinical variables;
2. **LightGBM Classifier:** Histogram-based gradient boosted decision trees supporting native categorical features and optimal missing value routing;
3. **XGBoost Classifier with Monotonicity Constraints:** Gradient boosted trees with directional non-decreasing constraints enforced on established deleterious factors (MELD, donor age, and cold ischemia time), ensuring that isolated elevations in recipient acuity or ischemic insult never decrease predicted risk, while allowing unrestricted second-order cross-terms to learn protective interactions.

Hyperparameters were tuned using nested 5-fold cross-validation with the Optuna Bayesian optimization library (Tree-structured Parzen Estimator algorithm) to maximize PR-AUC and minimize log-loss without data snooping.

### 2.8. Clinical Scoring Benchmarks
All machine learning models were benchmarked against four canonical scoring systems:
1. **Donor Risk Index (DRI, Feng et al., 2006):** Calculated according to its canonical coefficients for age, cause of death, race, height, DCD status, split liver, sharing, and cold ischemia;
2. **Eurotransplant DRI (ET-DRI, Braat et al., 2012);**
3. **Balance of Risk (BAR score, Dutkowski et al., 2012);**
4. **D-MELD Index (Donor Age multiplied by Recipient Laboratory MELD).**

### 2.9. Biological Interpretability via TreeSHAP
To eliminate the black-box barrier, exact polynomial TreeSHAP was applied to quantify marginal Shapley contributions for individual predictions. In addition, the Lundberg second-order interaction tensor was computed to isolate pure non-linear coupling effects between donor risk factors and recipient acuity.

### 2.10. Conformal Uncertainty Quantification (MAPIE)
To overcome the false certainty of uncalibrated point estimates, split conformal prediction was implemented using the MAPIE library:
$$P\big(Y_{n+1} \in \mathcal{C}(X_{n+1})\big) \ge 1 - \alpha$$
with nominal error rate fixed at alpha = 0.05 (guaranteeing 95% marginal coverage). Non-conformity scores were evaluated on an independent calibration partition (20% of development), yielding individualized prediction sets:
- {0}: High-confidence low risk graft (safe for conventional static cold storage);
- {1}: High-confidence prohibitive failure risk (justifying offer refusal for that specific recipient);
- {0, 1}: **Conformal Uncertainty Zone**, delineating marginal allografts that should not be discarded, but instead routed toward ex-vivo hypothermic oxygenated perfusion (HOPE) or normothermic machine perfusion (NMP) for pre-implantation viability testing.

### 2.11. Evaluation Metrics and Decision Curve Analysis (DCA)
Model validation adhered strictly to contemporary clinical prediction guidelines:
- **Discrimination:** AUROC with 95% confidence intervals derived from 2,000 bootstrap resamples, pairwise DeLong testing against the DRI, and Average Precision (PR-AUC);
- **Calibration:** Flexible calibration curves estimated with loess smoothers, calibration-in-the-large (intercept a with slope fixed to 1), calibration slope (logistic regression on logit probability), Brier score, and the Integrated Calibration Index (ICI);
- **Decision Curve Analysis (DCA):** Net Benefit was quantified across decision thresholds between 0.05 and 0.35, comparing machine learning against Treat-All, Treat-None, and DRI-directed allocation cutoffs.

---

## 3. Results
*(This section awaits extraction and ingestion of authorized UNOS/OPTN STAR dataset files under sources/unos_star/)*

- **Baseline Cohort Characteristics (Table 1):** `{{metric:tabela_01_baseline}}`
- **Discrimination Metrics (AUROC):**
  - Monotonic XGBoost: `{{metric:auroc_xgboost}}`
  - LightGBM: `{{metric:auroc_lightgbm}}`
  - Baseline ElasticNet: `{{metric:auroc_elasticnet}}`
  - Donor Risk Index (DRI): `{{metric:auroc_dri_feng}}`
  - Balance of Risk (BAR score): `{{metric:auroc_bar_dutkowski}}`
- **Calibration Metrics:**
  - Calibration Slope (XGBoost): `{{metric:calibration_slope_xgboost}}`
  - Calibration Intercept (XGBoost): `{{metric:calibration_intercept_xgboost}}`
  - Brier Score (XGBoost): `{{metric:brier_score_xgboost}}`
  - Brier Score (DRI): `{{metric:brier_score_dri}}`
- **Conformal Uncertainty and Clinical Utility:**
  - Empirical Conformal Coverage (Target 95%): `{{metric:conformal_empirical_coverage}}%`
  - Mean Conformal Set Size: `{{metric:conformal_mean_set_size}}`
  - Allografts in Conformal Uncertainty Zone {0, 1}: `{{metric:conformal_uncertain_zone_pct}}%`
  - DCA Net Benefit at 15% Threshold (ML): `{{metric:dca_net_benefit_thresh_15}}`
  - DCA Net Benefit at 15% Threshold (DRI): `{{metric:dca_net_benefit_dri_thresh_15}}`

---

## 4. Discussion
*(To be detailed following official data extraction and model execution)*

---

## 5. Declarations

- **Protocol Registration:** The study protocol is preregistered on the Open Science Framework (OSF Preregistration: `https://osf.io/wq2f7/`, parent project `https://osf.io/ejw2v/`), adhering to TRIPOD+AI and PROBAST+AI standards.
- **Data and Code Availability:** Source code and analytical pipelines are version-controlled in the project repository. UNOS/OPTN STAR files are subject to institutional Data Use Agreements and can be formally requested through the SRTR/OPTN portal.
- **Competing Interests:** The authors declare no commercial, financial, or political conflicts of interest related to this work.
- **Funding:** Conducted within institutional graduate academic research without commercial sponsorship from pharmaceutical or perfusion machine manufacturers.
- **Use of Artificial Intelligence and AI-Assisted Technologies in Scientific Writing:** During the preparation of this work, the authors used Claude Opus 5.5 (Anthropic) to assist with English language polishing, grammatical refinement, typographical corrections, and table layout formatting. Following the use of this tool, the authors critically reviewed, verified, and edited all generated content and take full responsibility for the scientific integrity, factual accuracy, and conclusions presented in this manuscript. In accordance with target journal authorship criteria, generative AI technologies are not listed as authors.
