from __future__ import annotations

import ast
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "graphify-out"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CRITICAL_SKILLS = [
    "hypothesis-tournament",
    "scientific-novelty-checker",
    "experimental-design-planner",
    "ro-crate-provenance-export",
    "nextflow-pipeline-runner",
    "snakemake-pipeline-runner",
    "cwl-workflow-bridge",
    "asreview-screening-bridge",
    "risk-of-bias-assistant",
    "grade-sof-table-builder",
    "openalex-literature-graph",
    "open-targets-drug-targeting",
    "chembl-bindingdb-miner",
    "alphafold-pdb-structure-router",
    "in-silico-validation-governor",
    "agent-benchmark-harness",
    "scientific-red-team-reviewer",
    "query-string-governor",
    "database-retrieval-governor",
    "topic-ideation-tournament",
    "evidence-lock-hardener",
    "stage-audit-governor",
    "author-identity-resolver",
    "guideline-router",
    "retraction-integrity-checker",
    "ptbr-article-writing",
]

LEGACY_ROOT_DIRS = [
    "Correção Orientador",
    "Doutorado",
    "Leitor de Artigos",
    "PDFS DR ANDRÉ",
    "REVISÃO LIGA",
    "Revisões Sistemáticas",
    "Submissão Final",
    "NMA_OSA_VPI",
]


def slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in value)
    return "_".join(part for part in cleaned.split("_") if part) or "node"


