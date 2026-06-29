from pathlib import Path

from article_machine.agent_skills import (
    WORLD_CLASS_SKILLS,
    audit_workspace_skills,
    catalog_workspace_skills,
    route_workspace_skills,
)
from article_machine.cli import main


def test_world_class_skills_exist_with_trigger_frontmatter() -> None:
    workspace = Path(__file__).resolve().parents[1]
    for skill_name in WORLD_CLASS_SKILLS:
        skill_path = workspace / "skills" / skill_name / "SKILL.md"
        assert skill_path.exists(), skill_name
        text = skill_path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert f"name: {skill_name}" in text
        assert "description: Use when" in text
        assert "TODO" not in text


def test_workspace_skill_audit_passes_for_world_class_layer() -> None:
    report = audit_workspace_skills()

    assert report["status"] == "pass"
    assert report["issues"] == []


def test_skill_catalog_parses_multiline_frontmatter_descriptions() -> None:
    catalog = catalog_workspace_skills()

    assert "Brain Imaging Data Structure" in catalog["skills"]["bids"]["description"]
    assert catalog["skills"]["bids"]["description"] != ">"


def test_skill_router_selects_discovery_and_validation_skills() -> None:
    report = route_workspace_skills(
        "Generate drug target hypotheses, check ChEMBL binding evidence, AlphaFold structure, and avoid in silico overclaiming."
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "hypothesis-tournament" in selected
    assert "chembl-bindingdb-miner" in selected
    assert "alphafold-pdb-structure-router" in selected
    assert "in-silico-validation-governor" in selected


def test_skill_router_selects_review_quality_skills() -> None:
    report = route_workspace_skills(
        "Run systematic review screening with ASReview, assess QUADAS-2 risk of bias, and build GRADE Summary of Findings."
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert "asreview-screening-bridge" in selected
    assert "risk-of-bias-assistant" in selected
    assert "grade-sof-table-builder" in selected


def test_skill_router_selects_ptbr_article_writing_for_portuguese_manuscripts() -> None:
    report = route_workspace_skills(
        "Escrever artigo cientifico em portugues brasileiro sem parecer traducao do ingles e com Evidence Lock."
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}
    trigger_map = {skill["skill"]: set(skill["matched_triggers"]) for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "ptbr-article-writing" in selected
    assert {"artigo cientifico", "portugues", "traducao"} <= trigger_map["ptbr-article-writing"]


def test_skill_router_selects_ptbr_article_writing_for_reference_styles() -> None:
    report = route_workspace_skills(
        "Formatar referencias em ABNT NBR 6023, citacoes ABNT NBR 10520 e Vancouver ICMJE para tese."
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}
    trigger_map = {skill["skill"]: set(skill["matched_triggers"]) for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "ptbr-article-writing" in selected
    assert {"abnt", "nbr 6023", "nbr 10520", "vancouver", "icmje"} <= trigger_map["ptbr-article-writing"]


def test_skill_router_supports_portuguese_and_avoids_short_substring_false_matches() -> None:
    report = route_workspace_skills("fazer docking e validar resultado in silico sem overclaim")
    selected = {skill["skill"] for skill in report["selected_skills"]}
    trigger_map = {skill["skill"]: set(skill["matched_triggers"]) for skill in report["selected_skills"]}

    assert "in-silico-validation-governor" in selected
    assert "chembl-bindingdb-miner" not in selected
    assert "hypothesis-tournament" not in selected
    assert "validar" in trigger_map["in-silico-validation-governor"]


def test_skill_router_selects_new_upstream_workflow_skills() -> None:
    report = route_workspace_skills(
        "Analyze bulk RNA-seq FASTQ with nf-core/rnaseq, build a counts matrix, run GSEA, and justify sample size with 80% power.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert "bulk-rnaseq" in selected
    assert "nextflow" in selected
    assert "pathway-enrichment" in selected
    assert "statistical-power" in selected


def test_skill_router_selects_document_parsing_and_lookup_skills() -> None:
    report = route_workspace_skills(
        "Parse scanned PDF papers with OCR and bounding boxes, then do DOI lookup for article metadata.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert "liteparse" in selected
    assert "paper-lookup" in selected


def test_skill_router_selects_agent_optimization_skills() -> None:
    report = route_workspace_skills(
        "Improve this agent harness over many experiments, beat the baseline, and draft new skills from repeated workflows.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert "agent-benchmark-harness" in selected
    assert "arbor" in selected
    assert "autoskill" in selected


def test_cli_skills_audit_and_route_commands() -> None:
    assert main(["skills", "audit"]) == 0
    assert main(["skills", "route", "--query", "benchmark whether this machine is world-class"]) == 0


def test_skill_index_and_agent_rules_mention_natural_routing() -> None:
    workspace = Path(__file__).resolve().parents[1]
    index = (workspace / "SKILL_INDEX.md").read_text(encoding="utf-8")
    agents = (workspace / "AGENTS.md").read_text(encoding="utf-8")
    manifest = (workspace / "AGENT_MANIFEST.md").read_text(encoding="utf-8")
    canon = (workspace / "SKILLS_CANON.md").read_text(encoding="utf-8")
    readme = (workspace / "README.md").read_text(encoding="utf-8")
    catalog = catalog_workspace_skills()

    assert catalog["status"] == "available"
    assert "Natural Skill Routing" in index
    assert "article-machine skills route" in agents
    assert "Do not bypass an applicable skill" in agents
    assert "Roteamento Natural de Skills" in manifest
    assert "World-Class Agent Skills" in canon
    assert "## Skill Routing" in readme
