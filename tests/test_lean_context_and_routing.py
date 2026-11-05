from __future__ import annotations

import json
from pathlib import Path

from article_machine.agent_skills import (
    WORLD_CLASS_SKILLS,
    audit_workspace_skills,
    route_workspace_skills,
)
from article_machine.cli import main
from article_machine.services.skill_registry import load_registry


def test_machine_continuous_learner_is_registered() -> None:
    registry = load_registry(Path("."))
    assert "machine-continuous-learner" in registry["skills"]
    assert registry["skills"]["machine-continuous-learner"]["status"] == "active"
    assert "analytical-method-validation" in registry["skills"]
    assert "pkpd-modeling" in registry["skills"]
    assert "relsa-severity-assessment" in registry["skills"]


def test_routing_7_intentions() -> None:
    # 1. Bench & Wet Lab
    r_bench = route_workspace_skills("protocolo de bancada elisa e western blot")
    assert r_bench["status"] == "routed"
    assert any(s["skill"] == "experimental-design-planner" for s in r_bench["selected_skills"])

    # 2. Continuous Learning (/learn)
    r_learn = route_workspace_skills("/learn registrar licoes aprendidas da sessao")
    assert r_learn["status"] == "routed"
    assert any(s["skill"] == "machine-continuous-learner" for s in r_learn["selected_skills"])

    # 3. Medical Publication 9-folder
    r_pub = route_workspace_skills("publish prepare preparar pacote de submissao")
    assert r_pub["status"] == "routed"
    assert any(s["skill"] == "publicacao-medica-organizada" for s in r_pub["selected_skills"])

    # 4. Meta-Analysis
    r_meta = route_workspace_skills("meta-análise médica em R com poucos estudos REML")
    assert r_meta["status"] == "routed"
    assert any(s["skill"] == "meta-analise-medica" for s in r_meta["selected_skills"])

    # 5. Clinical ML
    r_ml = route_workspace_skills("modelo preditivo clínico com calibração e incerteza")
    assert r_ml["status"] == "routed"
    assert any(s["skill"] == "metodos-ml-clinico" for s in r_ml["selected_skills"])

    # 6. Landmark & Seminal Literature
    r_land = route_workspace_skills("artigos seminais landmark nature nejm")
    assert r_land["status"] == "routed"
    assert any(s["skill"] == "pubmed-database" for s in r_land["selected_skills"])

    # 7. Red Team & Hostile Critical Review
    r_crit = route_workspace_skills("hostile peer review red team auditoria crítica")
    assert r_crit["status"] == "routed"
    assert any(s["skill"] == "scientific-red-team-reviewer" for s in r_crit["selected_skills"])

    # 8. Analytical Method Validation & Metrology
    r_amv = route_workspace_skills("validação de método analítico ICH Q2 LOD LOQ")
    assert any(s["skill"] == "analytical-method-validation" for s in r_amv["selected_skills"])

    # 9. PK/PD & Allometric Scaling
    r_pkpd = route_workspace_skills("farmacocinética clearance volume of distribution pkpd")
    assert any(s["skill"] == "pkpd-modeling" for s in r_pkpd["selected_skills"])

    # 10. Animal Severity Assessment & Humane Endpoint
    r_relsa = route_workspace_skills("escore gravidade animal relsa humane endpoint")
    assert any(s["skill"] == "relsa-severity-assessment" for s in r_relsa["selected_skills"])

    # 11. Uncertainty and Units
    r_unc = route_workspace_skills("propagação de incerteza GUM dimensional analysis")
    assert any(s["skill"] == "uncertainty-and-units" for s in r_unc["selected_skills"])

    # 12. Ontology Term Resolution
    r_ont = route_workspace_skills("resolver ontologia CURIE UBERON OLS4")
    assert any(s["skill"] == "ontology-term-resolution" for s in r_ont["selected_skills"])

    # 13. ISO Standards Readiness
    r_iso = route_workspace_skills("acreditação de laboratório iso 15189 gestão da qualidade")
    assert any(s["skill"] == "iso-standards-readiness" for s in r_iso["selected_skills"])


def test_bench_cli_lean_output(tmp_path: Path, capsys) -> None:
    target_dir = tmp_path / "bench_proj"
    target_dir.mkdir()

    # Generate assay template
    code = main(["bench", "template", str(target_dir), "--assay", "elisa"])
    assert code == 0
    captured = capsys.readouterr()
    # Ensure stdout is lean (under 30 lines)
    assert len(captured.out.splitlines()) < 30
    payload = json.loads(captured.out)
    assert payload["status"] == "created"
    assert payload["assay_key"] == "elisa"
    assert (target_dir / "experiments" / "protocols").exists()

    # Generate sample manifest
    code_manifest = main(["bench", "sample-manifest", str(target_dir)])
    assert code_manifest == 0
    captured_manifest = capsys.readouterr()
    assert len(captured_manifest.out.splitlines()) < 25
    payload_manifest = json.loads(captured_manifest.out)
    assert payload_manifest["status"] == "created"
