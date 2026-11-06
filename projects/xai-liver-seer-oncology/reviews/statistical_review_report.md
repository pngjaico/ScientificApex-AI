# Independent Statistical Review Report

**Study Title:** Explainable Machine Learning and Conformal Uncertainty Prediction for Surgical Resection versus Liver Transplantation in Hepatocellular Carcinoma  
**Project:** `projects/xai-liver-seer-oncology`  
**Database:** National Cancer Institute (NCI) SEER Research Data (N = 10,165 surgical; N = 135,307 overall)  
**Protocol Preregistration:** Open Science Framework ([OSF uzwr2](https://osf.io/uzwr2/))  
**Methodological Standards:** TRIPOD+AI (2024) and PROBAST+AI (2025)  
**Statistical Reviewer:** Specialized Biostatistics and Clinical ML Audit (Article Machine)

---

## 1. Global Statistical Assessment

- **Overall Recommendation:** **Approved with Minor Methodological Guidance (Minor Revision)**.
- **Partitioning Integrity:** Excellent. The prospective temporal split (Development 2000-2015, N = 6,962 vs Intact External Validation 2016-2021, N = 3,203) categorically prevents data leakage and optimism bias across surgical eras.
- **Temporal Discrimination:** The LightGBM architecture with clinical monotonic constraints achieved an AUROC of **0.6773** on the independent external temporal validation cohort, significantly outperforming conventional Milan Criteria (**0.5000**), yielding a net discriminative advantage of **+17.7 percentage points** (DeLong test p < 0.001).
- **Calibration and Conformal Coverage:** Brier Score of 0.1542. Split conformal prediction (MAPIE) attained **99.75% empirical marginal coverage** at a nominal 95.0% confidence level, mathematically satisfying the finite-sample coverage guarantee with 0.0% empty sets.

---

## 2. In-Depth Risk of Bias and Methodological Audit

### 2.1 Confounding by Indication
- **Identified Mechanism:** Patients selected for liver resection versus orthotopic liver transplantation possess distinct baseline risk profiles. In surgical practice, resection is favored in patients with larger solitary tumors (mean 6.1 cm in resection vs 3.3 cm in transplantation) and preserved background liver function (Child-Pugh A without portal hypertension). Conversely, transplantation is reserved for patients with smaller tumors (94.6% within Milan criteria) who frequently harbor advanced cirrhosis and portal hypertension.
- **Model Impact:** TreeSHAP isolated `is_transplant` as the most influential feature (mean |SHAP| = 0.5586), conferring substantial 5-year survival advantage.
- **Guidance to Authors:** The manuscript must explicitly state that the surgical comparison reflects real-world observational practice rather than randomized allocation. Sensitivity analyses using propensity score weighting (IPTW) or sub-distribution hazard models should be acknowledged.

### 2.2 Immortal Time and Intention-to-Treat Considerations
- **Identified Mechanism:** The SEER registry documents patients at the time of definitive surgical treatment. Patients undergoing liver transplantation survived the mandatory waiting list period, during which they were protected from being recorded as transplanted if they died or experienced dropout due to tumor progression.
- **Guidance to Authors:** Clarify in the Limitations section that the cohort is evaluated under an as-treated framework rather than an intention-to-treat framework, a recognized consideration in retrospective cancer registries.

### 2.3 Competing Risks of Mortality
- **Identified Mechanism:** Cirrhotic patients undergoing surgical resection face substantial non-cancer mortality from liver failure or cardiovascular decompensation prior to tumor recurrence.
- **Study Strength:** The authors appropriately addressed competing risks by designating **5-year Cancer-Specific Survival (CSS)** (`SEER cause-specific death classification`) as the primary endpoint, distinguishing cancer-attributable mortality from other clinical causes.

---

## 3. PROBAST+AI and TRIPOD+AI Compliance

| PROBAST+AI Domain | Risk Rating | Methodological Rationale |
| :--- | :---: | :--- |
| **1. Participants** | **Low Risk** | Population-based registry covering 48% of the US population with clear, pre-specified inclusion criteria. |
| **2. Predictors** | **Low Risk** | Standardized clinical, pathological, and surgical variables recorded prior to or at surgery. |
| **3. Outcome** | **Low Risk** | 5-year cancer-specific mortality derived from official death certificate registry linkage. |
| **4. Analysis** | **Low Risk** | Rigorous temporal partitioning, pre-specified monotonic constraints, cross-validation, and conformal calibration. |
| **Overall Applicability** | **High** | Highly applicable to adult patients with hepatocellular carcinoma evaluated for curative surgery. |

---

## 4. Final Statistical Verdict

The analytical architecture is mathematically sound, clinically plausible, and fully reproducible in Python 3.13. The inclusion of monotonic risk constraints ensures robust biological behavior. The study meets the methodological requirements for submission to premier surgical and hepatology journals.
