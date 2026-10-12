import json
from pathlib import Path

import pytest

from article_machine.projects import init_project
from article_machine.review import run_review_trinity
from article_machine.policy.gates import workspace_snapshot
from article_machine.serialization import load_structured_file, save_structured_file


def test_review_trinity_blocks_when_editorial_evidence_fails(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Review Trinity", "systematic-review")
    (project_dir / "drafts" / "manuscript.md").write_text(
        "# Manuscript\n\n{{claim:claim-001}}\n",
        encoding="utf-8",
    )
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"A claim.",'
            '"source_path":"sources/source.md","source_excerpt":"Evidence.",'
            '"reference_key":"ghost2026","status":"supported"}\n'
        ),
        encoding="utf-8",
    )

    report = run_review_trinity(project_dir)

    assert report["aggregate_status"] == "block"
    assert report["reviewers"]["editorial"]["status"] == "block"


def test_review_trinity_blocks_configured_ptbr_style_violations(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Review Style", "systematic-review")
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
    (project_dir / "deliverables" / "resumo.md").write_text(
        "A camada contextual mostrou HR 0,70.",
        encoding="utf-8",
    )
    standards = load_structured_file(project_dir / "standards.yaml")
    standards["ptbr_style_policy"] = {
        "enabled": True,
        "audit_paths": ["deliverables/resumo.md"],
    }
    save_structured_file(project_dir / "standards.yaml", standards)

    report = run_review_trinity(project_dir)

    assert report["aggregate_status"] == "block"
    assert any("PT-BR style audit blocked" in issue for issue in report["reviewers"]["editorial"]["issues"])
    payload = json.loads((project_dir / "reviews" / "ptbr_style_audit.json").read_text(encoding="utf-8"))
    assert payload["status"] == "block"


def _independent_evidence(contract: str, snapshot: dict) -> dict:
    return {
        "contract": contract,
        "independent": True,
        "status": "pass",
        "reviewer_id": "reviewer-external-01",
        "reviewed_at": "2026-10-12T12:00:00Z",
        "assessment": "The reviewer independently inspected the protected scientific inputs and documented the review rationale.",
        "input_snapshot": snapshot,
    }


@pytest.mark.parametrize("failed_item", ["PRISMA", "unconfigured-checklist"])
def test_methodology_blocks_failed_checklist_even_with_current_independent_review(
    tmp_path: Path, failed_item: str
) -> None:
    project_dir = init_project(tmp_path, "Methodology Fail", "systematic-review")
    protocol = load_structured_file(project_dir / "protocol.yaml")
    protocol["status"] = "frozen"
    save_structured_file(project_dir / "protocol.yaml", protocol)
    standards = load_structured_file(project_dir / "standards.yaml")
    standards["checklist_status"] = {
        item: {"status": "pass", "items": ["independently checked"]}
        for item in [*standards["guidelines"], *standards["risk_of_bias_tools"]]
    }
    if failed_item == "PRISMA":
        standards["checklist_status"][failed_item]["status"] = "fail"
    else:
        standards["checklist_status"][failed_item] = {"status": "fail"}
    save_structured_file(project_dir / "standards.yaml", standards)
    snapshot = workspace_snapshot(project_dir)
    save_structured_file(
        project_dir / "reviews" / "methodological_review.json",
        _independent_evidence("MethodologicalReviewEvidenceV1", snapshot),
    )

    report = run_review_trinity(project_dir)
    methodological = report["reviewers"]["methodological"]

    assert methodological["status"] == "block"
    assert any(failed_item in issue and "not pass" in issue for issue in methodological["issues"])
    assert not any("missing or stale" in issue for issue in methodological["issues"])


def test_quantitative_manifest_and_enabled_flag_do_not_replace_independent_review(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Quantitative Evidence", "systematic-review")
    standards = load_structured_file(project_dir / "standards.yaml")
    standards["quantitative_review"] = {"enabled": True}
    save_structured_file(project_dir / "standards.yaml", standards)
    (project_dir / "analysis" / "manifest.json").write_text('{"analysis":"complete"}', encoding="utf-8")

    report = run_review_trinity(project_dir)
    quantitative = report["reviewers"]["quantitative"]

    assert quantitative["status"] == "block"
    assert any("QuantitativeReviewEvidenceV1" in issue for issue in quantitative["issues"])


def test_independent_review_evidence_with_stale_protected_hashes_is_blocked(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Stale Independent Review", "systematic-review")
    standards = load_structured_file(project_dir / "standards.yaml")
    standards["quantitative_review"] = {"enabled": True}
    save_structured_file(project_dir / "standards.yaml", standards)
    (project_dir / "analysis" / "manifest.json").write_text('{"analysis":"complete"}', encoding="utf-8")
    stale_snapshot = workspace_snapshot(project_dir)
    stale_snapshot["input_hashes"]["analysis/manifest.json"] = "0" * 64
    save_structured_file(
        project_dir / "reviews" / "quantitative_review.json",
        _independent_evidence("QuantitativeReviewEvidenceV1", stale_snapshot),
    )

    report = run_review_trinity(project_dir)

    assert report["reviewers"]["quantitative"]["status"] == "block"
    assert any("stale for protected scientific inputs" in issue for issue in report["reviewers"]["quantitative"]["issues"])
