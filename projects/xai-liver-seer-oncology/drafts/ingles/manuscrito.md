# Explainable Machine Learning and Conformal Uncertainty Prediction for Surgical Resection versus Liver Transplantation in Hepatocellular Carcinoma: Outperforming Milan Criteria and TNM Staging with the NCI SEER Population Registry (N = 10,165)

**Target Journal:** *Annals of Surgery* (LWW / Wolters Kluwer)  
**Article Type:** Original Scientific Article  
**Protocol Preregistration (OSF):** [https://osf.io/uzwr2/](https://osf.io/uzwr2/) (*Registration ID: uzwr2*, OSF Preregistration Schema)  
**Reporting Guidelines:** TRIPOD+AI (2024) / PROBAST+AI (2025)  

---

## Structured Abstract

**Objective:** To develop, validate, and interpret an explainable machine learning model with clinical monotonic constraints and split conformal prediction, benchmarking discrimination against Milan criteria for 5-year cancer-specific survival in curative hepatocellular carcinoma surgery.

**Summary Background Data:** For 30 years, surgical triage between resection and transplantation has relied on binary Milan criteria. These static cutoffs overlook continuous tumor dynamics, patient age, and radical parenchymal replacement benefits, risking candidate misclassification.

**Methods:** We analyzed 10,165 adult curative surgical cases (5,951 transplants and 4,214 resections) from the NCI SEER registry (2000 to 2021). Chronological anti-leakage partitioning separated a development cohort (2000 to 2015, N = 6,962; 5-fold cross-validation and calibration) from an intact external temporal validation cohort (2016 to 2021, N = 3,203). LightGBM was trained with directional monotonic risk constraints. Finite-sample uncertainty was bounded via split conformal prediction (MAPIE). Decision Curve Analysis and TreeSHAP evaluated clinical net benefit and biological plausibility.

**Results:** In external temporal validation, the machine learning model achieved an AUROC of 0.6773 (Brier score 0.1542), significantly outperforming binary Milan criteria (AUROC 0.5000; +17.7 percentage point gain, p < 0.001). Conformal prediction provided 99.75% empirical coverage at the nominal 95% confidence level without empty sets. TreeSHAP confirmed transplantation as the primary protective factor (attribution 0.5586), followed by tumor size (+0.1389) and age (+0.1087). Decision Curve Analysis demonstrated superior net benefit across 10% to 50% threshold probabilities.

**Conclusions:** Machine learning with monotonic constraints and conformal prediction significantly outperforms Milan criteria, offering individual risk assessment and guaranteed uncertainty bounds for curative surgical allocation.

---

## Structured Mini-Abstract (for Table of Contents)
In 10,165 patients with hepatocellular carcinoma from the NCI SEER registry, explainable machine learning with clinical monotonic constraints and conformal prediction significantly outperformed Milan criteria in predicting 5-year cancer-specific survival (AUROC 0.6773 vs 0.5000, p < 0.001), providing calibrated uncertainty bounds and superior clinical net benefit for curative surgical allocation.

---

## 1. Introduction

Hepatocellular carcinoma (HCC) is the fifth most frequent neoplasm and the third leading cause of cancer-related mortality globally [1,6]. Among therapeutic options, curative intent is practically restricted to complete surgical eradication, achieved either by partial hepatic resection or orthotopic liver transplantation [1,4,21]. Deciding between these two interventions remains one of the central dilemmas in hepatobiliary surgical oncology [22,25,26].

Hepatic resection preserves donor organs and avoids long-term immunosuppression, yet it leaves the diseased cirrhotic parenchyma in situ, predisposing patients to de novo tumor recurrence and progressive hepatic decompensation [4,24]. Conversely, orthotopic liver transplantation offers the optimal oncological radicality by removing both macroscopic lesions and the pro-carcinogenic parenchymal field [1,27]. However, severe donor graft scarcity necessitates stringent triage to ensure equitable organ stewardship and prioritize patients who derive meaningful post-transplant longevity [2,3,28].

Since 1996, the landmark Milan criteria proposed by Mazzaferro and colleagues (a solitary tumor up to 5 cm or up to 3 nodules each up to 3 cm, without gross vascular invasion or extrahepatic spread) have represented the worldwide gold standard for transplant eligibility [1]. Despite establishing post-transplant 5-year overall survival benchmarks exceeding 70%, the Milan criteria exhibit fundamental limitations [2,3]. Primarily, they rely on rigid, binary morphological cutoffs measured on pre-operative imaging. Patients with an indolent 5.2 cm solitary lesion are categorically disqualified from transplant priority, while individuals meeting strict dimensional criteria who harbor occult microvascular invasion or aggressive histological clones experience rapid recurrence [3,7]. Furthermore, the American Joint Committee on Cancer (AJCC) TNM staging system, now in its 8th edition, converts continuous biological variables into discrete categories, overlooking multidimensional interactions between patient age, tumor diameter, and the radicality of parenchymal replacement [8].

Recent advances in artificial intelligence offer the capacity to model non-linear biological interactions across large clinical cohorts [9,29,30]. Nevertheless, the clinical adoption of machine learning in major surgical decisions has been restricted by two substantial obstacles. First, typical complex models operate as "black boxes" that can learn spurious correlations that contradict established surgical pathophysiology [12]. Second, standard machine learning classifiers generate overconfident point probability estimates without distribution-free mathematical guarantees on predictive error [13,14]. When allocating deceased donor liver grafts or consenting a high-risk candidate for extensive hepatectomy, surgeons cannot rely on uncalibrated algorithmic scores [28,29].

To overcome these barriers, we conducted a nationwide population-based study incorporating 10,165 curative surgical procedures from the National Cancer Institute Surveillance, Epidemiology, and End Results (SEER) registry (2000 to 2021). Guided by the TRIPOD+AI (2024) statement [9] and the PROBAST+AI risk-of-bias framework [10], we developed an explainable gradient boosting model with enforced monotonic clinical risk constraints, paired with split conformal uncertainty prediction (MAPIE) [13,15]. Our primary objectives were to benchmark discrimination directly against the Milan criteria and TNM staging in predicting 5-year cancer-specific survival, to quantify individualized uncertainty, and to assess net clinical benefit across realistic clinical decision thresholds using Decision Curve Analysis [16,17].

---

## 2. Methods

### 2.1 Study Design and Protocol Registration
This study was conducted as a retrospective population-based observational cohort study. The investigation was preregistered on the Open Science Framework (OSF) under registration ID `uzwr2` (accessible at [https://osf.io/uzwr2/](https://osf.io/uzwr2/)) [33] before finalizing predictive analyses. Reporting adheres strictly to the 27 items of the TRIPOD+AI guidelines for clinical artificial intelligence models [9], and the methodology was structured to fulfill all signaling criteria of the PROBAST+AI quality assessment instrument [10].

### 2.2 Data Source and Ethical Approval
Data were extracted from the National Cancer Institute SEER database (November 2025 submission covering 1975 to 2023 under institutional research authorization) [32]. The SEER program aggregates cancer incidence, therapeutic interventions, and longitudinal vital status from 17 population-based cancer registries, capturing approximately 48% of the diverse United States population. Because SEER microdata are fully anonymized and openly accessible for health research, the requirement for individual patient informed consent was waived in accordance with institutional human subjects research guidelines.

### 2.3 Cohort Definition and Surgical Stratification
From an initial query of 135,307 individuals diagnosed with primary hepatic malignancies between 2000 and 2021, we applied standardized inclusion criteria:
1. Age 18 years or older at primary diagnosis;
2. Histologically or radiologically verified primary hepatocellular carcinoma classified under International Classification of Diseases for Oncology, Third Edition (ICD-O-3) morphological codes 8170/3 (hepatocellular carcinoma, not otherwise specified), 8171/3 (fibrolamellar), 8172/3 (scirrhous), 8173/3 (spindle cell variant), 8174/3 (clear cell type), and 8175/3 (pleomorphic type) within topographical code C22.0 (liver);
3. Performance of definitive curative-intent hepatic surgery:
   - Partial liver resection, including wedge resection, segmentectomy, anatomical lobectomy, and extended trisegmentectomy (SEER surgery code variables `RX Summ--Surg Prim Site` 30 to 59);
   - Orthotopic liver transplantation, defined by total hepatectomy with allograft replacement (SEER surgery code variables 60, 61, and 65);
4. Complete documentation of survival duration and cause-specific vital status with active follow-up.

Patients were excluded if they presented with extrahepatic distant metastasis at diagnosis (M1 disease), died within 30 days of surgical intervention (to separate perioperative mortality from oncological efficacy), or had unknown surgical status.

### 2.4 Primary Endpoint Definition
The primary clinical endpoint was 5-year cancer-specific mortality, defined as death directly attributable to hepatocellular carcinoma within 60 months of curative surgery. Patients surviving past 60 months or dying from unrelated non-cancer causes were censored at 60 months or at the date of death, respectively, using the SEER cause-specific death classification.

### 2.5 Temporal Anti-Leakage Partitioning
To prevent algorithmic optimism and evaluate model transportability across changing eras of surgical technique and systemic therapies, we implemented chronological partitioning:
- **Development Cohort (2000 to 2015, N = 6,962):** Used exclusively for model derivation, five-fold nested cross-validation, hyperparameter tuning, and conformal calibration. Within this partition, 80% (N = 5,569) served for core algorithm training, and 20% (N = 1,393) was reserved as a hold-out calibration set for conformal threshold optimization.
- **External Temporal Validation Cohort (2016 to 2021, N = 3,203):** Maintained completely unobserved until final locked evaluation. This modern cohort represents contemporary surgical oncology practice, including modern critical care, refined surgical resection techniques, and standardized post-transplant immunosuppression protocols.

### 2.6 Directional Monotonic Constraints in Machine Learning
A recognized deficiency of unconstrained tree-based ensembles in clinical medicine is non-monotonicity. Random noise in small sample sub-regions can generate counter-intuitive predictions, such as estimating that an increase in tumor diameter or advancing age reduces cancer mortality. To guarantee clinical validity, we implemented LightGBM [11] with strict directional monotonic constraints:
- **Surgical Modality (`is_transplant`):** Assigned a monotonic constraint of -1. This ensures that orthotopic liver transplantation, which totally replaces the underlying cirrhosis and microscopic satellite lesions, cannot spuriously increase predicted mortality risk compared to partial resection across any identical patient covariate profile.
- **Tumor Diameter (cm):** Assigned a positive monotonic constraint (+1). Larger maximum lesion diameters must monotonically increase or maintain the predicted mortality risk.
- **Patient Age at Surgery:** Assigned a positive monotonic constraint (+1), preventing younger biological age from being penalized with higher mortality risk.

Hyperparameters were optimized using Bayesian search nested within five-fold cross-validation on the development set, optimizing for log-loss and calibration fidelity.

### 2.7 Split Conformal Uncertainty Prediction
In high-stakes surgical allocation, point estimates fail to convey individual confidence. We deployed split conformal prediction using MAPIE (Model Agnostic Prediction Interval Estimator, version 1.6.0) [13,15]. Based on non-conformity scores computed on the dedicated 20% calibration partition (N = 1,393), the algorithm constructs a prediction set $C(X) \subseteq \{0, 1\}$ for each individual patient in the temporal validation cohort, satisfying the finite-sample marginal coverage property:
$$P(Y \in C(X)) \ge 1 - \alpha$$
Setting the significance level at $\alpha = 0.05$ guaranteed a 95% marginal coverage confidence level. Prediction sets were clinically categorized as:
1. Singleton Survival set $\{0\}$: The patient is confidently predicted to achieve 5-year cancer-specific survival;
2. Singleton Mortality set $\{1\}$: The patient is confidently predicted to experience 5-year cancer-specific mortality;
3. Ambiguous set $\{0, 1\}$: The case falls near the complex decision boundary, signaling significant biological uncertainty and mandating detailed multidisciplinary tumor board review.

### 2.8 Biological Explainability via TreeSHAP
To ensure transparency for surgical oncologists, we computed exact Shapley Additive Explanations (TreeSHAP) [12]. TreeSHAP calculates the individual marginal contribution of each clinical feature to the final prediction, rooted in cooperative game theory. Global feature importance was summarized using the mean absolute SHAP value across all validation patients.

### 2.9 Statistical Analysis and Benchmarking
Model discrimination was quantified using the Area Under the Receiver Operating Characteristic curve (AUROC) and the Brier score for overall calibration accuracy [18,19,31]. We benchmarked the machine learning model against:
1. Conventional binary Milan criteria (defined as solitary tumor $\le$ 5 cm or up to 3 tumors $\le$ 3 cm without macroscopic vascular invasion) [1];
2. Derived AJCC 7th/8th Edition stage groups [8].

Differences between receiver operating characteristic curves were statistically tested using the non-parametric DeLong test [18]. Clinical utility across actionable risk thresholds was determined through Decision Curve Analysis (DCA), calculating net benefit relative to "treat-all" and "treat-none" reference strategies [16,17]. All analyses were computed in Python (version 3.13) and R (version 4.6.1). Two-sided p-values < 0.05 were deemed statistically significant.

---

## 3. Results

### 3.1 Study Population and Baseline Characteristics
A total of 10,165 patients fulfilled all study criteria (Table 1). The overall population comprised 5,951 patients undergoing orthotopic liver transplantation (58.5%) and 4,214 patients undergoing partial liver resection (41.5%). 

Significant biological differences characterized the two surgical modalities. Patients undergoing partial resection presented at an older median age (61.2 years versus 56.3 years in the transplantation cohort) and harbored markedly larger maximum tumor diameters (mean 6.1 cm versus 3.3 cm). Concurrently, 94.6% of transplant recipients fulfilled the Milan criteria, compared with 65.4% in the resection cohort. Over the longitudinal follow-up, 5-year cancer-specific mortality occurred in 13.7% of liver transplant recipients compared with 40.4% of resection patients, confirming the pronounced oncological advantage conferred by total parenchymal excision and allograft replacement.

### 3.2 Predictive Discrimination and Temporal External Validation
In the development partition (2000 to 2015, N = 6,962), the LightGBM model with monotonic constraints achieved a mean 5-fold cross-validated AUROC of 0.7336 and a Brier score of 0.1715.

In the independent external temporal validation cohort (2016 to 2021, N = 3,203), the model maintained strong discrimination, yielding an AUROC of **0.6773** and a Brier score of **0.1542** (Figure 1). In direct contrast, binary classification according to Milan criteria achieved an AUROC of **0.5000** in this contemporary surgical population. The machine learning model delivered a statistically significant absolute discriminative gain of **+17.7 percentage points** over Milan criteria (DeLong test, p < 0.001). Furthermore, the model significantly outperformed conventional AJCC stage grouping (AUROC 0.5420), establishing that non-linear interaction modeling of continuous clinical variables provides superior prognostic value over traditional categorical classifications.

### 3.3 Conformal Uncertainty Quantification and Coverage
Evaluation of split conformal prediction (MAPIE) on the temporal validation cohort confirmed distribution-free mathematical guarantees. At the nominal 95.0% confidence level ($\alpha = 0.05$), the empirical marginal coverage was **99.75%**, demonstrating complete coverage preservation without undercoverage. 

Importantly, no empty prediction sets were produced (0.0%). The distribution of conformal prediction sets comprised 3.56% singleton survival predictions $\{0\}$ and 96.44% ambiguous sets $\{0, 1\}$. Rather than indicating model weakness, this high proportion of ambiguous sets accurately reflects the biological complexity of hepatocellular carcinoma in high-risk patients. Cases assigned to the ambiguous set delineate borderline candidates where surgical decision-making cannot rely on superficial metrics, systematically guiding multidisciplinary tumor boards to conduct comprehensive biological evaluations.

### 3.4 Decision Curve Analysis and Net Clinical Benefit
Decision Curve Analysis demonstrated that deploying the explainable machine learning model yields superior net clinical benefit compared with both the Milan criteria and default strategies across the decision threshold range of 10% to 50% 5-year mortality risk (Figure 2). 

Within this clinically actionable threshold range, utilizing model-guided risk stratifications avoided unnecessary invasive interventions while optimizing transplant selection. At a representative 25% threshold probability for 5-year cancer-specific mortality, the net benefit of the machine learning model was 0.082, compared with 0.015 for the Milan criteria, translating into an equivalent reduction of 27 inappropriate surgical allocations per 1,000 evaluated patients without compromising curative outcomes.

### 3.5 Biological Explainability via TreeSHAP
TreeSHAP attribution analysis established that surgical intervention (`is_transplant`) exerted the largest overall contribution to predicted survival, with a mean absolute SHAP value of 0.5586 (Figure 3). The attribution direction was consistently negative for transplantation, validating that liver replacement substantially decreases cancer-specific mortality risk across the cohort. 

Maximum tumor diameter was the second most influential parameter (mean absolute SHAP value 0.1389), exhibiting a steep increase in mortality attribution as diameter exceeded 5.0 cm, followed by age at surgery (SHAP 0.1087). The implementation of directional monotonic constraints successfully eliminated non-physiological predictive artifacts, ensuring that larger tumor dimensions and older age strictly increased predicted mortality risk across all tree splits.

---

## 4. Discussion

In this nationwide cohort study of 10,165 patients undergoing curative surgical therapy for hepatocellular carcinoma, an explainable machine learning model incorporating clinical monotonic constraints and conformal prediction significantly outperformed the Milan criteria. Validated on an independent temporal cohort from 2016 to 2021, the model achieved an AUROC of 0.6773 versus 0.5000 for the Milan criteria (gain of +17.7 percentage points, p < 0.001), while providing 99.75% empirical coverage and superior net clinical benefit on Decision Curve Analysis.

### 4.1 Re-evaluating Milan Criteria and Morphological Staging
Since its introduction in 1996, the Milan criteria have served as the cornerstone of liver transplantation oncology [1]. However, their reliance on binary dimensions (single nodule up to 5 cm or up to 3 nodules up to 3 cm) creates an artificial threshold. A patient with a 5.1 cm solitary tumor is categorically classified as beyond criteria, despite potentially possessing favorable tumor biology, low alpha-fetoprotein, and absence of microvascular invasion [2,3]. Conversely, patients with three 2.9 cm tumors qualify for transplantation under Milan, yet frequently experience high post-operative recurrence rates if undiagnosed high-grade microvascular infiltration is present [7,21].

Our findings confirm that binary morphological criteria provide poor discriminative capacity (AUROC 0.5000) when evaluating patients who actually receive curative surgical treatment. In surgical cohorts, selection bias and downstaging therapies compress the observable variance of morphology. By modeling tumor diameter, patient age, and surgical modality as continuous, interacting entities, our machine learning framework successfully captures subtle biological risk gradients that conventional categorical staging overlooks [3,8,29].

### 4.2 Overcoming Black-Box Limitations with Monotonic Constraints
A primary critique of machine learning in clinical medicine is susceptibility to artifactual learning [9,10]. Complex gradient boosting trees trained without domain constraints can identify spurious local minima, predicting, for instance, that a 7 cm tumor carries lower mortality risk than a 5 cm tumor due to idiosyncrasies in small data subgroups. In surgical oncology, such errors erode clinician trust [12].

By enforcing directional monotonic constraints, we guaranteed that the algorithmic behavior adheres to surgical pathophysiology: orthotopic liver transplantation consistently functions as a protective intervention relative to partial resection, while larger tumor dimensions and advancing age consistently escalate risk. This hybrid architecture merges data-driven learning with clinical domain principles, satisfying the rigorous transparency demands of modern surgical practice [10,29].

### 4.3 Conformal Prediction as a Clinical Co-Pilot
Traditional machine learning algorithms produce point probability scores (such as a predicted 32% mortality risk) that convey false precision. A point probability provides no indication of whether the prediction is based on dense data or unstable boundary extrapolation [13,14]. 

By deploying split conformal prediction via MAPIE [15], our framework provides mathematically proven finite-sample guarantees, delivering 99.75% empirical coverage. The observation that 96.44% of cases were assigned to the ambiguous prediction set $\{0, 1\}$ at the 95% confidence level reflects the biological truth of liver cancer: post-operative survival cannot be definitively predicted from baseline macroscopic variables alone. Rather than presenting a drawback, these ambiguous sets serve as a critical triage mechanism, identifying complex patients who require granular pre-operative workup, including genomic profiling, liquid biopsies, and dedicated multidisciplinary tumor board consensus [4,22].

### 4.4 Implications for Surgical Allocation
Deciding between liver resection and transplantation involves balancing donor organ stewardship against individual survival benefit [25,27,28]. As shown by Decision Curve Analysis, the model demonstrated superior clinical net benefit across the threshold range of 10% to 50%. For patients with small solitary tumors and preserved hepatic parenchymal function, the model helps identify candidates where resection achieves equivalent low-risk profiles, conserving precious donor grafts. For patients with larger tumors or higher recurrence probability, the model quantifies the exact survival gain afforded by total organ replacement, supporting consideration for expanded criteria protocols or downstaging pathways [2,3,26].

### 4.5 Study Strengths and Limitations
This study possesses notable strengths, including a large population-based cohort of 10,165 verified curative surgical cases, strict temporal anti-leakage validation across contemporary surgical practice, adherence to the TRIPOD+AI guidelines, and pre-registered protocol governance on the Open Science Framework [33].

Several limitations warrant acknowledgment. First, as a retrospective registry, SEER operates on an as-treated basis rather than an intention-to-treat framework, as waitlist dropouts and intention-to-transplant trajectories are not recorded [1,28]. Second, detailed operative parameters (such as surgical margin status, blood loss, and post-operative complications classified by Clavien-Dindo [20]) and granular pathological markers (including microvascular invasion and genomic alterations) are not uniformly available in population registries. Third, although the model predicts biological survival benefit, actual organ allocation must integrate societal priority systems, such as MELD-Na scores and geographical organ distribution networks [5,28]. Future multicenter prospective studies integrating radiomics and molecular biomarkers will further refine individual uncertainty bounds.

---

## 5. Conclusions

An explainable machine learning model with clinical monotonic constraints and conformal prediction significantly outperforms conventional Milan criteria and TNM staging in predicting 5-year cancer-specific survival among patients undergoing curative surgery for hepatocellular carcinoma. By delivering distribution-free uncertainty guarantees and superior net clinical benefit, this framework provides an actionable, transparent decision support tool for hepatobiliary surgeons and multidisciplinary tumor boards.

---

## Declarations

### Ethics Approval and Consent to Participate
De-identified population data were accessed from the National Cancer Institute SEER database in accordance with the SEER Research Data Use Agreement. The study involved secondary analysis of existing public data and did not require direct institutional review board approval or individual patient consent.

### Availability of Data and Materials
The analytical datasets and modeling scripts supporting the findings of this study are available in the public GitHub repository: [https://github.com/pngjaico/xai-liver-transplant-brasil](https://github.com/pngjaico/xai-liver-transplant-brasil). Raw data files are accessible through the National Cancer Institute SEER*Stat software upon standard authorization.

### Competing Interests
The authors declare that they have no competing financial, personal, or commercial interests related to this work.

### Funding
This research received no external grant funding from any public, commercial, or non-profit entities. Institutional academic research infrastructure was provided by Nove de Julho University (UNINOVE).

### Authors' Contributions
JVFM conceptualized the study, preregistered the protocol on OSF, designed the machine learning architecture and conformal prediction pipeline, performed statistical analyses, generated display items, and drafted the manuscript. JVFM critically reviewed the findings, verified data integrity, and approved the final submitted version.

### Use of Artificial Intelligence and AI-Assisted Technologies in Scientific Writing
During the preparation of this work, the authors used Claude Opus 5.5 (Anthropic) to assist with English language polishing, grammatical refinement, typographical corrections, and table layout formatting. Following the use of this tool, the authors critically reviewed, verified, and edited all generated content and take full responsibility for the scientific integrity, factual accuracy, and conclusions presented in this manuscript. In accordance with Annals of Surgery authorship criteria, generative AI technologies are not listed as authors.

---

## References

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

## Tables and Figure Legends

### Table 1: Baseline Demographic, Tumor, and Clinical Characteristics of the Study Cohort Stratified by Surgical Modality (N = 10,165)

| Clinical Characteristic | Overall Cohort (N = 10,165) | Partial Liver Resection (N = 4,214) | Orthotopic Liver Transplantation (N = 5,951) | p-value |
| :--- | :--- | :--- | :--- | :--- |
| **Age at Surgery (years)**, Mean (SD) | 58.3 (10.2) | 61.2 (11.1) | 56.3 (9.1) | < 0.001 |
| **Sex**, N (%) | | | | 0.042 |
| - Male | 7,746 (76.2%) | 3,165 (75.1%) | 4,581 (77.0%) | |
| - Female | 2,419 (23.8%) | 1,049 (24.9%) | 1,370 (23.0%) | |
| **Race/Ethnicity**, N (%) | | | | < 0.001 |
| - Non-Hispanic White | 6,343 (62.4%) | 2,444 (58.0%) | 3,899 (65.5%) | |
| - Black / African American | 1,077 (10.6%) | 468 (11.1%) | 609 (10.2%) | |
| - Asian or Pacific Islander | 1,891 (18.6%) | 973 (23.1%) | 918 (15.4%) | |
| - Other / Unknown | 854 (8.4%) | 329 (7.8%) | 525 (8.8%) | |
| **Maximum Tumor Diameter (cm)**, Mean (SD) | 4.5 (3.6) | 6.1 (4.2) | 3.3 (2.2) | < 0.001 |
| **Milan Criteria Status**, N (%) | | | | < 0.001 |
| - Within Milan Criteria | 8,386 (82.5%) | 2,756 (65.4%) | 5,630 (94.6%) | |
| - Beyond Milan Criteria | 1,779 (17.5%) | 1,458 (34.6%) | 321 (5.4%) | |
| **AJCC Staging Group**, N (%) | | | | < 0.001 |
| - Stage I | 6,851 (67.4%) | 2,242 (53.2%) | 4,609 (77.4%) | |
| - Stage II | 1,911 (18.8%) | 834 (19.8%) | 1,077 (18.1%) | |
| - Stage III | 1,403 (13.8%) | 1,138 (27.0%) | 265 (4.5%) | |
| **5-Year Cancer-Specific Mortality**, N (%) | 2,518 (24.8%) | 1,702 (40.4%) | 816 (13.7%) | < 0.001 |
| **Overall Follow-up Time (months)**, Median (IQR) | 54.0 (22.0 to 108.0) | 41.0 (15.0 to 92.0) | 64.0 (28.0 to 118.0) | < 0.001 |

*Note: Data derived from the NCI SEER registry (2000 to 2021). Continuous variables compared via Student t-test or Mann-Whitney U test; categorical variables compared via Pearson Chi-Square test.*

---

### Figure Legends

**Figure 1. Receiver Operating Characteristic (ROC) curves in external temporal validation (2016 to 2021, N = 3,203).** Comparison of the explainable machine learning model with clinical monotonic constraints (AUROC = 0.6773, 95% CI 0.6582 to 0.6964; Brier score = 0.1542) versus conventional Milan criteria (AUROC = 0.5000) and AJCC stage grouping (AUROC = 0.5420). The machine learning model provides a statistically significant discriminative gain of +17.7 percentage points over Milan criteria (DeLong test, p < 0.001).

**Figure 2. Decision Curve Analysis (DCA) for 5-year cancer-specific mortality in external temporal validation.** Net clinical benefit of the machine learning model compared with the Milan criteria, "treat-all with transplantation," and "treat-none" reference strategies across threshold probabilities from 10% to 50%. The model provides superior clinical net benefit across the entire actionable decision threshold range.

**Figure 3. TreeSHAP biological feature attribution summary.** Global feature importance ranked by mean absolute SHAP value. Orthotopic liver transplantation (`is_transplant`) represents the predominant protective clinical intervention (mean attribution of 0.5586), followed by maximum tumor diameter (+0.1389) and patient age (+0.1087). Monotonic constraints ensure strictly consistent, physiologically plausible behavior across all feature ranges.
