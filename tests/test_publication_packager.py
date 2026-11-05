import json
from pathlib import Path

import pytest

from article_machine.cli import main
from article_machine.projects import init_project
from article_machine.services.publication_packager import (
    prepare_publication_package,
    validate_anti_ai_style,
    CANONICAL_AREAS,
    DISCLOSURE_EN,
    DISCLOSURE_PT,
)


def test_prepare_publication_package_creates_9_folders(tmp_path: Path):
    project_dir = init_project(tmp_path, "Projeto Teste Publicacao", "systematic-review")
    res = prepare_publication_package(
        project_dir=project_dir,
        target_journal="Transplantation",
        package_slug="pacote_ouro",
        version="v01",
    )
    assert res["status"] == "created"
    assert res["target_journal"] == "Transplantation"
    assert res["package_slug"] == "pacote_ouro"

    pub_root = Path(res["publication_root"])
    assert pub_root.is_dir()

    # Verify all 9 canonical folders exist
    for folder_name, is_bilingual in CANONICAL_AREAS:
        area = pub_root / folder_name
        assert area.is_dir(), f"Missing area folder: {folder_name}"
        if is_bilingual:
            assert (area / "portugues").is_dir()
            assert (area / "ingles").is_dir()

    # Verify manuscript starter files
    ms_en = list((pub_root / "01_manuscrito_principal" / "ingles").glob("*.md"))
    ms_pt = list((pub_root / "01_manuscrito_principal" / "portugues").glob("*.md"))
    assert len(ms_en) == 1
    assert len(ms_pt) == 1

    content_en = ms_en[0].read_text(encoding="utf-8")
    content_pt = ms_pt[0].read_text(encoding="utf-8")

    # Verify AI disclosure is present in both EN and PT
    assert "Claude Opus 5.5" in content_en
    assert "Transplantation" in content_en
    assert "Claude Opus 5.5" in content_pt
    assert "Transplantation" in content_pt

    # Verify anti-AI check passes on clean starter
    issues = validate_anti_ai_style(content_en)
    assert issues == []

    # Verify manifest exists
    assert (pub_root / "pacote_manifest.yaml").is_file()


def test_validate_anti_ai_style_detects_em_dashes():
    bad_text = "This method — although widely used — lacks robust calibration."
    issues = validate_anti_ai_style(bad_text)
    assert len(issues) == 1
    assert "conversational em-dash" in issues[0]


def test_cli_publish_prepare(tmp_path: Path, capsys):
    project_dir = init_project(tmp_path, "Projeto CLI Publish", "systematic-review")
    code = main([
        "publish",
        "prepare",
        str(project_dir),
        "--journal",
        "Annals of Surgery",
        "--slug",
        "cirurgia_nma",
    ])
    assert code == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["status"] == "created"
    assert payload["target_journal"] == "Annals of Surgery"
