import hashlib
import json
from pathlib import Path

from article_machine.benchmarks import aggregate_benchmark_payload, validate_benchmark_file, validate_benchmark_payload


def test_benchmark_v2_blocks_fabricated_hashes_even_when_scores_are_high() -> None:
    run = {
        "status": "pass", "fixture_hash": "a", "prompt": "p", "protocol_hash": "b", "output_hash": "c",
        "gold_answer_hash": "d", "rubric_hash": "e", "model": "gpt-5.6-sol", "reasoning_effort": "ultra",
        "duration_seconds": 1, "exit_code": 0,
        "scores": {name: 0.95 for name in ("correctness", "provenance", "reproducibility", "safety", "usefulness")},
    }
    report = aggregate_benchmark_payload({
        "cases": [{"id": "c1", "non_deterministic": True, "runs": [run, run, run]}],
        "provenance": {"runtime": {"model": "gpt-5.6-sol", "reasoning_effort": "ultra"}, "code_revision": "abcdef0", "task_id": "task-1"},
        "residual_risks": ["bounded corpus"], "gate_eligible": True,
    })
    validation = validate_benchmark_payload(report)
    assert validation["gate_eligible"] is False
    assert any("SHA-256 digest" in issue for issue in validation["issues"])


def test_v1_benchmark_is_historical_not_gate_eligible() -> None:
    validation = validate_benchmark_payload({"contract": "AgentBenchmarkReport", "level": "acceptance"})
    assert validation["gate_eligible"] is False


def test_file_backed_exact_json_is_bounded_and_ignores_rubric_score_claims(tmp_path: Path) -> None:
    artifacts = {
        "fixture": b'{"input":1}',
        "protocol": b'{"protocol":"v1"}',
        "output": b'{"answer":42}',
        "gold_answer": b'{"answer":42}',
        "rubric": json.dumps({"assertions": {name: True for name in (
            "provenance", "reproducibility", "safety", "usefulness"
        )}}).encode(),
    }
    refs = {}
    for name, content in artifacts.items():
        path = tmp_path / f"{name}.json"
        path.write_bytes(content)
        refs[name] = {"path": path.name, "sha256": hashlib.sha256(content).hexdigest()}
    run = {
        "run_id": "run-1", "evaluator": "exact-json-v1", "status": "pass",
        "fixture_hash": refs["fixture"]["sha256"], "protocol_hash": refs["protocol"]["sha256"],
        "output_hash": refs["output"]["sha256"], "gold_answer_hash": refs["gold_answer"]["sha256"],
        "rubric_hash": refs["rubric"]["sha256"], "artifacts": refs,
        "prompt": "fixed test prompt", "model": "deterministic-fixture-runner",
        "reasoning_effort": "deterministic", "duration_seconds": 0.01, "exit_code": 0,
        "scores": {name: 0.0 for name in ("correctness", "provenance", "reproducibility", "safety", "usefulness")},
    }
    report = {
        "contract": "AgentBenchmarkReportV2", "contract_version": 2, "level": "acceptance",
        "cases": [{"id": "exact-json", "non_deterministic": True,
                   "runs": [{**run, "run_id": f"run-{index}"} for index in range(1, 4)]}],
        "provenance": {"runtime": {"model": "deterministic-fixture-runner", "reasoning_effort": "deterministic"},
                       "code_revision": "abcdef0123", "task_id": "local-test"},
        "residual_risks": ["bounded deterministic fixture only"],
    }
    report_path = tmp_path / "benchmark_report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")

    result = validate_benchmark_file(report_path)

    assert result["gate_eligible"] is False
    assert result["eligibility_scope"] == "deterministic-artifact-regression"
    assert result["scoring"]["correctness"]["score"] == 1.0
    assert result["scoring"]["provenance"]["score"] == 1.0
    assert result["scoring"]["reproducibility"]["score"] == 1.0
    assert result["scoring"]["safety"]["score"] == 0.0
    assert result["scoring"]["usefulness"]["score"] == 0.0
    assert any("cannot unlock scientific acceptance" in issue for issue in result["issues"])

    rubric = json.dumps({"assertions": {name: False for name in (
        "provenance", "reproducibility", "safety", "usefulness"
    )}}).encode()
    (tmp_path / "rubric.json").write_bytes(rubric)
    digest = hashlib.sha256(rubric).hexdigest()
    for item in report["cases"][0]["runs"]:
        item["rubric_hash"] = digest
        item["artifacts"]["rubric"]["sha256"] = digest
    report_path.write_text(json.dumps(report), encoding="utf-8")
    changed_rubric = validate_benchmark_file(report_path)
    assert changed_rubric["gate_eligible"] is False
    assert changed_rubric["scoring"] == result["scoring"]

    report["cases"][0]["runs"][2]["run_id"] = "run-1"
    report_path.write_text(json.dumps(report), encoding="utf-8")
    repeated = validate_benchmark_file(report_path)
    assert repeated["gate_eligible"] is False
    assert any("distinct concrete run_id" in issue for issue in repeated["issues"])

    report["cases"][0]["runs"][2]["run_id"] = "run-3"
    report["cases"][0]["runs"][0]["output_hash"] = "0" * 64
    report_path.write_text(json.dumps(report), encoding="utf-8")
    forged = validate_benchmark_file(report_path)
    assert forged["gate_eligible"] is False
    assert any("independently verified" in issue for issue in forged["issues"])

    artifacts["output"] = b'{"answer":43}'
    (tmp_path / "output.json").write_bytes(artifacts["output"])
    tampered = validate_benchmark_file(report_path)
    assert tampered["gate_eligible"] is False
    assert any("independently verified" in issue for issue in tampered["issues"])
