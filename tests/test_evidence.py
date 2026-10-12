import json
from pathlib import Path

from article_machine.evidence import validate_evidence_lock
from article_machine.projects import init_project
from evidence_fixtures import register_claim_sources


def _seed_confidence_claim(project_dir: Path) -> None:
    (project_dir / "drafts" / "manuscript.md").write_text(
        "# Manuscript\n\nThis is a perfect production-grade article machine {{claim:claim-001}}.\n",
        encoding="utf-8",
    )
    (project_dir / "sources" / "study-001.md").write_text(
        "Machine audit passed a limited check.\n",
        encoding="utf-8",
    )
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"Machine audit passed a limited check.",'
            '"source_path":"sources/study-001.md","source_excerpt":"Machine audit passed a limited check.",'
            '"reference_key":"smith2024","status":"supported"}\n'
        ),
        encoding="utf-8",
    )
    (project_dir / "drafts" / "references.bib").write_text(
        "@article{smith2024,\n  title={A Study}\n}\n",
        encoding="utf-8",
    )


def _acceptance_benchmark() -> dict:
    return {
        "contract": "AgentBenchmarkReport",
        "level": "acceptance",
        "gate_eligible": True,
        "status": "pass",
        "aggregate_status": "pass",
        "cases": [{"id": "fixed-case-001", "status": "pass"}],
        "provenance": {
            "runtime": {"model": "gpt-5.6-sol", "reasoning_effort": "ultra"},
            "code_revision": "abc1234",
            "task_id": "task-benchmark-001",
        },
        "scoring": {
            dimension: {"status": "pass", "score": 0.9, "threshold": 0.8}
            for dimension in ("correctness", "provenance", "reproducibility", "safety", "usefulness")
        },
        "residual_risks": ["The fixed benchmark corpus does not cover every future project."],
    }


def test_evidence_lock_passes_with_claim_map_and_reference(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Review One", "systematic-review")
    (project_dir / "drafts" / "manuscript.md").write_text(
        "# Manuscript\n\n{{claim:claim-001}}\n",
        encoding="utf-8",
    )
    (project_dir / "sources" / "study-001.md").write_text(
        "Primary outcome improved by 12%.\n",
        encoding="utf-8",
    )
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"The intervention improved the primary outcome.",'
            '"source_path":"sources/study-001.md","source_excerpt":"Primary outcome improved by 12%.",'
            '"reference_key":"smith2024","status":"supported"}\n'
        ),
        encoding="utf-8",
    )
    (project_dir / "drafts" / "references.bib").write_text(
        "@article{smith2024,\n  title={A Study},\n  author={Smith, Jane},\n  year={2024}\n}\n",
        encoding="utf-8",
    )

    register_claim_sources(project_dir)
    report = validate_evidence_lock(project_dir)

    assert report["status"] == "pass"
    assert report["issues"] == []


def test_evidence_lock_accepts_powershell_utf8_bom_claim_map(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Review BOM", "systematic-review")
    (project_dir / "drafts" / "manuscript.md").write_text(
        "# Manuscript\n\n{{claim:claim-001}}\n",
        encoding="utf-8",
    )
    (project_dir / "sources" / "study-001.md").write_text(
        "Primary outcome improved by 12%.\n",
        encoding="utf-8",
    )
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"The intervention improved the primary outcome.",'
            '"source_path":"sources/study-001.md","source_excerpt":"Primary outcome improved by 12%.",'
            '"reference_key":"smith2024","status":"supported"}\n'
        ),
        encoding="utf-8-sig",
    )
    (project_dir / "drafts" / "references.bib").write_text(
        "@article{smith2024,\n  title={A Study},\n  year={2024}\n}\n",
        encoding="utf-8",
    )

    register_claim_sources(project_dir)
    report = validate_evidence_lock(project_dir)

    assert report["status"] == "pass"


def test_evidence_lock_blocks_when_reference_key_is_missing(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Review Two", "systematic-review")
    (project_dir / "drafts" / "manuscript.md").write_text(
        "# Manuscript\n\n{{claim:claim-001}}\n",
        encoding="utf-8",
    )
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"The intervention improved the primary outcome.",'
            '"source_path":"sources/study-001.md","source_excerpt":"Primary outcome improved by 12%.",'
            '"reference_key":"missing2024","status":"supported"}\n'
        ),
        encoding="utf-8",
    )

    report = validate_evidence_lock(project_dir)

    assert report["status"] == "block"
    assert any("missing2024" in issue for issue in report["issues"])


