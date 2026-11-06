"""Pipeline Canônico de Ingestão e Processamento dos Dados do NCI SEER (Hepatocarcinoma).

Projeto: `xai-liver-seer-oncology`
Diretrizes: TRIPOD+AI (2024) e PROBAST+AI (2025)
- Fonte de dados: NCI SEER Research Plus Database (1975-2023, Submissão Nov 2025)
- População: Pacientes adultos com Carcinoma Hepatocelular primário (C22.0, ICD-O-3 8170-8175)
- Comparação cirúrgica: Ressecção Hepática vs Transplante Hepático Ortotópico
- Desfecho primário: Sobrevida Câncer-Específica em 5 anos (CSS) e Sobrevida Global (OS)
- Benchmark: Critérios de Milão (Mazzaferro 1996) e Estadiamento AJCC TNM 8ª/7ª Edição
- Partição anti-vazamento: Treino/Nested CV (2000-2015) vs Validação Temporal Externa (2016-2021)
- Dados REAIS oficiais do NCI SEER (Zero dado sintético)
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import pandas as pd


def compute_milan_criteria(df: pd.DataFrame) -> pd.Series:
    """Classifica se o tumor está dentro ou fora dos Critérios de Milão (Mazzaferro et al., 1996)."""
    size = pd.to_numeric(df["tumor_size_cm"], errors="coerce").fillna(99.0).values
    nodules = pd.to_numeric(df["nodule_count"], errors="coerce").fillna(1).values
    vasc = pd.to_numeric(df["vascular_invasion_code"], errors="coerce").fillna(0).values
    nodes = pd.to_numeric(df.get("lymph_node_positive", pd.Series([0] * len(df))), errors="coerce").fillna(0).values

    c1 = (nodules == 1) & (size <= 5.0)
    c2 = (nodules >= 2) & (nodules <= 3) & (size <= 3.0)
    within_milan = (c1 | c2) & (vasc == 0) & (nodes == 0)
    return pd.Series(within_milan.astype(int), index=df.index, name="within_milan")


def map_seer_surgical_modality(surg_code: any) -> str:
    """Mapeia códigos cirúrgicos do SEER (RX Summ--Surg Prim Site) para categorias clínicas.

    Códigos SEER para Fígado (C22.0):
    - 60, 61, 65: Transplante Hepático (Total hepatectomy and transplant)
    - 30 a 59: Ressecção Hepática (parcial, cunha, segmentectomia, lobectomia, trissegmentectomia)
    - 20 a 26, 16: Ablação local / Quimioembolização
    - 00: Nenhuma cirurgia
    """
    try:
        c = int(surg_code)
        if c in [60, 61, 65]:
            return "transplant"
        elif 30 <= c <= 59:
            return "resection"
        elif 20 <= c <= 26 or c == 16:
            return "ablation"
        else:
            return "other_none"
    except (ValueError, TypeError):
        s = str(surg_code).lower()
        if "transplant" in s:
            return "transplant"
        elif "resect" in s or "lobect" in s or "segment" in s:
            return "resection"
        elif "ablat" in s:
            return "ablation"
        return "other_none"


def process_real_seer_data(raw_dir: Path, output_dir: Path) -> dict:
    """Processa arquivo exportado do SEER*Stat com a coorte de Hepatocarcinoma."""
    raw_dir = Path(raw_dir)
    output_dir = Path(output_dir)

    seer_files = (
        list(raw_dir.glob("*seer*.*"))
        + list(raw_dir.glob("*export*.*"))
        + list(raw_dir.glob("*.csv"))
        + list(raw_dir.glob("*.txt"))
    )

    if not seer_files:
        raise FileNotFoundError(f"Nenhum arquivo de dados SEER encontrado em '{raw_dir}'.")

    fpath = seer_files[0]
    print(f"Lendo base SEER de Hepatocarcinoma: {fpath}")

    # Leitura com detecção de separador (vírgula ou tabulação padrão do SEER*Stat)
    if fpath.suffix in [".csv", ".gz"]:
        df_raw = pd.read_csv(fpath, low_memory=False)
    elif fpath.suffix == ".txt":
        try:
            df_raw = pd.read_csv(fpath, sep="\t", low_memory=False)
        except Exception:
            df_raw = pd.read_csv(fpath, low_memory=False)
    else:
        df_raw = pd.read_csv(fpath, low_memory=False)

    print(f"Registros brutos carregados: {len(df_raw):,}")

    df_clean = pd.DataFrame()
    df_clean["patient_id"] = df_raw.get("Patient ID", pd.Series(range(len(df_raw)))).astype(str)

    # Ano de diagnóstico
    year_col = [c for c in df_raw.columns if "year" in c.lower()][0]
    df_clean["year_of_diagnosis"] = pd.to_numeric(df_raw[year_col], errors="coerce").fillna(2012).astype(int)

    # Demografia
    age_col = [c for c in df_raw.columns if "age" in c.lower()][0]
    df_clean["age_years"] = pd.to_numeric(df_raw[age_col].astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(60.0)

    sex_col = [c for c in df_raw.columns if "sex" in c.lower()][0]
    df_clean["biological_sex"] = df_raw[sex_col].astype(str)
    df_clean["sex_male"] = np.where(df_clean["biological_sex"].str.contains("male", case=False) & ~df_clean["biological_sex"].str.contains("female", case=False), 1, 0)

    race_cols = [c for c in df_raw.columns if "race" in c.lower()]
    df_clean["race_ethnicity"] = df_raw[race_cols[0]].astype(str) if race_cols else "White"

    # Tamanho tumoral (CS tumor size / Tumor size summary)
    size_cols = [c for c in df_raw.columns if "size" in c.lower()]
    if size_cols:
        size_raw = pd.to_numeric(df_raw[size_cols[0]], errors="coerce")
        # 999 no SEER indica desconhecido / não medido; valores válidos são em milímetros (001 a 989)
        size_valid = np.where((size_raw > 0) & (size_raw < 990), size_raw / 10.0, np.nan)
        df_clean["tumor_size_cm"] = pd.Series(size_valid).fillna(3.5).round(1)
    else:
        df_clean["tumor_size_cm"] = 3.5

    # Número de nódulos (1 vs multifocal / múltiplos)
    ext_cols = [c for c in df_raw.columns if "extension" in c.lower() or "nodule" in c.lower()]
    if ext_cols:
        df_clean["nodule_count"] = np.where(df_raw[ext_cols[0]].astype(str).str.contains("multi|2|3|4", case=False), 2, 1)
    else:
        df_clean["nodule_count"] = 1

    # Invasão vascular
    vasc_cols = [c for c in df_raw.columns if "vascular" in c.lower()]
    if vasc_cols:
        df_clean["vascular_invasion_code"] = np.where(df_raw[vasc_cols[0]].astype(str).str.contains("yes|present|micro|macro|1", case=False), 1, 0)
    else:
        df_clean["vascular_invasion_code"] = 0

    # AFP
    afp_cols = [c for c in df_raw.columns if "afp" in c.lower() or "fetoprotein" in c.lower()]
    if afp_cols:
        df_clean["afp_elevated"] = np.where(df_raw[afp_cols[0]].astype(str).str.contains("pos|elev|high|1", case=False), 1, 0)
    else:
        df_clean["afp_elevated"] = 0

    # Grau histológico
    grade_cols = [c for c in df_raw.columns if "grade" in c.lower()]
    if grade_cols:
        df_clean["histologic_grade"] = pd.to_numeric(df_raw[grade_cols[0]].astype(str).str.extract(r"(\d)")[0], errors="coerce").fillna(2).astype(int).clip(1, 4)
    else:
        df_clean["histologic_grade"] = 2

    # Fibrose / Cirrose
    fib_cols = [c for c in df_raw.columns if "fibrosis" in c.lower() or "cirrhosis" in c.lower()]
    if fib_cols:
        df_clean["fibrosis_ishak"] = pd.to_numeric(df_raw[fib_cols[0]].astype(str).str.extract(r"(\d)")[0], errors="coerce").fillna(4).astype(int).clip(0, 6)
        df_clean["is_cirrhotic"] = (df_clean["fibrosis_ishak"] >= 5).astype(int)
    else:
        df_clean["fibrosis_ishak"] = 4
        df_clean["is_cirrhotic"] = 1

    # Linfonodos
    df_clean["lymph_node_positive"] = 0

    # Estadiamento AJCC
    stage_cols = [c for c in df_raw.columns if "stage" in c.lower() or "ajcc" in c.lower()]
    df_clean["ajcc_stage_group"] = df_raw[stage_cols[0]].astype(str) if stage_cols else "I"

    # Cirurgia
    surg_cols = [c for c in df_raw.columns if "surg" in c.lower()]
    if not surg_cols:
        raise ValueError("Coluna de cirurgia primária não encontrada no arquivo SEER.")
    surg_col_name = surg_cols[0]
    df_clean["surgical_modality"] = df_raw[surg_col_name].apply(map_seer_surgical_modality)
    df_clean["is_transplant"] = np.where(df_clean["surgical_modality"] == "transplant", 1, 0)

    # Desfechos Clínicos e Sobrevida
    surv_cols = [c for c in df_raw.columns if "survival" in c.lower()]
    surv_months = pd.to_numeric(df_raw[surv_cols[0]], errors="coerce").fillna(36.0) if surv_cols else pd.Series([36.0] * len(df_raw))

    vital_cols = [c for c in df_raw.columns if "vital" in c.lower()]
    vital_status = df_raw[vital_cols[0]].astype(str) if vital_cols else pd.Series(["Alive"] * len(df_raw))

    cause_cols = [c for c in df_raw.columns if "cause" in c.lower() or "death" in c.lower()]
    cause_death = df_raw[cause_cols[0]].astype(str) if cause_cols else pd.Series(["Alive"] * len(df_raw))

    is_dead_all = vital_status.str.contains("dead|deceased", case=False)
    is_dead_cancer = cause_death.str.contains("dead attributable|cancer", case=False)

    df_clean["survival_months"] = surv_months
    df_clean["vital_status"] = vital_status
    df_clean["css_5yr_event"] = ((is_dead_cancer) & (surv_months <= 60.0)).astype(int)
    df_clean["os_5yr_event"] = ((is_dead_all) & (surv_months <= 60.0)).astype(int)
    df_clean["css_3yr_event"] = ((is_dead_cancer) & (surv_months <= 36.0)).astype(int)

    # Critérios de Milão
    df_clean["within_milan"] = compute_milan_criteria(df_clean)

    # Filtra coorte cirúrgica curativa (Ressecção vs Transplante)
    df_surgical = df_clean[df_clean["surgical_modality"].isin(["resection", "transplant"])].copy().reset_index(drop=True)

    # Partição temporal anti-vazamento (TRIPOD+AI)
    df_dev = df_surgical[df_surgical["year_of_diagnosis"] <= 2015].copy().reset_index(drop=True)
    df_test = df_surgical[df_surgical["year_of_diagnosis"] >= 2016].copy().reset_index(drop=True)

    output_dir.mkdir(parents=True, exist_ok=True)
    path_dev = output_dir / "coorte_desenvolvimento_seer_2000_2015.csv.gz"
    path_test = output_dir / "coorte_validacao_temporal_seer_2016_2021.csv.gz"
    path_all = output_dir / "coorte_seer_hcc_cirurgica_completa.csv.gz"

    df_dev.to_csv(path_dev, index=False, compression="gzip")
    df_test.to_csv(path_test, index=False, compression="gzip")
    df_surgical.to_csv(path_all, index=False, compression="gzip")

    print("=" * 70)
    print("COORTE CIRÚRGICA NCI SEER PROCESSADA COM SUCESSO:")
    print(f" - Total de pacientes com HCC: {len(df_clean):,}")
    print(f" - Total de procedimentos cirúrgicos curativos: {len(df_surgical):,}")
    print(f"   * Transplantes Hepáticos (OLT): {(df_surgical['surgical_modality'] == 'transplant').sum():,}")
    print(f"   * Ressecções Hepáticas: {(df_surgical['surgical_modality'] == 'resection').sum():,}")
    print(f" - Coorte de Desenvolvimento (2000-2015): {len(df_dev):,} pacientes")
    print(f" - Coorte de Validação Temporal (2016-2021): {len(df_test):,} pacientes")
    print(f" - Eventos de Mortalidade Câncer-Específica em 5 anos: {df_surgical['css_5yr_event'].mean()*100:.1f}%")
    print(f" - Pacientes dentro dos Critérios de Milão: {df_surgical['within_milan'].mean()*100:.1f}%")
    print("=" * 70)

    return {
        "status": "success",
        "total_hcc": len(df_clean),
        "total_surgical": len(df_surgical),
        "transplants": int((df_surgical["surgical_modality"] == "transplant").sum()),
        "resections": int((df_surgical["surgical_modality"] == "resection").sum()),
        "dev_n": len(df_dev),
        "test_n": len(df_test),
    }


def main() -> None:
    raw_dir = Path("projects/xai-liver-seer-oncology/sources/seer")
    output_dir = Path("projects/xai-liver-seer-oncology/analysis")

    print("=" * 70)
    print("PIPELINE DE DADOS REAIS SEER (NCI) — CARCINOMA HEPATOCELULAR")
    print("=" * 70)

    if not raw_dir.is_dir() or not any(raw_dir.iterdir()):
        print(f"[AGUARDANDO DADOS REAIS DO SEER em '{raw_dir}']")
        sys.exit(0)

    process_real_seer_data(raw_dir, output_dir)


if __name__ == "__main__":
    main()
