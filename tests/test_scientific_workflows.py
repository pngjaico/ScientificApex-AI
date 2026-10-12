import json
from pathlib import Path

import pytest

from article_machine.projects import init_project
from article_machine.services.scientific_workflows import audit_language, plan_scientific_workflow
from article_machine.life_science import route_life_science_lanes


@pytest.mark.parametrize("language,query", [
    ("pt-BR", "Planejar trabalhos científicos complexos: revisão sistemática em português"),
    ("en", "Plan a complex scientific systematic review and English manuscript"),
])
def test_workflow_packet_preserves_project_state_and_has_role_contracts(tmp_path: Path, language: str, query: str) -> None:
    project = init_project(tmp_path, "Bilingual review", "systematic-review")
    before = (project / "project.yaml").read_bytes()
    plan = plan_scientific_workflow(project, query, language)
    assert plan["status"] == "planned"
    assert plan["gate_eligible"] is False
    assert plan["coordination"]["effort"] == "medium"
    assert plan["delegation"]["implementation"]["model"] == "gpt-6-luna"
    assert plan["language"] == language
    assert (project / "project.yaml").read_bytes() == before
    assert json.loads((project / "context" / "scientific_workflow_plan.json").read_text())["language"] == language


def test_translation_detects_numeric_claim_and_citation_drift(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Translation", "systematic-review")
    (project / "drafts" / "en.md").write_text("RR 0.85, n=120 {{claim:c1}} [@key2025]", encoding="utf-8")
    (project / "drafts" / "pt.md").write_text("RR 0,85, n=120 {{claim:c1}} [@key2025]", encoding="utf-8")
    passed = audit_language(project, "pt-BR", "drafts/pt.md", "drafts/en.md")
    assert passed["status"] == "pass"
    assert passed["semantic_review_required"] is True
    (project / "drafts" / "pt.md").write_text("RR 0,95, n=120 {{claim:c2}} [@wrong]", encoding="utf-8")
    blocked = audit_language(project, "pt-BR", "drafts/pt.md", "drafts/en.md")
    assert blocked["status"] == "block"
    assert len(blocked["issues"]) == 3
    with pytest.raises(ValueError, match="inside"):
        audit_language(project, "en", "../outside.md")


def test_biomedical_lanes_understand_portuguese_queries() -> None:
    lanes = route_life_science_lanes("Investigar alvos e fármacos na inflamação intestinal")
    assert {"target-disease-evidence", "chemistry-pharmacology"} <= {lane["name"] for lane in lanes}
