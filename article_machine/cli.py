from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .agent_skills import audit_workspace_skills, catalog_workspace_skills, route_workspace_skills
from .analysis import preflight, run_r_script
from .context import build_task_packet
from .congress_profiles import save_congress_profile, use_congress_profile
from .deliverables import (
    build_deliverable,
    export_deliverable,
    import_conference_requirements,
    plan_deliverable,
    qa_deliverable,
    submit_deliverable,
)
from .discovery import build_discovery_plan
from .evidence import validate_evidence_lock
from .ingest import register_source
from .journals import catalog_journals, route_journals, verify_journal_presets, write_journal_report
from .life_science import catalog_life_science_skills, plan_life_science_retrieval
from .projects import advance_mode, init_project, register_review_protocol
from .ptbr_style import audit_text, build_generation_brief, naturalize_text, read_text_for_audit, write_audit_reports
from .review import run_review_trinity
from .zero_trust import (
    audit_retrieval,
    audit_stage,
    build_retrieval_plan,
    compile_query_plan,
    run_guard_check,
    run_idea_tournament,
    run_machine_audit,
    validate_query_plan,
)


def _print(payload: Any) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="article-machine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("name")
    init_parser.add_argument("--type", required=True, dest="project_type")
    init_parser.add_argument("--workspace-root", default=".")

    preflight_parser = subparsers.add_parser("preflight")
    preflight_parser.add_argument("project_dir")

    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("project_dir")
    ingest_parser.add_argument("--source", required=True)
    ingest_parser.add_argument("--kind", default="note")

    registry_parser = subparsers.add_parser("registry")
    registry_sub = registry_parser.add_subparsers(dest="registry_command", required=True)
    registry_register = registry_sub.add_parser("register")
    registry_register.add_argument("project_dir")
    registry_register.add_argument("--registry", required=True)
    registry_register.add_argument("--id", required=True, dest="registry_id")
    registry_register.add_argument("--url", required=True, dest="registry_url")
    registry_register.add_argument("--registered-at", required=True, dest="registered_at")
    registry_register.add_argument("--notes", default="")

    context_parser = subparsers.add_parser("context")
    context_sub = context_parser.add_subparsers(dest="context_command", required=True)
    context_build = context_sub.add_parser("build")
    context_build.add_argument("project_dir")
    context_build.add_argument("--mode", required=True)
    context_build.add_argument("--hypothesis")

    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("project_dir")
    analyze_parser.add_argument("--mode", required=True)
    analyze_parser.add_argument("--hypothesis")

    run_r_parser = subparsers.add_parser("run-r")
    run_r_parser.add_argument("project_dir")
    run_r_parser.add_argument("script_path")

    draft_parser = subparsers.add_parser("draft")
    draft_parser.add_argument("project_dir")

    review_parser = subparsers.add_parser("review")
    review_parser.add_argument("project_dir")

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("project_dir")

    congress_parser = subparsers.add_parser("congress")
    congress_sub = congress_parser.add_subparsers(dest="congress_command", required=True)
    congress_import = congress_sub.add_parser("import")
    congress_import.add_argument("project_dir")
    congress_import.add_argument("--source", required=True)
    congress_import.add_argument("--kind", choices=["deck", "poster", "abstract"], default="deck")
    congress_import.add_argument("--slug")
    congress_import.add_argument("--profile")
    congress_import.add_argument("--crawl", action="store_true")
    congress_import.add_argument("--author", action="append", dest="authors")
    congress_import.add_argument("--affiliation", action="append", dest="affiliations")
    congress_import.add_argument("--qr-url", default="")
    congress_import.add_argument("--logo", action="append", dest="logos")
    congress_save = congress_sub.add_parser("save-profile")
    congress_save.add_argument("deliverable_dir")
    congress_save.add_argument("--profile", required=True)
    congress_use = congress_sub.add_parser("use-profile")
    congress_use.add_argument("project_dir")
    congress_use.add_argument("--profile", required=True)
    congress_use.add_argument("--slug", required=True)

    deck_parser = subparsers.add_parser("deck")
    deck_sub = deck_parser.add_subparsers(dest="deck_command", required=True)
    for action in ["plan", "build", "qa", "export"]:
        action_parser = deck_sub.add_parser(action)
        action_parser.add_argument("deliverable_dir")
        if action == "export":
            action_parser.add_argument("--strict", action="store_true")

    poster_parser = subparsers.add_parser("poster")
    poster_sub = poster_parser.add_subparsers(dest="poster_command", required=True)
    for action in ["plan", "build", "qa", "export"]:
        action_parser = poster_sub.add_parser(action)
        action_parser.add_argument("deliverable_dir")
        if action == "export":
            action_parser.add_argument("--strict", action="store_true")

    submit_parser = subparsers.add_parser("submit")
    submit_sub = submit_parser.add_subparsers(dest="submit_command", required=True)
    submit_dry = submit_sub.add_parser("dry-run")
    submit_dry.add_argument("deliverable_dir")
    submit_run = submit_sub.add_parser("run")
    submit_run.add_argument("deliverable_dir")
    submit_run.add_argument("--confirm", action="store_true")

    life_science_parser = subparsers.add_parser("life-science")
    life_science_sub = life_science_parser.add_subparsers(dest="life_science_command", required=True)
    life_catalog = life_science_sub.add_parser("catalog")
    life_catalog.add_argument("--plugin-root")
    life_plan = life_science_sub.add_parser("plan")
    life_plan.add_argument("project_dir")
    life_plan.add_argument("--question", required=True)
    life_plan.add_argument("--plugin-root")

    skills_parser = subparsers.add_parser("skills")
    skills_sub = skills_parser.add_subparsers(dest="skills_command", required=True)
    skills_catalog = skills_sub.add_parser("catalog")
    skills_catalog.add_argument("--skills-dir")
    skills_audit = skills_sub.add_parser("audit")
    skills_audit.add_argument("--skills-dir")
    skills_route = skills_sub.add_parser("route")
    skills_route.add_argument("--query", required=True)
    skills_route.add_argument("--skills-dir")
    skills_route.add_argument("--limit", type=int, default=8)

    journal_parser = subparsers.add_parser("journal")
    journal_sub = journal_parser.add_subparsers(dest="journal_command", required=True)
    journal_catalog = journal_sub.add_parser("catalog")
    journal_catalog.add_argument("--domain")
    journal_catalog.add_argument("--tier")
    journal_catalog.add_argument("--presets-dir")
    journal_verify = journal_sub.add_parser("verify")
    journal_verify.add_argument("--presets-dir")
    journal_route = journal_sub.add_parser("route")
    journal_route.add_argument("project_dir")
    journal_route.add_argument("--domain")
    journal_route.add_argument("--limit", type=int, default=10)
    journal_route.add_argument("--presets-dir")
    journal_report = journal_sub.add_parser("report")
    journal_report.add_argument("project_dir")
    journal_report.add_argument("--domain")
    journal_report.add_argument("--presets-dir")

    guard_parser = subparsers.add_parser("guard")
    guard_sub = guard_parser.add_subparsers(dest="guard_command", required=True)
    guard_check = guard_sub.add_parser("check")
    guard_check.add_argument("project_dir")

    query_parser = subparsers.add_parser("query")
    query_sub = query_parser.add_subparsers(dest="query_command", required=True)
    query_validate = query_sub.add_parser("validate")
    query_validate.add_argument("project_dir")
    query_compile = query_sub.add_parser("compile")
    query_compile.add_argument("project_dir")

    retrieval_parser = subparsers.add_parser("retrieval")
    retrieval_sub = retrieval_parser.add_subparsers(dest="retrieval_command", required=True)
    retrieval_plan = retrieval_sub.add_parser("plan")
    retrieval_plan.add_argument("project_dir")
    retrieval_audit = retrieval_sub.add_parser("audit")
    retrieval_audit.add_argument("project_dir")

    idea_parser = subparsers.add_parser("idea")
    idea_sub = idea_parser.add_subparsers(dest="idea_command", required=True)
    idea_tournament = idea_sub.add_parser("tournament")
    idea_tournament.add_argument("project_dir")

    stage_parser = subparsers.add_parser("stage")
    stage_sub = stage_parser.add_subparsers(dest="stage_command", required=True)
    stage_audit = stage_sub.add_parser("audit")
    stage_audit.add_argument("project_dir")
    stage_audit.add_argument("--target-mode")

    machine_parser = subparsers.add_parser("machine")
    machine_sub = machine_parser.add_subparsers(dest="machine_command", required=True)
    machine_audit = machine_sub.add_parser("audit")
    machine_audit.add_argument("--workspace-root", default=".")

    style_parser = subparsers.add_parser("style")
    style_sub = style_parser.add_subparsers(dest="style_command", required=True)
    ptbr_audit = style_sub.add_parser("ptbr-audit")
    ptbr_audit.add_argument("paths", nargs="+")
    ptbr_audit.add_argument("--output")
    ptbr_audit.add_argument("--json-output")
    ptbr_audit.add_argument("--allow-issues", action="store_true")
    ptbr_brief = style_sub.add_parser("ptbr-brief")
    ptbr_brief.add_argument("--deliverable", required=True)
    ptbr_brief.add_argument("--audience", default="pesquisador")
    ptbr_brief.add_argument("--output")
    ptbr_naturalize = style_sub.add_parser("ptbr-naturalize")
    ptbr_naturalize.add_argument("input_path")
    ptbr_naturalize.add_argument("--output", required=True)
    ptbr_naturalize.add_argument("--json-output")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        project_dir = init_project(Path(args.workspace_root), args.name, args.project_type)
        _print({"status": "created", "project_dir": str(project_dir)})
        return 0
    if args.command == "preflight":
        _print(preflight(Path(args.project_dir)))
        return 0
    if args.command == "ingest":
        _print(register_source(Path(args.project_dir), args.source, args.kind))
        return 0
    if args.command == "registry" and args.registry_command == "register":
        _print(
            register_review_protocol(
                Path(args.project_dir),
                registry=args.registry,
                registry_id=args.registry_id,
                registry_url=args.registry_url,
                registered_at=args.registered_at,
                notes=args.notes,
            )
        )
        return 0
    if args.command == "context" and args.context_command == "build":
        _print(build_task_packet(Path(args.project_dir), args.mode, args.hypothesis))
        return 0
    if args.command == "analyze":
        project_dir = Path(args.project_dir)
        packet = build_task_packet(project_dir, args.mode, args.hypothesis)
        transition = advance_mode(project_dir, args.mode)
        payload = {"task_packet": packet, "transition": transition}
        if args.mode == "discovery" and transition["status"] == "passed":
            payload["discovery_plan"] = build_discovery_plan(project_dir)
        _print(payload)
        return 0
    if args.command == "run-r":
        _print(run_r_script(Path(args.project_dir), Path(args.script_path)))
        return 0
    if args.command == "draft":
        _print(validate_evidence_lock(Path(args.project_dir)))
        return 0
    if args.command == "review":
        _print(run_review_trinity(Path(args.project_dir)))
        return 0
    if args.command == "export":
        project_dir = Path(args.project_dir)
        export_path = project_dir / "exports" / "project_summary.json"
        payload = {
            "project_dir": str(project_dir),
            "manuscript": str(project_dir / "drafts" / "manuscript.md"),
            "review_report": str(project_dir / "reviews" / "review_report.json"),
        }
        export_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        _print({"status": "exported", "path": str(export_path)})
        return 0
    if args.command == "congress" and args.congress_command == "import":
        _print(
            import_conference_requirements(
                Path(args.project_dir),
                source=args.source,
                kind=args.kind,
                slug=args.slug,
                profile=args.profile,
                crawl=args.crawl,
                authors=args.authors,
                affiliations=args.affiliations,
                qr_url=args.qr_url,
                logos=args.logos,
            )
        )
        return 0
    if args.command == "congress" and args.congress_command == "save-profile":
        _print(save_congress_profile(Path(args.deliverable_dir), args.profile))
        return 0
    if args.command == "congress" and args.congress_command == "use-profile":
        _print(use_congress_profile(Path(args.project_dir), args.profile, args.slug))
        return 0
    if args.command in {"deck", "poster"}:
        action = args.deck_command if args.command == "deck" else args.poster_command
        deliverable_dir = Path(args.deliverable_dir)
        if action == "plan":
            _print(plan_deliverable(deliverable_dir))
            return 0
        if action == "build":
            _print(build_deliverable(deliverable_dir))
            return 0
        if action == "qa":
            _print(qa_deliverable(deliverable_dir))
            return 0
        if action == "export":
            _print(export_deliverable(deliverable_dir, strict=bool(getattr(args, "strict", False))))
            return 0
    if args.command == "submit":
        _print(
            submit_deliverable(
                Path(args.deliverable_dir),
                action="dry-run" if args.submit_command == "dry-run" else "run",
                confirm=bool(getattr(args, "confirm", False)),
            )
        )
        return 0
    if args.command == "life-science":
        plugin_root = Path(args.plugin_root) if getattr(args, "plugin_root", None) else None
        if args.life_science_command == "catalog":
            _print(catalog_life_science_skills(plugin_root))
            return 0
        if args.life_science_command == "plan":
            _print(plan_life_science_retrieval(Path(args.project_dir), args.question, plugin_root))
            return 0
    if args.command == "skills":
        skills_dir = Path(args.skills_dir) if getattr(args, "skills_dir", None) else None
        if args.skills_command == "catalog":
            _print(catalog_workspace_skills(skills_dir))
            return 0
        if args.skills_command == "audit":
            _print(audit_workspace_skills(skills_dir))
            return 0
        if args.skills_command == "route":
            _print(route_workspace_skills(args.query, skills_dir, limit=args.limit))
            return 0
    if args.command == "journal":
        presets_dir = Path(args.presets_dir) if getattr(args, "presets_dir", None) else None
        if args.journal_command == "catalog":
            _print(catalog_journals(domain=args.domain, tier=args.tier, presets_dir=presets_dir))
            return 0
        if args.journal_command == "verify":
            _print(verify_journal_presets(presets_dir))
            return 0
        if args.journal_command == "route":
            _print(route_journals(Path(args.project_dir), domain=args.domain, limit=args.limit, presets_dir=presets_dir))
            return 0
        if args.journal_command == "report":
            _print(write_journal_report(Path(args.project_dir), domain=args.domain, presets_dir=presets_dir))
            return 0
    if args.command == "guard" and args.guard_command == "check":
        _print(run_guard_check(Path(args.project_dir)))
        return 0
    if args.command == "query":
        if args.query_command == "validate":
            _print(validate_query_plan(Path(args.project_dir)))
            return 0
        if args.query_command == "compile":
            _print(compile_query_plan(Path(args.project_dir)))
            return 0
    if args.command == "retrieval":
        if args.retrieval_command == "plan":
            _print(build_retrieval_plan(Path(args.project_dir)))
            return 0
        if args.retrieval_command == "audit":
            _print(audit_retrieval(Path(args.project_dir)))
            return 0
    if args.command == "idea" and args.idea_command == "tournament":
        _print(run_idea_tournament(Path(args.project_dir)))
        return 0
    if args.command == "stage" and args.stage_command == "audit":
        _print(audit_stage(Path(args.project_dir), target_mode=args.target_mode))
        return 0
    if args.command == "machine" and args.machine_command == "audit":
        _print(run_machine_audit(Path(args.workspace_root)))
        return 0
    if args.command == "style" and args.style_command == "ptbr-audit":
        payload = write_audit_reports(
            args.paths,
            Path(args.output) if args.output else None,
            Path(args.json_output) if args.json_output else None,
        )
        _print(payload)
        if payload["status"] == "block" and not args.allow_issues:
            return 1
        return 0
    if args.command == "style" and args.style_command == "ptbr-brief":
        text = build_generation_brief(deliverable=args.deliverable, audience=args.audience)
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(text, encoding="utf-8")
            _print({"status": "written", "path": str(output)})
        else:
            print(text)
        return 0
    if args.command == "style" and args.style_command == "ptbr-naturalize":
        input_path = Path(args.input_path)
        output_path = Path(args.output)
        original_text = read_text_for_audit(input_path)
        revised_text = naturalize_text(original_text)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(revised_text, encoding="utf-8")
        payload = {
            "status": audit_text(revised_text, path=output_path)["status"],
            "input": str(input_path),
            "output": str(output_path),
            "original_report": audit_text(original_text, path=input_path),
            "revised_report": audit_text(revised_text, path=output_path),
        }
        if args.json_output:
            json_output = Path(args.json_output)
            json_output.parent.mkdir(parents=True, exist_ok=True)
            json_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        _print(payload)
        return 0
    return 1
