from __future__ import annotations

from datetime import date, timedelta
import json

from article_machine.journals import route_journals, verify_journal_presets
from article_machine.projects import init_project


def _journal(**overrides: object) -> dict:
    journal = {
        "journal_id": "example-journal",
        "title": "Example Journal",
        "issn": "1234-5678",
        "publisher": "Example Publisher",
        "society": "",
        "domains": ["general-surgery"],
        "tier": "A",
        "indexing": ["PubMed"],
        "metrics": {"impact_factor": 2.0, "impact_factor_year": date.today().year, "source": "official"},
        "article_types": ["original research"],
        "scope_fit": "Surgical research",
        "format_rules": {},
        "open_access": {},
        "apc": {},
        "turnaround": {},
        "source_urls": ["https://example.invalid/authors"],
        "last_verified_at": date.today().isoformat(),
        "verification_status": "verified",
        "red_flags": [],
    }
    journal.update(overrides)
    return journal


def _write_presets(directory, *journals: dict) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    # The public preset loader intentionally discovers YAML files only; JSON
    # remains valid YAML here and keeps malformed-type fixtures compact.
    (directory / "edge-cases.yaml").write_text(
        json.dumps({"journals": journals}), encoding="utf-8"
    )


def test_stale_verified_preset_blocks_journal_routing_before_ranking(tmp_path) -> None:
    preset_dir = tmp_path / "presets"
    stale_date = (date.today() - timedelta(days=366)).isoformat()
    _write_presets(preset_dir, _journal(last_verified_at=stale_date))
    project = init_project(tmp_path, "Stale Journal Route", "systematic-review")

    verification = verify_journal_presets(preset_dir)
    route = route_journals(project, presets_dir=preset_dir)

    assert verification["status"] == "block"
    assert any("metrics are stale" in issue for issue in verification["issues"])
    assert route["status"] == "blocked"
    assert route["ranked_journals"] == []
    assert any("metrics are stale" in issue for issue in route["issues"])


def test_malformed_metrics_object_blocks_route_without_evidence_lock_work(tmp_path) -> None:
    preset_dir = tmp_path / "presets"
    _write_presets(preset_dir, _journal(metrics=["not", "an", "object"]))
    project = init_project(tmp_path, "Malformed Journal Route", "systematic-review")

    report = route_journals(project, presets_dir=preset_dir)

    assert report["status"] == "blocked"
    assert report["ranked_journals"] == []
    assert any("metrics must be an object" in issue for issue in report["issues"])


def test_empty_or_malformed_preset_directory_cannot_pass_verification(tmp_path) -> None:
    preset_dir = tmp_path / "bad-presets"
    preset_dir.mkdir()
    assert verify_journal_presets(preset_dir)["status"] == "block"
    preset = preset_dir / "one.yaml"
    for invalid in ("journals: [unterminated", "journals: wrong-type", "{}"):
        preset.write_text(invalid)
        assert verify_journal_presets(preset_dir)["status"] == "block"
    preset.write_text(json.dumps(_journal()))
    assert verify_journal_presets(preset_dir)["journal_count"] == 1
