from copy import deepcopy
from datetime import date
import importlib.util
from pathlib import Path

import pytest

from article_machine.agent_skills import route_workspace_skills

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("funding_check", ROOT / "skills/fapesp-cnpq-projects/scripts/check_packet.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def packet():
    return {"agency": "CNPq", "modality": "test fixture", "call_id": "test-only", "status": "minuta-para-revisao", "verified_on": "2026-11-02",
            "sources": [{"id": "rule", "url": "https://www.gov.br/cnpq/", "version": "fixture", "accessed_on": "2026-11-02", "role": "current-rule"}],
            "requirements": [{"id": "abstract", "source_id": "rule", "locator": "fixture section", "kind": "mandatory", "rule": "fixture text limit", "verified": True}],
            "fields": [{"name": "abstract", "text": "a b\nc", "limit": 5, "source_id": "rule"}], "pending": []}


def check(value):
    return MODULE.check_packet(value, today=date(2026, 11, 2))


@pytest.mark.parametrize("query", ["Escrever projeto FAPESP no Mandaqui", "Adaptar proposta CNPq Universal", "Auxílio Regular para biomarcadores", "Bolsa de doutorado com plano de gestão de dados"])
def test_funding_routes(query):
    assert "fapesp-cnpq-projects" in {item["skill"] for item in route_workspace_skills(query)["selected_skills"]}


def test_no_funding_route_for_unrelated_medical_request():
    assert "fapesp-cnpq-projects" not in {item["skill"] for item in route_workspace_skills("Interpretar resultado de I-FABP e TC")["selected_skills"]}


def test_pass_is_explicitly_structural_only():
    assert check(packet())["status"] == "pass-structural-only"


def test_character_limit_includes_spaces_and_line_breaks():
    value = packet()
    value["fields"][0]["limit"] = 4
    assert any("5 characters exceeds 4" in e for e in check(value)["errors"])


def test_historical_rule_cannot_support_current_limits():
    value = packet()
    value["sources"][0]["role"] = "historical-example"
    assert any("historical" in e for e in check(value)["errors"])


@pytest.mark.parametrize("bad_url", ["https://fapesp.br.evil.example/rule", "http://fapesp.br/rule", "https://example.org/fapesp"])
def test_unofficial_or_insecure_url_is_rejected(bad_url):
    value = packet()
    value["sources"][0]["url"] = bad_url
    assert check(value)["status"] == "block"


def test_missing_evidence_and_pending_items_block():
    value = packet()
    value["requirements"][0]["verified"] = False
    value["fields"][0]["source_id"] = "unknown"
    value["pending"] = ["eligibility unresolved"]
    errors = check(value)["errors"]
    assert any("unverified" in e for e in errors)
    assert any("unknown source_id" in e for e in errors)
    assert any("unresolved" in e for e in errors)


@pytest.mark.parametrize("value", [None, [], {"sources": [None], "requirements": [None], "fields": [None]}, {"agency": [], "sources": [{"id": "x", "role": []}], "requirements": [{"kind": []}]}])
def test_invalid_packets_fail_without_crashing(value):
    assert check(deepcopy(value))["status"] == "block"


def test_future_dates_block_and_stale_dates_warn():
    value = packet()
    value["sources"][0]["accessed_on"] = "2027-01-01"
    assert any("future date" in e for e in check(value)["errors"])
    value["sources"][0]["accessed_on"] = "2026-01-01"
    assert check(value)["warnings"]
