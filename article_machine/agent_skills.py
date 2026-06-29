from __future__ import annotations

from pathlib import Path
import re
import unicodedata
from typing import Any


WORLD_CLASS_SKILLS: tuple[str, ...] = (
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
)


ROUTE_RULES: tuple[dict[str, Any], ...] = (
    {
        "skill": "hypothesis-tournament",
        "triggers": (
            "hypothesis",
            "hypotheses",
            "hipotese",
            "hipoteses",
            "idea",
            "ideia",
            "mechanism",
            "mecanismo",
            "target prioritization",
            "priorizacao",
            "drug repurposing",
            "descobrir",
            "aim",
        ),
        "reason": "Generate, critique, rank, and evolve testable scientific hypotheses.",
    },
    {
        "skill": "scientific-novelty-checker",
        "triggers": ("novel", "novelty", "novidade", "new mechanism", "first", "prior art", "already known", "incremental"),
        "reason": "Check novelty boundaries before strong claims or project commitment.",
    },
    {
        "skill": "experimental-design-planner",
        "triggers": (
            "experiment",
            "experimento",
            "experimental design",
            "validation experiment",
            "validacao",
            "controls",
            "controles",
            "endpoint",
            "sample size",
            "randomization",
            "blinding",
        ),
        "reason": "Convert a hypothesis into a protocol-ready design with controls and endpoints.",
    },
    {
        "skill": "experimental-design",
        "triggers": (
            "study design",
            "experimental design",
            "design of experiments",
            "doe",
            "randomization",
            "randomizacao",
            "blocking",
            "stratification",
            "factorial",
            "crossover",
            "plate layout",
            "batch effects",
            "pseudoreplication",
            "assign subjects",
            "assign samples",
            "setup this experiment",
            "confounding",
        ),
        "reason": "Use upstream DOE/randomization guidance before data collection.",
    },
    {
        "skill": "statistical-power",
        "triggers": (
            "sample size",
            "tamanho amostral",
            "power analysis",
            "statistical power",
            "80% power",
            "mde",
            "minimum detectable effect",
            "replicates",
            "replicatas",
            "quantos pacientes",
            "quantas amostras",
            "grant sample size",
        ),
        "reason": "Calculate defensible sample size and power before collection or protocol claims.",
    },
    {
        "skill": "ro-crate-provenance-export",
        "triggers": (
            "provenance",
            "proveniencia",
            "ro-crate",
            "fair",
            "replay",
            "reproduce",
            "reproducible",
            "reprodutibilidade",
            "hash",
            "manifest",
            "workflow run crate",
        ),
        "reason": "Package runs with hashes, environment, commands, inputs, and outputs.",
    },
    {
        "skill": "nextflow-pipeline-runner",
        "triggers": ("nextflow", "nf-core", "hpc", "cloud pipeline", "many samples", "containerized pipeline", "genomics pipeline"),
        "reason": "Use a scalable, production-grade pipeline when local scripts are insufficient.",
    },
    {
        "skill": "nextflow",
        "triggers": (
            "nextflow",
            "nf-core",
            "dsl2",
            "nextflow.config",
            "samplesheet",
            "slurm",
            "apptainer",
            "singularity",
            "wave",
            "resume run",
            "nf-test",
            "sarek",
            "rnaseq",
        ),
        "reason": "Build, run, and debug upstream Nextflow or nf-core workflows.",
    },
    {
        "skill": "bulk-rnaseq",
        "triggers": (
            "bulk rna-seq",
            "bulk rnaseq",
            "rna-seq",
            "rnaseq",
            "fastq",
            "fastqc",
            "star",
            "salmon",
            "featurecounts",
            "differential expression",
            "deseq2",
            "pydeseq2",
            "counts matrix",
        ),
        "reason": "Route raw or quantified bulk RNA-seq work through QC, quantification, DE, and figures.",
    },
    {
        "skill": "pathway-enrichment",
        "triggers": (
            "pathway enrichment",
            "enrichment analysis",
            "gene set",
            "gsea",
            "preranked",
            "go enrichment",
            "kegg",
            "reactome",
            "msigdb",
            "enrichr",
            "gene list",
            "differentially expressed genes",
        ),
        "reason": "Interpret gene lists or ranked genes with enrichment methods and correction gates.",
    },
    {
        "skill": "snakemake-pipeline-runner",
        "triggers": ("snakemake", "snakefile", "rules", "dry-run", "workflow report", "multi-step analysis"),
        "reason": "Turn local Python/R analyses into transparent rule-based workflows.",
    },
    {
        "skill": "cwl-workflow-bridge",
        "triggers": ("cwl", "common workflow language", "vendor-neutral", "workflow exchange", "portable workflow"),
        "reason": "Describe command-line workflows in a portable standard format.",
    },
    {
        "skill": "asreview-screening-bridge",
        "triggers": (
            "asreview",
            "active learning",
            "screening",
            "triagem",
            "revisao sistematica",
            "title abstract",
            "rayyan",
            "prioritization",
            "stopping rule",
        ),
        "reason": "Use active learning for review screening without losing auditability.",
    },
    {
        "skill": "risk-of-bias-assistant",
        "triggers": ("risk of bias", "risco de vies", "vies", "rob 2", "robins-i", "quadas", "probast", "amstar", "robis", "syrcle", "bias"),
        "reason": "Route study design to the correct bias tool with evidence snippets.",
    },
    {
        "skill": "grade-sof-table-builder",
        "triggers": ("grade", "summary of findings", "sof", "certainty", "certeza", "evidence profile", "downgrade", "imprecision"),
        "reason": "Build GRADE certainty and Summary of Findings outputs.",
    },
    {
        "skill": "openalex-literature-graph",
        "triggers": ("openalex", "citation graph", "bibliometric", "literature graph", "literatura", "works", "authors", "venue", "topic map"),
        "reason": "Map literature metadata, citation neighborhoods, venues, and topics.",
    },
    {
        "skill": "open-targets-drug-targeting",
        "triggers": (
            "open targets",
            "target disease",
            "target validation",
            "tractability",
            "safety",
            "known drugs",
            "drug target",
            "alvo",
            "alvos",
            "drogas",
            "descoberta de drogas",
        ),
        "reason": "Ground target prioritization in Open Targets evidence.",
    },
    {
        "skill": "chembl-bindingdb-miner",
        "triggers": ("chembl", "bindingdb", "pubchem", "compound", "composto", "ligand", "ligante", "ic50", "ki", "ec50", "smiles", "admet"),
        "reason": "Mine chemistry and binding databases with assay-context safeguards.",
    },
    {
        "skill": "alphafold-pdb-structure-router",
        "triggers": ("alphafold", "pdb", "protein structure", "estrutura", "proteina", "plddt", "pae", "binding pocket", "docking preparation", "structure"),
        "reason": "Route protein structure work across AlphaFold, PDB, and confidence checks.",
    },
    {
        "skill": "in-silico-validation-governor",
        "triggers": ("in silico", "docking", "virtual screening", "digital twin", "simulation", "simulacao", "model validation", "validar", "validacao", "overclaim", "leakage"),
        "reason": "Assign validation labels and prevent computational overclaims.",
    },
    {
        "skill": "agent-benchmark-harness",
        "triggers": (
            "benchmark",
            "evaluate agent",
            "baseline",
            "harness",
            "best",
            "perfect",
            "perfeito",
            "melhor",
            "world-class",
            "regression",
            "score",
            "quality audit",
        ),
        "reason": "Prove capability with benchmark tasks and scoring rather than impressions.",
    },
    {
        "skill": "scientific-red-team-reviewer",
        "triggers": ("red team", "stress test", "review critically", "revisar criticamente", "hallucination", "weak evidence", "causal overreach", "flaw", "falha"),
        "reason": "Attack claims and artifacts before submission or dissemination.",
    },
    {
        "skill": "query-string-governor",
        "triggers": (
            "query",
            "search string",
            "boolean string",
            "pubmed string",
            "string de busca",
            "strings",
            "operador booleano",
            "parentheses",
            "wildcard",
        ),
        "reason": "Compile and block unsafe search strings before database retrieval.",
    },
    {
        "skill": "database-retrieval-governor",
        "triggers": (
            "database",
            "banco de dados",
            "retrieval",
            "pubmed",
            "europe pmc",
            "crossref",
            "openalex",
            "orcid",
            "ror",
            "manifest",
        ),
        "reason": "Plan database retrieval with provider contracts, rate limits, cache, and manifests.",
    },
    {
        "skill": "exa-search",
        "triggers": (
            "web search",
            "search the web",
            "look up",
            "current info",
            "latest",
            "fetch url",
            "extract url",
            "academic domain",
            "research paper category",
            "buscar na web",
        ),
        "reason": "Use Exa-backed web retrieval when a current or URL-level search surface is needed.",
    },
    {
        "skill": "liteparse",
        "triggers": (
            "pdf parsing",
            "parse pdf",
            "document parsing",
            "extract pdf",
            "extract text",
            "ocr",
            "bounding boxes",
            "bboxes",
            "page renders",
            "batch ingest",
            "scanned pdf",
            "office files",
        ),
        "reason": "Use local parsing and OCR when document layout, bboxes, or scan handling matter.",
    },
    {
        "skill": "paper-lookup",
        "triggers": (
            "paper lookup",
            "find paper",
            "paper doi",
            "doi lookup",
            "pmid lookup",
            "full text",
            "article metadata",
            "paper metadata",
        ),
        "reason": "Resolve papers and metadata before writing or citing manuscript claims.",
    },
    {
        "skill": "research-lookup",
        "triggers": (
            "research lookup",
            "literature lookup",
            "literature search",
            "prior literature",
            "related work",
            "paper search",
            "bibliography search",
        ),
        "reason": "Find and structure literature before synthesis or manuscript drafting.",
    },
    {
        "skill": "topic-ideation-tournament",
        "triggers": (
            "tema",
            "temas",
            "topic",
            "ideation",
            "idea",
            "ideia",
            "research question",
            "pergunta de pesquisa",
            "publicavel",
        ),
        "reason": "Rank research ideas by novelty, data availability, feasibility, journal fit, and red-team risk.",
    },
    {
        "skill": "evidence-lock-hardener",
        "triggers": (
            "evidence lock",
            "claim",
            "source excerpt",
            "anti hallucination",
            "anti-alucinacao",
            "alucinacao",
            "hallucination",
            "citation",
            "trecho",
        ),
        "reason": "Harden claim/source/reference gates so unsupported factual text cannot pass.",
    },
    {
        "skill": "stage-audit-governor",
        "triggers": (
            "stage audit",
            "etapa",
            "auditoria de etapas",
            "mode gate",
            "submission gate",
            "bloquear etapa",
            "workflow gate",
        ),
        "reason": "Audit project modes and block advancement when required artifacts are incomplete.",
    },
    {
        "skill": "author-identity-resolver",
        "triggers": (
            "author fit",
            "autor",
            "orcid",
            "professor",
            "affiliation",
            "afiliacao",
            "andre",
            "nivaldo",
            "pubmed author",
        ),
        "reason": "Resolve authors and affiliations only from verified ORCID/PubMed/ROR evidence.",
    },
    {
        "skill": "guideline-router",
        "triggers": (
            "prisma",
            "consort",
            "strobe",
            "equator",
            "reporting guideline",
            "guideline",
            "checklist",
            "diretriz",
        ),
        "reason": "Route manuscript type to the correct reporting guideline before drafting or review.",
    },
    {
        "skill": "retraction-integrity-checker",
        "triggers": (
            "retraction",
            "retratacao",
            "expression of concern",
            "corrigendum",
            "erratum",
            "integrity",
            "crossmark",
        ),
        "reason": "Check cited records for retraction, expressions of concern, corrections, and integrity flags.",
    },
    {
        "skill": "ptbr-article-writing",
        "triggers": (
            "portugues",
            "português",
            "pt-br",
            "ptbr",
            "brazilian portuguese",
            "artigo cientifico",
            "artigo científico",
            "manuscrito em portugues",
            "manuscrito em português",
            "resumo em portugues",
            "resumo em português",
            "redacao cientifica",
            "redação científica",
            "escrita cientifica",
            "escrita científica",
            "traducao",
            "tradução",
            "translated from english",
            "translationese",
            "ptbr-audit",
            "ptbr-brief",
            "ptbr-naturalize",
            "abnt",
            "nbr 6023",
            "nbr 10520",
            "nbr 14724",
            "nbr 6028",
            "vancouver",
            "icmje",
            "nlm",
            "citing medicine",
            "referencias",
            "referências",
            "citacoes",
            "citações",
            "bibliografia",
            "reference style",
            "citation style",
        ),
        "reason": "Draft, naturalize, and audit claim-safe scientific writing and citation style in Brazilian Portuguese.",
    },
    {
        "skill": "life-science-router",
        "triggers": ("gene", "variant", "protein", "proteina", "drug", "omics", "microbiome", "microbioma", "clinical trial", "ensaio clinico", "pathway", "biomedical", "biomedico"),
        "reason": "Route biomedical retrieval through Life Science Research plugin skills.",
    },
    {
        "skill": "bids",
        "triggers": (
            "bids",
            "brain imaging data structure",
            "dicom to bids",
            "bids validator",
            "mri",
            "eeg",
            "meg",
            "pet",
            "ieeg",
            "nirs",
        ),
        "reason": "Use BIDS conventions for biomedical imaging dataset organization and validation.",
    },
    {
        "skill": "onekgpd",
        "triggers": (
            "1000 genomes",
            "1000 genomes project",
            "onekgpd",
            "grch38",
            "variant carriers",
            "homozygous reference",
            "population allele frequency",
            "alphamissense",
        ),
        "reason": "Query individual-level 1000 Genomes variant evidence with population annotations.",
    },
    {
        "skill": "tamarind",
        "triggers": (
            "tamarind",
            "tamarind.bio",
            "cloud gpu biology",
            "protein design",
            "binder design",
            "boltz",
            "chai",
            "rfdiffusion",
            "proteinmpnn",
            "diffdock",
            "autodock vina",
            "binding affinity",
        ),
        "reason": "Route cloud structural-biology and molecular-design jobs through Tamarind safeguards.",
    },
    {
        "skill": "pacsomatic",
        "triggers": (
            "pacsomatic",
            "nf-core/pacsomatic",
            "matched tumor-normal",
            "tumor normal",
            "somatic pipeline",
            "bam inputs",
        ),
        "reason": "Prepare and validate nf-core/pacsomatic tumor-normal workflow launches.",
    },
    {
        "skill": "hugging-science",
        "triggers": (
            "hugging science",
            "scientific datasets",
            "scientific models",
            "hugging face science",
            "hf inference",
            "gradio scientific",
            "scientific ml",
        ),
        "reason": "Discover scientific ML datasets, models, demos, and method citations.",
    },
    {
        "skill": "arbor",
        "triggers": (
            "arbor",
            "hypothesis tree",
            "htr",
            "improve this agent",
            "improve this harness",
            "beat the baseline",
            "many experiments",
            "iteratively optimize",
            "dev test gap",
            "optimize pipeline",
        ),
        "reason": "Use hypothesis-tree refinement for benchmarked iterative optimization.",
    },
    {
        "skill": "autoskill",
        "triggers": (
            "autoskill",
            "screenpipe",
            "repeated workflows",
            "draft new skills",
            "propose skills",
            "skill gaps",
            "workflow patterns",
        ),
        "reason": "Detect repeated workflows and draft new skills only when local screenpipe evidence exists.",
    },
    {
        "skill": "pi-agent",
        "triggers": (
            "pi agent",
            "pi coding agent",
            "pi terminal",
            "pi skills",
            "pi extensions",
            "pi subagents",
            "pi mcp",
        ),
        "reason": "Build or use Pi as a terminal coding harness and skill host.",
    },
    {
        "skill": "conference-deliverable-router",
        "triggers": ("slides", "poster", "congress", "congresso", "conference", "abstract", "oral presentation", "apresentacao oral", "handout", "submission pack"),
        "reason": "Use the HTML-first congress deliverable pipeline with Evidence Lock.",
    },
)


