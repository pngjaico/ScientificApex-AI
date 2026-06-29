from pathlib import Path

from article_machine.cli import main
from article_machine.life_science import (
    catalog_life_science_skills,
    plan_life_science_retrieval,
)
from article_machine.projects import init_project
from article_machine.serialization import load_structured_file


def test_catalog_life_science_skills_reads_skill_frontmatter(tmp_path: Path) -> None:
    plugin_root = tmp_path / "life-science-research"
    skill_dir = plugin_root / "skills" / "chembl-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\n"
        "name: chembl-skill\n"
        "description: Submit compact ChEMBL API requests for activity, molecule, target, mechanism, and text-search endpoints.\n"
        "---\n",
        encoding="utf-8",
    )

    catalog = catalog_life_science_skills(plugin_root)

    assert catalog["status"] == "available"
    assert catalog["plugin"]["name"] == "life-science-research"
    assert catalog["skills"]["chembl-skill"]["description"].startswith("Submit compact ChEMBL")


def test_plan_life_science_retrieval_routes_drug_discovery_question(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "IBD Drug Discovery", "drug-discovery")

    report = plan_life_science_retrieval(
        project_dir,
        "Find tractable drug targets and small-molecule evidence for TNF and JAK signaling in Crohn gut inflammation.",
    )
    plan_path = project_dir / "context" / "life_science" / "retrieval_plan.yaml"
    plan = load_structured_file(plan_path)
    selected = {skill["name"] for skill in plan["selected_skills"]}

    assert report["status"] == "planned"
    assert plan_path.exists()
    assert "target-disease-evidence" in plan["lanes"]
    assert "chemistry-pharmacology" in plan["lanes"]
    assert {"opentargets-skill", "chembl-skill", "bindingdb-skill", "pubchem-pug-skill"}.issubset(selected)
    assert plan["evidence_policy"]["label"] == "hypothesis-generating-until-validated"


def test_plan_life_science_retrieval_routes_variant_question(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Variant Review", "systematic-review")

    report = plan_life_science_retrieval(
        project_dir,
        "Interpret rs6025 variant evidence across ClinVar, gnomAD, GWAS, and PheWAS cohorts.",
    )
    selected = {skill["name"] for skill in report["selected_skills"]}

    assert "genetics-variant-interpretation" in report["lanes"]
    assert {"clinvar-variation-skill", "gnomad-graphql-skill", "gwas-catalog-skill"}.issubset(selected)


def test_cli_life_science_plan_writes_project_artifact(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "CLI Life Science", "intestinal-digital-twin")

    exit_code = main(
        [
            "life-science",
            "plan",
            str(project_dir),
            "--question",
            "Map microbiome, metabolite, and epithelial cell datasets for an in silico intestine model.",
        ]
    )

    assert exit_code == 0
    assert (project_dir / "context" / "life_science" / "retrieval_plan.yaml").exists()


def test_life_science_agent_skill_and_v2_roadmap_are_saved() -> None:
    workspace = Path(__file__).resolve().parents[1]
    skill_path = workspace / "skills" / "life-science-router" / "SKILL.md"
    roadmap_path = workspace / "docs" / "roadmaps" / "slides-posters-v2.md"

    assert skill_path.exists()
    assert "name: life-science-router" in skill_path.read_text(encoding="utf-8")
    assert roadmap_path.exists()
    assert "Slides and Posters V2" in roadmap_path.read_text(encoding="utf-8")
