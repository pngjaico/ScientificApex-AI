"""Adversarial scientific entrypoint and artifact-integrity regression tests."""

import io
import json
import zipfile
from pathlib import Path
from unittest.mock import patch

import pytest
from registration_fixtures import reviewed_registration_fixture

from article_machine.projects import init_project
from article_machine.services.clinical_datasets import fetch_open_dataset, ingest_and_verify_dataset
from article_machine.services.document_extraction import extract_document, extract_documents, extract_project_documents
from article_machine.services.results_ledger import audit_numerical_consistency
from article_machine.services.study_and_synthesis import (
    build_project_study_guide,
    harvest_analysis_outputs,
    synthesize_from_r_outputs,
)


@pytest.mark.parametrize(
    "operation",
    ["download", "ingest-false-flag", "extract", "batch", "project-extract", "harvest", "study", "synthesis"],
)
def test_unregistered_science_is_blocked_before_side_effects(tmp_path, operation):
    project = init_project(tmp_path, "Unregistered study", "prediction-model")
    source = project / "sources/fixture.docx"
    source.write_bytes(b"UNREAD SYNTHETIC FILE")
    output = project / "sources/extracted"
    with patch("article_machine.services.clinical_datasets._http_get_bytes") as network:
        calls = {
            "download": lambda: fetch_open_dataset(project, "uci-thoracic-surgery-postop"),
            "ingest-false-flag": lambda: ingest_and_verify_dataset(project, "vitaldb", enforce_registration_gate=False),
            "extract": lambda: extract_document(source, output),
            "batch": lambda: extract_documents(source.parent, output),
            "project-extract": lambda: extract_project_documents(project),
            "harvest": lambda: harvest_analysis_outputs(project),
            "study": lambda: build_project_study_guide(project),
            "synthesis": lambda: synthesize_from_r_outputs(project),
        }
        report = calls[operation]()
        assert report["status"] == "blocked"
        network.assert_not_called()
    assert source.read_bytes() == b"UNREAD SYNTHETIC FILE"
    assert not output.exists()
    assert not (project / "analysis/results_ledger.json").exists()
    assert not (project / "drafts/portugues").exists()


def test_registration_alone_does_not_unlock_unsupported_manuscript(tmp_path):
    project = init_project(tmp_path, "No evidence", "systematic-review")
    reviewed_registration_fixture(project)
    report = synthesize_from_r_outputs(project)
    assert report["status"] == "blocked"
    assert "Evidence Lock" in report["issues"][0]
    assert not (project / "drafts/portugues").exists()


def _ledger_project(tmp_path):
    project = init_project(tmp_path, "Numeric bindings", "machine-governance")
    (project / "analysis/results_ledger.json").write_text(json.dumps({"metrics": {"auc": 0.81, "n": 20}}))
    for lang in ("portugues", "ingles"):
        folder = project / "drafts" / lang
        folder.mkdir()
        (folder / "manuscrito.md").write_text("{{metric:auc}} 0.81; {{metric:n}} 20.", encoding="utf-8")
    return project


def test_explicit_numeric_bindings_accept_decimal_translation(tmp_path):
    project = _ledger_project(tmp_path)
    path = project / "drafts/portugues/manuscrito.md"
    path.write_text("{{metric:auc}} 0,81; {{metric:n}} 20.", encoding="utf-8")
    report = audit_numerical_consistency(project)
    assert report["status"] == "pass"
    assert report["gate_eligible"] is False
    assert report["human_semantic_review_required"] is True


@pytest.mark.parametrize(
    "text",
    [
        "0.81 and 20 without bindings",
        "{{metric:auc}} 0.8101; {{metric:n}} 20.",
        "{{metric:auc}} -0.81; {{metric:n}} 20.",
        "{{metric:auc}} 20; {{metric:n}} 0.81.",
        "{{metric:auc}} 0.81; {{metric:auc}} 0.72; {{metric:n}} 20.",
        "{{metric:auc}} 0.81; {{metric:n}} 200.",
    ],
)
def test_substrings_swapped_values_and_inconsistent_repetitions_cannot_pass(tmp_path, text):
    project = _ledger_project(tmp_path)
    (project / "drafts/ingles/manuscrito.md").write_text(text, encoding="utf-8")
    assert audit_numerical_consistency(project)["status"] == "blocked"


