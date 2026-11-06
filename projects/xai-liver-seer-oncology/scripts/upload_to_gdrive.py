#!/usr/bin/env python3
"""
Upload automatizado de todos os artefatos editoriais do Estudo 2 (NCI SEER) para o Google Drive.
Pasta Base do Estudo 2: 1258IZysNxXxxCxUpg3tgd_SO4tRmx3qc
"""

import subprocess
from pathlib import Path

mapping = {
    "1OYnCswIBJdO0BuuNvl9bMVXNzWzXhPfR": [
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/01_manuscritos_completos/manuscrito_portugues.md",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/01_manuscritos_completos/manuscrito_ingles_annals_of_surgery.md",
    ],
    "13hMLnrSkdV68NA5az1q7k-gghocSMsK_": [
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/02_figuras_alta_resolucao_300dpi/figura_01_curvas_roc_seer_vs_milao.png",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/02_figuras_alta_resolucao_300dpi/figura_02_curva_decisao_clinica_dca.png",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/02_figuras_alta_resolucao_300dpi/figura_03_shap_importancia_biologica.png",
    ],
    "1bZH1XcXECXpB9jXO6aneL6FTyrk8cuXM": [
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/03_tabelas_e_resultados/tabela_01_baseline_characteristics_seer.csv",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/03_tabelas_e_resultados/metrics_summary.json",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/03_tabelas_e_resultados/shap_feature_importance.csv",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/03_tabelas_e_resultados/dca_results.csv",
    ],
    "1iOj2f_WF5yCP3z_M6maDVqnLzoZjvhPu": [
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/04_documentos_de_submissao/title_page_annals_of_surgery.md",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/04_documentos_de_submissao/cover_letter_annals_of_surgery.md",
    ],
    "1j9Zb8-XeJmlvmxsFoBVEKQgrWhys-KIC": [
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/05_relatorios_de_revisao_e_checklists/clinical_peer_review_report.md",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/05_relatorios_de_revisao_e_checklists/relatorio_parecer_clinico_peer_review.md",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/05_relatorios_de_revisao_e_checklists/relatorio_revisao_estatistica_independente.md",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/05_relatorios_de_revisao_e_checklists/statistical_review_report.md",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/05_relatorios_de_revisao_e_checklists/relatorio_torneio_de_revistas.md",
    ],
    "1gBrNafBQTrOwHDTEx-gU0mcJwbQ6v6Ky": [
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/06_referencias_bibliograficas/references.bib",
    ],
    "13xExaSdnd71gxz_U6Koz5CmomcwiJ7jk": [
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/07_codigos_e_scripts_reprodutiveis/01_pipeline_dados_seer.py",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/07_codigos_e_scripts_reprodutiveis/02_treinamento_xai_conformal.py",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/07_codigos_e_scripts_reprodutiveis/03_gerar_figuras_publicacao.py",
        "projects/xai-liver-seer-oncology/publicacoes/annals_of_surgery/v01/07_codigos_e_scripts_reprodutiveis/04_gerar_tabela_01_baseline.py",
    ],
}

gdrive_exe = r"C:\Users\Usuario-pc\.gemini\config\plugins\gdrive\skills\gdrive\scripts\gdrive.cmd"

total = 0
for folder_id, files in mapping.items():
    for f in files:
        p = Path(f)
        if p.exists():
            print(f"Uploading {p.name} to {folder_id}...")
            cmd = [gdrive_exe, "mutate", "upload", str(p), "--parent", folder_id]
            res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if res.returncode == 0:
                print(f"  [OK] {p.name}")
                total += 1
            else:
                print(f"  [ERR] {p.name}: {res.stderr}")

print(f"\nUpload concluído com sucesso! Total de arquivos enviados: {total}")
