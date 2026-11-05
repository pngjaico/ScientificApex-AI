# Manuscript Outline: Candidate 3 (Gastrao 2027)

## Working Title
**Explainable Machine Learning (XAI) and Conformal Prediction for Expanded Criteria Donor (ECD) Allocation in Liver Transplantation: Outperforming the Donor Risk Index (DRI) Using the UNOS/OPTN Registry**

## Canonical Sections (TRIPOD+AI Compliant)
1. **Structured Abstract** (Background, Objectives, Methods, Results, Conclusions)
2. **Introduction** (Donor organ shortage, intrinsic limitations of linear scores including DRI, ET-DRI, BAR, and D-MELD, rationale for non-linear tree ensembles and conformal uncertainty quantification)
3. **Methods**
   - Data Source and UNOS/OPTN Registry Cohort (2010 to 2025)
   - Eligibility Criteria and Definition of Expanded Criteria Donors (ECD)
   - Donor, Recipient, and Matching Predictor Variables (Strict Anti-Data-Leakage Design)
   - Primary Outcomes (90-Day and 1-Year Graft Failure) and Secondary Outcomes
   - Validation Strategy: Prospective Temporal Holdout (2021 to 2025) and Geographic Transportability (11 UNOS Regions)
   - Model Development: ElasticNet Baseline versus Gradient Boosted Trees (LightGBM, XGBoost)
   - Hyperparameter Optimization: Nested 5-Fold Cross-Validation via Optuna
   - Biological Explainability: Exact TreeSHAP and Second-Order Interaction Values
   - Comprehensive Calibration: Flexible Loess Curves, Calibration-in-the-Large, Calibration Slope, Brier Score, and Integrated Calibration Index (ICI)
   - Split Conformal Prediction: MAPIE with Guaranteed 95% Marginal and Conditional Coverage
   - Decision Curve Analysis (DCA) and Discard Reduction Simulation
4. **Results**
   - Study Flowchart and Baseline Participant Characteristics (Table 1)
   - Discrimination and Calibration Benchmarking: ML Models versus DRI, ET-DRI, BAR, and D-MELD
   - Temporal External Validation and Regional Transportability Across 11 UNOS Regions
   - SHAP Attribution Profiles and Non-Linear Protective Matching Phenotypes
   - Conformal Prediction Set Distributions and Uncertainty Profiles Across MELD Strata
   - Clinical Net Benefit (DCA) and Quantified Organ Rescue Potential
5. **Discussion**
   - Clinical and Pathophysiological Interpretation
   - Alignment and Divergence from Prior Landmark Allocation Studies
   - Study Limitations (Observational Registry Constraints, Unmeasured Confounders)
   - Translation to Organ Allocation Policy and Synergy with Machine Perfusion
6. **Declarations**
   - Protocol Registration (OSF Preregistration)
   - Data and Code Availability Statements
   - Competing Interests and Funding
   - Use of Artificial Intelligence and AI-Assisted Technologies in Scientific Writing: During the preparation of this work, the authors used Claude Opus 5.5 (Anthropic) to assist with English language polishing, grammatical refinement, typographical corrections, and table layout formatting. Following the use of this tool, the authors critically reviewed, verified, and edited all generated content and take full responsibility for the scientific integrity, factual accuracy, and conclusions presented in this manuscript. In accordance with target journal authorship criteria, generative AI technologies are not listed as authors.
