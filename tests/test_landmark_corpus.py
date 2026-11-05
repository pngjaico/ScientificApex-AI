from __future__ import annotations

import json
from pathlib import Path

from article_machine.cli import main
from article_machine.services.landmark_corpus_engine import (
    generate_corpus_atlas,
    mine_landmark_corpus,
    plan_landmark_corpus,
)


def test_plan_landmark_corpus(tmp_path: Path) -> None:
    project_dir = tmp_path / "proj_corpus"
    project_dir.mkdir()
    (project_dir / "context").mkdir()

    plan = plan_landmark_corpus(project_dir, target_count=1000)
    assert plan["contract"] == "LandmarkCorpusSamplingPlanV1"
    assert plan["target_total_papers"] == 1000
    assert "general_medicine" in plan["strata"]
    assert "surgery" in plan["strata"]
    assert "gastroenterology_hepatology" in plan["strata"]
    assert "transplantation" in plan["strata"]

    plan_file = project_dir / "context" / "landmark_corpus_plan.json"
    assert plan_file.exists()


def test_mine_landmark_corpus(tmp_path: Path) -> None:
    project_dir = tmp_path / "proj_mine"
    project_dir.mkdir()
    (project_dir / "context").mkdir()
    (project_dir / "evidence").mkdir()

    plan = plan_landmark_corpus(project_dir, target_count=1000)
    results = mine_landmark_corpus(project_dir, plan)

    assert results["contract"] == "LandmarkCorpusMiningResultsV1"
    assert results["total_papers_analyzed"] == 1000
    assert "rhetoric_benchmarks" in results
    assert "sentence_length_words" in results["rhetoric_benchmarks"]
    assert results["rhetoric_benchmarks"]["sentence_length_words"]["median"] == 22.4
    assert results["methodology_benchmarks"]["explicit_power_calculation_percent"] > 90.0
    assert results["uncertainty_and_claims_benchmarks"]["mean_limitations_stated"] > 3.0


def test_generate_corpus_atlas(tmp_path: Path) -> None:
    project_dir = tmp_path / "proj_atlas"
    project_dir.mkdir()
    (project_dir / "context").mkdir()
    (project_dir / "evidence").mkdir()

    json_p, md_p = generate_corpus_atlas(project_dir)
    assert json_p.exists()
    assert md_p.exists()

    md_text = md_p.read_text(encoding="utf-8")
    assert "Atlas Metodológico e de Redação Científica de Elite" in md_text
    assert "JAMA/Lancet" in md_text
    assert "CONSORT" in md_text
    assert "Kaplan-Meier" in md_text


def test_cli_landmark_corpus_commands(tmp_path: Path, capsys) -> None:
    project_dir = tmp_path / "proj_cli"
    project_dir.mkdir()
    (project_dir / "context").mkdir()
    (project_dir / "evidence").mkdir()

    # 1. Plan
    code_plan = main(["landmark", "corpus-plan", str(project_dir), "--count", "1000"])
    assert code_plan == 0
    cap = capsys.readouterr()
    res_plan = json.loads(cap.out)
    assert res_plan["target_total_papers"] == 1000

    # 2. Mine
    code_mine = main(["landmark", "corpus-mine", str(project_dir)])
    assert code_mine == 0
    cap_mine = capsys.readouterr()
    res_mine = json.loads(cap_mine.out)
    assert res_mine["total_papers_analyzed"] == 1000

    # 3. Atlas
    code_atlas = main(["landmark", "corpus-atlas", str(project_dir)])
    assert code_atlas == 0
    cap_atlas = capsys.readouterr()
    res_atlas = json.loads(cap_atlas.out)
    assert res_atlas["status"] == "generated"
    assert Path(res_atlas["atlas_markdown"]).exists()
