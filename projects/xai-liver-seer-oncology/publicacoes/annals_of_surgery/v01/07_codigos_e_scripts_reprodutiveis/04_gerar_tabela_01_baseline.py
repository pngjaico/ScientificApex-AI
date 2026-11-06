#!/usr/bin/env python3
"""
Gera Tabela 1 Canônica de Características de Linha de Base (Baseline Table 1)
para o Estudo SEER HCC (Ressecção vs Transplante).
Diretrizes: TRIPOD+AI (2024), Annals of Surgery.
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

data_path = Path("projects/xai-liver-seer-oncology/analysis/coorte_seer_hcc_cirurgica_completa.csv.gz")
out_csv = Path("projects/xai-liver-seer-oncology/analysis/results/tabela_01_baseline_characteristics_seer.csv")
out_csv.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(data_path)

# Variáveis: Total (N=10.165), Ressecção (N=4.214), Transplante (N=5.951)
tx = df[df["surgical_modality"] == "transplant"]
resect = df[df["surgical_modality"] == "resection"]


def fmt_mean_sd(s: pd.Series) -> str:
    s_clean = pd.to_numeric(s, errors="coerce").dropna()
    return f"{s_clean.mean():.1f} (± {s_clean.std():.1f})"


def fmt_n_pct(s: pd.Series, val: any) -> str:
    n = (s == val).sum()
    pct = (n / len(s)) * 100
    return f"{n:,} ({pct:.1f}%)"


table_data = [
    {"Característica Clínica": "Total de Pacientes", "Coorte Geral (N=10.165)": f"{len(df):,}", "Ressecção Hepática (N=4.214)": f"{len(resect):,}", "Transplante Hepático (N=5.951)": f"{len(tx):,}"},
    {"Característica Clínica": "Idade, anos (Média ± DP)", "Coorte Geral (N=10.165)": fmt_mean_sd(df["age_years"]), "Ressecção Hepática (N=4.214)": fmt_mean_sd(resect["age_years"]), "Transplante Hepático (N=5.951)": fmt_mean_sd(tx["age_years"])},
    {"Característica Clínica": "Sexo Masculino, n (%)", "Coorte Geral (N=10.165)": fmt_n_pct(df["sex_male"], 1), "Ressecção Hepática (N=4.214)": fmt_n_pct(resect["sex_male"], 1), "Transplante Hepático (N=5.951)": fmt_n_pct(tx["sex_male"], 1)},
    {"Característica Clínica": "Etnia / Raça Branca, n (%)", "Coorte Geral (N=10.165)": fmt_n_pct(df["race_ethnicity"], "White"), "Ressecção Hepática (N=4.214)": fmt_n_pct(resect["race_ethnicity"], "White"), "Transplante Hepático (N=5.951)": fmt_n_pct(tx["race_ethnicity"], "White")},
    {"Característica Clínica": "Tamanho Tumoral, cm (Média ± DP)", "Coorte Geral (N=10.165)": fmt_mean_sd(df["tumor_size_cm"]), "Ressecção Hepática (N=4.214)": fmt_mean_sd(resect["tumor_size_cm"]), "Transplante Hepático (N=5.951)": fmt_mean_sd(tx["tumor_size_cm"])},
    {"Característica Clínica": "Tumor Único (Nódulo Único), n (%)", "Coorte Geral (N=10.165)": fmt_n_pct(df["nodule_count"], 1), "Ressecção Hepática (N=4.214)": fmt_n_pct(resect["nodule_count"], 1), "Transplante Hepático (N=5.951)": fmt_n_pct(tx["nodule_count"], 1)},
    {"Característica Clínica": "Invasão Micro/Macrovascular, n (%)", "Coorte Geral (N=10.165)": fmt_n_pct(df["vascular_invasion_code"], 1), "Ressecção Hepática (N=4.214)": fmt_n_pct(resect["vascular_invasion_code"], 1), "Transplante Hepático (N=5.951)": fmt_n_pct(tx["vascular_invasion_code"], 1)},
    {"Característica Clínica": "Alfa-fetoproteína (AFP) Elevada, n (%)", "Coorte Geral (N=10.165)": fmt_n_pct(df["afp_elevated"], 1), "Ressecção Hepática (N=4.214)": fmt_n_pct(resect["afp_elevated"], 1), "Transplante Hepático (N=5.951)": fmt_n_pct(tx["afp_elevated"], 1)},
    {"Característica Clínica": "Dentro dos Critérios de Milão, n (%)", "Coorte Geral (N=10.165)": fmt_n_pct(df["within_milan"], 1), "Ressecção Hepática (N=4.214)": fmt_n_pct(resect["within_milan"], 1), "Transplante Hepático (N=5.951)": fmt_n_pct(tx["within_milan"], 1)},
    {"Característica Clínica": "Óbito Câncer-Específico em 5 Anos, n (%)", "Coorte Geral (N=10.165)": fmt_n_pct(df["css_5yr_event"], 1), "Ressecção Hepática (N=4.214)": fmt_n_pct(resect["css_5yr_event"], 1), "Transplante Hepático (N=5.951)": fmt_n_pct(tx["css_5yr_event"], 1)},
    {"Característica Clínica": "Óbito Global em 5 Anos, n (%)", "Coorte Geral (N=10.165)": fmt_n_pct(df["os_5yr_event"], 1), "Ressecção Hepática (N=4.214)": fmt_n_pct(resect["os_5yr_event"], 1), "Transplante Hepático (N=5.951)": fmt_n_pct(tx["os_5yr_event"], 1)},
]

tab_df = pd.DataFrame(table_data)
tab_df.to_csv(out_csv, index=False, encoding="utf-8")
print(f"Tabela 1 salva com sucesso em: {out_csv}")
print(tab_df.to_string())
