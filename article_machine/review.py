from __future__ import annotations

from pathlib import Path

from .evidence import validate_evidence_lock
from .ptbr_style import audit_paths, render_markdown_report
from .serialization import load_structured_file, save_structured_file


def _aggregate_status(statuses: list[str]) -> str:
    if "block" in statuses:
        return "block"
    if "revise" in statuses:
        return "revise"
    if all(status == "pass" for status in statuses):
        return "pass"
    return "pending"


def _run_configured_ptbr_style_audit(project_dir: Path, standards: dict) -> dict:
    policy = standards.get("ptbr_style_policy") or {}
    if not policy.get("enabled"):
        return {"status": "pass", "issues": []}

    configured_paths = policy.get("audit_paths") or []
    paths: list[Path] = []
    missing_paths: list[str] = []
    for item in configured_paths:
        path = project_dir / item
        if path.exists():
            paths.append(path)
        else:
            missing_paths.append(str(item))

    issues = [f"PT-BR style audit path is missing: {item}" for item in missing_paths]
    if paths:
        payload = audit_paths(paths)
        save_structured_file(project_dir / "reviews" / "ptbr_style_audit.json", payload)
        (project_dir / "reviews" / "ptbr_style_audit.md").write_text(
            render_markdown_report(payload["reports"]),
            encoding="utf-8",
        )
        if payload["status"] == "block":
            issues.append(f"PT-BR style audit blocked {payload['issue_count']} issue(s).")
    elif not missing_paths:
        issues.append("PT-BR style audit is enabled, but no audit_paths were configured.")

    return {"status": "block" if issues else "pass", "issues": issues}


def run_review_trinity(project_dir: Path) -> dict:
    project_dir = Path(project_dir)
    protocol = load_structured_file(project_dir / "protocol.yaml")
    standards = load_structured_file(project_dir / "standards.yaml")
    evidence_report = validate_evidence_lock(project_dir)

    methodological_issues = []
    if protocol.get("status") not in {"frozen", "approved", "locked"}:
        methodological_issues.append("Protocol is not frozen.")
    if standards.get("guidelines") and not standards.get("checklist_status"):
        methodological_issues.append("Standards checklist is missing.")
    methodological_status = "pass" if not methodological_issues else "revise"

    quantitative_issues = []
    if standards.get("lane") == "computational-discovery":
        quantitative_issues.append("Discovery outputs require benchmark review before submission.")
    quantitative_status = "pass" if not quantitative_issues else "revise"

    ptbr_style_report = _run_configured_ptbr_style_audit(project_dir, standards)
    editorial_issues = list(evidence_report["issues"]) + ptbr_style_report["issues"]
    editorial_status = "pass" if evidence_report["status"] == "pass" and ptbr_style_report["status"] == "pass" else "block"

    reviewers = {
        "methodological": {"status": methodological_status, "issues": methodological_issues},
        "quantitative": {"status": quantitative_status, "issues": quantitative_issues},
        "editorial": {"status": editorial_status, "issues": editorial_issues},
    }
    report = {
        "aggregate_status": _aggregate_status([item["status"] for item in reviewers.values()]),
        "reviewers": reviewers,
    }
    save_structured_file(project_dir / "reviews" / "review_report.json", report)
    return report
