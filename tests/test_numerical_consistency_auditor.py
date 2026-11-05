from pathlib import Path
import json
import pytest

from article_machine.cli import main
from article_machine.projects import init_project
from article_machine.services.numerical_consistency_auditor import (
    extract_numerical_facts_from_text,
    audit_numerical_consistency,
)


def test_extract_numerical_facts():
    sample_text = """
    A total of n = 280 patients were enrolled.
    Mortality occurred in 28 (10.0%) participants in the intervention arm.
    The primary outcome showed HR = 0.65 [0.48, 0.88], with p = 0.004.
    Diagnostic accuracy was excellent (AUC = 0.89 [0.84, 0.94], P < 0.001).
    This conclusively proves our hypothesis.
    """
    facts = extract_numerical_facts_from_text(sample_text)

    assert 280 in facts["sample_sizes"]
    assert any(p["count"] == 28 and p["reported_pct"] == 10.0 for p in facts["percentages"])
    assert any(e["metric"] == "HR" and e["estimate"] == 0.65 and e["ci_lower"] == 0.48 and e["ci_upper"] == 0.88 for e in facts["effect_sizes"])
    assert any(e["metric"] == "AUC" and e["estimate"] == 0.89 for e in facts["effect_sizes"])
    assert any(p["value"] == 0.004 for p in facts["p_values"])
    assert "proves" in [o.lower() for o in facts["overclaims"]]


def test_audit_detects_ci_bounding_defect(tmp_path: Path):
    project_dir = init_project(tmp_path, "Projeto Audit Falha CI", "systematic-review")
    draft_dir = project_dir / "drafts"
    draft_dir.mkdir(parents=True, exist_ok=True)

    # Defect: Estimate 2.10 is outside [1.10, 1.80]
    bad_draft = draft_dir / "manuscript.md"
    bad_draft.write_text("The intervention showed RR = 2.10 [1.10, 1.80] and p = 0.02.", encoding="utf-8")

    report = audit_numerical_consistency(project_dir)
    assert report["status"] == "block"
    assert any(i["category"] == "ci_bounding_defect" for i in report["issues"])

    # Test CLI strict mode failure
    code = main(["audit", "numbers", str(project_dir), "--strict"])
    assert code == 1


def test_audit_detects_em_dash_in_english(tmp_path: Path):
    project_dir = init_project(tmp_path, "Projeto Audit EmDash", "clinical-ml")
    pub_en = project_dir / "publicacoes" / "revista_teste" / "07_manuscrito" / "ingles"
    pub_en.mkdir(parents=True, exist_ok=True)

    en_draft = pub_en / "manuscript_en.md"
    # Contains em-dash
    en_draft.write_text("Biomarker concentration \u2014 measured at baseline \u2014 was associated with mortality (HR = 1.50 [1.20, 1.80], p = 0.01).", encoding="utf-8")

    report = audit_numerical_consistency(project_dir)
    assert report["status"] in {"warning", "pass"}
    assert any(i["category"] == "em_dash_style_violation" for i in report["issues"])


def test_audit_passes_clean_project(tmp_path: Path):
    project_dir = init_project(tmp_path, "Projeto Audit Limpo", "bench-study")
    draft_dir = project_dir / "drafts"
    draft_dir.mkdir(parents=True, exist_ok=True)

    clean_draft = draft_dir / "manuscript.md"
    clean_draft.write_text("In a cohort of n = 150 animals, survival improved with HR = 0.60 [0.40, 0.90] (p = 0.012).", encoding="utf-8")

    report = audit_numerical_consistency(project_dir)
    assert report["status"] == "pass"
    assert len(report["issues"]) == 0

    code = main(["audit", "numbers", str(project_dir), "--strict"])
    assert code == 0
