from pathlib import Path

from article_machine.congress_profiles import save_congress_profile, use_congress_profile
from article_machine.deliverable_contracts import validate_deliverable_contract
from article_machine.deliverables import (
    build_deliverable,
    export_deliverable,
    import_conference_requirements,
    plan_deliverable,
    qa_deliverable,
)
from article_machine.projects import init_project
from article_machine.serialization import load_structured_file


def _seed_claim(project_dir: Path) -> None:
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"Treatment improved remission versus control.",'
            '"source_path":"sources/converted/study-001.md","source_excerpt":"Remission improved.",'
            '"reference_key":"smith2024","status":"supported"}\n'
        ),
        encoding="utf-8",
    )
    (project_dir / "drafts" / "references.bib").write_text(
        "@article{smith2024,\n  title={Study},\n  year={2024}\n}\n",
        encoding="utf-8",
    )


def _prepare_exportable_deck(tmp_path: Path, monkeypatch) -> Path:
    project_dir = init_project(tmp_path, "Versioned Deck", "systematic-review")
    _seed_claim(project_dir)
    import_conference_requirements(
        project_dir,
        source=(
            "# Congress V2\n\nOral presentation. Duration: 5 minutes. Maximum 5 slides. "
            "Abstract 250 words. Accepted files: PDF and PPTX. Portal: https://example.org/submit. "
            "Deadline: 2026-08-01."
        ),
        kind="deck",
        slug="versioned-deck",
        authors=["A. Researcher", "B. Mentor"],
        affiliations=["Doutorado Lab"],
        qr_url="https://example.org/project",
    )
    deliverable_dir = project_dir / "deliverables" / "versioned-deck"
    plan_deliverable(deliverable_dir)
    build_deliverable(deliverable_dir)

    monkeypatch.setattr(
        "article_machine.playwright_ops.playwright_available",
        lambda: {"status": "pass", "npx_path": "C:/Program Files/nodejs/npx.cmd"},
    )
    monkeypatch.setattr(
        "article_machine.playwright_ops.qa_html",
        lambda html_path, output_dir, profile: {
            "status": "pass",
            "overflow_elements": [],
            "screenshot": str(Path(output_dir) / "layout-qa.png"),
            "section_screenshots": [str(Path(output_dir) / "sections" / "slide-001.png")],
            "contrast": {"status": "pass", "minimum_ratio": 7.1},
        },
    )
    def fake_pdf(html_path: Path, output_path: Path, profile: str) -> dict:
        output_path.write_bytes(b"%PDF-1.4\n")
        return {"status": "pass", "path": str(output_path)}

    def fake_thumbnail(html_path: Path, output_path: Path, profile: str) -> dict:
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

    monkeypatch.setattr("article_machine.playwright_ops.export_html_pdf", fake_pdf)
    monkeypatch.setattr("article_machine.playwright_ops.capture_thumbnail", fake_thumbnail)
    monkeypatch.setattr("article_machine.pptx_bridge.export_editable_pptx", fake_pptx)
    qa_report = qa_deliverable(deliverable_dir)
    assert qa_report["status"] == "pass"
    return deliverable_dir


