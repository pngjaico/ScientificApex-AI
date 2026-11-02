import importlib.util
from pathlib import Path


def test_whole_tree_map_keeps_raw_dependencies_and_credentials_opaque(tmp_path):
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("mapa", root / "scripts/mapear_arvore_da_maquina.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    (tmp_path / "modelos").mkdir()
    (tmp_path / "modelos/modelo.md").write_text("Template")
    (tmp_path / ".env").write_text("DO_NOT_READ=synthetic-test")
    for name in ("raw", "node_modules", "evidence"):
        folder = tmp_path / name
        folder.mkdir()
        (folder / "sensitive_patient_filename.txt").write_text("SYNTHETIC TEST")
    graph, exclusions, errors = module.build_tree(tmp_path)
    assert "modelos/modelo.md" in graph
    assert ".env" not in graph
    assert all("sensitive_patient_filename" not in n for n in graph)
    assert all(graph.nodes[name]["opaque"] for name in ("raw", "node_modules", "evidence"))
    assert any(item["reason"] == "credential-or-private-file-names-redacted" for item in exclusions)
    assert not errors
