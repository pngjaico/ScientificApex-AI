import pytest
import scripts.generate_workspace_graph as workspace_graph

from scripts.generate_workspace_graph import build_extraction, reconcile_graphify_communities, validate_operational_graph


class _GraphWithCanonicalizedIds:
    def __init__(self, rows: list[tuple[str, dict]], edge_count: int = 0) -> None:
        self._rows = rows
        self._edge_count = edge_count

    def nodes(self, data: bool = False) -> list:
        assert data is True
        return self._rows

    def number_of_nodes(self) -> int:
        return len(self._rows)

    def number_of_edges(self) -> int:
        return self._edge_count


def test_operational_graph_maps_agent_flow_and_real_legacy_dirs() -> None:
    extraction, communities, _labels, manifest = build_extraction()
    nodes = {node["id"]: node for node in extraction["nodes"]}
    labels = {node["label"] for node in extraction["nodes"]}

    assert "flow_start_here" in nodes
    assert "flow_agents_control_plane" in nodes
    assert "flow_graph_first_query" in nodes
    assert "flow_skill_route" in nodes
    assert "flow_evidence_lock" in nodes
    assert "alias_pt_agent_new_workspace" in nodes
    assert "alias_pt_graph_fluidity" in nodes
    assert "alias_pt_always_use_graph" in nodes
    assert "alias_pt_model_orchestration" in nodes
    assert "doc_agents_agents_md" in nodes
    assert "doc_agents_graph_first_md" in nodes
    assert "skill_workspace_graph_navigator" in nodes
    assert "skill_project_entry_navigator" in nodes
    assert "skill_content_preservation_guardian" in nodes
    assert "runtime_skills_route" in nodes
    assert "runtime_skills_audit" in nodes
    assert "module_group_project_runtime" in nodes
    assert "module_group_evidence_gates" in nodes
    assert "module_group_deliverables" in nodes
    assert "doc_codex_readme_md" in nodes
    assert "codex_project_config" in nodes
    assert "codex_agent_workspace_explorer" in nodes
    assert "codex_agent_scientific_reviewer" in nodes
    assert "codex_agent_verification_runner" in nodes
    assert "codex_profile_xhigh_baseline" in nodes
    assert "codex_profile_ultra_benchmark" in nodes
    assert "runtime_venv_graphify" in nodes

    # A portable clone intentionally excludes legacy research corpora.
    for legacy in manifest["legacy_dirs_present"]:
        assert f"legacy: {legacy}" in labels
    assert manifest["detail_counts"]["doc_sections"] >= 20
    assert manifest["detail_counts"]["project_contracts"] >= manifest["project_count"] * 4
    assert manifest["detail_counts"]["project_artifact_areas"] >= manifest["project_count"]
    assert manifest["detail_counts"]["skill_sections"] >= manifest["critical_skill_count"]
    assert manifest["detail_counts"]["navigation_skills"] == 3
    assert manifest["detail_counts"]["codex_agents"] == 5
    assert manifest["detail_counts"]["codex_profiles"] == 2
    assert set(manifest["git_state"]) == {
        "available",
        "head_commit",
        "worktree_dirty",
        "status_entry_count",
    }
    assert manifest["git_state"]["available"] is True
    assert isinstance(manifest["git_state"]["worktree_dirty"], bool)

    assert ("hygiene_sources" in nodes) == (workspace_graph.ROOT / "sources").exists()
    assert "hygiene_agents" in nodes
    assert "hygiene_graphify_out" in nodes
    assert len(communities[5]) >= 1 + len(manifest["legacy_dirs_present"])
    assert len(communities[6]) > 2
    assert len(communities[7]) > 1


def test_operational_graph_source_has_no_common_mojibake_fragments() -> None:
    watched_text = "\n".join(
        [
            node["label"]
            for node in build_extraction()[0]["nodes"]
        ]
    )
    bad_fragments = ["Ã§", "Ã£", "Ã‰", "Ãƒ", "Ãµ", "Â·", "â†"]

    for fragment in bad_fragments:
        assert fragment not in watched_text


def test_operational_graph_key_navigation_nodes_are_not_single_edge_stubs() -> None:
    extraction = build_extraction()[0]
    degree: dict[str, int] = {}
    for edge in extraction["edges"]:
        degree[edge["source"]] = degree.get(edge["source"], 0) + 1
        degree[edge["target"]] = degree.get(edge["target"], 0) + 1

    key_prefixes = (
        "flow_",
        "doc_agents_",
        "graphify_",
        "hygiene_",
        "legacy_",
        "module_group_",
        "lane_",
        "mode_",
        "type_",
        "alias_",
    )
    weak = [
        node["id"]
        for node in extraction["nodes"]
        if node["id"].startswith(key_prefixes) and degree.get(node["id"], 0) <= 1
    ]

    assert weak == []


