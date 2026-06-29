from pathlib import Path

from article_machine.cli import main
from article_machine.projects import init_project
from article_machine.serialization import save_structured_file
from article_machine.zero_trust import (
    audit_retrieval,
    audit_stage,
    build_retrieval_plan,
    compile_query_plan,
    run_guard_check,
    run_idea_tournament,
    validate_provider_specs,
    validate_query_plan,
)


def _write_valid_query_plan(project_dir: Path, providers: list[str] | None = None) -> None:
    save_structured_file(
        project_dir / "context" / "query_plan.yaml",
        {
            "contract": "QueryPlan",
            "topic": "Biomarkers in acute intestinal ischemia",
            "providers": providers or ["pubmed", "europe_pmc", "openalex", "crossref"],
            "boolean": "AND",
            "concepts": [
                {
                    "id": "disease",
                    "terms": ["intestinal ischemia", "mesenteric ischemia"],
                    "field": "title",
                },
                {
                    "id": "biomarker",
                    "terms": ["biomarker"],
                    "synonyms": ["diagnostic marker"],
                    "field": "title",
                },
            ],
            "exclusions": [{"id": "animals", "terms": ["animal"], "field": "title"}],
            "date_range": {"from": "2020-01-01", "to": "2026-04-26"},
            "languages": ["english"],
            "limits": {"max_records": 200},
            "rationale": "Offline query contract for a deterministic test fixture.",
        },
    )


def _seed_passing_evidence(project_dir: Path) -> None:
    (project_dir / "drafts" / "manuscript.md").write_text(
        "# Manuscript\n\nBiomarkers can be compared {{claim:claim-001}}.\n",
        encoding="utf-8",
    )
    (project_dir / "sources" / "study-001.md").write_text(
        "Biomarkers can be compared in acute intestinal ischemia.\n",
        encoding="utf-8",
    )
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-001","statement":"Biomarkers can be compared.",'
            '"source_path":"sources/study-001.md","source_excerpt":"Biomarkers can be compared in acute intestinal ischemia.",'
            '"reference_key":"smith2024","status":"supported","doi":"10.1000/test.1","pmid":"123456"}\n'
        ),
        encoding="utf-8",
    )
    (project_dir / "drafts" / "references.bib").write_text(
        "@article{smith2024,\n  title={A Study},\n  year={2024}\n}\n",
        encoding="utf-8",
    )


