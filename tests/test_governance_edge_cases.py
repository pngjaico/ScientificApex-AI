"""Fail-closed lifecycle, freshness, and benchmark regression tests."""

import hashlib
import json
from pathlib import Path

import pytest

from article_machine.benchmarks import validate_benchmark_file, validate_benchmark_payload
from article_machine.policy.gates import canonical_gate, report_is_current, workspace_snapshot
from article_machine.projects import advance_mode, gate_mode, init_project, load_project, next_modes, register_review_protocol
from article_machine.review import _aggregate_status, run_review_trinity
from article_machine.serialization import load_structured_file, save_structured_file
from article_machine.zero_trust import audit_stage


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _machine_project(tmp_path: Path) -> Path:
    return init_project(tmp_path, "Governance Edges", "machine-governance")


def test_governance_transitions_enforce_order_and_prerequisite_chain(tmp_path: Path) -> None:
    project = _machine_project(tmp_path)
    assert load_project(project)["state"]["allowed_next_modes"] == ["inventory"]

    out_of_order = advance_mode(project, "upgrade")
    assert out_of_order["status"] == "blocked"
    assert load_project(project)["state"]["current_mode"] == "bootstrap"

    _write_json(project / "context" / "inventory_manifest.json", {"entries": ["code"]})
    inventory = advance_mode(project, "inventory")
    assert inventory["status"] == "passed"
    assert load_project(project)["state"]["allowed_next_modes"] == ["upgrade"]

    _write_json(project / "context" / "upgrade_record.json", {"changes": []})
    upgrade = advance_mode(project, "upgrade")
    assert upgrade["status"] == "passed"
    assert load_project(project)["state"]["allowed_next_modes"] == ["verification"]

    _write_json(project / "analysis" / "verification_report.json", {"status": "pass"})
    verification = advance_mode(project, "verification")
    assert verification["status"] == "passed"
    assert load_project(project)["state"]["allowed_next_modes"] == ["acceptance-benchmark"]

    # A file that merely exists is not a benchmark and cannot advance the lane.
    _write_json(project / "analysis" / "benchmark_report.json", {"status": "pass"})
    acceptance = advance_mode(project, "acceptance-benchmark")
    assert acceptance["status"] == "blocked"
    assert load_project(project)["state"]["current_mode"] == "verification"
    assert audit_stage(project, target_mode="release")["gate_eligible"] is False


def test_next_modes_returns_only_the_canonical_successor_for_each_lane() -> None:
    assert next_modes("inventory", "machine-governance") == ["upgrade"]
    assert next_modes("release", "machine-governance") == []
    assert next_modes("unknown", "machine-governance") == []
    assert next_modes("analysis", "computational-discovery") == ["discovery"]
    assert next_modes("extraction", "computational-discovery") == ["discovery"]
    assert next_modes("extraction", "evidence-writing") == ["analysis"]
    assert next_modes("drafting", "evidence-writing") == ["review-trinity"]
    assert next_modes("review-trinity", "evidence-writing") == ["submission"]
    assert next_modes("submission", "evidence-writing") == []
    assert next_modes("unknown", "evidence-writing") == []


