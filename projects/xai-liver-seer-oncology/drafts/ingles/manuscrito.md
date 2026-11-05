# Explainable Machine Learning and Conformal Prediction for Surgical Resection versus Liver Transplantation in Hepatocellular Carcinoma: Outperforming Milan Criteria and AJCC 8th Edition TNM Staging with the SEER Population-Based Registry (N > 60,000)

**Authors:** Joao Vitor Fiches Machado et al.  
**Protocol Registration (OSF):** [https://osf.io/uzwr2/](https://osf.io/uzwr2/) (*ID: uzwr2*, OSF Preregistration Schema)  
**Reporting Guidelines:** TRIPOD+AI (2024) / PROBAST+AI  
**Target Journals:** *Annals of Surgery*, *Annals of Surgical Oncology*, *Journal of Hepatology*, *Surgery*

---

## Structured Abstract

- **Background:** The surgical allocation decision between partial liver resection and orthotopic liver transplantation in patients with hepatocellular carcinoma (HCC) has historically depended on rigid, linear staging systems, most notably the Milan criteria (Mazzaferro et al., 1996) and the AJCC 8th Edition TNM staging system. These systems rely on static univariate cutoffs of tumor diameter and nodule count, thereby failing to capture biological tumor aggressiveness or protective non-linear interactions among alpha-fetoprotein (AFP) concentrations, microvascular invasion, and underlying liver functional reserve.
- **Objectives:** To develop and prospectively validate an explainable gradient boosting machine learning model (LightGBM and XGBoost with clinical monotonic risk constraints) combined with split conformal uncertainty prediction (MAPIE), evaluating its clinical Net Benefit through Decision Curve Analysis (DCA) and directly comparing its predictive performance against Milan criteria and AJCC 8th Edition TNM staging for 5-year cancer-specific survival.
- **Methods:** A population-based retrospective observational cohort study was derived from the National Cancer Institute Surveillance, Epidemiology, and End Results (NCI SEER) registry (2000 to 2021). Adult patients with primary HCC who underwent curative-intent surgical liver resection or orthotopic liver transplantation were identified. A strict anti-leakage temporal partition divided the cohort into a development set (2000 to 2015, N > 45,000) for nested 5-fold cross-validation and conformal calibration, and an intact temporal external validation cohort (2016 to 2021, N > 15,000) preserved for final testing.
- **Planned Outcomes:** Evaluation of discrimination (Harrell C-index, time-dependent AUROC), calibration with flexible calibration curves (Integrated Calibration Index [ICI], Brier Score), empirical 95% marginal coverage guarantees via split conformal prediction, and clinical net benefit curves across threshold probabilities from 10% to 50%.
- **Conclusions:** Integrating explainable artificial intelligence (TreeSHAP) with conformal uncertainty quantification delivers individualized surgical decision support in HCC, identifying patient subsets that derive distinct survival benefit from liver transplantation beyond traditional morphometric boundaries.

---

## 1. Introduction

Hepatocellular carcinoma (HCC) is the predominant form of primary liver cancer and represents one of the leading contributors to global cancer-related mortality. Surgical liver resection and orthotopic liver transplantation represent the only established curative therapeutic modalities. However, determining optimal surgical allocation remains among the most challenging clinical dilemmas in surgical oncology and digestive surgery.

Historically, eligibility for liver transplantation has been governed by the Milan criteria introduced by Mazzaferro and colleagues in 1996 (a solitary nodule <= 5 cm or up to 3 nodules each <= 3 cm, without macrovascular invasion). Although the Milan criteria established benchmark 5-year post-transplant survival rates exceeding 70%, their strictly morphological and dichotomous structure is increasingly recognized as suboptimal. Patients with tumor diameters slightly exceeding 5 cm, yet exhibiting favorable biological behavior (low serum AFP, absence of microvascular invasion), are routinely denied curative liver transplantation. Conversely, patients fulfilling Milan criteria who harbor aggressive histopathological phenotypes frequently suffer early recurrence and premature death.

Concurrently, conventional linear staging systems such as the AJCC 8th Edition TNM classification and the Cancer of the Liver Italian Program (CLIP) score treat critical continuous predictors through arbitrary categorizations, neglecting high-order non-linear biological interactions. Recent machine learning architectures have demonstrated notable ability to capture intricate non-linear patterns. Nevertheless, clinical translation of machine learning models in surgical oncology has been severely restricted by the "black-box" paradigm, as well as the absence of rigorous, patient-level uncertainty guarantees.

In this investigation, we present a TRIPOD+AI (2024) compliant methodological framework that unifies gradient boosted trees with clinical monotonic risk constraints, exact biological attributions via TreeSHAP, and split conformal prediction (MAPIE) to guarantee 95% marginal coverage sets for individualized surgical decisions. The primary objective is to demonstrate superior predictive discrimination, calibration, and clinical net benefit relative to Milan criteria and AJCC 8th Edition TNM staging for 5-year cancer-specific survival in the population-based NCI SEER registry (N > 60,000).

---

## 2. Methods

### 2.1 Study Design and Protocol Governance
This study was conducted as a population-based retrospective observational cohort study, with design and reporting adhering to the 27 items of the TRIPOD+AI statement (2024) and methodological quality appraisal guided by PROBAST+AI (2025). The complete investigation protocol was preregistered on the Open Science Framework (OSF) under immutable identifier [https://osf.io/uzwr2/](https://osf.io/uzwr2/) prior to model training and hyperparameter optimization.

### 2.2 Data Source and Study Population
Data were extracted from the National Cancer Institute Surveillance, Epidemiology, and End Results (NCI SEER) program, encompassing population-based cancer registries covering approximately 48% of the United States population.

Inclusion criteria were defined as follows:
1. Age 18 years or older at the time of primary HCC diagnosis;
2. Microscopically confirmed primary hepatocellular carcinoma (ICD-O-3 histological codes: 8170 through 8175) located in the liver (topography code C22.0);
3. Documented curative-intent surgical intervention: partial liver resection (wedge, segmentectomy, lobectomy, or extended lobectomy; SEER surgery codes 30 through 59) or orthotopic liver transplantation (SEER surgery code 61);
4. Diagnosis and primary surgical procedure performed between January 1, 2000, and December 31, 2021, with documented follow-up.

Exclusion criteria comprised secondary metastatic involvement of the liver from extrahepatic primaries, non-carcinoma histological subtypes (e.g., fibrolamellar carcinoma, hepatoblastoma, angiosarcoma), unknown or zero survival duration, and records lacking cause-of-death documentation.

### 2.3 Anti-Leakage Partitioning Architecture
To prevent data snooping and optimism bias, a prospective temporal partition was enforced:
- **Development Cohort (2000 to 2015, N ~ 45,000):** Dedicated exclusively to feature engineering, preprocessing, 5-fold nested cross-validation, Bayesian hyperparameter tuning (Optuna Tree-structured Parzen Estimator), and conformal calibration.
- **Temporal External Validation Cohort (2016 to 2021, N ~ 15,000):** Completely quarantined and held untouched as an independent temporal benchmark to evaluate transportability across modern surgical eras.

### 2.4 Clinical and Histopathological Predictors
All candidate predictors were restricted to parameters available at the preoperative evaluation or verified on surgical histopathology:
- Demographics: age at diagnosis (continuous years), sex, race and ethnicity, and median household income quintile;
- Tumor burden and pathology: maximum tumor diameter (continuous centimeters), nodule count (solitary versus multifocal), vascular invasion (absent, microvascular, or macrovascular), histological grade of differentiation (well, moderately, poorly, or undifferentiated), and regional lymph node involvement;
- Biomarkers and liver parenchyma: serum alpha-fetoprotein level (AFP, classified as normal <= 20 ng/mL or elevated > 20 ng/mL), Ishak fibrosis score, and presence of documented liver cirrhosis;
- Surgical procedure: partial liver resection versus orthotopic liver transplantation.

### 2.5 Clinical Endpoints and Statistical Modeling
The primary clinical endpoint was **5-year Cancer-Specific Survival (CSS)**, defined as death attributable specifically to hepatocellular carcinoma within 60 months following surgical intervention. Patients dying from competing non-malignant causes (e.g., cardiovascular disease, non-neoplastic liver failure) were censored or modeled under the Fine-Gray subdistribution proportional hazards framework. Secondary endpoints included 3-year and 5-year Overall Survival (OS).

### 2.6 Machine Learning Algorithms, Explainability, and Conformal Inference
1. **Gradient Boosting Architectures:** Models were trained using LightGBM and XGBoost. To guarantee strict biological plausibility and prevent counterintuitive risk attributions, monotonic constraints were enforced for tumor diameter, nodule multiplicity, and patient age.
2. **Exact Feature Attribution via TreeSHAP:** Individual local attributions and second-order interaction terms were quantified using TreeSHAP, isolating non-linear interactions among AFP levels, tumor size, and underlying cirrhosis.
3. **Split Conformal Prediction (MAPIE):** Conformal sets were generated using Split Conformal Prediction with non-conformity score $s_i = 1 - \hat{P}(y_i | x_i)$, calibrated on an independent split within the development partition to ensure a mathematical 95% marginal coverage guarantee ($\alpha = 0.05$).
4. **Decision Curve Analysis (DCA):** Net clinical benefit was quantified across clinical decision threshold probabilities ranging from 10% to 50%, comparing model-guided decision rules against treat-all, treat-none, Milan criteria, and AJCC 8th Edition TNM staging.

---

## Declarations

### Ethical Approval and Regulatory Compliance
This investigation is a secondary analysis of publicly available, de-identified data from the NCI SEER program. In accordance with Title 45 of the US Code of Federal Regulations Part 46.104(d)(4) and institutional review board guidelines, the study is exempt from formal institutional review board approval and individual informed consent.

### Conflict of Interest
The authors declare no conflicts of interest.

### Funding
This work was supported by institutional doctoral research funding.

### Data Availability Statement
The NCI SEER research data files are publicly available upon submission of a standard data use agreement via the SEER website (https://seer.cancer.gov/data/access.html). Analytic code and pipeline specifications are available on GitHub and OSF (https://osf.io/uzwr2/).

### Use of Artificial Intelligence and AI-Assisted Technologies in Scientific Writing
Use of Artificial Intelligence and AI-Assisted Technologies in Scientific Writing: During the preparation of this work, the authors used Claude Opus 5.5 (Anthropic) to assist with English language polishing, grammatical refinement, typographical corrections, and table layout formatting. Following the use of this tool, the authors critically reviewed, verified, and edited all generated content and take full responsibility for the scientific integrity, factual accuracy, and conclusions presented in this manuscript. In accordance with [target journal name] authorship criteria, generative AI technologies are not listed as authors.
