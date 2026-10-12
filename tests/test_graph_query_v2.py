from __future__ import annotations

import json
from pathlib import Path

import pytest

from article_machine.services.graph_query import query_operational_graph


def _graph(path: Path) -> Path:
    payload = {
        "nodes": [
            {"id": "skill", "label": "Skill routing registry", "source_file": "skills/registry.json", "community": 3, "degree": 4},
            {"id": "policy", "label": "Control plane policy", "source_file": ".codex/config.toml", "community": 1, "degree": 10},
            {"id": "project", "label": "Governance project protocol", "source_file": "projects/article-machine-governance-2026/protocol.yaml", "community": 2, "degree": 2},
            {"id": "raw", "label": "Patient raw dump", "source_file": "projects/article-machine-governance-2026/sources/patient.csv", "community": 2, "degree": 20},
        ]
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_scoped_graph_query_reranks_and_excludes_sensitive_nodes(tmp_path: Path) -> None:
    graph = _graph(tmp_path / "graph.json")
    skills = query_operational_graph("skill registry routing", scope="skills", graph_path=graph)
    assert [item["id"] for item in skills["results"]] == ["skill"]
    project = query_operational_graph("project protocol patient", scope="project:article-machine-governance-2026", graph_path=graph)
    assert [item["id"] for item in project["results"]] == ["project"]
    assert project["elapsed_ms"] < 10_000


def test_graph_query_rejects_untyped_or_empty_project_scope(tmp_path: Path) -> None:
    graph = _graph(tmp_path / "graph.json")
    with pytest.raises(ValueError, match="unsupported"):
        query_operational_graph("x", scope="all", graph_path=graph)
    with pytest.raises(ValueError, match="requires a project"):
        query_operational_graph("x", scope="project:", graph_path=graph)
