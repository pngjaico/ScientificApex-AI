"""Testes estruturais do pipeline de ingestão e escores clássicos UNOS STAR.

Garante que os cálculos de DRI (Feng 2006), BAR (Dutkowski 2012) e D-MELD
operem com precisão matemática em conformidade com as fórmulas originais
e que o leitor de arquivos processe tabelas compatíveis com o STAR files.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

PIPELINE_PATH = Path("projects/xai-liver-ecd-allocation-unos/analysis/01_pipeline_dados_unos.py")


@pytest.fixture
def unos_module():
    spec = importlib.util.spec_from_file_location("pipeline_unos", PIPELINE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_compute_dri_feng_2006_reference_donor(unos_module):
    """Doador ideal de referência (<40a, trauma, branco, >=170cm, DBD, local, CIT <8h) tem DRI = 1.0."""
    df = pd.DataFrame([{
        "donor_age": 25.0,
        "donor_cod": "trauma",
        "donor_race": "white",
        "donor_height_cm": 178.0,
        "donor_type_dcd": 0,
        "split_liver": 0,
        "allocation_share": "local",
        "cold_ischemia_time_hours": 5.0,
    }])
    dri = unos_module.compute_dri_feng_2006(df)
    assert np.isclose(dri.iloc[0], 1.0, atol=1e-3)


def test_compute_dri_feng_2006_marginal_donor(unos_module):
    """Doador marginal (DCD, idade 65, CVA, CIT 14h, regional) tem DRI significativamente elevado (>2.0)."""
    df = pd.DataFrame([{
        "donor_age": 65.0,              # +0.424
        "donor_cod": "cva",              # +0.145
        "donor_race": "white",           # 0
        "donor_height_cm": 165.0,        # +0.066 (<170cm)
        "donor_type_dcd": 1,             # +0.411
        "split_liver": 0,                # 0
        "allocation_share": "regional",  # +0.105
        "cold_ischemia_time_hours": 14.0 # +0.018
    }])
    # lin sum = 0.424 + 0.145 + 0.066 + 0.411 + 0.105 + 0.018 = 1.169
    # exp(1.169) ~ 3.218
    dri = unos_module.compute_dri_feng_2006(df)
    assert dri.iloc[0] > 3.0


def test_compute_bar_score(unos_module):
    """Calcula pontos BAR corretamente."""
    df = pd.DataFrame([{
        "recipient_lab_meld": 22.0,  # meld 20-24 => 3 pts
        "donor_age": 62.0,           # >60 => 1 pt
        "recipient_age": 63.0,       # >60 => 1 pt
        "cold_ischemia_time_hours": 10.0, # 8-12h => 1 pt
        "is_retransplant": 0,
        "recipient_ventilator": 1,   # 3 pts
    }])
    # total = 3 + 1 + 1 + 1 + 0 + 3 = 9 pts
    bar = unos_module.compute_bar_score(df)
    assert bar.iloc[0] == 9.0


def test_compute_dmeld(unos_module):
    """D-MELD = donor_age * recipient_lab_meld."""
    df = pd.DataFrame([{
        "donor_age": 50.0,
        "recipient_lab_meld": 24.0,
    }])
    dmeld = unos_module.compute_dmeld(df)
    assert dmeld.iloc[0] == 1200.0


def test_process_mock_star_data(tmp_path, unos_module):
    """Valida leitura e particionamento de arquivos com layout STAR."""
    raw_dir = tmp_path / "raw"
    out_dir = tmp_path / "out"
    raw_dir.mkdir()

    # Cria tabela TX_LI simulando colunas oficiais UNOS STAR
    n = 20
    tx_data = {
        "PX_ID": [f"PX_{i}" for i in range(n)],
        "DONOR_ID": [f"DON_{i}" for i in range(n)],
        "TX_DATE": ["2015-06-01"] * 10 + ["2023-03-15"] * 10,
        "REGION": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 2,
        "CAN_AGE_AT_TX": [45 + i for i in range(n)],
        "DON_TY": ["C"] * 15 + ["D"] * 5,
        "DON_AGE": [30 + i for i in range(n)],
        "DON_HGT_CM": [175.0] * n,
        "DON_WGT_KG": [78.0] * n,
        "COLD_ISCH_TM": [6.5] * n,
        "CAN_HGT_CM": [172.0] * n,
        "CAN_WGT_KG": [74.0] * n,
        "CAN_LAST_LAB_MELD": [20.0] * n,
        "CAN_VENTILATOR": [0] * n,
        "CAN_DIAL": [0] * n,
        "GSTATUS": [0] * 16 + [1] * 4,
        "GTIME": [1200.0] * 16 + [60.0] * 4,
        "COD_CAD_DON": [3] * n,
        "SHARE_TY": ["Local"] * n,
    }
    df_tx = pd.DataFrame(tx_data)
    df_tx.to_csv(raw_dir / "TX_LI.csv", index=False)

    res = unos_module.process_real_unos_star_data(raw_dir, out_dir)
    assert res["status"] == "success"
    assert res["dev_n"] == 10  # 2010-2020
    assert res["test_n"] == 10 # 2021-2025
    assert (out_dir / "coorte_desenvolvimento_2010_2020.csv.gz").exists()
    assert (out_dir / "coorte_validacao_temporal_2021_2025.csv.gz").exists()
