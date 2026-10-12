import json
from pathlib import Path
from types import SimpleNamespace

import article_machine.agent_skills as agent_skills
import article_machine.cli as cli_module
import article_machine.journals as journals
import article_machine.zero_trust as zero_trust

from article_machine.cli import main
from article_machine.projects import init_project
from article_machine.serialization import save_structured_file
from article_machine.zero_trust import (
    audit_retrieval,
    audit_git_skill_reproducibility,
    audit_routing_canaries,
    audit_stage,
    build_retrieval_plan,
    compile_query_plan,
    run_guard_check,
    run_idea_tournament,
    run_machine_audit,
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


def _acceptance_benchmark(level: str = "acceptance") -> dict:
    return {
        "contract": "AgentBenchmarkReport",
        "level": level,
        "gate_eligible": True,
        "status": "pass",
        "aggregate_status": "pass",
        "cases": [{"id": "fixed-case-001", "status": "pass"}],
        "provenance": {
            "runtime": {"model": "gpt-5.6-sol", "reasoning_effort": "ultra"},
            "code_revision": "abc1234",
            "prompt_id": "prompt-benchmark-001",
        },
        "scoring": {
            dimension: {"status": "pass", "score": 0.9, "threshold": 0.8}
            for dimension in ("correctness", "provenance", "reproducibility", "safety", "usefulness")
        },
        "residual_risks": ["The fixed benchmark corpus does not cover every future project."],
    }


def _write_benchmark(project_dir: Path, payload: dict) -> None:
    (project_dir / "analysis" / "benchmark_report.json").write_text(
        json.dumps(payload),
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
    assert any("Review Trinity is missing, blocked or stale" in issue for issue in report["issues"])
    assert any("journal route/report is missing or blocked" in issue for issue in report["issues"])
    assert any("agent-benchmark-harness benchmark is missing" in issue for issue in report["issues"])


def test_stage_audit_rejects_legacy_status_pass_benchmark_but_reports_it(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Legacy Stage Benchmark", "systematic-review")
    _write_benchmark(project_dir, {"status": "pass"})

    report = audit_stage(project_dir, target_mode="submission")
    benchmark_check = next(check for check in report["checks"] if check["check"] == "benchmark")

    assert benchmark_check["status"] == "block"
    assert benchmark_check["validation"]["legacy_readable"] is True
    assert benchmark_check["validation"]["reported_status"] == "pass"
    assert benchmark_check["validation"]["gate_eligible"] is False


def test_stage_audit_never_accepts_smoke_or_comparative_benchmark(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Reporting Benchmark", "systematic-review")

    for level in ("smoke", "comparative"):
        _write_benchmark(project_dir, _acceptance_benchmark(level=level))
        report = audit_stage(project_dir, target_mode="submission")
        benchmark_check = next(check for check in report["checks"] if check["check"] == "benchmark")

        assert benchmark_check["status"] == "block"
        assert any("reporting-only" in issue for issue in benchmark_check["validation"]["issues"])


def test_stage_audit_blocks_self_declared_acceptance_without_verified_artifacts(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Acceptance Stage Benchmark", "systematic-review")
    _write_benchmark(project_dir, _acceptance_benchmark())

    report = audit_stage(project_dir, target_mode="submission")
    benchmark_check = next(check for check in report["checks"] if check["check"] == "benchmark")

    assert benchmark_check["status"] == "block"
    assert benchmark_check["validation"]["gate_eligible"] is False
    assert any("independently verified file-backed" in issue for issue in benchmark_check["validation"]["issues"])


def test_stage_audit_blocks_acceptance_benchmark_below_scoring_threshold(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Failed Score Benchmark", "systematic-review")
    benchmark = _acceptance_benchmark()
    benchmark["scoring"]["correctness"]["score"] = 0.7
    _write_benchmark(project_dir, benchmark)

    report = audit_stage(project_dir, target_mode="submission")
    benchmark_check = next(check for check in report["checks"] if check["check"] == "benchmark")

    assert benchmark_check["status"] == "block"
    assert benchmark_check["validation"]["gate_eligible"] is False


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
    assert main(["stage", "audit", str(project_dir), "--target-mode", "submission"]) == 1
    assert main(["guard", "check", str(project_dir)]) == 0
    assert main(["machine", "audit", "--workspace-root", str(Path(__file__).resolve().parents[1])]) == 0


def test_benchmark_validate_cli_returns_gate_aware_exit_code(tmp_path: Path, capsys) -> None:
    project_dir = init_project(tmp_path, "Benchmark CLI", "systematic-review")
    _write_benchmark(project_dir, _acceptance_benchmark())

    assert main(["benchmark", "validate", str(project_dir)]) == 1
    passing_payload = json.loads(capsys.readouterr().out)
    assert passing_payload["gate_eligible"] is False

    _write_benchmark(project_dir, _acceptance_benchmark(level="smoke"))
    assert main(["benchmark", "validate", str(project_dir)]) == 1
    blocked_payload = json.loads(capsys.readouterr().out)
    assert blocked_payload["gate_eligible"] is False


def test_routing_canaries_cover_literal_sol_ultra_machine_request() -> None:
    root = Path(__file__).resolve().parents[1]

    report = audit_routing_canaries(root / "skills")

    assert report["status"] == "pass"
    canary = next(item for item in report["canaries"] if item["id"] == "current_sol_ultra_machine_upgrade")
    assert {"skill-upgrade-governor", "agent-benchmark-harness"} <= set(canary["selected_skills"])


def test_git_skill_reproducibility_blocks_untracked_required_skill(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / ".git").mkdir()
    captured: dict = {}

    def fake_run(command, **kwargs):
        captured.setdefault("commands", []).append(command)
        captured["env"] = kwargs["env"]
        if "ls-tree" in command:
            return SimpleNamespace(returncode=0, stdout=b"skills/tracked/SKILL.md\0", stderr=b"")
        return SimpleNamespace(returncode=0, stdout=b"skills/tracked/SKILL.md\0", stderr=b"")

    monkeypatch.setattr(zero_trust.subprocess, "run", fake_run)

    report = audit_git_skill_reproducibility(tmp_path, required_skills=("tracked", "missing"))

    assert report["status"] == "block"
    assert report["tracked_skills"] == ["tracked"]
    assert report["untracked_skills"] == ["missing"]
    assert report["committed_skills"] == ["tracked"]
    assert report["uncommitted_skills"] == ["missing"]
    assert all(command[-2:] == ["--", "skills"] for command in captured["commands"])
    assert captured["env"]["GIT_CONFIG_NOSYSTEM"] == "1"


def test_git_skill_reproducibility_blocks_skill_only_staged_in_index(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / ".git").mkdir()

    def fake_run(command, **_kwargs):
        if "ls-tree" in command:
            return SimpleNamespace(returncode=0, stdout=b"skills/committed/SKILL.md\0", stderr=b"")
        return SimpleNamespace(
            returncode=0,
            stdout=b"skills/committed/SKILL.md\0skills/staged/SKILL.md\0",
            stderr=b"",
        )

    monkeypatch.setattr(zero_trust.subprocess, "run", fake_run)

    report = audit_git_skill_reproducibility(tmp_path, required_skills=("committed", "staged"))

    assert report["status"] == "block"
    assert report["tracked_skills"] == ["committed", "staged"]
    assert report["committed_skills"] == ["committed"]
    assert report["staged_only_skills"] == ["staged"]
    assert report["uncommitted_skills"] == ["staged"]
    assert "clean clone" in " ".join(report["issues"])


def test_git_skill_reproducibility_passes_only_when_all_skills_are_in_head_and_index(
    tmp_path: Path, monkeypatch
) -> None:
    (tmp_path / ".git").mkdir()
    paths = b"skills/one/SKILL.md\0skills/two/SKILL.md\0"
    monkeypatch.setattr(
        zero_trust.subprocess,
        "run",
        lambda _command, **_kwargs: SimpleNamespace(returncode=0, stdout=paths, stderr=b""),
    )

    report = audit_git_skill_reproducibility(tmp_path, required_skills=("one", "two"))

    assert report["status"] == "pass"
    assert report["tracked_skills"] == ["one", "two"]
    assert report["committed_skills"] == ["one", "two"]
    assert report["untracked_skills"] == []
    assert report["uncommitted_skills"] == []


def _patch_passing_machine_audit_dependencies(monkeypatch) -> None:
    monkeypatch.setattr(zero_trust, "validate_provider_specs", lambda: {"status": "pass", "issues": []})
    monkeypatch.setattr(agent_skills, "audit_workspace_skills", lambda _path: {"status": "pass", "issues": []})
    monkeypatch.setattr(journals, "verify_journal_presets", lambda: {"status": "pass", "issues": []})
    monkeypatch.setattr(zero_trust, "audit_operational_graph", lambda _root: {"status": "pass", "issues": []})
    monkeypatch.setattr(zero_trust, "audit_routing_canaries", lambda _path: {"status": "pass", "issues": []})
    monkeypatch.setattr(zero_trust, "audit_git_skill_reproducibility", lambda _root: {"status": "pass", "issues": []})


def test_machine_audit_strict_passes_read_only_when_every_strict_check_passes(tmp_path: Path, monkeypatch) -> None:
    _patch_passing_machine_audit_dependencies(monkeypatch)
    (tmp_path / "reviews").mkdir()

    report = run_machine_audit(tmp_path, strict=True)

    assert report["status"] == "pass"
    assert report["strict"] is True
    assert report["read_only"] is True
    assert set(report["reports"]) >= {
        "operational_graph",
        "routing_canaries",
        "git_skill_reproducibility",
    }
    assert not (tmp_path / "reviews" / "machine_audit_report.json").exists()


def test_machine_audit_strict_failure_blocks_and_only_strict_cli_is_nonzero(tmp_path: Path, monkeypatch) -> None:
    _patch_passing_machine_audit_dependencies(monkeypatch)
    monkeypatch.setattr(
        zero_trust,
        "audit_operational_graph",
        lambda _root: {"status": "block", "issues": ["simulated graph reconciliation failure"]},
    )

    report = run_machine_audit(tmp_path, strict=True)

    assert report["status"] == "block"
    assert "simulated graph reconciliation failure" in report["issues"]

    monkeypatch.setattr(cli_module, "run_machine_audit", lambda _root, strict=False: {"status": "block"})
    assert main(["machine", "audit", "--workspace-root", str(tmp_path)]) == 0
    assert main(["machine", "audit", "--workspace-root", str(tmp_path), "--strict"]) == 1
