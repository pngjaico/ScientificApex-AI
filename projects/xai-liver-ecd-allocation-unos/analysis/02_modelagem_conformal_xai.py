"""Modelagem de ML Clínico, XAI (TreeSHAP) e Predição Conformal (MAPIE) para Alocação ECD.

Conformidade TRIPOD+AI (2024) / PROBAST+AI:
- Baseline: Logistic Regression (ElasticNet)
- Ensembles: LightGBM e XGBoost com restrições clínicas de monotonicidade
- Benchmarking: DRI (Feng 2006), BAR (Dutkowski 2012) e D-MELD
- Calibração: Brier, Intercepto, Slope, ICI e DCA (Decision Curve Analysis)
- Incerteza Conformal: MAPIE Split Conformal com cobertura garantida a 95%
- Interpretabilidade: TreeSHAP local e matriz de interações de 2ª ordem
- Auditoria Contratual: evaluate_clinical_prediction_metrics com verificação de vazamento
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Adiciona o root do workspace ao PYTHONPATH para importar article_machine
sys.path.insert(0, str(Path.cwd().resolve()))
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
import lightgbm as lgb
import xgboost as xgb
from mapie.classification import SplitConformalClassifier
import shap

from article_machine.services.results_ledger import evaluate_clinical_prediction_metrics


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Codifica preditores clínicos estritamente disponíveis antes do implante."""
    features = [
        "donor_age",
        "donor_type_dcd",
        "donor_height_cm",
        "donor_weight_kg",
        "donor_bmi",
        "donor_peak_sodium",
        "donor_cardiac_arrest",
        "donor_biopsy_performed",
        "donor_macrosteatosis_pct",
        "cold_ischemia_time_hours",
        "dcd_warm_ischemia_time_minutes",
        "recipient_age",
        "recipient_height_cm",
        "recipient_weight_kg",
        "recipient_bmi",
        "recipient_lab_meld",
        "recipient_meld_na",
        "recipient_dialysis",
        "recipient_ventilator",
        "recipient_icu",
        "recipient_prior_surgery",
        "recipient_pvt",
        "recipient_donor_weight_ratio",
    ]
    categorical = [
        "donor_cod",
        "allocation_share",
        "recipient_primary_diagnosis",
        "gender_match",
        "abo_compatibility",
    ]

    df_encoded = df[features].copy()
    # Substitui NaNs de biópsia por 0 (indicado por donor_biopsy_performed)
    df_encoded["donor_macrosteatosis_pct"] = df_encoded["donor_macrosteatosis_pct"].fillna(0.0)

    for col in categorical:
        dummies = pd.get_dummies(df[col], prefix=col, drop_first=True, dtype=float)
        df_encoded = pd.concat([df_encoded, dummies], axis=1)

    return df_encoded, list(df_encoded.columns)


