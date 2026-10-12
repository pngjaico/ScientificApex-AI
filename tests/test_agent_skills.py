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


def test_skill_router_selects_anti_ai_writing_governor_with_ptbr_companion() -> None:
    report = route_workspace_skills(
        "Tirar cara de IA do meu artigo científico em português sem perder Evidence Lock.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}
    trigger_map = {skill["skill"]: set(skill["matched_triggers"]) for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "anti-ai-writing-governor" in selected
    assert "ptbr-article-writing" in selected
    assert {"cara de ia", "tirar cara de ia"} <= trigger_map["anti-ai-writing-governor"]


def test_skill_router_selects_plugin_gateways_for_zotero_life_science_and_ngs() -> None:
    report = route_workspace_skills(
        "Integrar Zotero para references.bib e full text, Life Science para genes e NGS analysis para FASTQ RNA-seq.",
        limit=20,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "zotero-reference-manager" in selected
    assert "life-science-router" in selected
    assert "ngs-analysis-router" in selected


def test_skill_router_selects_deep_thinking_for_strong_decisions() -> None:
    report = route_workspace_skills(
        "Pense profundamente, faça premortem, steelman e matriz de decisão antes de dizer que está perfeito.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "deep-thinking-governor" in selected


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


def test_skill_router_selects_intestinal_transplant_research_skill() -> None:
    report = route_workspace_skills(
        "Extrair estrategia para transplante intestinal, falencia intestinal, GLP-2, dd-cfDNA e machine perfusion intestinal.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}
    trigger_map = {skill["skill"]: set(skill["matched_triggers"]) for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "intestinal-transplant-research" in selected
    assert {"transplante intestinal", "falencia intestinal", "glp-2", "dd-cfdna", "machine perfusion intestinal"} <= trigger_map[
        "intestinal-transplant-research"
    ]


def test_skill_router_selects_datasus_research_engine_skill() -> None:
    report = route_workspace_skills(
        "Criar estudo DATASUS completo com PySUS SIH RD, SIM, CNES, cache Parquet, DuckDB, coorte, tabelas e relatorio.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "datasus-research-engine" in selected


def test_skill_router_selects_skill_upgrade_governor_for_machine_skill_requests() -> None:
    report = route_workspace_skills(
        "Pesquisar must-have skills no GitHub, instalar skills novas e ajustar a Article Machine.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "skill-upgrade-governor" in selected


def test_skill_router_selects_upgrade_and_benchmark_for_literal_sol_ultra_machine_review() -> None:
    report = route_workspace_skills(
        "vamos melhorar a máquina, agora com o 5.6 sol ultra, ainda não mexi nela depois de ser lançado esse modelo, veja oq podemos melhorar, aprimorar, revisar, organizar e afins",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert selected == {"skill-upgrade-governor", "agent-benchmark-harness"}


def test_skill_router_repairs_utf8_mojibake_in_machine_upgrade_request() -> None:
    report = route_workspace_skills(
        "vamos melhorar a m\u00c3\u00a1quina com o 5.6 sol ultra",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["input_encoding_repaired"] is True
    assert {"skill-upgrade-governor", "agent-benchmark-harness"} <= selected


def test_skill_router_repairs_double_utf8_mojibake_without_generic_overmatch() -> None:
    upgrade = route_workspace_skills(
        "vamos melhorar a m\u00c3\u0192\u00c2\u00a1quina com gpt 5.6 sol ultra",
        limit=12,
    )
    common_review = route_workspace_skills(
        "Melhorar a revis\u00c3\u00a3o do manuscrito e organizar refer\u00c3\u00aancias.",
        limit=12,
    )

    assert upgrade["input_encoding_repaired"] is True
    assert {"skill-upgrade-governor", "agent-benchmark-harness"} <= {
        skill["skill"] for skill in upgrade["selected_skills"]
    }
    assert {"skill-upgrade-governor", "agent-benchmark-harness"}.isdisjoint(
        {skill["skill"] for skill in common_review["selected_skills"]}
    )


def test_machine_upgrade_route_does_not_overmatch_common_revision_requests() -> None:
    report = route_workspace_skills(
        "Melhorar a revisão do manuscrito, aprimorar a análise e organizar as referências.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert "skill-upgrade-governor" not in selected
    assert "agent-benchmark-harness" not in selected


def test_skill_router_selects_skill_upgrade_governor_for_external_github_skill_repos() -> None:
    report = route_workspace_skills(
        "Pesquisar GitHub por scientific research skills, avaliar claude-prism e academic-research-skills, fazer triagem de skills e integrar na maquina.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "skill-upgrade-governor" in selected


def test_skill_router_selects_manuscript_integrity_response_governor() -> None:
    report = route_workspace_skills(
        "Responder pareceristas com rebuttal, revisar integridade de referencias, citation integrity e consistencia do manuscrito.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "manuscript-integrity-response-governor" in selected


def test_skill_router_selects_academic_office_deliverables() -> None:
    report = route_workspace_skills(
        "Gerar DOCX e PPTX de artigo cientifico em um latex workspace local-first com Zotero e layout QA.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "academic-office-deliverables" in selected
    assert "zotero-reference-manager" in selected


def test_skill_router_selects_navigation_and_preservation_skills() -> None:
    report = route_workspace_skills(
        "Atualizar o graph extremamente detalhado para agente novo navegar o workspace, escolher projeto ativo e reorganizar sem comprometer conteudo bruto.",
        limit=12,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert report["status"] == "routed"
    assert "workspace-graph-navigator" in selected
    assert "project-entry-navigator" in selected
    assert "content-preservation-guardian" in selected
    assert "openalex-literature-graph" not in selected


def test_skill_router_selects_provider_registration_and_living_review_skills() -> None:
    report = route_workspace_skills(
        "Register the PROSPERO protocol, build an extraction schema, search PubMed, ClinicalTrials.gov NCT records, Europe PMC full text, arXiv and bioRxiv preprints, Crossref Unpaywall DOI metadata, Semantic Scholar citation graph, OpenCitations COCI, and maintain a living review freshness update.",
        limit=30,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert "protocol-registration-governor" in selected
    assert "extraction-schema-governor" in selected
    assert "living-review-monitor" in selected
    assert "pubmed-database" in selected
    assert "clinical-trials-database" in selected
    assert "literature-search-europepmc" in selected
    assert "literature-search-arxiv" in selected
    assert "literature-search-biorxiv" in selected
    assert "crossref-unpaywall-resolver" in selected
    assert "semantic-scholar-citation-graph" in selected
    assert "opencitations-citation-audit" in selected


def test_skill_router_selects_curated_tooluniverse_workflows() -> None:
    report = route_workspace_skills(
        "Run deep literature research with T1-T4 evidence grading, then meta-analysis forest plot, diagnostic accuracy ROC AUC, epidemiology PECO propensity score, dataset discovery, clinical guidelines, trial design endpoint selection, pharmacovigilance FAERS, target validation, ACMG variant interpretation, biological annotation, and drug repurposing.",
        limit=30,
    )
    selected = {skill["skill"] for skill in report["selected_skills"]}

    assert "tooluniverse-literature-deep-research" in selected
    assert "tooluniverse-meta-analysis" in selected
    assert "tooluniverse-diagnostic-test-evaluation" in selected
    assert "tooluniverse-epidemiological-analysis" in selected
    assert "tooluniverse-dataset-discovery" in selected
    assert "tooluniverse-clinical-guidelines" in selected
    assert "tooluniverse-clinical-trial-design" in selected
    assert "tooluniverse-pharmacovigilance" in selected
    assert "tooluniverse-drug-target-validation" in selected
    assert "tooluniverse-variant-interpretation" in selected
    assert "tooluniverse-data-integration-analysis" in selected
    assert "tooluniverse-drug-repurposing" in selected


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
    operation_map = (workspace / "docs" / "AGENT_OPERATION_MAP.md").read_text(encoding="utf-8")
    agents_local = (workspace / ".agents" / "AGENTS.md").read_text(encoding="utf-8")
    graph_first = (workspace / ".agents" / "GRAPH_FIRST.md").read_text(encoding="utf-8")
    zotero_skill = (workspace / "skills" / "zotero-reference-manager" / "SKILL.md").read_text(encoding="utf-8")
    catalog = catalog_workspace_skills()

    assert catalog["status"] == "available"
    assert "Natural Skill Routing" in index
    assert "article-machine skills route" in agents
    assert "Do not bypass an applicable skill" in agents
    assert "skill-upgrade-governor" in agents
    assert "manuscript-integrity-response-governor" in agents
    assert "Source-Specific Retrieval" in index
    assert "Curated ToolUniverse Layer" in index
    assert "Roteamento Natural de Skills" in manifest
    assert "World-Class Agent Skills" in canon
    assert "anti-ai-writing-governor" in index
    assert "anti-ai-writing-governor" in agents
    assert "anti-ai-writing-governor" in manifest
    assert "anti-ai-writing-governor" in canon
    assert "anti-ai-audit" in readme
    assert "deep-thinking-governor" in index
    assert "manuscript-integrity-response-governor" in index
    assert "academic-office-deliverables" in index
    assert "academic-office-deliverables" in manifest
    assert "manuscript-integrity-response-governor" in canon
    assert "zotero-reference-manager" in index
    assert "life-science-router" in index
    assert "ngs-analysis-router" in index
    assert "workspace-graph-navigator" in index
    assert "project-entry-navigator" in index
    assert "content-preservation-guardian" in index
    assert "zotero-reference-manager" in agents
    assert "workspace-graph-navigator" in agents
    assert "project-entry-navigator" in manifest
    assert "content-preservation-guardian" in canon
    assert "life-science-router" in agents
    assert "ngs-analysis-router" in manifest
    assert "deep-thinking-governor" in canon
    assert "## Skill Routing" in readme
    assert "docs/AGENT_OPERATION_MAP.md" in readme
    assert ".agents/AGENTS.md" in readme
    assert "query the graph first" in agents_local
    assert "Use the graph before broad manual exploration" in graph_first
    for local_skill in [
        "workspace-graph-navigator",
        "project-entry-navigator",
        "content-preservation-guardian",
    ]:
        assert (workspace / ".agents" / "skills" / local_skill / "SKILL.md").exists()
    assert "Evidence Lock" in operation_map
    assert "Query the graph" in operation_map
    assert "zotero-reference-manager" in operation_map
    assert "plugin:zotero" in zotero_skill
    assert ".machine/plugin_bindings.json" in zotero_skill
