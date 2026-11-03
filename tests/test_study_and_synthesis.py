"""Tests for Study Companion, Expanded Bilingual Templates, and R-Output-Driven Synthesis."""

from __future__ import annotations

from pathlib import Path

from registration_fixtures import reviewed_registration_fixture
from scientific_fixtures import supported_synthetic_claim

from article_machine.projects import init_project
from article_machine.serialization import load_structured_file, save_structured_file
from article_machine.services.study_and_synthesis import (
    build_project_study_guide,
    harvest_analysis_outputs,
    list_synthesis_templates,
    synthesize_from_r_outputs,
)


def test_list_synthesis_templates_has_all_four_categories() -> None:
    cat = list_synthesis_templates()
    assert cat["status"] == "pass"
    assert len(cat["publication_templates"]) >= 6
    assert len(cat["slide_templates"]) >= 4
    assert len(cat["poster_templates"]) >= 4
    assert len(cat["abstract_templates"]) >= 4


def test_harvest_r_outputs_and_synthesize_bilingual_deliverables(tmp_path: Path) -> None:
    project = init_project(tmp_path, "NMA Mesenteric Biomarkers", "network-meta-analysis")
    protocol = load_structured_file(project / "protocol.yaml")
    protocol["research_question"] = (
        "Which serum biomarker (D-dimer, Procalcitonin, I-FABP, L-lactate) has the highest "
        "accuracy for transmural bowel necrosis?"
    )
    save_structured_file(project / "protocol.yaml", protocol)
    reviewed_registration_fixture(project)
    claim_id = supported_synthetic_claim(project)

    # Simulate R script outputs in analysis/ and figures/
    (project / "analysis" / "01_nma_model.R").write_text("# R script\n", encoding="utf-8")
    (project / "analysis" / "nma_league_summary.csv").write_text(
        "comparison,estimate,ci_lower,ci_upper,p_score\n"
        "Procalcitonin_vs_Lactate,2.45,1.42,4.21,0.88\n"
        "IFABP_vs_Lactate,2.10,1.25,3.52,0.79\n",
        encoding="utf-8",
    )
    save_structured_file(
        project / "analysis" / "r_model_metrics.json",
        {"k_studies": 18, "n_patients": 2410, "tau2": 0.084, "i2_percent": 31.5},
    )
    (project / "figures" / "forest_plot_nma.svg").write_text("<svg></svg>", encoding="utf-8")

    harvest = harvest_analysis_outputs(project)
    assert harvest["status"] == "pass"
    assert harvest["metrics"]["k_studies"] == 18
    assert harvest["metrics"]["n_patients"] == 2410
    assert len(harvest["tables"]) == 1
    assert len(harvest["figures"]) == 1
    assert (project / "analysis" / "results_ledger.json").is_file()
    ledger = load_structured_file(project / "analysis/results_ledger.json")
    ledger["metric_claims"] = {key: claim_id for key in ledger["metrics"]}
    save_structured_file(project / "analysis/results_ledger.json", ledger)

    # Build Study Companion
    study = build_project_study_guide(project)
    assert study["status"] == "pass"
    assert (project / study["study_guides"]["portugues"]).is_file()
    assert (project / study["study_guides"]["ingles"]).is_file()
    assert (project / study["study_guides"]["interactive_html"]).is_file()
    pt_study_txt = (project / study["study_guides"]["portugues"]).read_text(encoding="utf-8")
    assert "Hartung-Knapp" in pt_study_txt
    assert "2410" in pt_study_txt

    # Synthesize complete bilingual manuscripts, abstracts, slides, and posters from R outputs
    synth = synthesize_from_r_outputs(
        project,
        publication_template_id="annals-wjes-bjs-surgical",
        slide_template_id="defesa-qualificacao-doutorado-40min",
        poster_template_id="a0-retrato-classico",
        slug="wses-2026",
    )
    assert synth["status"] == "pass", synth
    assert synth["submission_eligible"] is False
    assert synth["human_review_verified"] is False
    manuscript = (project / synth["manuscripts"]["portugues"]).read_text(encoding="utf-8")
    assert "verificação humana integral" not in manuscript
    assert "RASCUNHO AUTOMÁTICO" in manuscript
    assert (project / synth["manuscripts"]["portugues"]).is_file()
    assert (project / synth["manuscripts"]["ingles"]).is_file()
    assert (project / synth["abstracts"]["portugues"]).is_file()
    assert (project / synth["abstracts"]["ingles"]).is_file()
    assert synth["conference_outputs"]["status"] == "not-generated-dedicated-pipeline-required"
    for language in ("portugues", "ingles"):
        assert (project / synth["conference_outputs"]["routing_guides"][language]).is_file()
    assert not (project / "deliverables/wses-2026").exists()
