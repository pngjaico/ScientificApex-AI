from pathlib import Path

from article_machine.policy.gates import canonical_gate, report_is_current
from article_machine.projects import advance_mode, init_project
from article_machine.serialization import load_structured_file, save_structured_file


def test_v2_gate_records_hashes_and_rejects_stale_report(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Gate", "systematic-review")
    report = canonical_gate(project, "protocol-freeze", [{"name": "x", "status": "pass", "message": "ok"}])
    assert report["contract"] == "StageGateReportV2"
    assert report_is_current(project, report)
    (project / "protocol.yaml").write_text("changed", encoding="utf-8")
    assert not report_is_current(project, report)


def test_transition_stores_canonical_gate(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Gate", "systematic-review")
    protocol = project / "protocol.yaml"
    payload = load_structured_file(protocol)
    payload["research_question"] = "Q"
    payload["objectives"] = ["O"]
    save_structured_file(protocol, payload)
    result = advance_mode(project, "protocol-freeze")
    assert result["status"] == "passed"
    assert result["gate"]["contract"] == "StageGateReportV2"
