#!/usr/bin/env python3
"""
Monta a estrutura canônica de pastas da publicação para submissão e upload no Google Drive.
Projeto: `xai-liver-seer-oncology`
Target Journal: Annals of Surgery (LWW)
"""

import shutil
from pathlib import Path

base_proj = Path("projects/xai-liver-seer-oncology")
pkg_dir = base_proj / "publicacoes" / "annals_of_surgery" / "v01"

# Limpar se existir para garantir integridade
if pkg_dir.exists():
    shutil.rmtree(pkg_dir)

pkg_dir.mkdir(parents=True, exist_ok=True)

# 01 Manuscritos
man_dir = pkg_dir / "01_manuscritos_completos"
man_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(base_proj / "drafts" / "ingles" / "manuscrito.md", man_dir / "manuscrito_ingles_annals_of_surgery.md")
shutil.copy2(base_proj / "drafts" / "portugues" / "manuscrito.md", man_dir / "manuscrito_portugues.md")

# 02 Figuras 300 dpi
fig_dir = pkg_dir / "02_figuras_alta_resolucao_300dpi"
fig_dir.mkdir(parents=True, exist_ok=True)
for fig in (base_proj / "analysis" / "figuras").glob("*.png"):
    shutil.copy2(fig, fig_dir / fig.name)

# 03 Tabelas e Resultados
tab_dir = pkg_dir / "03_tabelas_e_resultados"
tab_dir.mkdir(parents=True, exist_ok=True)
for f in [
    base_proj / "analysis" / "results" / "tabela_01_baseline_characteristics_seer.csv",
    base_proj / "analysis" / "results" / "metrics_summary.json",
    base_proj / "analysis" / "results" / "shap_feature_importance.csv",
    base_proj / "analysis" / "results" / "dca_results.csv",
]:
    if f.exists():
        shutil.copy2(f, tab_dir / f.name)

# 04 Documentos de Submissão
sub_dir = pkg_dir / "04_documentos_de_submissao"
sub_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(base_proj / "deliverables" / "title_page_annals_of_surgery.md", sub_dir / "title_page_annals_of_surgery.md")
shutil.copy2(base_proj / "deliverables" / "cover_letter_annals_of_surgery.md", sub_dir / "cover_letter_annals_of_surgery.md")

# 05 Relatórios de Revisão e Auditoria
rev_dir = pkg_dir / "05_relatorios_de_revisao_e_checklists"
rev_dir.mkdir(parents=True, exist_ok=True)
for r in (base_proj / "reviews").glob("*.md"):
    shutil.copy2(r, rev_dir / r.name)
if (base_proj / "evidence" / "relatorio_torneio_de_revistas.md").exists():
    shutil.copy2(base_proj / "evidence" / "relatorio_torneio_de_revistas.md", rev_dir / "relatorio_torneio_de_revistas.md")

# 06 Referências Bibliográficas
ref_dir = pkg_dir / "06_referencias_bibliograficas"
ref_dir.mkdir(parents=True, exist_ok=True)
shutil.copy2(base_proj / "drafts" / "references.bib", ref_dir / "references.bib")

# 07 Códigos e Scripts
code_dir = pkg_dir / "07_codigos_e_scripts_reprodutiveis"
code_dir.mkdir(parents=True, exist_ok=True)
for c in [
    base_proj / "analysis" / "01_pipeline_dados_seer.py",
    base_proj / "analysis" / "02_treinamento_xai_conformal.py",
    base_proj / "analysis" / "03_gerar_figuras_publicacao.py",
    base_proj / "analysis" / "04_gerar_tabela_01_baseline.py",
]:
    if c.exists():
        shutil.copy2(c, code_dir / c.name)

print(f"Pacote editorial para Annals of Surgery montado com sucesso em: {pkg_dir}")