def test_operational_graph_skill_sections_are_chained_not_mass_stubs() -> None:
    extraction, _communities, _labels, manifest = build_extraction()
    degree: dict[str, int] = {}
    for edge in extraction["edges"]:
        degree[edge["source"]] = degree.get(edge["source"], 0) + 1
        degree[edge["target"]] = degree.get(edge["target"], 0) + 1

    weak_skill_sections = [
        node["id"]
        for node in extraction["nodes"]
        if node["id"].startswith("skill_section_") and degree.get(node["id"], 0) <= 1
    ]

    assert len(weak_skill_sections) < manifest["critical_skill_count"]


def test_codex_control_plane_heading_is_connected_to_runtime_policy() -> None:
    extraction = build_extraction()[0]
    section_ids = {
        node["id"]
        for node in extraction["nodes"]
        if node["id"].startswith("doc_section_codex_readme_md_")
    }
    linked_sections = {
        edge["source"]
        for edge in extraction["edges"]
        if edge["target"] == "codex_control_plane" and edge["relation"] == "summarizes"
    }

    assert section_ids
    assert section_ids <= linked_sections


def test_operational_graph_manifest_declares_fluid_html_mode() -> None:
    _extraction, _communities, _labels, manifest = build_extraction()

    assert manifest["query_alias_count"] >= 13
    assert manifest["html_mode"]["layout"] == "fixed-community"
    assert manifest["html_mode"]["physics_default"] is False
    assert manifest["html_mode"]["labels_default"] == "hubs-only"


def test_graphify_canonicalized_ids_are_reconciled_before_report_generation() -> None:
    extraction, communities, _labels, _manifest = build_extraction()
    rows = []
    for node in extraction["nodes"]:
        canonical_id = (
            "article_machine_cli_analyze"
            if node["id"] == "cli_analyze"
            else node["id"]
        )
        rows.append(
            (
                canonical_id,
                {key: value for key, value in node.items() if key != "id"},
            )
        )

    reconciled = reconcile_graphify_communities(
        _GraphWithCanonicalizedIds(rows),
        communities,
    )

    assert "article_machine_cli_analyze" in reconciled[1]
    assert "cli_analyze" not in reconciled[1]
    assert {node_id for members in reconciled.values() for node_id in members} == {
        node_id for node_id, _attributes in rows
    }


def test_graphify_community_reconciliation_rejects_missing_stable_ids() -> None:
    graph = _GraphWithCanonicalizedIds([("article_machine_cli_analyze", {})])

    with pytest.raises(ValueError, match="missing its stable operational_id"):
        reconcile_graphify_communities(graph, {1: ["cli_analyze"]})


def test_read_only_operational_graph_validation_reconciles_graphify_ids(tmp_path, monkeypatch) -> None:
    def fake_builder(extraction):
        rows = []
        for node in extraction["nodes"]:
            canonical_id = "article_machine_cli_analyze" if node["id"] == "cli_analyze" else node["id"]
            rows.append((canonical_id, {key: value for key, value in node.items() if key != "id"}))
        return _GraphWithCanonicalizedIds(rows, edge_count=len(extraction["edges"]))

    monkeypatch.setattr(workspace_graph, "_build_graphify_graph_in_memory", fake_builder)
    monkeypatch.setattr(workspace_graph, "OUT", tmp_path / "must-not-be-created")

    report = validate_operational_graph(workspace_graph.ROOT)

    assert report["status"] == "pass"
    assert report["read_only"] is True
    assert report["checks"]["graphify_id_community_reconciliation"]["operational_ids"] > 0
    assert not workspace_graph.OUT.exists()


def test_read_only_operational_graph_validation_blocks_graphify_failure(monkeypatch) -> None:
    def fail_builder(_extraction):
        raise ValueError("simulated Graphify canonicalization failure")

    monkeypatch.setattr(workspace_graph, "_build_graphify_graph_in_memory", fail_builder)

    report = validate_operational_graph(workspace_graph.ROOT)

    assert report["status"] == "block"
    assert "simulated Graphify canonicalization failure" in report["issues"][0]
