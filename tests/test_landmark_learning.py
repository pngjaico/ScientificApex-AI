import json
from pathlib import Path

import pytest

from article_machine.cli import main
from article_machine.projects import init_project
from article_machine.services.landmark_learning import (
    ELITE_JOURNALS,
    dissect_landmark_paper,
    search_landmark_papers,
)


def test_search_landmark_papers():
    res = search_landmark_papers("intestinal ischemia reperfusion IFABP", limit=5)
    assert res["status"] == "planned"
    assert "intestinal ischemia reperfusion IFABP" in res["query"]
    assert len(res["target_elite_journals"]) > 0
    assert "Nature" in [j["name"] for j in ELITE_JOURNALS.values()]
    assert "The New England Journal of Medicine" in [j["name"] for j in ELITE_JOURNALS.values()]
    assert "Annals of Surgery" in [j["name"] for j in ELITE_JOURNALS.values()]


def test_dissect_landmark_paper_creates_dossier(tmp_path: Path):
    project_dir = init_project(tmp_path, "Projeto Estudo Landmark", "systematic-review")
    res = dissect_landmark_paper(
        project_dir=project_dir,
        title="Hypothermic Oxygenated Machine Perfusion in Liver Transplantation",
        journal="The New England Journal of Medicine",
        year=2021,
        doi="10.1056/NEJMoa2015603",
        authors="van Rijn et al.",
        primary_endpoint="Non-anastomotic biliary strictures at 6 months",
        study_design="Multicenter Double-Blind Randomized Controlled Trial",
        slug="van_rijn_nejm_2021",
    )
    assert res["status"] == "created"
    assert res["slug"] == "van_rijn_nejm_2021"

    dossier = Path(res["dossier_path"])
    assert dossier.is_file()

    content = dossier.read_text(encoding="utf-8")
    assert "The New England Journal of Medicine" in content
    assert "10.1056/NEJMoa2015603" in content
    assert "Poder Amostral" in content
    assert "Storyline Visual" in content
    assert "Calibração e Sobriedade dos Claims" in content

    # Manifest file
    manifest = project_dir / "context" / "landmark_learnings" / "manifest_van_rijn_nejm_2021.yaml"
    assert manifest.is_file()


def test_cli_landmark_commands(tmp_path: Path, capsys):
    project_dir = init_project(tmp_path, "Projeto CLI Landmark", "systematic-review")

    # 1. Search command
    code = main(["landmark", "search", "--query", "liver machine perfusion HOPE"])
    assert code == 0
    captured = capsys.readouterr()
    search_res = json.loads(captured.out)
    assert search_res["status"] == "planned"

    # 2. Dissect command
    code = main([
        "landmark",
        "dissect",
        str(project_dir),
        "--title",
        "Landmark Trial in Gut Barrier",
        "--journal",
        "Annals of Surgery",
        "--year",
        "2023",
        "--doi",
        "10.1097/SLA.0000000000005555",
        "--slug",
        "gut_barrier_annals",
    ])
    assert code == 0
    captured = capsys.readouterr()
    dissect_res = json.loads(captured.out)
    assert dissect_res["status"] == "created"
    assert dissect_res["slug"] == "gut_barrier_annals"