def _workspace_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _skills_dir(skills_dir: Path | None = None) -> Path:
    return Path(skills_dir) if skills_dir else _workspace_root() / "skills"


def _parse_frontmatter(skill_path: Path) -> dict[str, str]:
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {"name": skill_path.parent.name, "description": ""}
    parts = text.split("---", 2)
    payload: dict[str, str] = {}

    current_key: str | None = None
    current_lines: list[str] = []

    def clean(value: str) -> str:
        return value.strip().strip('"').strip("'")

    def flush_multiline() -> None:
        nonlocal current_key, current_lines
        if current_key:
            payload[current_key] = clean(" ".join(line.strip() for line in current_lines if line.strip()))
        current_key = None
        current_lines = []

    for line in parts[1].splitlines():
        if current_key and (line.startswith(" ") or line.startswith("\t") or not line.strip()):
            current_lines.append(line)
            continue
        flush_multiline()
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in {"name", "description"}:
            continue
        value = value.strip()
        if value in {">", "|", ">-", "|-", ">+", "|+"}:
            current_key = key
            current_lines = []
        else:
            payload[key] = clean(value)
    flush_multiline()
    payload.setdefault("name", skill_path.parent.name)
    payload.setdefault("description", "")
    return payload


def catalog_workspace_skills(skills_dir: Path | None = None) -> dict:
    root = _skills_dir(skills_dir)
    skills: dict[str, dict] = {}
    if not root.exists():
        return {"status": "missing", "skills_dir": str(root), "skills": {}, "skill_count": 0}

    for skill_md in sorted(root.glob("*/SKILL.md")):
        meta = _parse_frontmatter(skill_md)
        name = meta["name"]
        skills[name] = {
            "name": name,
            "description": meta["description"],
            "skill_file": str(skill_md),
        }
    return {
        "status": "available",
        "skills_dir": str(root),
        "skills": skills,
        "skill_count": len(skills),
        "world_class_skills": list(WORLD_CLASS_SKILLS),
    }


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.lower())
    return "".join(character for character in normalized if not unicodedata.combining(character))


