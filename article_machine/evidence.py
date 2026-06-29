from __future__ import annotations

import json
import re
from pathlib import Path

from .serialization import save_structured_file


CLAIM_PATTERN = re.compile(r"\{\{claim:([a-zA-Z0-9_.-]+)\}\}")
BIB_PATTERN = re.compile(r"@\w+\{([^,]+),")
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
PMID_PATTERN = re.compile(r"^\d{1,12}$")
PROHIBITED_CONFIDENCE_PATTERN = re.compile(
    r"\b(perfect|world-best|world best|production-grade|production grade|perfeito|melhor do mundo)\b",
    re.IGNORECASE,
)
FACTUAL_CUE_PATTERN = re.compile(
    r"(\b(is|are|was|were|has|have|had|contains|showed|reported|increased|decreased|"
    r"improved|reduced|associated|demonstrated|found|identified|compared|selected|expects|"
    r"validates|implements|seeds|requires|reported)\b|"
    r"\b(PubMed|Crossref|OpenAlex|PRISMA|CONSORT|EQUATOR|DOI|PMID)\b|"
    r"\d{4}|%|\bp\s*[<=>]|\bCI\b|\bOR\b|\bRR\b|\bHR\b)",
    re.IGNORECASE,
)


def _load_claim_entries(project_dir: Path) -> tuple[list[dict], list[str]]:
    claim_path = Path(project_dir) / "evidence" / "claim_map.jsonl"
    claims: list[dict] = []
    issues: list[str] = []
    if not claim_path.exists():
        return claims, issues
    for line_number, line in enumerate(claim_path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        content = line.strip()
        if not content:
            continue
        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            issues.append(f"evidence/claim_map.jsonl line {line_number} is not valid JSON: {exc.msg}.")
            continue
        claim_id = payload.get("claim_id")
        if claim_id:
            payload["_line_number"] = line_number
            claims.append(payload)
        else:
            issues.append(f"evidence/claim_map.jsonl line {line_number} is missing claim_id.")
    return claims, issues


def _claim_map_from_entries(entries: list[dict], issues: list[str]) -> dict[str, dict]:
    claims: dict[str, dict] = {}
    seen: dict[str, int] = {}
    for entry in entries:
        claim_id = str(entry.get("claim_id"))
        if claim_id in seen:
            issues.append(
                f"Duplicate claim_id '{claim_id}' in evidence/claim_map.jsonl lines {seen[claim_id]} and {entry.get('_line_number')}."
            )
            continue
        seen[claim_id] = int(entry.get("_line_number") or 0)
        claims[claim_id] = entry
    return claims


def _load_bib_keys(project_dir: Path) -> set[str]:
    bib_path = Path(project_dir) / "drafts" / "references.bib"
    if not bib_path.exists():
        return set()
    text = bib_path.read_text(encoding="utf-8")
    return {match.group(1).strip() for match in BIB_PATTERN.finditer(text)}


def _normalize_excerpt(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _resolve_source_path(project_dir: Path, source_path: str) -> Path:
    candidate = Path(source_path)
    if candidate.is_absolute():
        return candidate
    project_candidate = project_dir / candidate
    if project_candidate.exists():
        return project_candidate
    workspace_candidate = project_dir.parents[1] / candidate if len(project_dir.parents) > 1 else project_candidate
    if workspace_candidate.exists():
        return workspace_candidate
    return project_candidate


def _source_contains_excerpt(source_path: Path, source_excerpt: str) -> bool:
    source_text = source_path.read_text(encoding="utf-8", errors="replace")
    if source_excerpt in source_text:
        return True
    return _normalize_excerpt(source_excerpt) in _normalize_excerpt(source_text)


def _benchmark_passed(project_dir: Path) -> bool:
    benchmark_path = project_dir / "analysis" / "benchmark_report.json"
    if not benchmark_path.exists():
        return False
    try:
        payload = json.loads(benchmark_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return payload.get("status") == "pass" or payload.get("aggregate_status") == "pass"


def _unmarked_factual_lines(manuscript: str) -> list[int]:
    lines: list[int] = []
    in_code_block = False
    for line_number, line in enumerate(manuscript.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or not stripped:
            continue
        if stripped.startswith("#") or stripped in {"---", "***"}:
            continue
        if CLAIM_PATTERN.search(stripped):
            continue
        if FACTUAL_CUE_PATTERN.search(stripped):
            lines.append(line_number)
    return lines


def validate_evidence_lock(project_dir: Path) -> dict:
    project_dir = Path(project_dir)
    manuscript_path = project_dir / "drafts" / "manuscript.md"
    manuscript = manuscript_path.read_text(encoding="utf-8") if manuscript_path.exists() else ""
    claim_ids = CLAIM_PATTERN.findall(manuscript)
    claim_entries, issues = _load_claim_entries(project_dir)
    claim_map = _claim_map_from_entries(claim_entries, issues)
    bib_keys = _load_bib_keys(project_dir)

    if not claim_ids:
        issues.append("No claim markers were found in drafts/manuscript.md.")

    for line_number in _unmarked_factual_lines(manuscript):
        issues.append(f"Factual-looking sentence on drafts/manuscript.md line {line_number} has no {{{{claim:...}}}} marker.")

    if PROHIBITED_CONFIDENCE_PATTERN.search(manuscript) and not _benchmark_passed(project_dir):
        issues.append(
            "Prohibited confidence language ('perfect', 'world-best', 'production-grade', 'perfeito', or equivalent) requires a passing agent-benchmark-harness report."
        )

    required_fields = ["statement", "source_path", "source_excerpt", "reference_key", "status"]
    for claim_id in claim_ids:
        claim = claim_map.get(claim_id)
        if claim is None:
            issues.append(f"Claim marker '{claim_id}' is missing from evidence/claim_map.jsonl.")
            continue
        for field in required_fields:
            if not claim.get(field):
                issues.append(f"Claim '{claim_id}' is missing required field '{field}'.")
        if claim.get("status") != "supported":
            issues.append(f"Claim '{claim_id}' is not marked as supported.")
        reference_key = claim.get("reference_key")
        if reference_key and reference_key not in bib_keys:
            issues.append(f"Reference key '{reference_key}' for claim '{claim_id}' is missing from drafts/references.bib.")
        source_path_value = claim.get("source_path")
        source_excerpt = claim.get("source_excerpt")
        if source_path_value and source_excerpt:
            source_path = _resolve_source_path(project_dir, str(source_path_value))
            if not source_path.exists():
                issues.append(f"Source path '{source_path_value}' for claim '{claim_id}' does not exist.")
            elif not _source_contains_excerpt(source_path, str(source_excerpt)):
                issues.append(f"Source excerpt for claim '{claim_id}' does not appear in '{source_path_value}'.")
        doi = claim.get("doi")
        if doi and not DOI_PATTERN.match(str(doi).strip()):
            issues.append(f"Claim '{claim_id}' declares invalid DOI '{doi}'.")
        pmid = claim.get("pmid")
        if pmid and not PMID_PATTERN.match(str(pmid).strip()):
            issues.append(f"Claim '{claim_id}' declares invalid PMID '{pmid}'.")

    status = "pass" if not issues else "block"
    report = {
        "status": status,
        "claims_checked": claim_ids,
        "issues": issues,
    }
    save_structured_file(project_dir / "reviews" / "evidence_lock_report.json", report)
    return report
