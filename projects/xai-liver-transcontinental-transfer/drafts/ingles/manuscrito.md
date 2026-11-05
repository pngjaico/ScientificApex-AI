# Transcontinental Machine Learning Transportability and Conformal Uncertainty Calibration in Liver Transplantation: Cross-System External Validation between Brazilian SUS and US SEER Registries (N > 85,000)

**Authors:** Joao Vitor Fiches Machado et al.  
**Protocol Registration (OSF):** [https://osf.io/w9mnq/](https://osf.io/w9mnq/) (*ID: w9mnq*, OSF Preregistration Schema)  
**Reporting Guidelines:** TRIPOD+AI (2024) / PROBAST+AI (2025)  
**Target Journals:** *Lancet Digital Health*, *Nature Medicine*, *JAMA Surgery*

---

## Structured Abstract

- **Background:** The clinical generalizability of medical artificial intelligence models is frequently undermined by distribution shift. Predictive algorithms derived from high-income health systems (such as United States national registries) often display substantial performance degradation when transferred to universal public health environments in middle-income countries (such as Brazil's Unified Health System [SUS]), driven by structural divergences in underlying disease etiology, waitlist dynamics, and graft allocation policies.
- **Objectives:** To rigorously evaluate geographic transportability and calibration degradation of gradient boosted machine learning models (LightGBM and XGBoost) across North American (NCI SEER, N > 60,000) and Brazilian (Sao Paulo State and SUS national registry, N > 25,000) cohorts, establishing domain adaptation strategies and distribution-free conformal uncertainty quantification (MAPIE) with 95% marginal coverage guarantees.
- **Methods:** A transcontinental cross-system external validation benchmark was established. Models trained in each national jurisdiction were evaluated under direct transfer without adjustment (naive transfer) and compared against supervised domain adaptation. Predictive discrimination (time-dependent AUROC, C-index), flexible calibration (observed-to-expected ratio, Integrated Calibration Index), and decision curve analysis (DCA) were evaluated.
- **Planned Outcomes:** Exact quantification of cross-border calibration loss, empirical evaluation of conformal prediction set sizes across recipient risk strata, and identification of clinical subgroups vulnerable to transfer error.
- **Conclusions:** Enforcing split conformal prediction and domain adaptation safeguards algorithmic equity and prevents clinical harm when deploying machine learning across divergent international healthcare systems.

---

## 1. Introduction

The rapid acceleration of clinical artificial intelligence has intensified concerns surrounding algorithmic transportability, fairness, and external validity across heterogeneous healthcare delivery systems. The vast majority of published medical machine learning models originate from high-income jurisdictions, predominantly the United States and Western Europe.

In liver transplantation and surgical oncology, healthcare delivery in Brazil and the United States diverges sharply. While the United States registry infrastructure (captured in NCI SEER and UNOS) operates within a mixed-payer landscape marked by increasing proportions of metabolic dysfunction-associated steatohepatitis (MASH), Brazil's Sistema Unico de Saude (SUS) directs the largest public, state-funded transplant service globally, characterized by distinct waitlist dynamics, geographical logistics, and donor epidemiology.

Directly applying models trained in foreign registries without evaluating cross-system transportability introduces substantial clinical risk, potentially skewing prognostic estimations and organ allocation decisions. In this study, we present the first transcontinental cross-system external validation benchmark between NCI SEER and Brazilian registries, measuring performance loss under real-world domain shifts and establishing conformal prediction as an empirical safeguard.

---

## 2. Methods

### 2.1 Protocol Registration and Methodological Governance
The complete study protocol was preregistered on the Open Science Framework under identifier [https://osf.io/w9mnq/](https://osf.io/w9mnq/) in accordance with TRIPOD+AI (2024) and PROBAST+AI (2025) standards.

### 2.2 Study Cohorts
- **United States Cohort (NCI SEER):** Adult patients undergoing surgical liver resection or liver transplantation between 2000 and 2021 (N > 60,000).
- **Brazilian Cohort (Sao Paulo and SUS National):** Adult recipients undergoing liver transplantation or surgical resection between 2007 and 2022 (N > 25,000).

### 2.3 Transportability Analysis and Conformal Inference
- Quantification of covariate shift using Wasserstein distance and Jensen-Shannon divergence;
- Cross-system performance degradation assessed via changes in C-index, Brier score, and calibration slope and intercept;
- Conformal uncertainty quantification (Split Conformal Prediction using MAPIE) to generate prediction sets with guaranteed 95% marginal coverage, highlighting ambiguous cases requiring manual multidisciplinary review.

---

## Declarations

### Ethical Approval and Regulatory Compliance
This study represents secondary analysis of de-identified, publicly accessible health databases and open scientific registry cohorts. The investigation is exempt from institutional review board oversight under US Title 45 CFR 46.104(d)(4) and corresponding Brazilian National Health Council (CNS/CONEP) ethical standards.

### Conflict of Interest
The authors declare no competing financial or personal interests.

### Funding
Doctoral research fellowship support from institutional sources.

### Data Availability Statement
Data from NCI SEER are publicly accessible upon completion of a research data agreement at https://seer.cancer.gov/data/access.html. The Sao Paulo transplant registry is open under Zenodo (DOI: 10.5281/zenodo.18189988). Analytic pipelines are registered on OSF (https://osf.io/w9mnq/).

### Use of Artificial Intelligence and AI-Assisted Technologies in Scientific Writing
Use of Artificial Intelligence and AI-Assisted Technologies in Scientific Writing: During the preparation of this work, the authors used Claude Opus 5.5 (Anthropic) to assist with English language polishing, grammatical refinement, typographical corrections, and table layout formatting. Following the use of this tool, the authors critically reviewed, verified, and edited all generated content and take full responsibility for the scientific integrity, factual accuracy, and conclusions presented in this manuscript. In accordance with [target journal name] authorship criteria, generative AI technologies are not listed as authors.
