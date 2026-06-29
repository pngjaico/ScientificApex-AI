from pathlib import Path

from article_machine.discovery import build_discovery_plan
from article_machine.projects import init_project


def test_build_discovery_plan_materializes_profile_for_drug_discovery(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Hit Discovery", "drug-discovery")

    report = build_discovery_plan(project_dir)

    assert report["project_type"] == "drug-discovery"
    assert report["lane"] == "computational-discovery"
    assert "rdkit" in report["skills"]
    assert "diffdock" in report["skills"]
    assert "hypothesis-generating" in report["policy_labels"]
    assert (project_dir / report["output_path"]).is_file()
