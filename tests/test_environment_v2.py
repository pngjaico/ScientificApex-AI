from pathlib import Path

from test_contracts_v2 import _v2_project

from article_machine.services.environment import check_environment, preflight_environment, prepare_environment


def test_check_never_prepares_and_preflight_requires_all_contracts(tmp_path: Path) -> None:
    project = _v2_project(tmp_path)
    check = check_environment(project, "python")
    assert check["contract"] == "EnvironmentCheckV2"
    prepared = prepare_environment(project, "python")
    assert prepared["executed"] is False
    report = preflight_environment(project)
    assert report["status"] == "passed"
    assert "browser" in report["checks"]


def test_preflight_blocks_missing_contract_version(tmp_path: Path) -> None:
    project = _v2_project(tmp_path)
    (project / "standards.yaml").write_text("lane: evidence-writing\n", encoding="utf-8")
    report = preflight_environment(project)
    assert report["status"] == "blocked"
    assert report["checks"]["standards.yaml"]["status"] == "blocked"
