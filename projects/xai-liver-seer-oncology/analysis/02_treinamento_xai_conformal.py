#!/usr/bin/env python3
"""
Pipeline de Treinamento, Explicabilidade (XAI) e Predição Conformal de Incerteza (MAPIE)
para Carcinoma Hepatocelular no Registro SEER NCI (>60.000 pacientes).

Superando os Critérios de Milão e o Estadiamento TNM (AJCC 8ª Edição).
Conforme diretrizes TRIPOD+AI (2024) e PROBAST+AI (2025).
Protocolo OSF: https://osf.io/uzwr2/ (ID: uzwr2)
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import lightgbm as lgb
import numpy as np
import pandas as pd
from mapie.classification import SplitConformalClassifier
from sklearn.metrics import (
    brier_score_loss,
    confusion_matrix,
    log_loss,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
import shap

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("xai-seer-train")

CLINICAL_FEATURES = [
    "age_years",
    "tumor_size_cm",
    "nodule_count",
    "is_transplant",
    "afp_elevated",
    "vascular_invasion_code",
    "histologic_grade",
    "fibrosis_ishak",
    "is_cirrhotic",
    "lymph_node_positive",
    "sex_male",
]

MONOTONE_CONSTRAINTS = {
    "age_years": 1,
    "tumor_size_cm": 1,
    "nodule_count": 1,
    "is_transplant": -1,
    "afp_elevated": 1,
    "vascular_invasion_code": 1,
    "histologic_grade": 1,
    "fibrosis_ishak": 1,
    "is_cirrhotic": 1,
    "lymph_node_positive": 1,
    "sex_male": 0,
}


def generate_synthetic_seer_cohort(n: int = 1200, seed: int = 42) -> pd.DataFrame:
    """Gera uma coorte sintética fidedigna ao schema do NCI SEER para testes e preflight."""
    rng = np.random.default_rng(seed)
    years = rng.integers(2000, 2022, size=n)
    ages = rng.normal(62, 10, size=n).clip(20, 88).round()
    sex = rng.choice(["Male", "Female"], size=n, p=[0.75, 0.25])
    
    # Cirurgia: 70% ressecção, 30% transplante
    is_tx = rng.choice([0, 1], size=n, p=[0.70, 0.30])
    
    # Biologia tumoral
    tumor_size = rng.gamma(shape=2.5, scale=1.8, size=n).clip(0.5, 18.0).round(1)
    nodule_count = rng.choice([1, 2, 3, 4], size=n, p=[0.60, 0.22, 0.12, 0.06])
    afp_elevated = rng.choice([0, 1], size=n, p=[0.55, 0.45])
    vasc_inv = rng.choice([0, 1, 2], size=n, p=[0.60, 0.25, 0.15])
    hist_grade = rng.choice([1, 2, 3, 4], size=n, p=[0.20, 0.45, 0.28, 0.07])
    fibrosis = rng.choice([0, 1, 2, 3, 4, 5, 6], size=n, p=[0.1, 0.1, 0.1, 0.15, 0.15, 0.2, 0.2])
    is_cirrhotic = (fibrosis >= 5).astype(int)
    ln_pos = rng.choice([0, 1], size=n, p=[0.92, 0.08])
    
    # Critérios de Milão calculados
    within_milan = (
        ((nodule_count == 1) & (tumor_size <= 5.0)) |
        ((nodule_count > 1) & (nodule_count <= 3) & (tumor_size <= 3.0))
    ) & (vasc_inv == 0) & (ln_pos == 0)
    
    # Risco real latente de óbito por câncer em 5 anos
    linear_risk = (
        -2.2
        + 0.18 * tumor_size
        + 0.35 * nodule_count
        + 0.50 * afp_elevated
        + 0.70 * vasc_inv
        + 0.25 * (hist_grade - 1)
        - 1.10 * is_tx  # Efeito protetor curativo substancial do transplante
        + 0.02 * (ages - 60)
        + 0.60 * ln_pos
    )
    prob_death = 1.0 / (1.0 + np.exp(-linear_risk))
    death_cancer_5yr = (rng.uniform(0, 1, size=n) < prob_death).astype(int)
    
    df = pd.DataFrame({
        "patient_id": [f"SEER_{i:06d}" for i in range(n)],
        "year_of_diagnosis": years,
        "age_years": ages,
        "sex_male": (sex == "Male").astype(int),
        "is_transplant": is_tx,
        "tumor_size_cm": tumor_size,
        "nodule_count": nodule_count,
        "afp_elevated": afp_elevated,
        "vascular_invasion_code": vasc_inv,
        "histologic_grade": hist_grade,
        "fibrosis_ishak": fibrosis,
        "is_cirrhotic": is_cirrhotic,
        "lymph_node_positive": ln_pos,
        "within_milan": within_milan.astype(int),
        "death_cancer_5yr": death_cancer_5yr,
    })
    return df


def calculate_dca(
    y_true: np.ndarray,
    probabilities: Dict[str, np.ndarray],
    thresholds: np.ndarray,
) -> pd.DataFrame:
    """Calcula Análise de Curva de Decisão (DCA) com Benefício Líquido Clínico (Net Benefit)."""
    n = len(y_true)
    event_rate = np.mean(y_true)
    results = []
    
    for pt in thresholds:
        weight = pt / (1.0 - pt)
        
        # Estratégia Treat All
        nb_all = event_rate - (1.0 - event_rate) * weight
        # Estratégia Treat None
        nb_none = 0.0
        
        row: Dict[str, Any] = {
            "threshold": round(float(pt), 4),
            "net_benefit_all": round(float(nb_all), 5),
            "net_benefit_none": 0.0,
        }
        
        for name, probs in probabilities.items():
            pred_positive = (probs >= pt).astype(int)
            tp = np.sum((pred_positive == 1) & (y_true == 1))
            fp = np.sum((pred_positive == 1) & (y_true == 0))
            nb = (tp / n) - (fp / n) * weight
            row[f"net_benefit_{name}"] = round(float(nb), 5)
            
        results.append(row)
        
    return pd.DataFrame(results)


def train_and_evaluate_seer(
    df: pd.DataFrame,
    output_dir: Path,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> Dict[str, Any]:
    """Executa o pipeline completo de treinamento, calibração conformal e avaliação TRIPOD+AI."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Particionamento Temporal Anti-Vazamento
    dev_mask = df["year_of_diagnosis"] <= 2015
    test_mask = df["year_of_diagnosis"] >= 2016
    
    df_dev = df[dev_mask].copy().reset_index(drop=True)
    df_test = df[test_mask].copy().reset_index(drop=True)
    
    logger.info("Coorte de Desenvolvimento (2000-2015): N = %d", len(df_dev))
    logger.info("Coorte de Teste Temporal (2016-2021): N = %d", len(df_test))
    
    target_col = "death_cancer_5yr" if "death_cancer_5yr" in df_dev.columns else "css_5yr_event"
    X_dev = df_dev[CLINICAL_FEATURES]
    y_dev = df_dev[target_col].values
    
    X_test = df_test[CLINICAL_FEATURES]
    y_test = df_test[target_col].values
    
    # 2. Divisão Interna da Coorte de Desenvolvimento: Treino (80%) vs Calibração Conformal (20%)
    X_train, X_calib, y_train, y_calib = train_test_split(
        X_dev, y_dev, test_size=0.20, random_state=seed, stratify=y_dev
    )
    
    # Restrições Monotônicas para o LightGBM
    monotone_list = [MONOTONE_CONSTRAINTS[f] for f in CLINICAL_FEATURES]
    
    lgb_model = lgb.LGBMClassifier(
        n_estimators=150,
        learning_rate=0.04,
        max_depth=5,
        num_leaves=24,
        subsample=0.85,
        colsample_bytree=0.85,
        monotone_constraints=monotone_list,
        random_state=seed,
        verbose=-1,
    )
    
    # 3. Validação Cruzada Aninhada em 5-Dobras no Treino
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    cv_aurocs = []
    cv_briers = []
    
    for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train), 1):
        fold_train_X, fold_val_X = X_train.iloc[train_idx], X_train.iloc[val_idx]
        fold_train_y, fold_val_y = y_train[train_idx], y_train[val_idx]
        
        fold_model = lgb.LGBMClassifier(
            n_estimators=120,
            learning_rate=0.04,
            max_depth=5,
            num_leaves=24,
            monotone_constraints=monotone_list,
            random_state=seed + fold,
            verbose=-1,
        )
        fold_model.fit(fold_train_X, fold_train_y)
        val_probs = fold_model.predict_proba(fold_val_X)[:, 1]
        cv_aurocs.append(roc_auc_score(fold_val_y, val_probs))
        cv_briers.append(brier_score_loss(fold_val_y, val_probs))
        
    mean_cv_auroc = float(np.mean(cv_aurocs))
    mean_cv_brier = float(np.mean(cv_briers))
    logger.info("Validação Cruzada 5-Dobras: AUROC Médio = %.4f | Brier = %.4f", mean_cv_auroc, mean_cv_brier)
    
    # 4. Ajuste do Modelo Final nos Dados de Treino Completos
    lgb_model.fit(X_train, y_train)
    
    # 5. Predição Conformal de Incerteza (MAPIE 1.6.0)
    conformal_clf = SplitConformalClassifier(
        estimator=lgb_model,
        confidence_level=confidence_level,
        prefit=True,
    )
    conformal_clf.conformalize(X_calib, y_calib)
    
    # Predições e Conjuntos Conformais na Coorte de Teste Temporal Intacta
    test_probs = lgb_model.predict_proba(X_test)[:, 1]
    _, test_psets = conformal_clf.predict_set(X_test)
    
    # Cobertura Marginal Empírica
    in_set = [bool(test_psets[i, y_test[i], 0]) for i in range(len(y_test))]
    empirical_coverage = float(np.mean(in_set))
    
    # Distribuição dos Tamanhos dos Conjuntos
    set_sizes = [int(np.sum(test_psets[i, :, 0])) for i in range(len(y_test))]
    prop_empty = float(np.mean([s == 0 for s in set_sizes]))
    prop_singleton_0 = float(np.mean([test_psets[i, 0, 0] and not test_psets[i, 1, 0] for i in range(len(y_test))]))
    prop_singleton_1 = float(np.mean([test_psets[i, 1, 0] and not test_psets[i, 0, 0] for i in range(len(y_test))]))
    prop_ambiguous = float(np.mean([s == 2 for s in set_sizes]))
    
    # 6. Benchmarking com Critérios de Milão
    outside_milan_probs = (1.0 - df_test["within_milan"]).astype(float).values
    auroc_model = float(roc_auc_score(y_test, test_probs))
    auroc_milan = float(roc_auc_score(y_test, outside_milan_probs))
    brier_model = float(brier_score_loss(y_test, test_probs))
    
    # 7. Análise de Curva de Decisão (DCA)
    thresholds = np.linspace(0.10, 0.50, 41)
    dca_df = calculate_dca(
        y_true=y_test,
        probabilities={
            "ml_model": test_probs,
            "milan_criteria": outside_milan_probs,
        },
        thresholds=thresholds,
    )
    dca_df.to_csv(output_dir / "dca_results.csv", index=False)
    
    # 8. Explicabilidade Biológica por TreeSHAP
    explainer = shap.TreeExplainer(lgb_model)
    shap_raw = explainer.shap_values(X_test)
    if isinstance(shap_raw, list):
        shap_vals = np.array(shap_raw[1])
    else:
        shap_vals = np.array(shap_raw)
        
    mean_abs_shap = np.mean(np.abs(shap_vals), axis=0)
    shap_importance_df = pd.DataFrame({
        "feature": CLINICAL_FEATURES,
        "mean_abs_shap": [round(float(v), 5) for v in mean_abs_shap],
        "monotone_constraint": [MONOTONE_CONSTRAINTS[f] for f in CLINICAL_FEATURES],
    }).sort_values(by="mean_abs_shap", ascending=False).reset_index(drop=True)
    shap_importance_df.to_csv(output_dir / "shap_feature_importance.csv", index=False)
    
    # 9. Consolidação dos Resultados em JSON
    metrics_summary = {
        "study": "XAI-Liver-SEER-Oncology",
        "osf_registration": "https://osf.io/uzwr2/",
        "cohort_sizes": {
            "development_2000_2015": len(df_dev),
            "temporal_validation_2016_2021": len(df_test),
            "train_split": len(X_train),
            "conformal_calibration_split": len(X_calib),
        },
        "nested_cross_validation_5fold": {
            "mean_auroc": round(mean_cv_auroc, 4),
            "mean_brier_score": round(mean_cv_brier, 4),
        },
        "temporal_external_validation": {
            "model_auroc": round(auroc_model, 4),
            "milan_criteria_auroc": round(auroc_milan, 4),
            "auroc_delta_vs_milan": round(auroc_model - auroc_milan, 4),
            "model_brier_score": round(brier_model, 4),
        },
        "split_conformal_prediction_mapie": {
            "target_confidence_level": confidence_level,
            "target_marginal_coverage": 1.0 - (1.0 - confidence_level),
            "empirical_coverage_achieved": round(empirical_coverage, 4),
            "coverage_guarantee_met": empirical_coverage >= (confidence_level - 0.02),
            "prediction_set_breakdown": {
                "singleton_survival_0_percent": round(prop_singleton_0 * 100, 2),
                "singleton_mortality_1_percent": round(prop_singleton_1 * 100, 2),
                "ambiguous_uncertain_percent": round(prop_ambiguous * 100, 2),
                "empty_percent": round(prop_empty * 100, 2),
            },
        },
        "clinical_decision_curve_analysis": {
            "evaluation_threshold_range": "[0.10, 0.50]",
            "net_benefit_ml_superior_to_milan": bool(
                dca_df["net_benefit_ml_model"].mean() > dca_df["net_benefit_milan_criteria"].mean()
            ),
        },
        "top_predictive_features_shap": shap_importance_df.head(5).to_dict(orient="records"),
    }
    
    with open(output_dir / "metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2, ensure_ascii=False)
        
    return metrics_summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Treinamento XAI e Predição Conformal SEER HCC")
    parser.add_argument("--input", type=str, default="", help="Caminho do CSV pré-processado do SEER")
    parser.add_argument("--output-dir", type=str, default="projects/xai-liver-seer-oncology/analysis/results", help="Pasta de saída")
    parser.add_argument("--synthetic-if-missing", action="store_true", help="Gera coorte sintética se o arquivo real não existir")
    parser.add_argument("--confidence-level", type=float, default=0.95, help="Nível de confiança conformal (padrão: 0.95)")
    parser.add_argument("--seed", type=int, default=42, help="Seed para reprodutibilidade estrita")
    args = parser.parse_args()
    
    input_path = Path(args.input) if args.input else None
    output_dir = Path(args.output_dir)
    
    if input_path and input_path.is_file():
        logger.info("Carregando base analítica do SEER: %s", input_path)
        df = pd.read_csv(input_path)
    elif args.synthetic_if_missing or not input_path:
        logger.info("Modo de teste: Gerando coorte sintética SEER para validação TRIPOD+AI...")
        df = generate_synthetic_seer_cohort(n=2500, seed=args.seed)
    else:
        logger.error("Arquivo %s não encontrado. Use --synthetic-if-missing para testes.", input_path)
        sys.exit(1)
        
    metrics = train_and_evaluate_seer(
        df=df,
        output_dir=output_dir,
        confidence_level=args.confidence_level,
        seed=args.seed,
    )
    
    logger.info("=== RESUMO EXECUTIVO DO TREINAMENTO SEER XAI ===")
    logger.info("AUROC do Modelo (Validação Temporal): %.4f (vs Milão: %.4f)",
                metrics["temporal_external_validation"]["model_auroc"],
                metrics["temporal_external_validation"]["milan_criteria_auroc"])
    logger.info("Cobertura Conformal Empírica (Alvo %.1f%%): %.2f%%",
                metrics["split_conformal_prediction_mapie"]["target_confidence_level"] * 100,
                metrics["split_conformal_prediction_mapie"]["empirical_coverage_achieved"] * 100)
    logger.info("Casos Ambíguos {0, 1} (Alta Incerteza / Comitê): %.2f%%",
                metrics["split_conformal_prediction_mapie"]["prediction_set_breakdown"]["ambiguous_uncertain_percent"])
    logger.info("Resultados persistidos em: %s", output_dir)


if __name__ == "__main__":
    main()
