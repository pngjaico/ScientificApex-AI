#!/usr/bin/env python3
"""
Execução Computacional do Torneio de Revistas (Journal Selection Tournament).
Projeto: `xai-liver-seer-oncology`
Tema: XAI e Predição Conformal de Incerteza (MAPIE) para Ressecção vs Transplante Hepático no HCC (NCI SEER N=10.165).
"""

from pathlib import Path
import pandas as pd

# 8 Candidatas Pré-Selecionadas com PubMed/MEDLINE Obrigatório e APC ZERO
journals = [
    {
        "nome": "Annals of Surgery",
        "editora": "Wolters Kluwer (LWW)",
        "issn": "0003-4932",
        "medline": True,
        "modelo_custo_zero": "Híbrido Tradicional (Sem APC para Autores)",
        "jif": 9.2,
        "qualis": "A1",
        "p1_impacto": 9.8,        # Peso 2.5
        "p2_alinhamento": 9.5,    # Peso 2.5 (Revista #1 mundial de cirurgia)
        "p3_velocidade": 7.5,     # Peso 2.0 (Muito concorrida, 3-4 semanas 1º parecer)
        "p4_arquitetura": 9.0,    # Peso 1.5 (Excelente suporte a TRIPOD+AI, DCA e SHAP)
        "p5_seguranca_fin": 10.0,  # Peso 1.5 (Garantia formal de zero APC via assinatura)
    },
    {
        "nome": "American Journal of Transplantation (AJT)",
        "editora": "Elsevier",
        "issn": "1600-6135",
        "medline": True,
        "modelo_custo_zero": "Acordo Transformativo CAPES-Elsevier (APC US$ 0)",
        "jif": 8.9,
        "qualis": "A1",
        "p1_impacto": 9.5,
        "p2_alinhamento": 9.8,    # Revista oficial da AST/ASTS, foco máximo em transplante
        "p3_velocidade": 8.5,     # Mediana de 21 dias para 1º parecer
        "p4_arquitetura": 9.5,    # Suporte total a apêndices metodológicos de ML
        "p5_seguranca_fin": 10.0, # Isenção total e automática via CAPES
    },
    {
        "nome": "Liver Transplantation",
        "editora": "Wolters Kluwer (AASLD)",
        "issn": "1527-6465",
        "medline": True,
        "modelo_custo_zero": "Híbrido Tradicional (Sem APC)",
        "jif": 4.7,
        "qualis": "A1",
        "p1_impacto": 8.2,
        "p2_alinhamento": 10.0,   # Especializada especificamente em transplante de fígado
        "p3_velocidade": 8.0,
        "p4_arquitetura": 8.8,
        "p5_seguranca_fin": 10.0,
    },
    {
        "nome": "HPB (Official Journal of the IHPBA)",
        "editora": "Elsevier",
        "issn": "1365-182X",
        "medline": True,
        "modelo_custo_zero": "Acordo Transformativo CAPES-Elsevier (APC US$ 0)",
        "jif": 3.2,
        "qualis": "A2",
        "p1_impacto": 7.6,
        "p2_alinhamento": 9.5,    # Revista foco em cirurgia hepato-pancreato-biliar
        "p3_velocidade": 8.5,
        "p4_arquitetura": 8.5,
        "p5_seguranca_fin": 10.0,
    },
    {
        "nome": "Surgery",
        "editora": "Elsevier",
        "issn": "0039-6060",
        "medline": True,
        "modelo_custo_zero": "Acordo Transformativo CAPES-Elsevier (APC US$ 0)",
        "jif": 3.8,
        "qualis": "A1",
        "p1_impacto": 8.0,
        "p2_alinhamento": 8.8,
        "p3_velocidade": 8.0,
        "p4_arquitetura": 8.5,
        "p5_seguranca_fin": 10.0,
    },
    {
        "nome": "World Journal of Surgery",
        "editora": "Oxford University Press (ISS/SIC)",
        "issn": "0364-2313",
        "medline": True,
        "modelo_custo_zero": "Acordo Transformativo CAPES-Oxford (APC US$ 0)",
        "jif": 2.6,
        "qualis": "A2",
        "p1_impacto": 7.2,
        "p2_alinhamento": 8.5,
        "p3_velocidade": 8.5,
        "p4_arquitetura": 8.0,
        "p5_seguranca_fin": 10.0,
    },
    {
        "nome": "Journal of Surgical Oncology",
        "editora": "Wiley",
        "issn": "0022-4790",
        "medline": True,
        "modelo_custo_zero": "Acordo Transformativo CAPES-Wiley (APC US$ 0)",
        "jif": 2.5,
        "qualis": "A2",
        "p1_impacto": 7.0,
        "p2_alinhamento": 9.0,    # Foco em oncologia cirúrgica
        "p3_velocidade": 8.0,
        "p4_arquitetura": 8.0,
        "p5_seguranca_fin": 10.0,
    },
    {
        "nome": "Journal of Hepatology",
        "editora": "Elsevier",
        "issn": "0168-8278",
        "medline": True,
        "modelo_custo_zero": "Acordo Transformativo CAPES-Elsevier (APC US$ 0)",
        "jif": 26.8,
        "qualis": "A1",
        "p1_impacto": 10.0,       # IF gigante
        "p2_alinhamento": 8.5,    # Mais clínico/molecular do que cirúrgico
        "p3_velocidade": 6.5,     # Desk reject massivo (>85%)
        "p4_arquitetura": 8.5,
        "p5_seguranca_fin": 10.0,
    },
]

# Pesos Oficiais da Skill:
# Pilar 1: 2.5 | Pilar 2: 2.5 | Pilar 3: 2.0 | Pilar 4: 1.5 | Pilar 5: 1.5 (Soma = 10.0)
for j in journals:
    score = (
        j["p1_impacto"] * 2.5 +
        j["p2_alinhamento"] * 2.5 +
        j["p3_velocidade"] * 2.0 +
        j["p4_arquitetura"] * 1.5 +
        j["p5_seguranca_fin"] * 1.5
    ) / 10.0
    j["score_final"] = round(score, 2)

df_tourney = pd.DataFrame(journals).sort_values(by="score_final", ascending=False).reset_index(drop=True)
df_tourney.index = df_tourney.index + 1
df_tourney.index.name = "Posição"

print("=" * 80)
print("RESULTADO DO TORNEIO MULTICRITÉRIO DE REVISTAS CIENTÍFICAS")
print("=" * 80)
print(df_tourney[["nome", "editora", "jif", "qualis", "score_final", "modelo_custo_zero"]].to_string())

out_dir = Path("projects/xai-liver-seer-oncology/evidence")
out_dir.mkdir(parents=True, exist_ok=True)
df_tourney.to_csv(out_dir / "torneio_revistas_ranqueamento.csv", encoding="utf-8")
