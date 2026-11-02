import json
from pathlib import Path

import pytest

from article_machine.ingest import register_source
from article_machine.analysis import preflight, run_r_script, run_python_script
from article_machine.projects import init_project
from article_machine.serialization import load_structured_file, save_structured_file


def test_ingest_same_basename_preserves_both_versions_and_registers_hashes(tmp_path):
    project = init_project(tmp_path, "Sources", "systematic-review")
    from registration_fixtures import reviewed_registration_fixture
    reviewed_registration_fixture(project)
    source = tmp_path / "paper.txt"
    source.write_text("First observed result")
    first = register_source(project, str(source), "file")
    source.write_text("Corrected observed result")
    second = register_source(project, str(source), "file")
    assert first["source_id"] != second["source_id"]
    assert (project / first["copied_to"]).read_text() == "First observed result"
    assert (project / second["copied_to"]).read_text() == "Corrected observed result"
    assert register_source(project, str(source), "file")["sha256"] == second["sha256"]
    (project / second["copied_to"]).write_text("tampered")
    with pytest.raises(ValueError, match="changed"):
        register_source(project, str(source), "file")
    with pytest.raises(ValueError, match="absent"):
        register_source(project, str(tmp_path / "missing"), "file")
    with pytest.raises(ValueError, match="kind"):
        register_source(project, "input", "unknown")
    for kind in ("doi", "url", "note"):
        entry = register_source(project, "10.1234/example" if kind == "doi" else "https://example.org", kind)
        assert entry["retrieval_status"] == "registered-not-retrieved"
        assert "sha256" not in entry


def test_historical_contract_is_readable_but_cannot_execute(tmp_path, monkeypatch):
    project = init_project(tmp_path, "Historical", "systematic-review")
    compute = load_structured_file(project / "compute.yaml")
    compute.pop("contract_version")
    save_structured_file(project / "compute.yaml", compute)
    monkeypatch.setattr("article_machine.analysis.shutil.which", lambda _: None)
    report = preflight(project)
    assert report["gate_eligible"] is False
    assert run_r_script(project, project / "analysis" / "a.R")["status"] == "blocked"
    assert run_python_script(project, project / "analysis" / "a.py")["status"] == "blocked"
    compute["r"]["required"] = True
    save_structured_file(project / "compute.yaml", compute)
    assert preflight(project)["status"] == "blocked"