def test_registration_requirements_block_extraction_until_registered(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Registered Review", "systematic-review")
    project_payload = load_project(project)
    project_payload["state"]["current_mode"] = "screening"
    project_payload["state"]["allowed_next_modes"] = ["extraction"]
    save_structured_file(project / "project.yaml", project_payload)
    (project / "sources" / "registry.jsonl").write_text(
        '{"id":"source-1","registered_at":"2021-01-01"}\n', encoding="utf-8"
    )

    protocol = load_structured_file(project / "protocol.yaml")
    protocol["registration"]["required"] = True
    save_structured_file(project / "protocol.yaml", protocol)
    blocked = gate_mode(project, "extraction")
    assert blocked["status"] == "blocked"
    assert any("registration.status" in issue for issue in blocked["issues"])

    register_review_protocol(
        project, "OSF", "osf-123", "https://osf.io/osf-123", "2026-01-01", notes="preregistered"
    )
    assert gate_mode(project, "extraction")["status"] == "blocked"
    from registration_fixtures import reviewed_registration_fixture
    reviewed_registration_fixture(project)
    extraction = gate_mode(project, "extraction")
    assert extraction["status"] == "passed"

    project_payload = load_project(project)
    project_payload["state"]["current_mode"] = "extraction"
    project_payload["state"]["allowed_next_modes"] = ["analysis"]
    save_structured_file(project / "project.yaml", project_payload)
    analysis = gate_mode(project, "analysis")
    assert analysis["status"] == "passed"


@pytest.mark.parametrize(
    "relative_path",
    [
        "protocol.yaml",
        "sources/registry.jsonl",
        "analysis/manifest.json",
        "article_machine/stale_control.py",
    ],
)
def test_canonical_gate_rejects_staleness_after_each_protected_input_change(
    tmp_path: Path, relative_path: str
) -> None:
    project = init_project(tmp_path, "Freshness", "systematic-review")
    target = project / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("before", encoding="utf-8")
    report = canonical_gate(project, "protocol-freeze", [{"name": "fixture", "status": "pass"}])
    assert report_is_current(project, report)

    target.write_text("after", encoding="utf-8")
    assert report_is_current(project, report) is False


def test_review_report_staleness_is_detected_after_source_and_red_team_change(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Review Freshness", "systematic-review")
    (project / "sources" / "registry.jsonl").write_text('{"id":"source-1"}\n', encoding="utf-8")
    red_team = project / "reviews" / "red_team_report.json"
    red_team.write_text("{}", encoding="utf-8")
    red_team.write_text(
        json.dumps({"contract": "ScientificRedTeamReportV2", "independent": True, "status": "pass",
                    "input_snapshot": workspace_snapshot(project)}),
        encoding="utf-8",
    )
    report = run_review_trinity(project)
    assert report["review_snapshot"]
    assert report["red_team_sha256"]
    assert report["reviewers"]["red_team"]["status"] == "pass"

    (project / "sources" / "registry.jsonl").write_text('{"id":"source-2"}\n', encoding="utf-8")
    source_gate = gate_mode(project, "submission")
    assert any("stale" in issue for issue in source_gate["issues"])

    # Rerunning review cannot make the old independent red-team verdict current.
    report = run_review_trinity(project)
    assert report["review_snapshot"]
    assert report["reviewers"]["red_team"]["status"] == "block"
    assert any("rerun the independent review" in issue for issue in report["reviewers"]["red_team"]["issues"])

    # Only a newly recorded independent report with the current snapshot refreshes it.
    red_team.write_text("{}", encoding="utf-8")
    red_team.write_text(
        json.dumps({"contract": "ScientificRedTeamReportV2", "independent": True, "status": "pass",
                    "input_snapshot": workspace_snapshot(project)}),
        encoding="utf-8",
    )
    report = run_review_trinity(project)
    assert report["reviewers"]["red_team"]["status"] == "pass"
    red_team.write_text("{}", encoding="utf-8")
    red_team_gate = gate_mode(project, "submission")
    assert any("red-team artifact" in issue for issue in red_team_gate["issues"])

    stage = audit_stage(project, target_mode="submission")
    review_check = next(item for item in stage["checks"] if item["check"] == "review_report")
    assert review_check["status"] == "block"


@pytest.mark.parametrize(
    ("audit_paths", "expected_issue"),
    [(["deliverables/missing.md"], "path is missing"), ([], "no audit_paths were configured")],
)
def test_review_blocks_incomplete_configured_style_audit(
    tmp_path: Path, audit_paths: list[str], expected_issue: str
) -> None:
    project = init_project(tmp_path, "Style Audit Config", "systematic-review")
    standards = load_structured_file(project / "standards.yaml")
    standards["ptbr_style_policy"] = {"enabled": True, "audit_paths": audit_paths}
    save_structured_file(project / "standards.yaml", standards)

    report = run_review_trinity(project)

    assert report["reviewers"]["editorial"]["status"] == "block"
    assert any(expected_issue in issue for issue in report["reviewers"]["editorial"]["issues"])


def test_review_aggregate_status_is_block_first_then_revise_pass_pending() -> None:
    assert _aggregate_status(["pass", "block"]) == "block"
    assert _aggregate_status(["pass", "revise"]) == "revise"
    assert _aggregate_status(["pass", "pass"]) == "pass"
    assert _aggregate_status(["pass", "pending"]) == "pending"


def _benchmark_report(root: Path) -> dict:
    values = {
        "fixture": b'{"input":1}',
        "protocol": b'{"version":1}',
        "output": b'{"answer":42}',
        "gold_answer": b'{"answer":42}',
        "rubric": b'{"assertions":{"provenance":true,"reproducibility":true,"safety":true,"usefulness":true}}',
    }
    refs = {}
    for name, content in values.items():
        (root / f"{name}.json").write_bytes(content)
        refs[name] = {"path": f"{name}.json", "sha256": hashlib.sha256(content).hexdigest()}
    run = {
        "run_id": "run-1", "evaluator": "exact-json-v1", "status": "pass",
        "fixture_hash": refs["fixture"]["sha256"], "protocol_hash": refs["protocol"]["sha256"],
        "output_hash": refs["output"]["sha256"], "gold_answer_hash": refs["gold_answer"]["sha256"],
        "rubric_hash": refs["rubric"]["sha256"], "artifacts": refs,
        "prompt": "fixed benchmark prompt", "model": "fixture-runner",
        "reasoning_effort": "deterministic", "duration_seconds": 0.1, "exit_code": 0,
        # Deliberately optimistic producer claims: implementation must ignore them.
        "scores": {name: 1.0 for name in ("correctness", "provenance", "reproducibility", "safety", "usefulness")},
    }
    return {
        "contract": "AgentBenchmarkReportV2", "contract_version": 2, "level": "acceptance",
        "cases": [{"id": "case-1", "runs": [run]}],
        "provenance": {"runtime": {"model": "fixture-runner", "reasoning_effort": "deterministic"},
                       "code_revision": "abcdef0123", "task_id": "negative-regression"},
        "residual_risks": ["synthetic fail-closed test data"],
    }


@pytest.mark.parametrize("malformed_artifact", ["fixture", "protocol", "output", "gold_answer", "rubric"])
def test_benchmark_blocks_malformed_json_artifacts(tmp_path: Path, malformed_artifact: str) -> None:
    report = _benchmark_report(tmp_path)
    path = tmp_path / f"{malformed_artifact}.json"
    content = b"{malformed"
    path.write_bytes(content)
    reference = report["cases"][0]["runs"][0]["artifacts"][malformed_artifact]
    reference["sha256"] = hashlib.sha256(content).hexdigest()
    hash_field = f"{malformed_artifact}_hash"
    if hash_field in report["cases"][0]["runs"][0]:
        report["cases"][0]["runs"][0][hash_field] = reference["sha256"]
    report_path = tmp_path / "benchmark_report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")

    result = validate_benchmark_file(report_path)

    assert result["gate_eligible"] is False
    assert any("independently verified" in issue for issue in result["issues"])


def test_benchmark_recomputes_correctness_instead_of_trusting_claimed_scores(tmp_path: Path) -> None:
    report = _benchmark_report(tmp_path)
    output = b'{"answer":43}'
    (tmp_path / "output.json").write_bytes(output)
    digest = hashlib.sha256(output).hexdigest()
    run = report["cases"][0]["runs"][0]
    run["artifacts"]["output"]["sha256"] = digest
    run["output_hash"] = digest
    report_path = tmp_path / "benchmark_report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")

    result = validate_benchmark_file(report_path)

    assert result["gate_eligible"] is False
    assert any("scoring.correctness.score must meet or exceed its threshold" in issue for issue in result["issues"])


