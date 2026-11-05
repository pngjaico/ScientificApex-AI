import csv
import json
from pathlib import Path

import pytest

from article_machine.cli import main
from article_machine.projects import init_project
from article_machine.services.bench_protocols import (
    SUPPORTED_ASSAYS,
    generate_bench_template,
    validate_sample_manifest,
)


def test_init_project_wet_lab_creates_experiment_structure(tmp_path: Path):
    project_dir = init_project(tmp_path, "Experimento Bancada IFABP", "wet-lab-experiment")
    assert project_dir.is_dir()
    assert (project_dir / "experiments" / "protocols").is_dir()
    assert (project_dir / "experiments" / "data" / "raw").is_dir()
    assert (project_dir / "experiments" / "samples" / "sample_manifest.csv").is_file()
    assert (project_dir / "experiments" / "checklists" / "pre_execution_gate.yaml").is_file()


@pytest.mark.parametrize("assay_key", list(SUPPORTED_ASSAYS.keys()))
def test_generate_bench_template_for_all_supported_assays(tmp_path: Path, assay_key: str):
    project_dir = init_project(tmp_path, f"Teste {assay_key}", "wet-lab-experiment")
    res = generate_bench_template(project_dir, assay_key)
    assert res["status"] == "created"
    assert res["assay_key"] == assay_key
    assert len(res["created_files"]) >= 1

    for f_rel in res["created_files"]:
        f_abs = project_dir / f_rel
        assert f_abs.is_file()
        content = f_abs.read_text(encoding="utf-8")
        assert len(content) > 20


def test_elisa_generates_plate_map_and_r_script(tmp_path: Path):
    project_dir = init_project(tmp_path, "Projeto ELISA", "wet-lab-experiment")
    res = generate_bench_template(project_dir, "elisa", "IFABP_ELISA_Sanduiche")
    assert any("plate_map" in f for f in res["created_files"])
    assert any("fit_elisa_4pl" in f for f in res["created_files"])


def test_chiu_score_generates_grading_sheet(tmp_path: Path):
    project_dir = init_project(tmp_path, "Projeto Chiu", "wet-lab-experiment")
    res = generate_bench_template(project_dir, "chiu")
    assert any("chiu" in f for f in res["created_files"])
    assert any("leitura_histologica" in f for f in res["created_files"])


def test_validate_sample_manifest(tmp_path: Path):
    manifest_file = tmp_path / "sample_manifest.csv"
    # Create valid manifest
    rows = [
        ["sample_id", "subject_id", "group", "tissue", "freeze_thaw_cycles"],
        ["S001", "RAT01", "HOPE", "ileum", "1"],
        ["S002", "RAT02", "SCS", "ileum", "1"],
    ]
    with manifest_file.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

    report = validate_sample_manifest(manifest_file)
    assert report["status"] == "pass"
    assert report["total_samples"] == 2

    # Add duplicate and high freeze-thaw
    rows.append(["S001", "RAT03", "HOPE", "ileum", "4"])
    with manifest_file.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

    bad_report = validate_sample_manifest(manifest_file)
    assert bad_report["status"] == "warning"
    assert any("duplicate sample_id" in iss for iss in bad_report["issues"])
    assert any("freeze-thaw" in iss for iss in bad_report["issues"])


def test_cli_bench_commands(tmp_path: Path, capsys):
    project_dir = init_project(tmp_path, "Projeto CLI Bench", "wet-lab-experiment")
    code = main(["bench", "template", str(project_dir), "--assay", "rt-qpcr"])
    assert code == 0
    captured = capsys.readouterr()
    res = json.loads(captured.out)
    assert res["status"] == "created"
    assert res["assay_key"] == "rt-qpcr"
