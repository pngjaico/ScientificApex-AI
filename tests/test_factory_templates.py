from pathlib import Path

from article_machine.contracts.compute import load_compute_contract
from article_machine.serialization import load_structured_file
from article_machine.standards import route_standards


def test_prediction_reporting_and_bias_defaults_use_current_ai_guidance():
    standards = route_standards("prediction-model")
    assert "TRIPOD+AI" in standards["guidelines"]
    assert "PROBAST+AI" in standards["risk_of_bias_tools"]


def test_bilingual_factory_templates_have_real_contracts_and_required_locks():
    root = Path(__file__).resolve().parents[1]
    for name in ("aprendizado_de_maquina_clinico", "meta_analise_em_r", "manuscrito"):
        project = root / "modelos" / name
        contract = load_compute_contract(project)
        assert load_structured_file(project / "project.yaml")["state"]["current_mode"] == "bootstrap"
        for language in ("portugues", "ingles"):
            assert (project / language / "PROTOCOLO.md").is_file()
            assert (project / language / "LEIA-ME.md").is_file()
        if name == "aprendizado_de_maquina_clinico":
            assert "TRIPOD+AI" in load_structured_file(project / "standards.yaml")["guidelines"]
        if contract.python.required:
            assert (project / contract.python.lockfile).is_file()
        if contract.r.required:
            assert (project / contract.r.lockfile).is_file()