def test_numerical_ledger_rejects_missing_pair_invalid_numbers_and_traversal(tmp_path):
    project = _ledger_project(tmp_path)
    assert audit_numerical_consistency(project, "../outside.json")["status"] == "blocked"
    (project / "analysis/results_ledger.json").write_text('{"metrics":{"auc":NaN}}')
    assert audit_numerical_consistency(project)["status"] == "blocked"


def test_force_extraction_preserves_previous_outputs_and_source(tmp_path: Path):
    import docx

    source = tmp_path / "synthetic.docx"
    document = docx.Document()
    document.add_paragraph("Synthetic software extraction fixture.")
    document.save(source)
    before = source.read_bytes()
    first = extract_document(source, tmp_path / "output")
    old_text = (Path(first["output_dir"]) / "text.md").read_bytes()
    second = extract_document(source, tmp_path / "output", force=True)
    assert second["status"] == "pass"
    archived = Path(second["archived_previous_output"])
    assert (archived / "text.md").read_bytes() == old_text
    assert source.read_bytes() == before


def test_altered_derived_document_cannot_pass_cached_hash_check(tmp_path):
    import docx

    source = tmp_path / "synthetic.docx"
    document = docx.Document()
    document.add_paragraph("Original synthetic content.")
    document.save(source)
    first = extract_document(source, tmp_path / "output")
    text = Path(first["output_dir"]) / "text.md"
    text.write_text("Tampered synthetic number 999", encoding="utf-8")
    second = extract_document(source, tmp_path / "output")
    assert second["status"] == "pass"
    assert second["cached"] is False
    assert "999" not in text.read_text(encoding="utf-8")
    assert (Path(second["archived_previous_output"]) / "text.md").read_text() == "Tampered synthetic number 999"


@pytest.mark.parametrize("invalid", ['{"metrics":{"auc":0.8,"auc":0.7}}', '{"metrics":{"auc":NaN}}'])
def test_harvest_preserves_ambiguous_or_nonfinite_canonical_ledger(tmp_path, invalid):
    project = init_project(tmp_path, "Invalid ledger", "machine-governance")
    ledger = project / "analysis/results_ledger.json"
    ledger.write_text(invalid)
    assert harvest_analysis_outputs(project)["status"] == "blocked"
    assert ledger.read_text() == invalid


def test_harvest_conflicting_result_and_claim_binding_preserve_ledger(tmp_path):
    project = init_project(tmp_path, "Conflicting metrics", "machine-governance")
    ledger = project / "analysis/results_ledger.json"
    ledger.write_text(json.dumps({"metrics": {"auc": 0.81}, "metric_claims": {"auc": "original"}}))
    before = ledger.read_bytes()
    (project / "analysis/model_metrics.json").write_text(
        json.dumps({"metrics": {"auc": 0.92}, "metric_claims": {"auc": "different"}})
    )
    result = harvest_analysis_outputs(project)
    assert result["status"] == "blocked"
    assert len(result["issues"]) == 2
    assert ledger.read_bytes() == before


@pytest.mark.parametrize("value", [float("nan"), float("inf"), True, 1.5])
def test_extraction_counts_reject_nonfinite_boolean_and_fractional_values(value):
    from article_machine.services.extraction_validator import validate_extraction_records

    assert validate_extraction_records([{"events": value, "total": 20}])["status"] == "blocked"


def test_unknown_extraction_mode_and_empty_record_fail_closed():
    from article_machine.services.extraction_validator import validate_extraction_records

    assert validate_extraction_records([{"events": 1, "total": 20}], mode="typo")["status"] == "blocked"
    assert validate_extraction_records([{}])["status"] == "blocked"


def test_dataset_fetch_preserves_nonempty_source_directory_without_network(tmp_path):
    project = init_project(tmp_path, "Keep dataset", "machine-governance")
    folder = project / "sources/datasets/uci-thoracic-surgery-postop"
    folder.mkdir(parents=True)
    original = folder / "original.csv"
    original.write_bytes(b"original source")
    with patch("article_machine.services.clinical_datasets._http_get_bytes") as network:
        report = fetch_open_dataset(project, "uci-thoracic-surgery-postop")
    network.assert_not_called()
    assert report["status"] == "blocked"
    assert original.read_bytes() == b"original source"