def test_evidence_lock_blocks_missing_source_file(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Missing Source", "systematic-review")
    (project_dir / "drafts" / "manuscript.md").write_text("# Manuscript\n\n{{claim:claim-001}}\n", encoding="utf-8")
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"The intervention improved the primary outcome.",'
            '"source_path":"sources/missing.md","source_excerpt":"Primary outcome improved by 12%.",'
            '"reference_key":"smith2024","status":"supported"}\n'
        ),
        encoding="utf-8",
    )
    (project_dir / "drafts" / "references.bib").write_text("@article{smith2024,\n  title={A Study}\n}\n", encoding="utf-8")

    report = validate_evidence_lock(project_dir)

    assert report["status"] == "block"
    assert any("does not exist" in issue for issue in report["issues"])


def test_evidence_lock_blocks_false_excerpt(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "False Excerpt", "systematic-review")
    (project_dir / "drafts" / "manuscript.md").write_text("# Manuscript\n\n{{claim:claim-001}}\n", encoding="utf-8")
    (project_dir / "sources" / "study-001.md").write_text("Observed remission did not change.\n", encoding="utf-8")
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"The intervention improved remission.",'
            '"source_path":"sources/study-001.md","source_excerpt":"Remission improved by 15%.",'
            '"reference_key":"smith2024","status":"supported"}\n'
        ),
        encoding="utf-8",
    )
    (project_dir / "drafts" / "references.bib").write_text("@article{smith2024,\n  title={A Study}\n}\n", encoding="utf-8")

    report = validate_evidence_lock(project_dir)

    assert report["status"] == "block"
    assert any("does not appear" in issue for issue in report["issues"])


def test_evidence_lock_blocks_duplicate_claim_and_invalid_identifiers(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Duplicate Claim", "systematic-review")
    (project_dir / "drafts" / "manuscript.md").write_text("# Manuscript\n\n{{claim:claim-001}}\n", encoding="utf-8")
    (project_dir / "sources" / "study-001.md").write_text("Primary outcome improved by 12%.\n", encoding="utf-8")
    claim = (
        '{"claim_id":"claim-001","statement":"The intervention improved the primary outcome.",'
        '"source_path":"sources/study-001.md","source_excerpt":"Primary outcome improved by 12%.",'
        '"reference_key":"smith2024","status":"supported","doi":"bad-doi","pmid":"12AB"}\n'
    )
    (project_dir / "evidence" / "claim_map.jsonl").write_text(claim + claim, encoding="utf-8")
    (project_dir / "drafts" / "references.bib").write_text("@article{smith2024,\n  title={A Study}\n}\n", encoding="utf-8")

    report = validate_evidence_lock(project_dir)

    assert report["status"] == "block"
    assert any("Duplicate claim_id" in issue for issue in report["issues"])
    assert any("invalid DOI" in issue for issue in report["issues"])
    assert any("invalid PMID" in issue for issue in report["issues"])


def test_evidence_lock_blocks_unmarked_factual_sentence(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Unmarked Fact", "systematic-review")
    (project_dir / "drafts" / "manuscript.md").write_text(
        "# Manuscript\n\nThe intervention improved remission by 15%.\n",
        encoding="utf-8",
    )

    report = validate_evidence_lock(project_dir)

    assert report["status"] == "block"
    assert any("has no {{claim:...}} marker" in issue for issue in report["issues"])


def test_evidence_lock_blocks_perfect_language_without_benchmark(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Perfect Claim", "systematic-review")
    _seed_confidence_claim(project_dir)

    report = validate_evidence_lock(project_dir)

    assert report["status"] == "block"
    assert any("Prohibited confidence language" in issue for issue in report["issues"])


def test_evidence_lock_rejects_legacy_status_pass_benchmark(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Legacy Benchmark", "systematic-review")
    _seed_confidence_claim(project_dir)
    (project_dir / "analysis" / "benchmark_report.json").write_text(
        json.dumps({"status": "pass"}),
        encoding="utf-8",
    )

    report = validate_evidence_lock(project_dir)

    assert report["status"] == "block"
    assert any("Prohibited confidence language" in issue for issue in report["issues"])


def test_evidence_lock_rejects_confidence_language_with_self_declared_v1_benchmark(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Acceptance Benchmark", "systematic-review")
    _seed_confidence_claim(project_dir)
    (project_dir / "analysis" / "benchmark_report.json").write_text(
        json.dumps(_acceptance_benchmark()),
        encoding="utf-8",
    )

    report = validate_evidence_lock(project_dir)

    assert report["status"] == "block"
    assert any("Prohibited confidence language" in issue for issue in report["issues"])