def _trigger_matches(query: str, trigger: str) -> bool:
    trigger_normalized = _normalize_text(trigger)
    pattern = re.escape(trigger_normalized).replace("\\ ", r"\s+")
    if re.search(rf"\b{pattern}\b", query):
        return True
    return len(trigger_normalized) >= 5 and trigger_normalized in query


def route_workspace_skills(query: str, skills_dir: Path | None = None, limit: int = 8) -> dict:
    normalized = re.sub(r"\s+", " ", _normalize_text((query or "").strip()))
    catalog = catalog_workspace_skills(skills_dir)
    available = catalog.get("skills", {})
    matches: list[dict] = []

    for rule in ROUTE_RULES:
        matched = [trigger for trigger in rule["triggers"] if _trigger_matches(normalized, trigger)]
        if not matched or rule["skill"] not in available:
            continue
        matches.append(
            {
                "skill": rule["skill"],
                "matched_triggers": matched,
                "reason": rule["reason"],
                "skill_file": available[rule["skill"]]["skill_file"],
            }
        )

    matches.sort(key=lambda item: (-len(item["matched_triggers"]), item["skill"]))
    return {
        "status": "routed" if matches else "no-match",
        "query": query,
        "selected_skills": matches[:limit],
        "guidance": "Use the selected skills before attempting the task directly. If no skill matches, proceed normally and consider creating a skill if the workflow repeats.",
    }


def audit_workspace_skills(skills_dir: Path | None = None) -> dict:
    catalog = catalog_workspace_skills(skills_dir)
    skills = catalog.get("skills", {})
    issues: list[str] = []
    for skill_name in WORLD_CLASS_SKILLS:
        skill = skills.get(skill_name)
        if not skill:
            issues.append(f"{skill_name} is missing.")
            continue
        description = str(skill.get("description") or "")
        if not description.startswith("Use when"):
            issues.append(f"{skill_name} description must start with 'Use when'.")
        if "TODO" in description:
            issues.append(f"{skill_name} description still contains TODO text.")
    return {
        "status": "pass" if not issues else "block",
        "skills_dir": catalog.get("skills_dir"),
        "checked_skills": list(WORLD_CLASS_SKILLS),
        "issues": issues,
    }
