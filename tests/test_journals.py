from pathlib import Path

from article_machine.cli import main
from article_machine.journals import (
    catalog_journals,
    route_journals,
    validate_journal_preset,
    verify_journal_presets,
    write_journal_report,
)
from article_machine.projects import init_project


def _seed_supported_manuscript(project_dir: Path) -> None:
    (project_dir / "drafts" / "manuscript.md").write_text(
        "# Manuscript\n\nAcute intestinal ischemia biomarkers can be compared by network meta-analysis {{claim:claim-supported}}.\n",
        encoding="utf-8",
    )
    (project_dir / "sources" / "converted" / "study-001.md").write_text(
        "Biomarker comparison in acute intestinal ischemia.\n",
        encoding="utf-8",
    )
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-supported","statement":"Biomarkers can be compared in acute intestinal ischemia.",'
            '"source_path":"sources/converted/study-001.md","source_excerpt":"Biomarker comparison in acute intestinal ischemia.",'
            '"reference_key":"smith2024","status":"supported"}\n'
        ),
        encoding="utf-8",
    )
    (project_dir / "drafts" / "references.bib").write_text(
        "@article{smith2024,\n  title={Study 1},\n  year={2024}\n}\n",
        encoding="utf-8",
    )


def test_journal_presets_validate_and_catalog_domains() -> None:
    report = verify_journal_presets()
    assert report["status"] == "pass"
    assert report["journal_count"] >= 30

    catalog = catalog_journals(domain="gastroenterology", tier="A")
    titles = {journal["title"] for journal in catalog["journals"]}
    assert "Gastroenterology" in titles
    assert "Gut" in titles


def test_verified_preset_requires_sources_and_fresh_date() -> None:
    broken = {
        "journal_id": "broken",
        "title": "Broken",
        "issn": "0000-0000",
        "publisher": "Publisher",
        "society": "",
        "domains": ["general-surgery"],
        "tier": "A",
        "indexing": ["PubMed"],
        "metrics": {"impact_factor": 1.0, "impact_factor_year": 2024, "source": ""},
        "article_types": ["original research"],
        "scope_fit": "test",
        "format_rules": {},
        "open_access": {},
        "apc": {},
        "turnaround": {},
        "source_urls": [],
        "last_verified_at": "",
        "verification_status": "verified",
        "red_flags": [],
    }

    issues = validate_journal_preset(broken)
    assert any("verified presets require source_urls" in issue for issue in issues)
    assert any("impact_factor requires metrics.source" in issue for issue in issues)


def test_red_flagged_journals_are_detected_without_blocking_schema(tmp_path: Path) -> None:
    preset_dir = tmp_path / "presets"
    preset_dir.mkdir()
    (preset_dir / "flagged.yaml").write_text(
        """
schema_version: 1
journals:
- journal_id: suspicious-journal
  title: Suspicious Journal
  issn: 1234-5678
  publisher: Unknown
  society: ''
  domains: [general-surgery]
  tier: C
  indexing: [needs-verification]
  metrics:
    impact_factor: null
    impact_factor_year: null
    source: ''
  article_types: [original research]
  scope_fit: broad
  format_rules: {}
  open_access: {}
  apc: {}
  turnaround: {}
  source_urls: [https://example.invalid]
  last_verified_at: '2026-04-26'
  verification_status: unverified
  red_flags: [publisher-not-verified, indexing-claim-needs-audit]
""",
        encoding="utf-8",
    )

    report = verify_journal_presets(preset_dir)
    assert report["status"] == "pass"
    assert report["red_flagged_journals"] == ["suspicious-journal"]


def test_route_blocks_recommendation_without_evidence_lock(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Weak Journal Route", "network-meta-analysis")

    report = route_journals(project_dir, domain="gastroenterology", limit=3)

    assert report["status"] == "blocked"
    assert report["evidence_lock_status"] == "block"
    assert report["ranked_journals"]
    assert report["message"] == "Journal recommendation blocked until Evidence Lock passes."


def test_route_is_deterministic_and_builds_fallback_ladder(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Gut Biomarker NMA", "network-meta-analysis")
    _seed_supported_manuscript(project_dir)

    first = route_journals(project_dir, domain="gastroenterology", limit=5)
    second = route_journals(project_dir, domain="gastroenterology", limit=5)

    assert first["status"] == "routed"
    assert [item["journal_id"] for item in first["ranked_journals"]] == [
        item["journal_id"] for item in second["ranked_journals"]
    ]
    assert set(first["fallback_ladder"]) == {"A", "B", "C"}
    assert first["ranked_journals"][0]["score"] <= 100
    assert first["ranked_journals"][0]["red_team_notes"]


def test_journal_report_writes_markdown_and_json(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Journal Report", "network-meta-analysis")
    _seed_supported_manuscript(project_dir)

    report = write_journal_report(project_dir, domain="gastroenterology")

    assert report["status"] == "routed"
    assert (project_dir / "analysis" / "journal_strategy_report.md").exists()
    assert (project_dir / "analysis" / "journal_strategy_report.json").exists()


def test_cli_journal_commands(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "CLI Journal", "network-meta-analysis")
    _seed_supported_manuscript(project_dir)

    assert main(["journal", "catalog", "--domain", "gastroenterology"]) == 0
    assert main(["journal", "verify"]) == 0
    assert main(["journal", "route", str(project_dir), "--domain", "gastroenterology", "--limit", "2"]) == 0
    assert main(["journal", "report", str(project_dir), "--domain", "gastroenterology"]) == 0
