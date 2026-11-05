"""Testes estruturais do pipeline de dados SEER (Carcinoma Hepatocelular).

Garante que o cálculo dos Critérios de Milão (Mazzaferro 1996), mapeamento de estadiamento
TNM 8ª Edição e categorização de modalidades cirúrgicas operem com precisão matemática.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

PIPELINE_PATH = Path("projects/xai-liver-seer-oncology/analysis/01_pipeline_dados_seer.py")


@pytest.fixture
def seer_module():
    spec = importlib.util.spec_from_file_location("pipeline_seer", PIPELINE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_milan_criteria_solitary_small_tumor(seer_module):
    """Nódulo único de 3.5 cm sem invasão vascular está DENTRO de Milão."""
    df = pd.DataFrame([{
        "tumor_size_cm": 3.5,
        "tumor_nodule_count": 1,
        "vascular_invasion": 0,
        "lymph_nodes_positive": 0,
    }])
    milan = seer_module.compute_milan_criteria(df)
    assert milan.iloc[0] == 1


def test_milan_criteria_large_tumor(seer_module):
    """Nódulo único de 6.0 cm (>5cm) está FORA de Milão."""
    df = pd.DataFrame([{
        "tumor_size_cm": 6.0,
        "tumor_nodule_count": 1,
        "vascular_invasion": 0,
        "lymph_nodes_positive": 0,
    }])
    milan = seer_module.compute_milan_criteria(df)
    assert milan.iloc[0] == 0


def test_milan_criteria_vascular_invasion(seer_module):
    """Nódulo de 2.0 cm com invasão vascular está FORA de Milão."""
    df = pd.DataFrame([{
        "tumor_size_cm": 2.0,
        "tumor_nodule_count": 1,
        "vascular_invasion": 1,
        "lymph_nodes_positive": 0,
    }])
    milan = seer_module.compute_milan_criteria(df)
    assert milan.iloc[0] == 0


def test_map_seer_surgical_modality(seer_module):
    """Valida códigos cirúrgicos SEER oficiais."""
    assert seer_module.map_seer_surgical_modality(61) == "transplant"
    assert seer_module.map_seer_surgical_modality(30) == "resection"
    assert seer_module.map_seer_surgical_modality(50) == "resection"
    assert seer_module.map_seer_surgical_modality(21) == "ablation"
    assert seer_module.map_seer_surgical_modality(0) == "other_none"


def test_process_mock_seer_data(tmp_path, seer_module):
    """Valida leitura e particionamento temporal da coorte SEER."""
    raw_dir = tmp_path / "raw"
    out_dir = tmp_path / "out"
    raw_dir.mkdir()

    n = 20
    seer_data = {
        "Patient ID": [f"SEER_{i}" for i in range(n)],
        "Year of diagnosis": [2010] * 10 + [2018] * 10,
        "Age at diagnosis": [62] * n,
        "Sex": ["Male"] * 15 + ["Female"] * 5,
        "CS tumor size (2004-2015)": [35] * n,  # 3.5 cm
        "CS extension (2004-2015)": ["Solitary"] * n,
        "Vascular invasion": ["No"] * n,
        "RX Summ--Surg Prim Site (1998+)": [61] * 10 + [30] * 10,  # 10 transplant, 10 resection
        "Survival months": [72] * 16 + [24] * 4,
        "Vital status recode (study cutoff used)": ["Alive"] * 16 + ["Dead"] * 4,
        "SEER cause-specific death classification": ["Alive"] * 16 + ["Dead attributable to this cancer"] * 4,
        "Derived AJCC Stage Group, 8th ed (2018+)": ["I"] * n,
    }
    df = pd.DataFrame(seer_data)
    df.to_csv(raw_dir / "seer_hcc_surgical.csv", index=False)

    res = seer_module.process_real_seer_data(raw_dir, out_dir)
    assert res["status"] == "success"
    assert res["dev_n"] == 10  # 2000-2015
    assert res["test_n"] == 10 # 2016-2021
    assert (out_dir / "coorte_desenvolvimento_seer_2000_2015.csv.gz").exists()
    assert (out_dir / "coorte_validacao_temporal_seer_2016_2021.csv.gz").exists()