def test_import_conference_v2_extracts_confidence_deadline_filetypes_and_branding(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Rich Congress", "systematic-review")

    import_conference_requirements(
        project_dir,
        source=(
            "# International Congress\n\nPoster A0 landscape. Abstract 250 words. "
            "Accepted files: PDF, PPTX. Deadline: 2026-07-15. Portal: https://submit.example.org. Logo required."
        ),
        kind="poster",
        slug="rich-poster",
        authors=["Ana Silva", "Bruno Costa"],
        affiliations=["University Lab"],
        qr_url="https://osf.io/example",
        logos=["assets/logo.png"],
    )

    deliverable_dir = project_dir / "deliverables" / "rich-poster"
    conference = load_structured_file(deliverable_dir / "conference.yaml")
    theme = load_structured_file(deliverable_dir / "theme.yaml")

    assert conference["profile"] == "A0 landscape"
    assert conference["limits"]["max_words_abstract"] == 250
    assert conference["submission"]["portal_url"] == "https://submit.example.org"
    assert conference["requirements_confidence"]["status"] == "pass"
    assert {"pdf", "pptx"}.issubset(set(conference["accepted_file_types"]))
    assert conference["deadline"] == "2026-07-15"
    assert conference["authors"] == ["Ana Silva", "Bruno Costa"]
    assert conference["qr"]["url"] == "https://osf.io/example"
    assert theme["branding"]["affiliations"] == ["University Lab"]
    assert theme["palette"]["accent_2"] == "#9b3f00"


def test_import_conference_uses_digital_poster_profile_when_rules_are_electronic(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Digital Poster", "systematic-review")

    import_conference_requirements(
        project_dir,
        source=(
            "# GastroSP\n\nAccepted poster file: one-page electronic poster in PowerPoint saved as PDF. "
            "No print size specified."
        ),
        kind="poster",
        slug="digital-poster",
    )

    conference = load_structured_file(project_dir / "deliverables" / "digital-poster" / "conference.yaml")

    assert conference["profile"] == "digital 16:9 landscape"
    assert conference["dimensions"]["format"] == "16:9-digital"


def test_plan_deliverable_uses_audit_claim_map_fallback_for_legacy_projects(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Legacy Audit Poster", "systematic-review")
    audit_dir = project_dir / "audit_top1" / "analysis_audit"
    audit_dir.mkdir(parents=True, exist_ok=True)
    (audit_dir / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-audit","claim":"Urinary I-FABP ranked first in the exploratory network.",'
            '"support":"analysis/final_validated_pscore_ranking.csv",'
            '"status":"allowed_with_exploratory_qualifier"}\n'
        ),
        encoding="utf-8",
    )
    import_conference_requirements(
        project_dir,
        source="# Legacy Congress\n\nPoster.",
        kind="poster",
        slug="legacy-poster",
    )

    report = plan_deliverable(project_dir / "deliverables" / "legacy-poster")

    assert report["status"] == "planned"
    assert report["approved_claim_ids"] == ["claim-audit"]


def test_validate_deliverable_contract_blocks_ambiguous_strict_export(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Ambiguous Congress", "systematic-review")
    import_conference_requirements(
        project_dir,
        source="Please prepare a short presentation.",
        kind="deck",
        slug="ambiguous-deck",
    )

    report = validate_deliverable_contract(project_dir / "deliverables" / "ambiguous-deck", strict=True)

    assert report["status"] == "block"
    assert any("requirements confidence" in issue.lower() for issue in report["issues"])


def test_plan_deliverable_accepts_powershell_utf8_bom_claim_map(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "BOM Deck", "systematic-review")
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"Treatment improved remission versus control.",'
            '"source_path":"sources/converted/study-001.md","source_excerpt":"Remission improved.",'
            '"reference_key":"smith2024","status":"supported"}\n'
        ),
        encoding="utf-8-sig",
    )
    (project_dir / "drafts" / "references.bib").write_text(
        "@article{smith2024,\n  title={Study},\n  year={2024}\n}\n",
        encoding="utf-8",
    )
    import_conference_requirements(
        project_dir,
        source="# Congress\n\nOral presentation. Duration: 5 minutes. Maximum 5 slides.",
        kind="deck",
        slug="bom-deck",
    )

    report = plan_deliverable(project_dir / "deliverables" / "bom-deck")

    assert report["status"] == "planned"
    assert report["approved_claim_ids"] == ["claim-001"]


def test_export_is_versioned_and_manifest_does_not_duplicate_latest_aliases(tmp_path: Path, monkeypatch) -> None:
    deliverable_dir = _prepare_exportable_deck(tmp_path, monkeypatch)

    first = export_deliverable(deliverable_dir, strict=True)
    second = export_deliverable(deliverable_dir, strict=True)
    manifest = load_structured_file(deliverable_dir / "manifest.json")
    paths = [artifact["path"] for artifact in manifest["artifacts"] if artifact["role"].endswith("export")]

    assert first["export_version"] == "export-v001"
    assert second["export_version"] == "export-v002"
    assert (deliverable_dir / "exports" / "export-v001" / "versioned-deck.html").exists()
    assert (deliverable_dir / "exports" / "export-v002" / "versioned-deck.html").exists()
    assert (deliverable_dir / "exports" / "versioned-deck.html").exists()
    assert all("export-v" in path for path in paths)
    assert len(paths) == len(set(paths))


def test_save_and_use_congress_profile_recreates_requirements(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Profile Source", "systematic-review")
    import_conference_requirements(
        project_dir,
        source="# Saved Congress\n\nOral presentation. Duration: 10 minutes. Maximum 9 slides. Abstract 300 words.",
        kind="deck",
        slug="source-deck",
    )
    source_dir = project_dir / "deliverables" / "source-deck"

    saved = save_congress_profile(source_dir, "saved-congress")
    recreated = use_congress_profile(project_dir, "saved-congress", "new-deck")
    conference = load_structured_file(project_dir / "deliverables" / "new-deck" / "conference.yaml")

    assert saved["status"] == "saved"
    assert recreated["status"] == "created"
    assert conference["profile"] == "10-min"
    assert conference["limits"]["max_slides"] == 9
