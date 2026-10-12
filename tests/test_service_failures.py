import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from article_machine.services import machine
from article_machine.services.graph_query import query_operational_graph
from article_machine.services.plugins import audit_scientific_plugins, resolve_scientific_plugin
from article_machine.services.scientific_workflows import audit_language, plan_scientific_workflow
from article_machine.services.skill_registry import audit_skill_provenance, build_skill_update_plan, resolve_plugin_binding
from article_machine.projects import init_project


def test_machine_checks_record_failures_and_do_not_truncate_sensitive_file_inventory(tmp_path, monkeypatch):
    def completed(command, **kwargs):
        if command[1:3] == ["ls-files", "-z"]:
            output = ".env\0" + "a.py\0" * 5000
        elif command[1] == "status":
            output = " M module.py\n"
        else:
            output = "1.0\n"
        return SimpleNamespace(returncode=0, stdout=output, stderr="")
    monkeypatch.setattr(machine.subprocess, "run", completed)
    assert machine._tracked_sensitive(tmp_path)["tracked_sensitive_paths"] == [".env"]
    assert machine._git_status(tmp_path)["clean"] is False
    monkeypatch.setattr(machine.subprocess, "run", lambda *args, **kwargs: (_ for _ in ()).throw(OSError("absent")))
    assert machine._run(["missing-tool"], tmp_path)["status"] == "block"
    monkeypatch.setattr(machine.subprocess, "run", lambda *args, **kwargs: (_ for _ in ()).throw(subprocess.TimeoutExpired("cmd", 1)))
    assert machine._run(["timeout-tool"], tmp_path)["exit_code"] is None


def test_machine_doctor_and_release_keep_unverified_benchmark_blocked(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text("[project]\nname='fixture'\n")
    project = init_project(tmp_path, "Governance", "machine-governance")
    monkeypatch.setattr(machine, "_run", lambda *args, **kwargs: {"status": "pass", "stdout_tail": "", "exit_code": 0})
    monkeypatch.setattr(machine, "_tracked_sensitive", lambda root: {"status": "pass"})
    monkeypatch.setattr(machine, "audit_skill_provenance", lambda **kwargs: {"status": "pass"})
    monkeypatch.setattr(machine, "query_operational_graph", lambda *args, **kwargs: {"status": "ok"})
    report = machine.machine_doctor(tmp_path, project)
    assert report["checks"]["project_preflight"]["status"] == "blocked"
    release = machine.release_audit(project)
    assert release["gate_eligible"] is False
    assert "benchmark" in release["issues"]
    assert release["remote_ci_verified"] is False


def test_plugin_binding_failures_are_explicit(tmp_path, monkeypatch):
    (tmp_path / ".machine").mkdir()
    binding_file = tmp_path / ".machine" / "plugin_bindings.json"
    binding_file.write_text(json.dumps({"bindings": {"life-science-research": []}}))
    with pytest.raises(ValueError, match="exactly one"):
        resolve_scientific_plugin("life-science-research", tmp_path)
    binding_file.write_text(json.dumps({"bindings": {"life-science-research": [{"root": str(tmp_path), "version": "1"}]}}))
    with pytest.raises(ValueError, match="skills directory"):
        resolve_scientific_plugin("life-science-research", tmp_path)
    monkeypatch.setenv("CODEX_HOME", str(tmp_path))
    audit = audit_scientific_plugins(tmp_path)
    assert audit["status"] == "inspected"
    assert all(not entry["human_data_upload_authorized"] for entry in audit["plugins"])
    binding_file.write_text(json.dumps({"bindings": {"x": ["invalid"]}}))
    with pytest.raises(ValueError, match="object"):
        resolve_plugin_binding("x", tmp_path)
    with pytest.raises(ValueError, match="exactly one"):
        resolve_plugin_binding("absent", tmp_path)


def test_language_workflow_missing_unsupported_and_translation_signs(tmp_path):
    assert plan_scientific_workflow(tmp_path, "question", "en")["status"] == "block"
    project = init_project(tmp_path, "Language", "systematic-review")
    assert plan_scientific_workflow(project, " ", "en")["status"] == "block"
    with pytest.raises(ValueError, match="language"):
        plan_scientific_workflow(project, "question", "es")
    with pytest.raises(ValueError, match="language"):
        audit_language(project, "es")
    assert audit_language(project, "en", "drafts/absent.md")["status"] == "block"
    assert audit_language(project, "en", reference="drafts/absent.md")["status"] == "block"
    (project / "drafts" / "en.md").write_text("effect -0.5 p<0.05 {{claim:a}}")
    (project / "drafts" / "pt.md").write_text("efeito 0,5 p>0,05 {{claim:a}}")
    report = audit_language(project, "pt-BR", "drafts/pt.md", "drafts/en.md")
    assert {"translation changed numeric_values", "translation changed inequalities"} <= set(report["issues"])


def test_graph_negative_query_returns_no_hub_noise(tmp_path):
    graph = tmp_path / "graph.json"
    graph.write_text(json.dumps({"nodes": [{"id": "hub", "label": "gates", "degree": 100, "source_file": "article_machine/cli.py"}]}))
    assert query_operational_graph("unrelatedword", graph_path=graph)["results"] == []


def test_registry_missing_or_corrupted_entries_block(tmp_path):
    skills = tmp_path / "skills"
    (skills / "one").mkdir(parents=True)
    (skills / "one" / "SKILL.md").write_text("---\nname: one\ndescription: One\n---")
    assert audit_skill_provenance(root=tmp_path, strict=True)["status"] == "block"
    (skills / "registry.json").write_text(json.dumps({"skills": {"one": {}}}))
    assert audit_skill_provenance(root=tmp_path, strict=True)["status"] == "block"
    assert build_skill_update_plan(tmp_path)["status"] == "block"
