"""Unit tests for the Collaborative Retrieval Portal Service (article_machine/services/retrieval_portal.py)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from article_machine.cli import main
from article_machine.services.retrieval_portal import (
    build_portal,
    generate_portal_html,
    load_project_studies,
    portal_status,
)


@pytest.fixture
def mock_project(tmp_path: Path) -> Path:
    proj_dir = tmp_path / "mock-meta-analysis-2027"
    proj_dir.mkdir(parents=True)
    
    # project.yaml
    (proj_dir / "project.yaml").write_text(
        "name: Mock Perfusion Trial NMA\ntarget_journal: Journal of Clinical Surgery\n",
        encoding="utf-8"
    )

    # screening status
    screening_dir = proj_dir / "screening"
    screening_dir.mkdir()
    sample_studies = [
        {
            "record_id": "STUDY-0001",
            "title": "Dual Hypothermic Oxygenated Perfusion in Liver Transplantation",
            "authors": ["Schlegel A", "Muller X"],
            "year": 2023,
            "journal": "Annals of Surgery",
            "doi": "10.1097/SLA.0000000000005720",
            "pmid": "36301646",
            "study_design_tier": "Tier-1_RCT",
            "downloaded": True
        },
        {
            "record_id": "STUDY-0002",
            "title": "Normothermic Machine Perfusion vs Cold Storage in Liver Transplantation",
            "authors": ["Nasralla D", "Coussios CC"],
            "year": 2018,
            "journal": "Nature",
            "doi": "10.1038/s41586-018-0047-9",
            "pmid": "29670285",
            "study_design_tier": "Tier-1_RCT",
            "downloaded": False
        }
    ]
    (screening_dir / "core_100_full_text_status.json").write_text(
        json.dumps(sample_studies, indent=2), encoding="utf-8"
    )

    # sources/full_texts
    ft_dir = proj_dir / "sources/full_texts"
    ft_dir.mkdir(parents=True)
    (ft_dir / "STUDY-0001_2023_Schlegel.pdf").write_bytes(b"%PDF-1.4 dummy content")

    return proj_dir


def test_load_project_studies(mock_project: Path):
    studies = load_project_studies(mock_project)
    assert len(studies) == 2
    assert studies[0]["record_id"] == "STUDY-0001"
    assert studies[1]["record_id"] == "STUDY-0002"


def test_generate_portal_html(mock_project: Path):
    html = generate_portal_html(mock_project)
    assert "<!DOCTYPE html>" in html
    assert "STUDY-0001" in html
    assert "STUDY-0002" in html
    assert "10.1097/SLA.0000000000005720" in html
    assert "pharosreader" in html
    assert "WhatsApp" in html
    assert "projectSelector" in html
    assert "tabBtnAuthors" in html
    assert "tabContentAuthors" in html
    assert "authorOrcid" in html
    assert "saveAuthorProfile" in html
    assert "exportCoauthorsCSV" in html
    assert "CRediT" in html


def test_build_portal(mock_project: Path):
    res = build_portal(mock_project, firebase_project="pharosreader")
    assert res["status"] == "pass"
    assert res["studies_count"] == 2
    
    portal_dir = mock_project / "portal_recuperacao"
    assert (portal_dir / "public/index.html").is_file()
    assert (portal_dir / "firebase.json").is_file()
    assert (portal_dir / "storage.rules").is_file()
    assert (portal_dir / ".firebaserc").is_file()
    assert "match /coauthors/" in (portal_dir / "storage.rules").read_text(encoding="utf-8")
    assert (portal_dir / "portal_manifest.json").is_file()


def test_portal_status(mock_project: Path):
    # Before build
    st = portal_status(mock_project)
    assert st["status"] == "pass"
    assert st["total_studies"] == 2
    assert st["completed"] == 1
    assert st["pending"] == 1
    assert st["coverage_percentage"] == 50.0

    # Build and check
    build_portal(mock_project)
    st2 = portal_status(mock_project)
    assert st2["portal_built"] is True


def test_cli_portal_status_and_build(mock_project: Path, capsys):
    # CLI portal status
    rc = main(["portal", "status", str(mock_project)])
    assert rc == 0
    captured = capsys.readouterr()
    assert "PortalStatusReport" in captured.out

    # CLI portal build
    rc_build = main(["portal", "build", str(mock_project)])
    assert rc_build == 0
    captured_build = capsys.readouterr()
    assert "BuildPortalResult" in captured_build.out
