"""Tests for Methodology Engine, Extraction Validator, Results Ledger, Corpus Pipeline, and Clinical Datasets."""

from __future__ import annotations

from pathlib import Path

from registration_fixtures import reviewed_registration_fixture

from article_machine.projects import init_project
from article_machine.serialization import load_structured_file, save_structured_file
from article_machine.services.clinical_datasets import (
    ingest_and_verify_dataset,
    list_clinical_datasets,
    prepare_dataset_stage,
)
from article_machine.services.corpus_pipeline import (
    ingest_drop_folders_and_deduplicate,
    prepare_search_workspace,
)
from article_machine.services.extraction_validator import validate_extraction_records
from article_machine.services.methodology_engine import (
    audit_equator_compliance,
    compile_registration_packet,
    validate_protocol_methodology,
)
from article_machine.services.results_ledger import (
    audit_numerical_consistency,
    evaluate_clinical_prediction_metrics,
)
from article_machine.zero_trust import audit_retrieval


def test_protocol_validation_and_bilingual_registration_packet(tmp_path: Path) -> None:
    project = init_project(tmp_path, "SR Protocol Test", "systematic-review")
    # Initially incomplete
    initial = validate_protocol_methodology(project)
    assert initial["status"] == "blocked"
    assert "pico.population" in initial["missing_fields"]

    # Populate full PRISMA-P / PROSPERO protocol specification
    protocol = load_structured_file(project / "protocol.yaml")
    protocol.update(
        {
            "research_question": "Does hyperbaric oxygen therapy reduce intestinal ischemia-reperfusion injury?",
            "human_health_outcomes": True,
            "pico": {
                "population": "Patients or experimental models with acute mesenteric ischemia",
                "intervention": "Hyperbaric oxygen therapy (HBOT)",
                "comparator": "Normobaric oxygen or sham control",
                "outcomes": ["Mucosal histopathology score", "30-day mortality", "Serum lactate"],
            },
            "eligibility": {
                "inclusion": ["Randomized or controlled comparative studies"],
                "exclusion": ["Narrative reviews, case reports without control group"],
            },
            "information_sources": ["pubmed", "embase", "scopus", "cochrane_central"],
            "risk_of_bias_tool": "RoB 2 / SYRCLE",
            "synthesis_plan": {
                "effect_measure": "Log Odds Ratio and Standardized Mean Difference (Hedges g)",
                "model": "Random-effects REML with Hartung-Knapp-Sidik-Jonkman (HKSJ)",
                "heterogeneity": "I2, tau2 with confidence intervals, and prediction intervals",
            },
            "certainty_assessment": "GRADE Summary of Findings per outcome",
        }
    )
    save_structured_file(project / "protocol.yaml", protocol)

    valid = validate_protocol_methodology(project)
    assert valid["status"] == "pass"

    packet = compile_registration_packet(project)
    assert packet["status"] == "pass"
    assert packet["recommended_registry"] == "PROSPERO"
    assert (project / packet["json_packet_path"]).is_file()
    assert (project / packet["paired_deliverables"]["portugues"]).is_file()
    assert (project / packet["paired_deliverables"]["ingles"]).is_file()

    eq = audit_equator_compliance(project)
    assert eq["status"] == "pass"
    assert eq["checklists"]["PRISMA 2020"]["status"] == "protocol-ready"


def test_extraction_validator_catches_denominator_se_and_nma_disconnect() -> None:
    # 1. Denominator error (events > total) and un-converted SE
    bad_rows = [
        {"study_id": "Smith2024", "events": 25, "total": 20, "sd": 1.2, "dispersion_type": "SE"},
    ]
    rep = validate_extraction_records(bad_rows, mode="pairwise")
    assert rep["status"] == "blocked"
    assert any("impossible denominator mismatch" in i for i in rep["issues"])
    assert any("Standard Error (SE)" in i for i in rep["issues"])

    # 2. Disconnected NMA network & orphan single-arm study
    disconnected_nma = [
        {"study_id": "S1", "treatment": "DrugA", "events": 5, "total": 50},
        {"study_id": "S1", "treatment": "Placebo", "events": 10, "total": 50},
        {"study_id": "S2", "treatment": "DrugB", "events": 4, "total": 40},
        {"study_id": "S2", "treatment": "DrugC", "events": 8, "total": 40},
        {"study_id": "S3_orphan", "treatment": "DrugA", "events": 2, "total": 20},
    ]
    nma_rep = validate_extraction_records(disconnected_nma, mode="nma")
    assert nma_rep["status"] == "blocked"
    assert any("disconnected" in i.lower() for i in nma_rep["issues"])
    assert any("fewer than 2 distinct treatment arms" in i for i in nma_rep["issues"])

    # 3. Connected valid NMA
    connected_nma = [
        {"study_id": "S1", "treatment": "DrugA", "events": 5, "total": 50},
        {"study_id": "S1", "treatment": "Placebo", "events": 10, "total": 50},
        {"study_id": "S2", "treatment": "DrugB", "events": 4, "total": 40},
        {"study_id": "S2", "treatment": "Placebo", "events": 9, "total": 40},
    ]
    ok_nma = validate_extraction_records(connected_nma, mode="nma")
    assert ok_nma["status"] == "pass"
    assert ok_nma["network_summary"]["connected"] is True

    # 4. Diagnostic 2x2 table validation
    diag_ok = [
        {"study_id": "D1", "tp": 45, "fp": 5, "fn": 5, "tn": 45, "total": 100, "sensitivity": 0.9, "specificity": 0.9},
    ]
    assert validate_extraction_records(diag_ok, mode="diagnostic")["status"] == "pass"


