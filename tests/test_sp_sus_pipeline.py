"""Unit tests for São Paulo & DATASUS Liver Transplant Pipeline."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SP_SUS_PIPELINE_PATH = Path("projects/xai-liver-ecd-allocation-unos/analysis/01_pipeline_dados_sp_sus.py")


@pytest.fixture
def sp_sus_module():
    spec = importlib.util.spec_from_file_location("sp_sus_pipeline", SP_SUS_PIPELINE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_dri_calculation_baseline_and_high_risk(sp_sus_module):
    # Doador jovem (<40), trauma, CIT < 8h, local
    df_low = pd.DataFrame([{
        "donor_age": 30.0,
        "donor_cod": "trauma",
        "donor_race": "white",
        "donor_height_cm": 175.0,
        "donor_type_dcd": 0,
        "split_liver": 0,
        "allocation_share": "local",
        "cold_ischemia_time_hours": 5.0,
    }])
    dri_low = sp_sus_module.compute_dri_feng_2006(df_low).iloc[0]
    assert np.isclose(dri_low, 1.0, atol=0.05)

    # Doador idoso (65), AVC, DCD, CIT 14h, national
    df_high = pd.DataFrame([{
        "donor_age": 65.0,
        "donor_cod": "cva",
        "donor_race": "white",
        "donor_height_cm": 165.0,
        "donor_type_dcd": 1,
        "split_liver": 0,
        "allocation_share": "national",
        "cold_ischemia_time_hours": 14.0,
    }])
    dri_high = sp_sus_module.compute_dri_feng_2006(df_high).iloc[0]
    assert dri_high > 2.5
    assert dri_high > dri_low


def test_bar_score_calculation(sp_sus_module):
    # Paciente baixo risco: MELD 12, doador 30, receptor 45, CIT 5h, sem retransplante/ventilação
    df_low = pd.DataFrame([{
        "recipient_lab_meld": 12.0,
        "donor_age": 30.0,
        "recipient_age": 45.0,
        "cold_ischemia_time_hours": 5.0,
        "is_retransplant": 0,
        "recipient_ventilator": 0,
    }])
    bar_low = sp_sus_module.compute_bar_score(df_low).iloc[0]
    assert bar_low == 0.0

    # Paciente alto risco: MELD 36 (11 pts), doador 65 (1 pt), receptor 62 (1 pt), CIT 14h (2 pts), retrans (5 pts), vent (3 pts)
    df_high = pd.DataFrame([{
        "recipient_lab_meld": 36.0,
        "donor_age": 65.0,
        "recipient_age": 62.0,
        "cold_ischemia_time_hours": 14.0,
        "is_retransplant": 1,
        "recipient_ventilator": 1,
    }])
    bar_high = sp_sus_module.compute_bar_score(df_high).iloc[0]
    assert bar_high == 23.0  # 11 + 1 + 1 + 2 + 5 + 3 = 23 pontos


def test_dmeld_calculation(sp_sus_module):
    df = pd.DataFrame([{
        "donor_age": 50.0,
        "recipient_lab_meld": 24.0,
    }])
    dmeld = sp_sus_module.compute_dmeld(df).iloc[0]
    assert dmeld == 1200.0


def test_ecd_flag(sp_sus_module):
    # Doador jovem sem critérios de risco -> NÃO ECD
    df_std = pd.DataFrame([{
        "donor_age": 35.0,
        "donor_type_dcd": 0,
        "donor_macrosteatosis": 5.0,
        "cold_ischemia_time_hours": 6.0,
        "donor_sodium": 142.0,
        "donor_cardiac_arrest": 0,
        "donor_inotropes": 0,
    }])
    assert sp_sus_module.compute_ecd_flag(df_std).iloc[0] == 0

    # Doador com esteatose 35% -> ECD
    df_ecd1 = pd.DataFrame([{
        "donor_age": 40.0,
        "donor_type_dcd": 0,
        "donor_macrosteatosis": 35.0,
        "cold_ischemia_time_hours": 6.0,
        "donor_sodium": 142.0,
        "donor_cardiac_arrest": 0,
        "donor_inotropes": 0,
    }])
    assert sp_sus_module.compute_ecd_flag(df_ecd1).iloc[0] == 1


def test_synthetic_cohort_generation(sp_sus_module):
    df = sp_sus_module.generate_synthetic_sp_sus_cohort(n_sp=100, n_sus=200, seed=42)
    assert len(df) == 300
    assert (df["cohort_origin"] == "SP_REGISTRY").sum() == 100
    assert (df["cohort_origin"] == "DATASUS_NATIONAL").sum() == 200
    assert "score_dri" in df.columns
    assert "score_bar" in df.columns
    assert "score_dmeld" in df.columns
    assert "is_ecd" in df.columns
    assert "graft_loss_90d" in df.columns
    assert "graft_loss_1yr" in df.columns
