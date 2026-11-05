# UNOS/OPTN STAR Data Request Specification

## Project: `xai-liver-ecd-allocation-unos`
**Explainable Machine Learning (XAI) and Conformal Prediction for Expanded Criteria Donor (ECD) Allocation in Liver Transplantation**

---

## 1. Project Overview and Institutional Information

- **Study Title:** Explainable Machine Learning (XAI) and Conformal Prediction for Expanded Criteria Donor (ECD) Allocation in Liver Transplantation: Outperforming the Donor Risk Index (DRI) using the UNOS/OPTN Population Registry
- **Principal Investigator:** Joao Vitor Fiches Machado and research team
- **Target Venues:** Liver Transplantation Plenary Session (Gastrao 2027); Target Journals: *Liver Transplantation*, *Transplantation*, *American Journal of Transplantation*.
- **Ethical Framework and IRB Exemption:** Qualified for Institutional Review Board exemption under United States Federal Regulation **45 CFR 46.104(d)(4)** (secondary research involving de-identified, publicly available, or restricted health registry datasets without individual patient re-identification).
- **Data Use Agreement (DUA):** Full compliance with the official OPTN Data Use Agreement, including strict preservation of donor and recipient anonymity, prohibition of re-identification attempts, and secure storage in access-controlled environments.

---

## 2. Scientific Rationale and Objectives

Orthotopic liver transplantation is severely constrained by an ongoing organ shortage. Consequently, hundreds of potentially viable deceased-donor livers categorized under Expanded Criteria Donors (ECD) or Donation after Circulatory Death (DCD) are discarded annually. 

Current organ allocation and risk stratification depend heavily on classical linear risk scores, particularly the Donor Risk Index (DRI, Feng et al., 2006) and the Balance of Risk (BAR score, Dutkowski et al., 2012). These scores are inherently additive and fail to capture critical non-linear donor-recipient interactions. For instance, younger or lower-acuity recipients (laboratory MELD < 20) may safely absorb marginal ECD grafts without compromising survival, whereas high-acuity recipients (laboratory MELD > 30) paired with prolonged cold ischemia experience compounded risk escalation.

This project requests the complete national cohort of deceased-donor liver transplants performed between January 1, 2010, and December 31, 2025. The study aims to develop and validate explainable gradient boosted trees (LightGBM and XGBoost with clinical monotonicity constraints), split conformal prediction (MAPIE) with guaranteed 95% marginal coverage, and second-order TreeSHAP interaction metrics, benchmarking their clinical Net Benefit via Decision Curve Analysis (DCA) directly against the DRI and BAR scores.

---

## 3. Requested Datasets (OPTN/SRTR STAR Release)

We request the standard Liver Transplant Analysis and Research (STAR) files:

| STAR File / Table | Description | Key Identifiers |
| :--- | :--- | :--- |
| **`TX_LI` (Liver Transplant)** | Complete baseline, operative, and longitudinal follow-up records for all deceased-donor liver transplants. | `TRR_ID_CODE`, `PX_ID`, `DONOR_ID` |
| **`DONOR_DECEASED` (Deceased Donor)** | Comprehensive donor demographics, cause of death, biopsy macrosteatosis, resuscitation history, hemodynamics, and preservation times. | `DONOR_ID` |
| **`CAND_LI` (Liver Candidate)** | Longitudinal waiting list trajectory, laboratory MELD/MELD-Na scores at allocation, and candidate acuity markers. | `PX_ID` |

---

## 4. Target Variable Dictionary

### Donor Variables (`DONOR_DECEASED`)
- `DON_AGE`: Donor age (years).
- `DON_TY`: Donor type (`C` = Brain death DBD, `D` = Circulatory death DCD).
- `COD_CAD_DON`: Cause of death (1=Anoxia, 2=CVA/Stroke, 3=Head trauma, 4=CNS tumor, 5=Other).
- `MACRO_FAT_LIV_DON`: Percentage of macrovacuolar fat on donor liver biopsy.
- `HIST_CARD_ARREST_DON`: History of cardiac arrest with CPR.
- `SODIUM_SERUM_DON`: Peak terminal serum sodium (mEq/L).
- `COLD_ISCH_TM`: Cold ischemia time (hours).
- `WARM_ISCH_TM`: Donor warm ischemia time (minutes, for DCD donors).
- `DON_HGT_CM`, `DON_WGT_KG`: Donor height and weight.
- `SGOT_DON`, `SGPT_DON`: Peak transaminases (AST/ALT, IU/L).
- `INOTROP_SUPPORT_DON`: Inotropic / vasopressor support count.

### Recipient and Match Variables (`TX_LI` and `CAND_LI`)
- `CAN_AGE_AT_TX`: Recipient age at transplantation.
- `CAN_GENDER`: Recipient biological sex.
- `CAN_ABO`, `DON_ABO`: Recipient and donor ABO blood groups.
- `CAN_HGT_CM`, `CAN_WGT_KG`: Recipient height and weight.
- `CAN_DGN`: Primary liver disease diagnosis (MASH, ALD, HCV, HBV, Cholestatic, HCC).
- `CAN_LAST_LAB_MELD`: Laboratory MELD score at transplant.
- `CAN_LAST_SRTR_LAB_MELD`: Laboratory MELD-Na score at transplant.
- `CAN_PREV_ABDOM_SURG`: Previous abdominal surgery (Yes/No).
- `CAN_PORTAL_VEIN_THROMB`: Portal vein thrombosis presence and grade.
- `CAN_VENTILATOR`: Mechanical ventilation at time of transplant.
- `CAN_DIAL`: Renal replacement therapy or hemodialysis within 7 days prior to transplant.
- `CAN_MED_COND`: Medical condition at transplant (1=ICU, 2=Hospitalized non-ICU, 3=Outpatient).
- `SHARE_TY`: Allocation sharing category (Local, Regional, National; DSA versus Acuity Circles).
- `REGION`: UNOS geographical region (1 to 11).

### Clinical Outcomes (`TX_LI`)
- `GSTATUS`: Graft status (1 = Graft failure, 0 = Functioning graft).
- `GTIME`: Days from transplant to graft failure or censoring.
- `PSTATUS`: Patient survival status (1 = Deceased, 0 = Alive).
- `PTIME`: Days from transplant to death or censoring.
- `COD`: Primary cause of graft loss or recipient mortality.

---

## 5. Submission Procedure

1. Submit this specification through the SRTR Data Request portal ([https://www.srtr.org/requesting-srtr-data/](https://www.srtr.org/requesting-srtr-data/)).
2. Complete institutional DUA signatures.
3. Upon receipt, place the raw files in:
   `projects/xai-liver-ecd-allocation-unos/sources/unos_star/`
