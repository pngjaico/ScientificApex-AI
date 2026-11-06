"""Unit tests for SEER Machine Learning Training & Conformal Prediction Pipeline."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("lightgbm")
pytest.importorskip("mapie")
pytest.importorskip("shap")

CANDIDATE_PATHS = [
    Path("analysis/seer/02_treinamento_xai_conformal.py"),
    Path("projects/xai-liver-seer-oncology/analysis/02_treinamento_xai_conformal.py"),
    Path("../projects/xai-liver-seer-oncology/analysis/02_treinamento_xai_conformal.py"),
]
ML_PIPELINE_PATH = next((p for p in CANDIDATE_PATHS if p.exists()), CANDIDATE_PATHS[1])


@pytest.fixture
def ml_module():
    spec = importlib.util.spec_from_file_location("seer_ml_module", ML_PIPELINE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_synthetic_cohort_generation(ml_module):
    df = ml_module.generate_synthetic_seer_cohort(n=500, seed=123)
    assert len(df) == 500
    for col in ml_module.CLINICAL_FEATURES:
        assert col in df.columns
    assert "death_cancer_5yr" in df.columns
    assert "year_of_diagnosis" in df.columns
    assert "within_milan" in df.columns
    assert df["death_cancer_5yr"].nunique() == 2
    assert df["year_of_diagnosis"].min() >= 2000
    assert df["year_of_diagnosis"].max() <= 2021


def test_dca_calculation(ml_module):
    y_true = np.array([0, 1, 0, 1, 1, 0, 1, 0])
    probs = {
        "model_a": np.array([0.1, 0.9, 0.2, 0.8, 0.7, 0.3, 0.6, 0.2]),
    }
    thresholds = np.array([0.2, 0.5])
    dca_df = ml_module.calculate_dca(y_true, probs, thresholds)
    assert len(dca_df) == 2
    assert "threshold" in dca_df.columns
    assert "net_benefit_model_a" in dca_df.columns
    assert "net_benefit_all" in dca_df.columns
    assert "net_benefit_none" in dca_df.columns
    assert dca_df["net_benefit_none"].iloc[0] == 0.0


def test_train_and_evaluate_pipeline(ml_module, tmp_path: Path):
    df = ml_module.generate_synthetic_seer_cohort(n=600, seed=42)
    output_dir = tmp_path / "results"
    
    metrics = ml_module.train_and_evaluate_seer(
        df=df,
        output_dir=output_dir,
        confidence_level=0.95,
        seed=42,
    )
    
    assert (output_dir / "metrics_summary.json").exists()
    assert (output_dir / "dca_results.csv").exists()
    assert (output_dir / "shap_feature_importance.csv").exists()
    
    assert "temporal_external_validation" in metrics
    assert "split_conformal_prediction_mapie" in metrics
    assert metrics["split_conformal_prediction_mapie"]["empirical_coverage_achieved"] >= 0.88
    assert len(metrics["top_predictive_features_shap"]) == 5
