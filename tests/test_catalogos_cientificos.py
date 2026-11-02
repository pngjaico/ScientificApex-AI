import importlib.util
import json
from pathlib import Path

import pytest

from article_machine.agent_skills import route_workspace_skills

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "catalogos", ROOT / "skills/catalogos-cientificos-sob-demanda/scripts/consultar_catalogos.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_external_catalogs_keep_five_pinned_sources_and_no_execution():
    report = MODULE.search_catalogs(ROOT, "ml-paper-writing")
    assert len(report["sources_available"]) == 5
    assert report["entries"][0]["name"] == "ml-paper-writing"
    assert report["entries"][0]["source_id"] == "orchestra"
    assert all(row["execution_authorized"] is False and len(row["pinned_sha"]) == 40 for row in report["entries"])


@pytest.mark.parametrize("query", ["cinco catalogos cientificos", "scientific skill catalogs", "Orchestra-Research"])
def test_catalog_gateway_is_routed_in_both_languages(query):
    report = route_workspace_skills(query)
    assert any(row["skill"] == "catalogos-cientificos-sob-demanda" for row in report["selected_skills"])


def test_inventory_revision_drift_fails_closed(tmp_path):
    base = tmp_path / "integracoes/catalogos_cientificos"
    base.mkdir(parents=True)
    (base / "manifesto_das_fontes.json").write_text(json.dumps({"sources": [{"id": "test", "head_sha": "a"}]}))
    (base / "inventario_de_habilidades.json").write_text(
        json.dumps({"sources": [{"source_id": "test", "pinned_sha": "b", "entries": []}]})
    )
    with pytest.raises(ValueError, match="revision drift"):
        MODULE.search_catalogs(tmp_path)
