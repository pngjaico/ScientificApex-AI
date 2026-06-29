from pathlib import Path

from article_machine.deliverables import (
    build_deliverable,
    export_deliverable,
    import_conference_requirements,
    plan_deliverable,
    qa_deliverable,
    submit_deliverable,
)
from article_machine.projects import init_project
from article_machine.serialization import load_structured_file, save_structured_file
from article_machine.visuals import route_visual_backend


def _seed_claims(project_dir: Path) -> None:
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        "\n".join(
            [
                (
                    '{"claim_id":"claim-supported","statement":"Intervention improved remission.",'
                    '"source_path":"sources/converted/study-001.md","source_excerpt":"Remission improved by 15%.",'
                    '"reference_key":"smith2024","status":"supported"}'
                ),
                (
                    '{"claim_id":"claim-blocked","statement":"Safety was perfect.",'
                    '"source_path":"sources/converted/study-002.md","source_excerpt":"Safety data incomplete.",'
                    '"reference_key":"jones2024","status":"blocked"}'
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (project_dir / "drafts" / "references.bib").write_text(
        "@article{smith2024,\n  title={Study 1},\n  year={2024}\n}\n"
        "@article{jones2024,\n  title={Study 2},\n  year={2024}\n}\n",
        encoding="utf-8",
    )


def test_import_conference_creates_deliverable_scaffold(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Congress Project", "systematic-review")

    report = import_conference_requirements(
        project_dir,
        source="# Gastro Week 2026\n\nOral presentation. Duration: 5 minutes. Maximum 6 slides.\n",
        kind="deck",
        slug="gastro-week-oral",
    )

    deliverable_dir = project_dir / "deliverables" / "gastro-week-oral"
    conference = load_structured_file(deliverable_dir / "conference.yaml")

    assert report["status"] == "created"
    assert deliverable_dir.is_dir()
    assert conference["kind"] == "deck"
    assert conference["profile"] == "5-min"
    assert conference["limits"]["max_slides"] == 6
    assert (deliverable_dir / "storyboard.yaml").exists()
    assert (deliverable_dir / "theme.yaml").exists()
    assert (deliverable_dir / "qa_report.json").exists()


def test_plan_deliverable_uses_only_supported_claims(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Claim Safe Deck", "systematic-review")
    _seed_claims(project_dir)
    import_conference_requirements(
        project_dir,
        source="# Event\n\nOral presentation. Duration: 10 minutes. Maximum 8 slides.\n",
        kind="deck",
        slug="claim-safe-deck",
    )

    report = plan_deliverable(project_dir / "deliverables" / "claim-safe-deck")
    storyboard = load_structured_file(project_dir / "deliverables" / "claim-safe-deck" / "storyboard.yaml")

    assert report["status"] == "planned"
    claim_ids = {
        claim_id
        for scene in storyboard["scenes"]
        for claim_id in scene.get("source_claim_ids", [])
    }
    assert claim_ids == {"claim-supported"}
    assert "claim-blocked" not in (project_dir / "deliverables" / "claim-safe-deck" / "conference_abstract.md").read_text(
        encoding="utf-8"
    )


def test_qa_blocks_storyboard_with_unsupported_claim(tmp_path: Path, monkeypatch) -> None:
    project_dir = init_project(tmp_path, "Poster QA", "systematic-review")
    _seed_claims(project_dir)
    import_conference_requirements(
        project_dir,
        source="# Event\n\nPoster. A0 portrait.\n",
        kind="poster",
        slug="poster-a0",
    )
    deliverable_dir = project_dir / "deliverables" / "poster-a0"
    plan_deliverable(deliverable_dir)
    build_deliverable(deliverable_dir)

    storyboard = load_structured_file(deliverable_dir / "storyboard.yaml")
    storyboard["scenes"][0]["source_claim_ids"].append("claim-blocked")
    save_structured_file(deliverable_dir / "storyboard.yaml", storyboard)

    monkeypatch.setattr(
        "article_machine.playwright_ops.playwright_available",
        lambda: {"status": "pass", "npx_path": "C:/Program Files/nodejs/npx.cmd"},
    )
    monkeypatch.setattr(
        "article_machine.playwright_ops.qa_html",
        lambda html_path, output_dir, profile: {
            "status": "pass",
            "overflow_elements": [],
            "screenshot": str(Path(output_dir) / "qa.png"),
        },
    )

    report = qa_deliverable(deliverable_dir)

    assert report["status"] == "block"
    assert any("claim-blocked" in issue for issue in report["issues"])


def test_visual_backend_router_prefers_configured_backends(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

    assert route_visual_backend("technical-diagram")["backend"] == "scientific-schematics"
    assert route_visual_backend("title-illustration")["backend"] == "openai-gpt-image"
    assert route_visual_backend("chart")["backend"] == "python-r-native"


def test_export_deliverable_records_artifacts(tmp_path: Path, monkeypatch) -> None:
    project_dir = init_project(tmp_path, "Export Deck", "systematic-review")
    _seed_claims(project_dir)
    import_conference_requirements(
        project_dir,
        source="# Congress\n\nOral presentation. Duration: 5 minutes. Maximum 5 slides.\n",
        kind="deck",
        slug="export-deck",
    )
    deliverable_dir = project_dir / "deliverables" / "export-deck"
    plan_deliverable(deliverable_dir)
    build_deliverable(deliverable_dir)

    monkeypatch.setattr(
        "article_machine.playwright_ops.playwright_available",
        lambda: {"status": "pass", "npx_path": "C:/Program Files/nodejs/npx.cmd"},
    )

    def fake_qa(html_path: Path, output_dir: Path, profile: str) -> dict:
        qa_image = Path(output_dir) / "qa.png"
        qa_image.write_bytes(b"png")
        return {
            "status": "pass",
            "overflow_elements": [],
            "screenshot": str(qa_image),
        }

    def fake_pdf(html_path: Path, output_path: Path, profile: str) -> dict:
        output_path.write_bytes(b"%PDF-1.4\n")
        return {"status": "pass", "path": str(output_path)}

    def fake_thumb(html_path: Path, output_path: Path, profile: str) -> dict:
        output_path.write_bytes(b"png")
        return {"status": "pass", "path": str(output_path)}

    def fake_pptx(
        spec_path: Path,
        output_path: Path,
        kind: str,
        conference_path: Path | None = None,
    ) -> dict:
        output_path.write_bytes(b"PPTX")
        return {"status": "pass", "path": str(output_path)}

    monkeypatch.setattr("article_machine.playwright_ops.qa_html", fake_qa)
    monkeypatch.setattr("article_machine.playwright_ops.export_html_pdf", fake_pdf)
    monkeypatch.setattr("article_machine.playwright_ops.capture_thumbnail", fake_thumb)
    monkeypatch.setattr("article_machine.pptx_bridge.export_editable_pptx", fake_pptx)

    qa_report = qa_deliverable(deliverable_dir)
    export_report = export_deliverable(deliverable_dir)

    assert qa_report["status"] == "pass"
    assert export_report["status"] == "exported"
    assert (deliverable_dir / "exports" / "export-deck.html").exists()
    assert (deliverable_dir / "exports" / "export-deck.pdf").exists()
    assert (deliverable_dir / "exports" / "export-deck.pptx").exists()
    assert len(export_report["manifest"]["artifacts"]) >= 3
    assert export_report["manifest"]["state"]["current_stage"] == "export"


def test_submission_dry_run_blocks_without_playwright(tmp_path: Path, monkeypatch) -> None:
    project_dir = init_project(tmp_path, "Submit Deck", "systematic-review")
    _seed_claims(project_dir)
    import_conference_requirements(
        project_dir,
        source="https://example.org/congress/submit",
        kind="deck",
        slug="submit-deck",
    )
    deliverable_dir = project_dir / "deliverables" / "submit-deck"
    plan_deliverable(deliverable_dir)
    build_deliverable(deliverable_dir)

    qa_report = load_structured_file(deliverable_dir / "qa_report.json")
    qa_report["status"] = "pass"
    save_structured_file(deliverable_dir / "qa_report.json", qa_report)

    monkeypatch.setattr(
        "article_machine.playwright_ops.playwright_available",
        lambda: {"status": "blocked", "message": "npx is not available."},
    )

    report = submit_deliverable(deliverable_dir, action="dry-run")

    assert report["status"] == "blocked"
    assert "npx" in report["message"]