def test_query_validate_and_compile_are_deterministic(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Valid Query", "systematic-review")
    _write_valid_query_plan(project_dir)

    validation = validate_query_plan(project_dir)
    first = compile_query_plan(project_dir)
    second = compile_query_plan(project_dir)

    assert validation["status"] == "pass"
    assert first["status"] == "pass"
    assert {item["provider"] for item in first["compiled_queries"]} == {"pubmed", "europe_pmc", "openalex", "crossref"}
    assert [item["query_hash"] for item in first["compiled_queries"]] == [
        item["query_hash"] for item in second["compiled_queries"]
    ]
    assert all(len(item["query_hash"]) == 64 for item in first["compiled_queries"])
    assert (project_dir / "context" / "retrieval" / "compiled_queries.json").exists()


def test_query_validate_blocks_unsafe_terms_and_incompatible_fields(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Invalid Query", "systematic-review")
    save_structured_file(
        project_dir / "context" / "query_plan.yaml",
        {
            "contract": "QueryPlan",
            "topic": "Unsafe query",
            "providers": ["crossref"],
            "boolean": "XOR",
            "concepts": [
                {"id": "bad-boolean", "terms": ["cancer OR tumor"], "field": "title"},
                {"id": "bad-wildcard", "terms": ["a*"], "field": "title"},
                {"id": "bad-field", "terms": ["humans"], "field": "mesh"},
                {"id": "bad-parentheses", "terms": ["(broken"], "field": "title"},
            ],
        },
    )

    report = validate_query_plan(project_dir)

    assert report["status"] == "block"
    assert any("raw boolean logic" in issue for issue in report["issues"])
    assert any("dangerous wildcard" in issue for issue in report["issues"])
    assert any("incompatible with provider 'crossref'" in issue for issue in report["issues"])
    assert any("broken parentheses" in issue for issue in report["issues"])
    assert any("must be AND or OR" in issue for issue in report["issues"])


def test_provider_spec_audit_blocks_missing_rate_limit() -> None:
    report = validate_provider_specs(
        {
            "bad": {
                "contract": "ProviderSpec",
                "provider": "bad",
                "source_url": "https://example.invalid",
                "base_url": "https://example.invalid",
                "supported_fields": ["title"],
                "requires_manifest_fields": ["provider", "query_hash", "retrieved_at", "record_count", "records_sha256"],
            }
        }
    )

    assert report["status"] == "block"
    assert any("rate_limit" in issue for issue in report["issues"])


def test_retrieval_plan_and_manifest_audit_are_offline(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Retrieval Audit", "systematic-review")
    _write_valid_query_plan(project_dir, providers=["pubmed"])

    plan = build_retrieval_plan(project_dir)
    blocked_audit = audit_retrieval(project_dir)
    query_hash = plan["compiled_queries"][0]["query_hash"]
    save_structured_file(
        project_dir / "evidence" / "retrieval" / "pubmed.json",
        {
            "provider": "pubmed",
            "query_hash": query_hash,
            "retrieved_at": "2026-04-26T00:00:00+00:00",
            "record_count": 0,
            "records_sha256": "a" * 64,
        },
    )
    passing_audit = audit_retrieval(project_dir)

    assert plan["status"] == "pass"
    assert blocked_audit["status"] == "block"
    assert any("No retrieval manifests" in issue for issue in blocked_audit["issues"])
    assert passing_audit["status"] == "pass"


def test_idea_tournament_blocks_promotion_without_required_evidence(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Ideas", "systematic-review")
    save_structured_file(
        project_dir / "context" / "ideas" / "idea_candidates.json",
        {
            "ideas": [
                {
                    "idea_id": "weak",
                    "title": "Weak idea",
                    "novelty_status": "",
                    "database_plan": "",
                    "red_team_notes": [],
                },
                {
                    "idea_id": "strong",
                    "title": "Registry-based transplant outcomes study",
                    "novelty_status": "probably-novel",
                    "database_plan": "SRTR-like registry variables will be audited before analysis.",
                    "red_team_notes": ["Confounding and missingness may kill causal claims."],
                    "feasibility": 12,
                    "journal_fit": 10,
                    "author_fit": 6,
                    "ethical_risk": 2,
                    "statistical_risk": 4,
                    "publication_chance": 11,
                },
            ]
        },
    )

    report = run_idea_tournament(project_dir)

    assert report["status"] == "block"
    assert report["ranked_ideas"][0]["idea_id"] == "strong"
    assert any("weak: missing required field" in issue for issue in report["issues"])


def test_stage_audit_blocks_submission_without_review_journal_and_benchmark(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Stage Audit", "systematic-review")
    _seed_passing_evidence(project_dir)
    _write_valid_query_plan(project_dir, providers=["pubmed"])
    build_retrieval_plan(project_dir)

    report = audit_stage(project_dir, target_mode="submission")

    assert report["status"] == "block"
    assert any("Review Trinity aggregate_status is not pass" in issue for issue in report["issues"])
    assert any("journal route/report is missing or blocked" in issue for issue in report["issues"])
    assert any("agent-benchmark-harness benchmark is missing" in issue for issue in report["issues"])


def test_stage_audit_pass_messages_do_not_read_like_failures(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Stage Audit Messages", "systematic-review")

    report = audit_stage(project_dir, target_mode="protocol-freeze")
    passed_messages = [check["message"].lower() for check in report["checks"] if check["status"] == "pass"]

    assert passed_messages
    assert not any("missing" in message or "empty" in message or "not frozen" in message for message in passed_messages)


def test_guard_check_aggregates_zero_trust_reports(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Guard", "systematic-review")
    _write_valid_query_plan(project_dir, providers=["pubmed"])

    report = run_guard_check(project_dir)

    assert report["status"] == "block"
    assert "evidence_lock" in report["reports"]
    assert "query_validation" in report["reports"]
    assert "retrieval_audit" in report["reports"]
    assert "stage_audit" in report["reports"]
    assert (project_dir / "reviews" / "guardrail_report.json").exists()


def test_zero_trust_cli_commands_return_json_status(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "CLI Zero Trust", "systematic-review")
    _write_valid_query_plan(project_dir, providers=["pubmed"])

    assert main(["query", "validate", str(project_dir)]) == 0
    assert main(["query", "compile", str(project_dir)]) == 0
    assert main(["retrieval", "plan", str(project_dir)]) == 0
    assert main(["retrieval", "audit", str(project_dir)]) == 0
    assert main(["idea", "tournament", str(project_dir)]) == 0
    assert main(["stage", "audit", str(project_dir), "--target-mode", "submission"]) == 0
    assert main(["guard", "check", str(project_dir)]) == 0
    assert main(["machine", "audit", "--workspace-root", str(Path(__file__).resolve().parents[1])]) == 0
