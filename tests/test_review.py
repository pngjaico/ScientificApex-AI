import json
from pathlib import Path

from article_machine.projects import init_project
from article_machine.review import run_review_trinity
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
