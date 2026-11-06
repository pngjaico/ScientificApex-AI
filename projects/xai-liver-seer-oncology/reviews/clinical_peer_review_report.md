# Clinical Peer Review Report

**Manuscript Title:** Explainable Machine Learning and Conformal Uncertainty Prediction for Surgical Resection versus Liver Transplantation in Hepatocellular Carcinoma  
**Authors:** Joao Vitor Fiches Machado et al.  
**Project:** `projects/xai-liver-seer-oncology` (OSF: `uzwr2`)  
**Target Journals:** *Annals of Surgery* / *American Journal of Transplantation*  
**Editorial Recommendation:** **Accept with Minor Revisions**

---

## 1. Evaluation of Surgical and Scientific Merit

This investigation addresses one of the most persistent and debated management decisions in gastrointestinal and hepatobiliary surgery: the individualized selection between liver resection and orthotopic liver transplantation for primary hepatocellular carcinoma (HCC).

Since their establishment in 1996, the Milan criteria by Mazzaferro and colleagues have defined transplant eligibility based on static morphological thresholds (single tumor <= 5 cm or up to 3 tumors <= 3 cm). While effective at securing acceptable post-transplant survival, this binary system excludes patients with modestly expanded tumors who possess indolent tumor biology, while failing to detect early recurrence in patients within Milan who harbor aggressive microvascular invasion.

The primary innovation of this study is the integration of gradient boosted decision trees with clinical monotonic constraints and split conformal uncertainty estimation (MAPIE) across a population cohort of **10,165 curative surgical procedures** from the National Cancer Institute SEER database. The demonstration of temporal AUROC of **0.6773** compared with **0.5000** for Milan criteria in independent external validation represents a meaningful contribution to surgical risk assessment.

---

## 2. Specific Comments for the Authors

### Introduction
- The clinical rationale and historical limitations of the Milan criteria and AJCC 8th Edition TNM staging are articulately framed.
- The clinical motivation for monotonic constraints is praiseworthy, as it guarantees that larger tumor diameters or older age cannot spuriously decrease predicted mortality risk.

### Methods
- The study adheres strictly to the 27 items of the TRIPOD+AI (2024) statement.
- The temporal division into development (2000-2015, N = 6,962) and intact validation (2016-2021, N = 3,203) provides an effective guardrail against optimism bias.
- The 95% conformal prediction framework delivers actionable safety margins for multidisciplinary tumor boards.

### Results and Figures
- The 300 DPI Figures 1, 2, and 3 demonstrate high graphical clarity and journal-ready presentation.
- Decision Curve Analysis confirms clinical net benefit across the threshold range of 10% to 50%.
- Identifying liver transplantation as the primary protective factor (SHAP value = 0.5586) aligns with pathophysiology, as transplantation removes both the neoplastic lesion and the underlying oncogenic cirrhotic parenchymal field.

### Discussion and Future Directions
- **Recommendation 1:** Expand the discussion on how this model could function in organ-scarce allocation frameworks (such as the Brazilian Unified Health System - SUS or Eurotransplant), emphasizing that the tool aids in quantifying personalized surgical benefit rather than circumventing waitlist rules.
- **Recommendation 2:** Note the clinical role of locoregional bridging therapies (such as transarterial chemoembolization or thermal ablation) during waitlist intervals.

---

## 3. Final Conclusion

The manuscript demonstrates high technical rigor, biological plausibility, and direct translational relevance to surgical oncology. Final acceptance is recommended following minor textual updates.
