from pathlib import Path

import pytest

from article_machine.agent_skills import WORLD_CLASS_SKILLS, route_workspace_skills
from scripts.generate_skill_registry import K_DENSE_ML_VISUAL_SKILLS, LOCAL_CURATED_SKILLS
from article_machine.services.skill_registry import load_registry, tree_hash


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "metodos-ml-clinico",
    "meta-analise-medica",
    "publicacao-medica-organizada",
)


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        (
            "clinical prediction model with nested cross-validation, calibration, TRIPOD+AI and PROBAST+AI",
            "metodos-ml-clinico",
        ),
        (
            "modelo preditivo clínico com validação cruzada aninhada, calibração e validação externa",
            "metodos-ml-clinico",
        ),
        (
            "clinical prediction model in PT-BR and English",
            "metodos-ml-clinico",
        ),
        (
            "modelo preditivo clínico em português e inglês",
            "metodos-ml-clinico",
        ),
        (
            "medical meta-analysis in R using REML, Hartung-Knapp and GRADE",
            "meta-analise-medica",
        ),
        (
            "meta-análise médica em R, PICO, PRISMA e Hartung-Knapp com poucos estudos",
            "meta-analise-medica",
        ),
        (
            "medical meta-analysis report in PT-BR and English",
            "meta-analise-medica",
        ),
        (
            "relatório de meta-análise médica em português e inglês",
            "meta-analise-medica",
        ),
        (
            "organize medical manuscript versions and journal-specific publication folders",
            "publicacao-medica-organizada",
        ),
        (
            "organizar publicação médica por revista e versão com checklist de submissão",
            "publicacao-medica-organizada",
        ),
        (
            "organizar publicação médica em português e inglês",
            "publicacao-medica-organizada",
        ),
    ],
)
def test_rotas_pt_en_ativas(query: str, expected: str) -> None:
    result = route_workspace_skills(query)
    routes = {item["skill"]: item for item in result["selected_skills"]}
    assert result["status"] == "routed"
    assert expected in routes
    assert routes[expected]["registry_status"] == "active"
    assert routes[expected]["promotion_requires_review"] is False


def test_fontes_agents_e_copias_canonicas_sao_identicas() -> None:
    for name in SKILLS:
        source = ROOT / ".agents" / "skills" / name
        canonical = ROOT / "skills" / name
        assert tree_hash(source) == tree_hash(canonical)


def test_paridade_de_idioma_e_artefatos_tecnicos_compartilhados() -> None:
    ml = (ROOT / ".agents/skills/metodos-ml-clinico/SKILL.md").read_text(encoding="utf-8")
    meta = (ROOT / ".agents/skills/meta-analise-medica/SKILL.md").read_text(encoding="utf-8")
    publication = (ROOT / ".agents/skills/publicacao-medica-organizada/SKILL.md").read_text(encoding="utf-8")
    for content in (ml, meta, publication):
        assert "portugues/" in content
        assert "ingles/" in content
        assert "bilingual-scientific-writing" in content
        assert "audit-language" in content
    assert "código" in ml and "dados analíticos" in ml and "lock de ambiente" in ml
    assert "Código R" in meta and "dados extraídos" in meta and "lock" in meta
    assert "07_manuscrito/portugues/" in publication
    assert "07_manuscrito/ingles/" in publication


def test_frase_bilingue_generica_nao_aciona_skill_ml() -> None:
    result = route_workspace_skills("preciso preparar uma entrega em português e inglês")
    assert "metodos-ml-clinico" not in {item["skill"] for item in result["selected_skills"]}


def test_skills_locais_ativas_fora_do_gate_world_class_ate_versionamento() -> None:
    registry = load_registry(ROOT)["skills"]
    assert set(SKILLS) <= LOCAL_CURATED_SKILLS
    assert set(SKILLS).isdisjoint(WORLD_CLASS_SKILLS)
    for name in SKILLS:
        entry = registry[name]
        assert entry["status"] == "active"
        assert entry["pinned_revision"] == "workspace-2026-11-01"
        assert entry["license"] == "LicenseRef-Local-Private"
        assert entry["required_for_clone"] is False


def test_skills_kdense_sobem_como_piloto_com_licencas_por_skill() -> None:
    registry = load_registry(ROOT)["skills"]
    expected_licenses = {
        "scikit-learn": "BSD-3-Clause",
        "pytorch-lightning": "Apache-2.0",
        "scientific-visualization": "MIT",
    }
    assert K_DENSE_ML_VISUAL_SKILLS == expected_licenses
    for name, license_name in expected_licenses.items():
        entry = registry[name]
        assert entry["status"] == "pilot"
        assert entry["pinned_revision"] == "5f2bc0341354fd5590aef76a533ada1e1e5b4e62"
        assert entry["license"] == license_name
        assert entry["required_for_clone"] is False