def test_dataset_zip_flattening_collision_is_blocked_before_extraction(tmp_path):
    project = init_project(tmp_path, "ZIP collision", "machine-governance")
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr("a/patients.csv", "a")
        archive.writestr("b/patients.csv", "b")
    with patch("article_machine.services.clinical_datasets._http_get_bytes", return_value=payload.getvalue()):
        report = fetch_open_dataset(project, "uci-thoracic-surgery-postop")
    assert report["status"] == "blocked"
    assert not list((project / "sources/datasets/uci-thoracic-surgery-postop").glob("*.csv"))


def test_dataset_file_integrity_pass_is_not_scientific_or_license_approval(tmp_path):
    project = init_project(tmp_path, "Integrity scope", "machine-governance")
    folder = project / "sources/datasets/uci-thoracic-surgery-postop"
    folder.mkdir(parents=True)
    (folder / "synthetic.csv").write_text("patient,outcome\nSYN-001,1\n")
    report = ingest_and_verify_dataset(project, "uci-thoracic-surgery-postop")
    assert report["status"] == "pass"
    assert report["scientific_use_eligible"] is False
    manifest = json.loads((project / report["manifest_path"]).read_text())
    assert manifest["license_verified"] is False
    assert manifest["cohort_identity_verified"] is False


@pytest.mark.parametrize(
    "row,mode",
    [
        ({"tp": 1, "fp": 1, "fn": 1, "tn": 1, "total": float("nan"), "sensitivity": float("nan")}, "diagnostic"),
        ({"events": 999}, "pairwise"),
        ({"sd": 1, "mean": float("inf"), "n": -2}, "pairwise"),
    ],
)
def test_invalid_present_fields_cannot_escape_extraction_validation(row, mode):
    from article_machine.services.extraction_validator import validate_extraction_records

    assert validate_extraction_records([row], mode=mode)["status"] == "blocked"


def test_numeric_audit_checks_every_marker_including_invalid_unknown_repetitions(tmp_path):
    project = _ledger_project(tmp_path)
    text = "{{metric:auc}} 0.81; {{metric:n}} 20; {{metric:auc}} NaN; {{metric:invented}} Infinity."
    for language in ("portugues", "ingles"):
        (project / f"drafts/{language}/manuscrito.md").write_text(text)
    report = audit_numerical_consistency(project)
    assert report["status"] == "blocked"
    assert any("invented" in issue for issue in report["issues"])
    assert any("finite numeric" in issue for issue in report["issues"])


def test_unhashable_patient_id_and_malformed_yaml_fail_closed(tmp_path):
    from article_machine.services.results_ledger import evaluate_clinical_prediction_metrics
    from article_machine.services.scientific_execution import scientific_execution_gate

    assert (
        evaluate_clinical_prediction_metrics([0, 1], [0.2, 0.8], patient_ids_train=[[1]], patient_ids_test=["a", "b"])[
            "status"
        ]
        == "blocked"
    )
    (tmp_path / "project.yaml").write_text("project_type: [\n")
    assert scientific_execution_gate(tmp_path, "analysis")["status"] == "blocked"


def test_removed_original_result_blocks_reharvest_and_preserves_provenance(tmp_path):
    project = init_project(tmp_path, "Original source", "machine-governance")
    source = project / "analysis/model_metrics.json"
    source.write_text('{"metrics":{"auc":0.81}}')
    assert harvest_analysis_outputs(project)["status"] == "pass"
    ledger = project / "analysis/results_ledger.json"
    before = ledger.read_bytes()
    source.unlink()  # temporary synthetic fixture, never user data
    assert harvest_analysis_outputs(project)["status"] == "blocked"
    assert ledger.read_bytes() == before


def test_incomplete_cache_manifest_cannot_hide_missing_canonical_text(tmp_path):
    import hashlib

    import docx

    source = tmp_path / "synthetic.docx"
    document = docx.Document()
    document.add_paragraph("Synthetic source")
    document.save(source)
    first = extract_document(source, tmp_path / "out")
    folder = Path(first["output_dir"])
    (folder / "text.md").unlink()  # corrupt only temporary derived fixture
    (folder / "sentinel").write_bytes(b"x")
    first["derived_sha256"] = {"sentinel": hashlib.sha256(b"x").hexdigest()}
    (folder / "manifest.json").write_text(json.dumps(first))
    second = extract_document(source, tmp_path / "out")
    assert second["status"] == "pass"
    assert second["cached"] is False
    assert (folder / "text.md").is_file()