def test_benchmark_blocks_tampered_hash_path_escape_and_unknown_evaluator(tmp_path: Path) -> None:
    report = _benchmark_report(tmp_path)
    report_path = tmp_path / "benchmark_report.json"

    report["cases"][0]["runs"][0]["output_hash"] = "0" * 64
    report_path.write_text(json.dumps(report), encoding="utf-8")
    assert validate_benchmark_file(report_path)["gate_eligible"] is False

    report = _benchmark_report(tmp_path)
    report["cases"][0]["runs"][0]["artifacts"]["output"]["path"] = "../outside.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    assert validate_benchmark_file(report_path)["gate_eligible"] is False

    report = _benchmark_report(tmp_path)
    report["cases"][0]["runs"][0]["evaluator"] = "llm-judge"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    result = validate_benchmark_file(report_path)
    assert result["gate_eligible"] is False
    assert any("independently verified" in issue for issue in result["issues"])


def test_payload_only_scores_and_repeated_nondeterministic_run_are_never_gate_eligible(tmp_path: Path) -> None:
    report = _benchmark_report(tmp_path)
    report["cases"][0]["non_deterministic"] = True
    report["cases"][0]["runs"] = [report["cases"][0]["runs"][0]] * 3
    report["aggregation"] = "recomputed-v2"
    report["scoring"] = {
        dimension: {"score": 1.0, "threshold": 0.9, "status": "pass"}
        for dimension in ("correctness", "provenance", "reproducibility", "safety", "usefulness")
    }

    result = validate_benchmark_payload(report)

    assert result["gate_eligible"] is False
    assert any("file-backed evaluation evidence" in issue for issue in result["issues"])
    assert any("distinct concrete run_id" in issue for issue in result["issues"])


