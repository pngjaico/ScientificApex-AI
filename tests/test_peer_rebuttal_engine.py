from pathlib import Path
import json
import pytest

from article_machine.cli import main
from article_machine.projects import init_project
from article_machine.services.peer_rebuttal_engine import (
    parse_peer_review_letter,
    draft_rebuttal_response,
    generate_peer_rebuttal_package,
)


def test_parse_peer_review_letter():
    raw_letter = """
    Editor Comments:
    1. Please provide the full data dictionary and ensure compliance with STROBE guidelines.
    2. Also clarify the ethics approval number in the Methods.

    Reviewer 1:
    - The sample size in subgroup B appears underpowered.
    - The authors should explain the choice of random effects REML over fixed effects.

    Reviewer 2:
    1. The biomarker cut-off of 2.5 ng/mL needs ROC justification.
    """
    sections = parse_peer_review_letter(raw_letter)
    assert len(sections) == 3
    assert sections[0]["role"] == "Editor"
    assert len(sections[0]["items"]) == 2
    assert sections[1]["role"] == "Reviewer 1"
    assert len(sections[1]["items"]) == 2
    assert sections[2]["role"] == "Reviewer 2"
    assert len(sections[2]["items"]) == 1


def test_draft_rebuttal_response():
    drafts = draft_rebuttal_response(
        role="Reviewer 1",
        item_index=1,
        critique="The sample size in subgroup B appears underpowered.",
    )
    assert "en" in drafts
    assert "pt" in drafts
    # Check that English draft contains no em-dashes
    assert "\u2014" not in drafts["en"]
    assert "**Response:**" in drafts["en"]
    assert "AUTHOR TO COMPLETE" in drafts["en"]
    assert "we performed an additional sensitivity analysis" not in drafts["en"]
    assert "**Resposta:**" in drafts["pt"]
    assert "AUTOR PREENCHER" in drafts["pt"]


def test_generate_peer_rebuttal_package_and_cli(tmp_path: Path):
    project_dir = init_project(tmp_path, "Projeto Rebuttal", "systematic-review")

    review_file = project_dir / "raw_reviews.txt"
    review_file.write_text("""
    Reviewer 1:
    1. The inclusion criteria for pediatric cohorts should be stated explicitly.
    2. Please add a sensitivity analysis excluding high-risk-of-bias studies.
    """, encoding="utf-8")

    code = main([
        "publish",
        "rebuttal",
        str(project_dir),
        "--peer-review",
        str(review_file),
        "--journal",
        "Transplantation",
    ])
    assert code == 0

    rebuttal_dir = project_dir / "publicacoes" / "transplantation" / "08_resposta_pareceristas"
    assert rebuttal_dir.exists()

    en_letter = rebuttal_dir / "ingles" / "rebuttal_letter_to_reviewers.md"
    pt_letter = rebuttal_dir / "portugues" / "carta_resposta_pareceristas.md"
    manifest = rebuttal_dir / "rebuttal_manifest.json"

    assert en_letter.exists()
    assert pt_letter.exists()
    assert manifest.exists()

    with open(manifest, "r", encoding="utf-8") as f:
        meta = json.load(f)
    assert meta["contract"] == "PeerRebuttalManifestV1"
    assert meta["target_journal"] == "Transplantation"
    assert meta["total_comments_addressed"] == 2


def test_parse_handles_bom_header():
    sections = parse_peer_review_letter("\ufeffReviewer 1:\n1. Point A.\n")
    assert sections[0]["role"] == "Reviewer 1"
