"""Tests for Workspace Hygiene Governor, Anti-Pollution Shield, and Real-Flow Skill Bindings."""

from __future__ import annotations

from pathlib import Path

from article_machine.agent_skills import route_workspace_skills
from article_machine.projects import init_project
from article_machine.services.workspace_hygiene import (
    audit_project_hygiene,
    audit_workspace_hygiene,
    organize_project_strays,
    resolve_real_flow_bindings,
    write_active_mode_guide,
)


def test_real_flow_bindings_inject_mandatory_skills_and_commands(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Hygiene SR Test", "systematic-review")
    guide = write_active_mode_guide(project, mode="analysis")
    assert guide["contract"] == "RealFlowSkillBindingsV1"
    skill_names = {s["skill"] for s in guide["mandatory_skills"]}
    assert "meta-analise-medica" in skill_names
    assert "statistical-analysis" in skill_names
    assert "scientific-visualization" in skill_names
    assert (project / guide["guide_path"]).is_file()

    ml_proj = init_project(tmp_path, "Hygiene ML Test", "prediction-model")
    ml_bind = resolve_real_flow_bindings(ml_proj, mode="analysis")
    ml_skills = {s["skill"] for s in ml_bind["mandatory_skills"]}
    assert "metodos-ml-clinico" in ml_skills
    assert "scikit-learn" in ml_skills


def test_project_hygiene_detects_strays_and_organizes_with_manifest(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Dirty Project", "network-meta-analysis")
    # Drop stray files in the root of the project
    (project / "loose_script.R").write_text("# stray R script\n", encoding="utf-8")
    (project / "loose_plot.png").write_bytes(b"PNGDATA")
    (project / "embase_dump.ris").write_text("TY  - JOUR\nER  - \n", encoding="utf-8")

    initial_check = audit_project_hygiene(project)
    assert initial_check["clean"] is False
    assert "loose_script.R" in initial_check["stray_files"]

    ws_check = audit_workspace_hygiene(tmp_path)
    assert ws_check["status"] == "blocked"
    assert "dirty-project" in ws_check["dirty_project_roots"]

    org = organize_project_strays(project, apply=True)
    assert org["status"] == "pass"
    assert org["moves_count"] == 3
    assert (project / org["manifest_path"]).is_file()
    assert (project / "analysis" / "legacy_root_organized" / "loose_script.R").is_file()
    assert (project / "figures" / "legacy_root_organized" / "loose_plot.png").is_file()
    assert (project / "sources" / "legacy_root_organized" / "embase_dump.ris").is_file()

    after_check = audit_project_hygiene(project)
    assert after_check["clean"] is True


def test_newly_routed_skills_are_reachable() -> None:
    for query, expected_skill in [
        ("ggplot2 patchwork calibration plot scientific visualization", "scientific-visualization"),
        ("scikit-learn randomforestclassifier calibratedclassifiercv", "scikit-learn"),
        ("pytorch-lightning lightningmodule deep learning trainer", "pytorch-lightning"),
        ("confounding dag collider bias immortal time bias", "scientific-critical-thinking"),
        ("author instructions journal formatting rules venue-templates", "venue-templates"),
    ]:
        routed = route_workspace_skills(query)
        matched = {item["skill"] for item in routed["selected_skills"]}
        assert expected_skill in matched