def test_benchmark_missing_report_and_unreadable_json_are_blocked(tmp_path: Path) -> None:
    missing = validate_benchmark_file(tmp_path / "missing.json")
    assert missing["gate_eligible"] is False

    malformed = tmp_path / "broken.json"
    malformed.write_text("{not-json", encoding="utf-8")
    unreadable = validate_benchmark_file(malformed)
    assert unreadable["gate_eligible"] is False
    assert any("valid JSON" in issue for issue in unreadable["issues"])

    bad_encoding = tmp_path / "bad-encoding.json"
    bad_encoding.write_bytes(b"\xff\xfe")
    encoded = validate_benchmark_file(bad_encoding)
    assert encoded["gate_eligible"] is False


def test_benchmark_payload_validator_accumulates_malformed_contract_edges() -> None:
    assert validate_benchmark_payload([])["gate_eligible"] is False
    invalid_run = {
        "duration_seconds": 10**5000,
        "exit_code": 7,
        "evaluator": "unknown-evaluator",
        "artifacts": {},
    }
    payload = {
        "contract": "AgentBenchmarkReportV2",
        "level": "unrecognized-level",
        "cases": [
            None,
            {"id": "", "runs": []},
            {"id": "reused", "runs": [None, invalid_run]},
            {"id": "reused", "non_deterministic": True, "runs": [{"run_id": ""}]},
        ],
        "provenance": [],
        "scoring": {
            "correctness": {"score": 10**5000, "threshold": 1.5},
            "provenance": None,
            "reproducibility": {"score": -1.0, "threshold": True},
            "safety": {"score": 0.5, "threshold": None},
            "usefulness": {"score": 0.4, "threshold": 0.6},
        },
        "residual_risks": [None, "todo"],
    }

    result = validate_benchmark_payload(payload)

    assert result["gate_eligible"] is False
    assert len(result["issues"]) >= 15