def test_clinical_ml_metrics_and_cross_language_numerical_ledger(tmp_path: Path) -> None:
    # 1. Patient-level leakage must block
    leaked = evaluate_clinical_prediction_metrics(
        [0, 1, 0, 1],
        [0.1, 0.9, 0.2, 0.8],
        patient_ids_train=["P1", "P2"],
        patient_ids_test=["P2", "P3"],
    )
    assert leaked["status"] == "blocked"
    assert any("PATIENT LEAKAGE" in i for i in leaked["issues"])

    # 2. Valid evaluation
    valid_ml = evaluate_clinical_prediction_metrics(
        [0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
        [0.05, 0.12, 0.20, 0.82, 0.91, 0.76, 0.15, 0.88, 0.25, 0.79],
        patient_ids_train=["P1", "P2", "P3"],
        patient_ids_test=[f"test-{i}" for i in range(10)],
    )
    assert valid_ml["status"] == "pass"
    assert valid_ml["discrimination"]["auroc"] > 0.95
    assert len(valid_ml["decision_curve_analysis"]["thresholds_with_higher_net_benefit"]) > 0
    assert valid_ml["decision_curve_analysis"]["clinical_benefit_established"] is False

    # 3. Cross-language numerical ledger check (dot vs comma equivalence)
    project = init_project(tmp_path, "Ledger Check", "prediction-model")
    save_structured_file(
        project / "analysis" / "results_ledger.json",
        {"metrics": {"auroc": "0.892", "brier": "0.114", "n_cohort": "1450"}},
    )
    (project / "drafts" / "portugues").mkdir(parents=True, exist_ok=True)
    (project / "drafts" / "ingles").mkdir(parents=True, exist_ok=True)
    (project / "drafts" / "portugues" / "manuscrito.md").write_text(
        "Coorte {{metric:n_cohort}} 1450; AUROC {{metric:auroc}} 0,892; Brier {{metric:brier}} 0,114.\n",
        encoding="utf-8",
    )
    (project / "drafts" / "ingles" / "manuscrito.md").write_text(
        "Cohort {{metric:n_cohort}} 1450; AUROC {{metric:auroc}} 0.892; Brier {{metric:brier}} 0.114.\n",
        encoding="utf-8",
    )
    num_audit = audit_numerical_consistency(project)
    assert num_audit["status"] == "pass"


def test_multi_database_search_embase_ris_pubmed_nbib_and_prisma_deduplication(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Multi-DB PRISMA Review", "systematic-review")
    reviewed_registration_fixture(project)

    save_structured_file(
        project / "context" / "query_plan.yaml",
        {
            "contract": "QueryPlan",
            "topic": "Procalcitonin and D-dimer in acute transmural intestinal necrosis",
            "providers": ["pubmed", "embase", "scopus", "cochrane_central", "lilacs_bvs"],
            "boolean": "AND",
            "concepts": [
                {"id": "condition", "field": "title_abstract", "terms": ["intestinal ischemia", "mesenteric ischemia"]},
                {"id": "biomarker", "field": "title_abstract", "terms": ["procalcitonin", "d-dimer"]},
            ],
            "date_range": {"from": "2015-01-01", "to": "2026-11-01"},
            "limits": {"max_records": 500},
            "rationale": "Multi-database PRISMA-S search across 5 databases.",
        },
    )

    prep = prepare_search_workspace(project)
    assert prep["status"] == "pass"
    queries_by_prov = {q["provider"]: q["query"] for q in prep["compiled_queries"]}
    assert "TITLE-ABS-KEY(" in queries_by_prov["scopus"]
    assert ":ti,ab,kw" in queries_by_prov["embase"]
    assert ":ti,ab,kw" in queries_by_prov["cochrane_central"]
    assert "tw:(" in queries_by_prov["lilacs_bvs"]

    # Drop an Embase .ris export with 2 records
    embase_ris = (
        "TY  - JOUR\n"
        "TI  - Procalcitonin predicts transmural bowel necrosis in acute mesenteric ischemia\n"
        "AU  - Silva, Joao\n"
        "PY  - 2024\n"
        "JO  - World Journal of Emergency Surgery\n"
        "DO  - 10.1186/s13017-024-00500-1\n"
        "AN  - 2024998877\n"
        "AB  - Full abstract from Embase with detailed subgroup data.\n"
        "KW  - Emtree_Mesenteric_Ischemia\n"
        "ER  - \n\n"
        "TY  - CONF\n"
        "TI  - D-dimer kinetics in strangulated intestinal obstruction\n"
        "AU  - Costa, Maria\n"
        "PY  - 2023\n"
        "JO  - Intensive Care Medicine Supplement\n"
        "AN  - 639112233\n"
        "ER  - \n"
    )
    (project / "sources" / "manual_imports" / "embase" / "embase_export.ris").write_text(embase_ris, encoding="utf-8")

    # Drop a PubMed .nbib export with 1 duplicate (same DOI) and 1 unique record
    pubmed_nbib = (
        "PMID- 38991122\n"
        "TI  - Procalcitonin predicts transmural bowel necrosis in acute mesenteric ischemia.\n"
        "FAU - Silva, Joao\n"
        "DP  - 2024 May\n"
        "JT  - World journal of emergency surgery\n"
        "LID - 10.1186/s13017-024-00500-1 [doi]\n"
        "MH  - MeSH_Procalcitonin\n\n"
        "PMID- 37112233\n"
        "TI  - Lactate versus D-dimer in early acute mesenteric ischemia.\n"
        "FAU - Pereira, Lucas\n"
        "DP  - 2022 Jan\n"
        "JT  - Annals of Surgery\n"
        "LID - 10.1097/SLA.0000000000005000 [doi]\n\n"
    )
    (project / "sources" / "manual_imports" / "pubmed" / "pubmed_export.nbib").write_text(pubmed_nbib, encoding="utf-8")

    # Drop a Scopus .csv export with a title+year+author duplicate of Costa 2023 (missing DOI)
    scopus_csv = (
        "Title,Authors,Year,Source title,DOI,EID,Abstract\n"
        '"D-dimer kinetics in strangulated intestinal obstruction","Costa, Maria; '
        'Santos, P.",2023,"Intensive Care Medicine","",2-s2.0-851000999,"Abstract '
        'from Scopus."\n'
    )
    (project / "sources" / "manual_imports" / "scopus" / "scopus_export.csv").write_text(scopus_csv, encoding="utf-8")

    # Drop empty files for cochrane_central and lilacs_bvs so all 5 manifests are written
    (project / "sources" / "manual_imports" / "cochrane_central" / "central.ris").write_text("", encoding="utf-8")
    (project / "sources" / "manual_imports" / "lilacs_bvs" / "lilacs.ris").write_text("", encoding="utf-8")

    dedup = ingest_drop_folders_and_deduplicate(project)
    assert dedup["status"] == "pass"
    assert dedup["total_identified"] == 5
    assert dedup["total_duplicates_removed"] == 2
    assert dedup["duplicates_removed_by_stage"]["doi_exact"] == 1
    assert dedup["duplicates_removed_by_stage"]["title_year_author"] == 1
    assert dedup["unique_records_for_screening"] == 3

    # Verify zero-loss metadata enrichment on merged record
    queue_lines = (project / dedup["screening_queue_path"]).read_text(encoding="utf-8").splitlines()
    assert len(queue_lines) == 3
    first_merged = load_structured_file(project / "evidence" / "prisma" / "prisma_flow_counts.json")
    assert first_merged["identification"]["total_records_identified"] == 5

    # Verify retrieval audit passes on generated manifests
    ret_audit = audit_retrieval(project)
    assert ret_audit["status"] == "pass"


def test_clinical_datasets_catalog_staging_and_manifest_verification(tmp_path: Path) -> None:
    open_icu = list_clinical_datasets(domain="icu", access_tier="open-direct")
    assert any(d["id"] == "mimic-iv-demo-open" for d in open_icu)
    assert any(d["id"] == "physionet-sepsis-challenge" for d in open_icu)

    project = init_project(tmp_path, "UGIB Dynamic Risk", "prediction-model")
    reviewed_registration_fixture(project)

    stage = prepare_dataset_stage(project, dataset_ids=["mimic-iv", "mimic-iv-demo-open", "vitaldb"])
    assert stage["status"] == "pass"
    assert stage["selected_count"] == 3
    assert (project / stage["guides"]["portugues"]).is_file()
    assert (project / stage["guides"]["ingles"]).is_file()

    # Drop a synthetic sample CSV into mimic-iv-demo-open folder and verify manifest
    demo_csv = project / "sources" / "datasets" / "mimic-iv-demo-open" / "admissions_sample.csv"
    demo_csv.write_text("subject_id,hadm_id,outcome\n10001,20001,0\n10002,20002,1\n", encoding="utf-8")

    ver = ingest_and_verify_dataset(project, "mimic-iv-demo-open")
    assert ver["status"] == "pass"
    assert ver["file_count"] == 1
    assert ver["files"][0]["row_count"] == 2
    assert ver["files"][0]["columns"] == ["subject_id", "hadm_id", "outcome"]