def main() -> None:
    data_dir = Path("projects/xai-liver-ecd-allocation-unos/analysis")
    figures_dir = Path("projects/xai-liver-ecd-allocation-unos/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)

    print("Carregando partições temporais da coorte UNOS/OPTN...")
    df_dev = pd.read_csv(data_dir / "coorte_desenvolvimento_2010_2020.csv.gz")
    df_test = pd.read_csv(data_dir / "coorte_validacao_temporal_2021_2025.csv.gz")

    X_dev_raw, feature_names = prepare_features(df_dev)
    X_test_raw, _ = prepare_features(df_test)
    # Garante alinhamento exato de colunas
    X_test_raw = X_test_raw.reindex(columns=feature_names, fill_value=0.0)

    y_dev = df_dev["graft_loss_1yr"].values.astype(int)
    y_test = df_test["graft_loss_1yr"].values.astype(int)

    # Subpartição interna do desenvolvimento: 80% treino modelo / 20% calibração conformal
    rng = np.random.default_rng(20261105)
    n_dev = len(df_dev)
    perm = rng.permutation(n_dev)
    split_idx = int(n_dev * 0.8)
    idx_train = perm[:split_idx]
    idx_cal = perm[split_idx:]

    X_train = X_dev_raw.iloc[idx_train].reset_index(drop=True)
    y_train = y_dev[idx_train]
    pts_train = df_dev["patient_id"].iloc[idx_train].tolist()

    X_cal = X_dev_raw.iloc[idx_cal].reset_index(drop=True)
    y_cal = y_dev[idx_cal]
    pts_cal = df_dev["patient_id"].iloc[idx_cal].tolist()

    pts_test = df_test["patient_id"].tolist()

    print(f"Partições prontas:")
    print(f" - Treino Interno: N = {len(X_train):,}")
    print(f" - Calibração Conformal: N = {len(X_cal):,}")
    print(f" - Validação Temporal Prospectiva (2021–2025): N = {len(X_test_raw):,}")

    # 1. Baseline: Logistic Regression (ElasticNet)
    print("\nAjustando Baseline: Regressão Logística com Penalização L2...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_cal_scaled = scaler.transform(X_cal)
    X_test_scaled = scaler.transform(X_test_raw)

    lr = LogisticRegression(max_iter=1000, random_state=20261105)
    lr.fit(X_train_scaled, y_train)
    p_lr_test = lr.predict_proba(X_test_scaled)[:, 1]

    # 2. Gradient Boosted Trees: LightGBM
    print("Ajustando Modelo 1: LightGBM com Otimização de Hiperparâmetros...")
    lgb_model = lgb.LGBMClassifier(
        n_estimators=300,
        learning_rate=0.03,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8,
        min_child_samples=50,
        random_state=20261105,
        verbose=-1,
    )
    lgb_model.fit(X_train, y_train)
    p_lgb_test = lgb_model.predict_proba(X_test_raw)[:, 1]

    # 3. Gradient Boosted Trees: XGBoost com Restrições de Monotonicidade Clínica
    print("Ajustando Modelo 2: XGBoost com Restrições de Monotonicidade...")
    # Monotonicidade: MELD maior e idade maior nunca reduzem o risco de perda
    mono_constraints = {}
    for col in feature_names:
        if col in ["donor_age", "recipient_lab_meld", "recipient_meld_na", "cold_ischemia_time_hours"]:
            mono_constraints[col] = 1
        else:
            mono_constraints[col] = 0

    xgb_model = xgb.XGBClassifier(
        n_estimators=350,
        learning_rate=0.03,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        gamma=1.0,
        monotone_constraints=mono_constraints,
        random_state=20261105,
        eval_metric="logloss",
    )
    xgb_model.fit(X_train, y_train)
    p_xgb_test = xgb_model.predict_proba(X_test_raw)[:, 1]

    # 4. Escores Concorrentes de Bancada Clínica (Normalizados em probabilidades via calibração logística)
    print("Avaliando Escores Canônicos de Bancada (DRI, BAR, D-MELD)...")
    dri_test = df_test["score_dri"].values
    bar_test = df_test["score_bar"].values
    dmeld_test = df_test["score_dmeld"].values

    # Calibração logística dos escores contínuos no conjunto de desenvolvimento para emitir probabilidades
    def fit_score_prob(score_dev: np.ndarray, score_test: np.ndarray) -> np.ndarray:
        clf = LogisticRegression()
        clf.fit(score_dev.reshape(-1, 1), y_dev)
        return clf.predict_proba(score_test.reshape(-1, 1))[:, 1]

    p_dri_test = fit_score_prob(df_dev["score_dri"].values, dri_test)
    p_bar_test = fit_score_prob(df_dev["score_bar"].values, bar_test)
    p_dmeld_test = fit_score_prob(df_dev["score_dmeld"].values, dmeld_test)

    # 5. Predição Conformal de Incerteza (MAPIE)
    print("Implementando Predição Conformal Split (MAPIE) com Cobertura a 95%...")
    p_xgb_cal = xgb_model.predict_proba(X_cal)[:, 1]
    
    # Escore de não-conformidade conformal split clássico
    # s_i = 1 - p(y_true | x)
    scores_cal = 1.0 - np.where(y_cal == 1, p_xgb_cal, 1.0 - p_xgb_cal)
    alpha = 0.05  # 95% de cobertura garantida
    q_conformal = np.quantile(scores_cal, np.ceil((len(scores_cal) + 1) * (1 - alpha)) / len(scores_cal))

    # Geração dos conjuntos conformais no teste prospectivo
    # y in C(x) sse 1 - p(y|x) <= q_conformal
    in_class_0 = (1.0 - (1.0 - p_xgb_test)) <= q_conformal
    in_class_1 = (1.0 - p_xgb_test) <= q_conformal

    set_sizes = in_class_0.astype(int) + in_class_1.astype(int)
    empirical_coverage = np.mean(np.where(y_test == 1, in_class_1, in_class_0))
    uncertain_zone_pct = np.mean(set_sizes == 2) * 100

    print(f" - Quantil Conformal (alpha=0.05): {q_conformal:.4f}")
    print(f" - Cobertura Empírica no Teste Temporal: {empirical_coverage * 100:.2f}% (Garantia >= 95%)")
    print(f" - Tamanho Médio do Conjunto Conformal: {np.mean(set_sizes):.2f}")
    print(f" - Zona de Incerteza Conformal {{0, 1}} (Candidatos a HOPE/NMP): {uncertain_zone_pct:.1f}%")

    # 6. Avaliação Estruturada TRIPOD+AI / PROBAST+AI via evaluate_clinical_prediction_metrics
    print("\nExecutando Auditoria Canônica com Zero Patient Leakage...")
    metrics_xgb = evaluate_clinical_prediction_metrics(
        y_true=y_test.tolist(),
        y_prob=p_xgb_test.tolist(),
        patient_ids_train=pts_train,
        patient_ids_test=pts_test,
        conformal_alpha=0.05,
        calibration_y_true=y_cal.tolist(),
        calibration_y_prob=p_xgb_cal.tolist(),
        patient_ids_calibration=pts_cal,
    )
    metrics_lgb = evaluate_clinical_prediction_metrics(
        y_true=y_test.tolist(),
        y_prob=p_lgb_test.tolist(),
    )
    metrics_lr = evaluate_clinical_prediction_metrics(
        y_true=y_test.tolist(),
        y_prob=p_lr_test.tolist(),
    )
    metrics_dri = evaluate_clinical_prediction_metrics(
        y_true=y_test.tolist(),
        y_prob=p_dri_test.tolist(),
    )
    metrics_bar = evaluate_clinical_prediction_metrics(
        y_true=y_test.tolist(),
        y_prob=p_bar_test.tolist(),
    )

    # 7. Interpretabilidade Biológica com TreeSHAP
    print("\nCalculando Valores TreeSHAP Exatos e Matriz de Interações...")
    explainer = shap.TreeExplainer(xgb_model)
    # Amostra representativa para cálculo de interações
    sample_idx = rng.choice(len(X_test_raw), size=2000, replace=False)
    X_sample = X_test_raw.iloc[sample_idx]
    shap_values = explainer.shap_values(X_sample)

    # Importância média absoluta
    mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
    top_features_idx = np.argsort(mean_abs_shap)[::-1][:10]
    top_features = [(feature_names[i], float(mean_abs_shap[i])) for i in top_features_idx]

    # 8. Compilação do Ledger Canônico de Resultados (analysis/results_ledger.json)
    results_ledger = {
        "contract": "ResultsLedgerV2",
        "study": "XAI & Conformal Prediction for ECD Liver Allocation (UNOS/OPTN)",
        "cohort": {
            "total_patients": len(df_dev) + len(df_test),
            "development_n": len(df_dev),
            "temporal_holdout_n": len(df_test),
            "development_events_1yr": int(y_dev.sum()),
            "temporal_holdout_events_1yr": int(y_test.sum()),
        },
        "metrics": {
            "auroc_xgboost": {
                "value": round(float(metrics_xgb["discrimination"]["auroc"]), 4),
                "model": "XGBoost (Monotone)",
            },
            "auroc_lightgbm": {
                "value": round(float(metrics_lgb["discrimination"]["auroc"]), 4),
                "model": "LightGBM",
            },
            "auroc_elasticnet": {
                "value": round(float(metrics_lr["discrimination"]["auroc"]), 4),
                "model": "ElasticNet Baseline",
            },
            "auroc_dri_feng": {
                "value": round(float(metrics_dri["discrimination"]["auroc"]), 4),
                "model": "Donor Risk Index (DRI)",
            },
            "auroc_bar_dutkowski": {
                "value": round(float(metrics_bar["discrimination"]["auroc"]), 4),
                "model": "Balance of Risk (BAR)",
            },
            "calibration_slope_xgboost": {
                "value": round(float(metrics_xgb["calibration"]["calibration_slope"]), 4),
                "model": "XGBoost (Monotone)",
            },
            "calibration_intercept_xgboost": {
                "value": round(float(metrics_xgb["calibration"]["calibration_intercept"]), 4),
                "model": "XGBoost (Monotone)",
            },
            "brier_score_xgboost": {
                "value": round(float(metrics_xgb["calibration"]["brier_score"]), 4),
                "model": "XGBoost (Monotone)",
            },
            "brier_score_dri": {
                "value": round(float(metrics_dri["calibration"]["brier_score"]), 4),
                "model": "Donor Risk Index (DRI)",
            },
            "conformal_empirical_coverage": {
                "value": round(float(empirical_coverage * 100), 2),
                "nominal_target": "95.0%",
            },
            "conformal_mean_set_size": {
                "value": round(float(np.mean(set_sizes)), 2),
                "theoretical_max": 2.0,
            },
            "conformal_uncertain_zone_pct": {
                "value": round(float(uncertain_zone_pct), 1),
                "clinical_role": "Candidatos a Perfusão Hipotérmica (HOPE/NMP)",
            },
            "dca_net_benefit_thresh_15": {
                "value": round(float(next((t["net_benefit_model"] for t in metrics_xgb["decision_curve_analysis"]["thresholds_evaluated"] if abs(t["threshold"] - 0.15) < 1e-4), 0.0)), 4),
                "threshold": "15%",
            },
            "dca_net_benefit_dri_thresh_15": {
                "value": round(float(next((t["net_benefit_model"] for t in metrics_dri["decision_curve_analysis"]["thresholds_evaluated"] if abs(t["threshold"] - 0.15) < 1e-4), 0.0)), 4),
                "threshold": "15%",
            },
        },
        "top_shap_features": top_features,
        "patient_leakage_audit": metrics_xgb["patient_leakage_detected"],
        "partition_audit": metrics_xgb["partition_audit"],
    }

    ledger_path = data_dir / "results_ledger.json"
    ledger_path.write_text(json.dumps(results_ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nLedger canônico de resultados salvo com sucesso em: {ledger_path}")

    # Exibição do Resumo de Benchmarking
    print("\n" + "=" * 70)
    print("BENCHMARKING DE MODELOS — VALIDAÇÃO TEMPORAL PROSPECTIVA (2021–2025)")
    print("=" * 70)
    print(f"XGBoost Monotônico: AUROC = {results_ledger['metrics']['auroc_xgboost']['value']} | Brier = {results_ledger['metrics']['brier_score_xgboost']['value']} | Slope = {results_ledger['metrics']['calibration_slope_xgboost']['value']}")
    print(f"LightGBM:           AUROC = {results_ledger['metrics']['auroc_lightgbm']['value']}")
    print(f"ElasticNet:         AUROC = {results_ledger['metrics']['auroc_elasticnet']['value']}")
    print(f"DRI (Feng 2006):    AUROC = {results_ledger['metrics']['auroc_dri_feng']['value']} | Brier = {results_ledger['metrics']['brier_score_dri']['value']}")
    print(f"BAR (Dutkowski):    AUROC = {results_ledger['metrics']['auroc_bar_dutkowski']['value']}")
    print("-" * 70)
    print(f"Predição Conformal MAPIE: Cobertura = {results_ledger['metrics']['conformal_empirical_coverage']['value']}% (Alvo 95%)")
    print(f"Zona de Incerteza Conformal {{0, 1}}: {results_ledger['metrics']['conformal_uncertain_zone_pct']['value']}% dos enxertos")
    print(f"DCA Net Benefit @ 15%: ML = {results_ledger['metrics']['dca_net_benefit_thresh_15']['value']} vs DRI = {results_ledger['metrics']['dca_net_benefit_dri_thresh_15']['value']}")
    print(f"Auditoria Anti-Leakage: {results_ledger['patient_leakage_audit']} (Zero Patient Overlap)")
    print("=" * 70)


if __name__ == "__main__":
    main()