def read_structured(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        from article_machine.serialization import load_structured_file

        payload = load_structured_file(path)
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def add_node(nodes: dict[str, dict[str, Any]], node_id: str, label: str, file_type: str, source_file: str = "") -> None:
    nodes[node_id] = {
        "id": node_id,
        "label": label,
        "file_type": file_type,
        "source_file": source_file,
        "source_location": None,
        "source_url": None,
        "captured_at": None,
        "author": None,
        "contributor": None,
    }


def add_edge(
    edges: list[dict[str, Any]],
    source: str,
    target: str,
    relation: str,
    confidence: str = "EXTRACTED",
    source_file: str = "",
    weight: float = 1.0,
) -> None:
    edges.append(
        {
            "source": source,
            "target": target,
            "relation": relation,
            "confidence": confidence,
            "confidence_score": 1.0 if confidence == "EXTRACTED" else 0.75,
            "source_file": source_file,
            "source_location": None,
            "weight": weight,
        }
    )


def cli_commands() -> list[str]:
    cli_path = ROOT / "article_machine" / "cli.py"
    tree = ast.parse(cli_path.read_text(encoding="utf-8"))
    commands: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        attr = getattr(node.func, "attr", "")
        if attr != "add_parser" or not node.args:
            continue
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            commands.append(first.value)
    ignored = {"register", "build", "import", "plan", "qa", "dry-run", "run", "catalog", "audit", "route"}
    return sorted({cmd for cmd in commands if cmd not in ignored})


def project_dirs() -> list[Path]:
    projects_root = ROOT / "projects"
    if not projects_root.exists():
        return []
    return sorted(
        p
        for p in projects_root.iterdir()
        if p.is_dir()
        and all((p / name).exists() for name in ["project.yaml", "protocol.yaml", "standards.yaml", "compute.yaml"])
    )


def build_extraction() -> tuple[dict[str, Any], dict[int, list[str]], dict[int, str], dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    add_node(nodes, "workspace_doutorado", "Doutorado Workspace", "document", ".")
    hubs = {
        "hub_runtime": "Runtime And Commands",
        "hub_article_machine": "Article Machine Package",
        "hub_projects": "Article Machine Projects",
        "hub_skills": "Critical Scientific Skills",
        "hub_docs": "Agent Documentation",
        "hub_legacy": "Legacy And Raw Sources",
        "hub_graphify": "Graphify Operational Map",
        "hub_git": "Git Hygiene",
    }
    for node_id, label in hubs.items():
        add_node(nodes, node_id, label, "rationale", ".")
        add_edge(edges, "workspace_doutorado", node_id, "contains", "EXTRACTED", ".")

    runtime_nodes = {
        "runtime_venv_article_machine": ".venv python -m article_machine",
        "runtime_global_graphify": "global python -m graphify",
        "runtime_pytest": ".venv python -m pytest",
        "runtime_machine_audit": "article_machine machine audit",
    }
    for node_id, label in runtime_nodes.items():
        add_node(nodes, node_id, label, "code", "docs/AGENT_START_HERE.md")
        add_edge(edges, "hub_runtime", node_id, "documents", "EXTRACTED", "docs/AGENT_START_HERE.md")

    for doc in ["AGENTS.md", "README.md", "SKILL_INDEX.md", "docs/AGENT_START_HERE.md", "docs/ARTICLE_MACHINE_AGENT_PLAYBOOK.md", "docs/WORKSPACE_REORG_PLAN.md"]:
        path = ROOT / doc
        if path.exists():
            node_id = "doc_" + slug(doc)
            add_node(nodes, node_id, doc, "document", doc)
            add_edge(edges, "hub_docs", node_id, "documents", "EXTRACTED", doc)
            add_edge(edges, node_id, "hub_article_machine", "references", "INFERRED", doc, 0.8)

    for module in sorted((ROOT / "article_machine").glob("*.py")):
        node_id = "module_" + slug(module.stem)
        rel = module.relative_to(ROOT).as_posix()
        add_node(nodes, node_id, f"article_machine.{module.stem}", "code", rel)
        add_edge(edges, "hub_article_machine", node_id, "contains", "EXTRACTED", rel)

    for command in cli_commands():
        node_id = "cli_" + slug(command)
        add_node(nodes, node_id, f"article-machine {command}", "code", "article_machine/cli.py")
        add_edge(edges, "module_cli", node_id, "defines_cli", "EXTRACTED", "article_machine/cli.py")
        add_edge(edges, "hub_runtime", node_id, "exposes", "EXTRACTED", "article_machine/cli.py")

    for project_dir in project_dirs():
        project = read_structured(project_dir / "project.yaml")
        protocol = read_structured(project_dir / "protocol.yaml")
        rel = project_dir.relative_to(ROOT).as_posix()
        label = project.get("name") or project_dir.name
        node_id = "project_" + slug(project_dir.name)
        add_node(nodes, node_id, str(label), "document", f"{rel}/project.yaml")
        add_edge(edges, "hub_projects", node_id, "contains", "EXTRACTED", f"{rel}/project.yaml")
        lane = str(project.get("lane") or "unknown")
        mode = str(project.get("state", {}).get("current_mode") or "unknown")
        ptype = str(project.get("project_type") or "unknown")
        for value, prefix, relation in [(lane, "lane", "uses_lane"), (mode, "mode", "current_mode"), (ptype, "type", "project_type")]:
            meta_id = f"{prefix}_{slug(value)}"
            add_node(nodes, meta_id, f"{prefix}: {value}", "rationale", f"{rel}/project.yaml")
            add_edge(edges, node_id, meta_id, relation, "EXTRACTED", f"{rel}/project.yaml")
        if not protocol.get("research_question"):
            add_edge(edges, node_id, "hub_git", "needs_review_missing_research_question", "INFERRED", f"{rel}/protocol.yaml", 0.6)

    skills_root = ROOT / "skills"
    for skill_name in CRITICAL_SKILLS:
        skill_path = skills_root / skill_name / "SKILL.md"
        if skill_path.exists():
            node_id = "skill_" + slug(skill_name)
            rel = skill_path.relative_to(ROOT).as_posix()
            add_node(nodes, node_id, skill_name, "document", rel)
            add_edge(edges, "hub_skills", node_id, "routes_to", "EXTRACTED", rel)
            add_edge(edges, "doc_SKILL_INDEX_md".lower(), node_id, "references", "INFERRED", "SKILL_INDEX.md", 0.8)

    for dirname in LEGACY_ROOT_DIRS:
        path = ROOT / dirname
        if path.exists():
            node_id = "legacy_" + slug(dirname)
            add_node(nodes, node_id, dirname, "document", dirname)
            add_edge(edges, "hub_legacy", node_id, "needs_triage", "INFERRED", dirname, 0.7)

    if (ROOT / "projects" / "projects").exists():
        add_node(nodes, "defect_nested_projects", "projects/projects nested directory", "rationale", "projects/projects")
        add_edge(edges, "hub_projects", "defect_nested_projects", "needs_review", "INFERRED", "projects/projects", 0.8)
        add_edge(edges, "defect_nested_projects", "hub_git", "hygiene_risk", "INFERRED", "projects/projects", 0.8)

    add_node(nodes, "graphify_outputs", "graphify-out graph.json graph.html GRAPH_REPORT.md", "document", "graphify-out")
    add_edge(edges, "hub_graphify", "graphify_outputs", "produces", "EXTRACTED", "scripts/generate_workspace_graph.py")
    add_edge(edges, "graphify_outputs", "hub_docs", "supports_agent_navigation", "INFERRED", "docs/AGENT_START_HERE.md", 0.8)

    communities = {
        0: ["workspace_doutorado", "hub_runtime", "runtime_venv_article_machine", "runtime_global_graphify", "runtime_pytest", "runtime_machine_audit"],
        1: ["hub_article_machine"] + [n for n in nodes if n.startswith("module_") or n.startswith("cli_")],
        2: ["hub_projects"] + [n for n in nodes if n.startswith("project_") or n.startswith("lane_") or n.startswith("mode_") or n.startswith("type_") or n == "defect_nested_projects"],
        3: ["hub_skills"] + [n for n in nodes if n.startswith("skill_")],
        4: ["hub_docs"] + [n for n in nodes if n.startswith("doc_")],
        5: ["hub_legacy"] + [n for n in nodes if n.startswith("legacy_")],
        6: ["hub_graphify", "graphify_outputs"],
        7: ["hub_git"],
    }
    communities = {cid: [n for n in members if n in nodes] for cid, members in communities.items()}
    labels = {
        0: "Runtime Commands",
        1: "Article Machine",
        2: "Projects And Modes",
        3: "Scientific Skills",
        4: "Agent Docs",
        5: "Legacy Sources",
        6: "Graphify Map",
        7: "Git Hygiene",
    }
    manifest = {
        "root": str(ROOT),
        "project_count": len(project_dirs()),
        "critical_skill_count": sum(1 for s in CRITICAL_SKILLS if (skills_root / s / "SKILL.md").exists()),
        "legacy_dirs_present": [d for d in LEGACY_ROOT_DIRS if (ROOT / d).exists()],
        "limitations": [
            "Operational graph only; full root semantic graph timed out and would mix caches, PDFs, and raw data.",
            "Edges marked INFERRED are navigation/risk inferences, not scientific evidence.",
            "Use project-specific graphify runs for manuscript evidence graphs.",
        ],
    }
    extraction = {"nodes": list(nodes.values()), "edges": edges, "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
    return extraction, communities, labels, manifest


def write_graph() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    extraction, communities, labels, manifest = build_extraction()
    (OUT / ".graphify_python").write_text(sys.executable, encoding="utf-8")
    (OUT / ".graphify_root").write_text(str(ROOT), encoding="utf-8")
    (OUT / ".graphify_extract.json").write_text(json.dumps(extraction, ensure_ascii=False, indent=2), encoding="utf-8")
    (OUT / "workspace_graph_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    from graphify.analyze import god_nodes, suggest_questions, surprising_connections
    from graphify.build import build_from_json
    from graphify.cluster import score_all
    from graphify.export import to_html, to_json
    from graphify.report import generate

    graph = build_from_json(extraction)
    cohesion = score_all(graph, communities)
    questions = [
        {
            "question": "How should a new agent choose an active Article Machine project?",
            "why": "Connects runtime commands, project modes, and required project files.",
        },
        {
            "question": "Which parts of the workspace are hygiene risks before committing?",
            "why": "Highlights untracked/generated areas, legacy folders, and nested projects.",
        },
        {
            "question": "How do Graphify and Article Machine runtimes differ in this checkout?",
            "why": "Shows the split between global graphify and the local Article Machine venv.",
        },
        {
            "question": "Which skills are mandatory before strong scientific claims?",
            "why": "Bridges critical scientific skills to the Article Machine gates.",
        },
    ]
    detection = {
        "total_files": manifest["project_count"] + manifest["critical_skill_count"] + len(manifest["legacy_dirs_present"]) + 8,
        "total_words": 0,
        "warning": "Root semantic graph was not run: the workspace is too broad and detection timed out. This is an operational navigation graph.",
    }
    report = generate(
        graph,
        communities,
        cohesion,
        labels,
        god_nodes(graph),
        surprising_connections(graph, communities),
        detection,
        {"input": 0, "output": 0},
        str(ROOT),
        suggested_questions=questions,
    )
    report += "\n\n## Operational Limitations\n"
    for item in manifest["limitations"]:
        report += f"- {item}\n"
    to_json(graph, communities, str(OUT / "graph.json"))
    to_html(graph, communities, str(OUT / "graph.html"), community_labels=labels)
    (OUT / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps({"status": "written", "nodes": graph.number_of_nodes(), "edges": graph.number_of_edges(), "out": str(OUT)}, indent=2))


if __name__ == "__main__":
    write_graph()
