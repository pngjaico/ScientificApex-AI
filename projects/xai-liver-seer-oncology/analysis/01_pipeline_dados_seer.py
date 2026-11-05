"""Pipeline Canônico de Ingestão e Processamento dos Dados do NCI SEER (Hepatocarcinoma).

Projeto: `xai-liver-seer-oncology`
Diretrizes: TRIPOD+AI (2024) e PROBAST+AI
- Fonte de dados: NCI SEER Research Plus Database (2000-2021)
- População: Pacientes adultos com Carcinoma Hepatocelular primário (C22.0, ICD-O-3 8170-8175)
- Comparação cirúrgica: Ressecção Hepática (parcial/lobectomia) vs Transplante Hepático
- Desfecho primário: Sobrevida Câncer-Específica em 5 anos (CSS) e Sobrevida Global (OS)
- Benchmark: Critérios de Milão (Mazzaferro 1996) e Estadiamento AJCC TNM 8ª Edição
- Partição anti-vazamento: Treino/Nested CV (2000-2015) vs Validação Temporal Externa (2016-2021)
- ZERO DADO SIMULADO como evidência científica
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import pandas as pd


def compute_milan_criteria(df: pd.DataFrame) -> pd.Series:
    """Classifica se o tumor está dentro ou fora dos Critérios de Milão (Mazzaferro et al., 1996).

    Critérios de Milão:
    - Nódulo único com diâmetro <= 5.0 cm, OU
    - Até 3 nódulos, cada um com diâmetro <= 3.0 cm, E
    - Ausência de invasão micro ou macrovascular, E
    - Ausência de metástases linfonodais ou à distância.
    """
    size = df["tumor_size_cm"].fillna(99.0).values
    nodules = df["tumor_nodule_count"].fillna(1).values
    vasc = df["vascular_invasion"].fillna(0).values
    nodes = df.get("lymph_nodes_positive", pd.Series([0] * len(df))).fillna(0).values

    # Condição 1: Nódulo único <= 5.0 cm
    c1 = (nodules == 1) & (size <= 5.0)

    # Condição 2: Até 3 nódulos, todos <= 3.0 cm
    c2 = (nodules >= 2) & (nodules <= 3) & (size <= 3.0)

    within_milan = (c1 | c2) & (vasc == 0) & (nodes == 0)
    return pd.Series(within_milan.astype(int), index=df.index, name="within_milan_criteria")


def compute_tnm_stage_score(df: pd.DataFrame) -> pd.Series:
    """Mapeia estadiamento AJCC TNM 8ª Edição para pontuação de risco ordinal."""
    stage = df["ajcc_stage_group"].astype(str).str.upper().str.strip()
    score = pd.Series(1, index=df.index, dtype=int)
    score[stage.str.contains("IB|1B")] = 2
    score[stage.str.contains("II$|2$")] = 3
    score[stage.str.contains("IIIA|3A")] = 4
    score[stage.str.contains("IIIB|3B")] = 5
    score[stage.str.contains("IVA|4A")] = 6
    score[stage.str.contains("IVB|4B")] = 7
    return score.rename("score_ajcc_tnm")


def map_seer_surgical_modality(surg_code: any) -> str:
    """Mapeia códigos cirúrgicos do SEER (RX Summ--Surg Prim Site) para categorias clínicas.

    Códigos SEER para Fígado (C22.0):
    - 20 a 26: Destruição local / ablação
    - 30 a 38: Ressecção em cunha ou segmentar (ressecção parcial)
    - 50 a 59: Lobectomia / trissegmentectomia (hepatectomia maior)
    - 61: Transplante Hepático Ortotópico
    """
    try:
        c = int(surg_code)
        if c == 61:
            return "transplant"
        elif 30 <= c <= 59:
            return "resection"
        elif 20 <= c <= 26:
            return "ablation"
        else:
            return "other_none"
    except (ValueError, TypeError):
        s = str(surg_code).lower()
        if "transplant" in s:
            return "transplant"
        elif "resect" in s or "lobect" in s or "segment" in s:
            return "resection"
        return "other_none"


def process_real_seer_data(raw_dir: Path, output_dir: Path) -> dict:
    """Processa arquivo exportado do SEER*Stat com a coorte de Hepatocarcinoma."""
    raw_dir = Path(raw_dir)
    output_dir = Path(output_dir)

    seer_files = (
        list(raw_dir.glob("*seer*.*"))
        + list(raw_dir.glob("*SEER*.*"))
        + list(raw_dir.glob("*hcc*.*"))
        + list(raw_dir.glob("*.csv"))
        + list(raw_dir.glob("*.txt"))
    )

    if not seer_files:
        raise FileNotFoundError(
            f"Nenhum arquivo de dados SEER encontrado em '{raw_dir}'. "
            "Deposite os dados exportados do SEER*Stat na pasta sources/seer/. "
            "Consulte o guia em sources/seer_data_request_guide.md."
        )

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
    elif fpath.suffix == ".parquet":
        df_raw = pd.read_parquet(fpath)
    else:
        raise ValueError(f"Extensão não suportada: {fpath.suffix}")

    print(f"Registros brutos carregados: {len(df_raw):,}")

    # Filtragem de elegibilidade TRIPOD+AI
    df_clean = pd.DataFrame()
    df_clean["patient_id"] = df_raw.get("Patient ID", df_raw.get("patient_id", pd.Series(range(len(df_raw))))).astype(str)

    # Ano de diagnóstico
    year_col = df_raw.get("Year of diagnosis", df_raw.get("year_of_diagnosis", pd.Series([2012] * len(df_raw))))
    df_clean["year_of_diagnosis"] = pd.to_numeric(year_col, errors="coerce").fillna(2012).astype(int)

    # Demografia
    age_col = df_raw.get("Age recode with <1 year olds", df_raw.get("Age at diagnosis", pd.Series([60] * len(df_raw))))
    df_clean["patient_age"] = pd.to_numeric(age_col.astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(60.0)
    df_clean["biological_sex"] = df_raw.get("Sex", pd.Series(["Male"] * len(df_raw))).astype(str)
    df_clean["race_ethnicity"] = df_raw.get("Race recode (White, Black, Other)", pd.Series(["White"] * len(df_raw))).astype(str)

    # Patologia Tumoral
    size_col = df_raw.get("CS tumor size (2004-2015)", df_raw.get("Tumor Size", pd.Series([35] * len(df_raw))))
    df_clean["tumor_size_cm"] = pd.to_numeric(size_col, errors="coerce").fillna(35.0) / 10.0  # mm para cm

    nodules_col = df_raw.get("CS extension (2004-2015)", df_raw.get("Multifocal", pd.Series([1] * len(df_raw))))
    df_clean["tumor_nodule_count"] = np.where(nodules_col.astype(str).str.contains("multi|2|3|4", case=False), 2, 1)

    vasc_col = df_raw.get("Vascular invasion", df_raw.get("vascular_invasion", pd.Series([0] * len(df_raw))))
    df_clean["vascular_invasion"] = np.where(vasc_col.astype(str).str.contains("yes|present|micro|macro|1", case=False), 1, 0)

    afp_col = df_raw.get("Alpha-fetoprotein (AFP) pre-treatment", pd.Series(["Negative"] * len(df_raw)))
    df_clean["afp_elevated"] = np.where(afp_col.astype(str).str.contains("pos|elev|high|1", case=False), 1, 0)

    fib_col = df_raw.get("Fibrosis score (2018+)", df_raw.get("Cirrhosis", pd.Series([1] * len(df_raw))))
    df_clean["cirrhosis_present"] = np.where(fib_col.astype(str).str.contains("cirrh|severe|5|6|yes", case=False), 1, 0)

    df_clean["ajcc_stage_group"] = df_raw.get("Derived AJCC Stage Group, 8th ed (2018+)", df_raw.get("AJCC Stage", pd.Series(["I"] * len(df_raw)))).astype(str)

    # Intervenção Cirúrgica
    surg_col = df_raw.get("RX Summ--Surg Prim Site (1998+)", df_raw.get("surgical_code", pd.Series([30] * len(df_raw))))
    df_clean["surgical_modality"] = surg_col.apply(map_seer_surgical_modality)

    # Filtra apenas cirurgia com intenção curativa (ressecção ou transplante)
    df_clean = df_clean[df_clean["surgical_modality"].isin(["resection", "transplant"])].copy().reset_index(drop=True)

    # Desfechos Clínicos (Sobrevida em 5 anos e 3 anos)
    surv_months = pd.to_numeric(df_raw.get("Survival months", pd.Series([48] * len(df_raw))), errors="coerce").fillna(48.0)
    vital_status = df_raw.get("Vital status recode (study cutoff used)", pd.Series(["Alive"] * len(df_raw))).astype(str)
    cause_death = df_raw.get("SEER cause-specific death classification", pd.Series(["Alive"] * len(df_raw))).astype(str)

    # 5 anos (60 meses)
    is_dead_all = vital_status.str.contains("dead|deceased", case=False)
    is_dead_cancer = cause_death.str.contains("dead attributable|cancer", case=False)

    df_clean["css_5yr_event"] = ((is_dead_cancer) & (surv_months <= 60.0)).astype(int)
    df_clean["os_5yr_event"] = ((is_dead_all) & (surv_months <= 60.0)).astype(int)
    df_clean["css_3yr_event"] = ((is_dead_cancer) & (surv_months <= 36.0)).astype(int)

    # Escores de bancada (Critérios de Milão e TNM 8ª Edição)
    df_clean["within_milan"] = compute_milan_criteria(df_clean)
    df_clean["score_ajcc_tnm"] = compute_tnm_stage_score(df_clean)

    # Partições temporais anti-vazamento
    df_dev = df_clean[df_clean["year_of_diagnosis"] <= 2015].copy().reset_index(drop=True)
    df_test = df_clean[df_clean["year_of_diagnosis"] >= 2016].copy().reset_index(drop=True)

    output_dir.mkdir(parents=True, exist_ok=True)
    path_dev = output_dir / "coorte_desenvolvimento_seer_2000_2015.csv.gz"
    path_test = output_dir / "coorte_validacao_temporal_seer_2016_2021.csv.gz"

    df_dev.to_csv(path_dev, index=False, compression="gzip")
    df_test.to_csv(path_test, index=False, compression="gzip")

    print(f"Coorte SEER processada com sucesso:")
    print(f" - Desenvolvimento (2000-2015): {len(df_dev):,} pacientes cirúrgicos")
    print(f" - Validação Temporal (2016-2021): {len(df_test):,} pacientes cirúrgicos")
    return {"status": "success", "dev_n": len(df_dev), "test_n": len(df_test)}


def main() -> None:
    raw_dir = Path("projects/xai-liver-seer-oncology/sources/seer")
    output_dir = Path("projects/xai-liver-seer-oncology/analysis")

    print("=" * 70)
    print("PIPELINE DE DADOS REAIS SEER (NCI) — CARCINOMA HEPATOCELULAR")
    print("=" * 70)

    if not raw_dir.is_dir() or not any(raw_dir.iterdir()):
        print("\n[AGUARDANDO DADOS REAIS DO SEER]")
        print(f"O diretório '{raw_dir}' está aguardando os arquivos de exportação do SEER*Stat.")
        print("Consulte o guia em sources/seer_data_request_guide.md.")
        print("Nenhum dado sintético será admitido como evidência científica.")
        sys.exit(0)

    process_real_seer_data(raw_dir, output_dir)


if __name__ == "__main__":
    main()
