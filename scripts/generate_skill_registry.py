"""Generate the complete, deterministic Article Machine skill registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from article_machine.agent_skills import ROUTE_RULES, WORLD_CLASS_SKILLS, _parse_frontmatter  # noqa: E402
from article_machine.services.skill_registry import REGISTRY_SCHEMA_VERSION, tree_hash  # noqa: E402

K_DENSE_URL = "https://github.com/K-Dense-AI/scientific-agent-skills"
TOOLUNIVERSE_URL = "https://github.com/mims-harvard/ToolUniverse"
TOOLUNIVERSE_REVISION = "v1.3.1"
LOCAL_URL = "local://doutorado/article-machine"
CURATED_K_DENSE = {
    "research-lookup", "database-lookup", "citation-management", "literature-review",
    "statistical-analysis", "peer-review", "clinical-reports", "venue-templates",
    "scientific-writing", "scientific-critical-thinking",
}
K_DENSE_MANIFEST = "skills/registry.sources/kdense-curated-a1043ef.json"
K_DENSE_ADDITIONS_MANIFEST = "skills/registry.sources/kdense-curated-foundations-a1043ef.json"
K_DENSE_MANIFEST_BY_SKILL = {
    **{name: K_DENSE_MANIFEST for name in CURATED_K_DENSE - {"scientific-writing", "scientific-critical-thinking"}},
    "scientific-writing": K_DENSE_ADDITIONS_MANIFEST,
    "scientific-critical-thinking": K_DENSE_ADDITIONS_MANIFEST,
}
K_DENSE_SOURCE_BY_MANIFEST: dict[str, dict] = {}
for _manifest in set(K_DENSE_MANIFEST_BY_SKILL.values()):
    try:
        K_DENSE_SOURCE_BY_MANIFEST[_manifest] = json.loads((ROOT / _manifest).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        K_DENSE_SOURCE_BY_MANIFEST[_manifest] = {}
PLUGIN_BRIDGES = {"life-science-router", "ngs-analysis-router", "zotero-reference-manager"}


def _source_for(name: str) -> tuple[dict[str, str], str, str, str]:
    if name.startswith("tooluniverse-"):
        return ({"provider": "ToolUniverse", "url": TOOLUNIVERSE_URL}, TOOLUNIVERSE_REVISION, "NOASSERTION", "hold")
    if name in PLUGIN_BRIDGES:
        return ({"provider": "Article Machine plugin bridge", "url": LOCAL_URL}, "workspace-2026-10-12", "LicenseRef-Local-Private", "active")
    if name in CURATED_K_DENSE:
        source = K_DENSE_SOURCE_BY_MANIFEST.get(K_DENSE_MANIFEST_BY_SKILL[name], {})
        revision = source.get("revision", "local-unverified")
        license_name = source.get("license", "NOASSERTION")
        status = "active" if license_name != "NOASSERTION" and revision != "local-unverified" else "hold"
        return ({"provider": "K-Dense AI", "url": K_DENSE_URL}, revision, license_name, status)
    if name in WORLD_CLASS_SKILLS:
        return ({"provider": "Article Machine curated layer", "url": LOCAL_URL}, "workspace-2026-10-12", "LicenseRef-Local-Private", "active")
    return ({"provider": "local unverified skill tree", "url": LOCAL_URL}, "local-unverified", "NOASSERTION", "hold")


def _observed_contract_fields(skill_file: Path) -> tuple[list[str], list[str], list[str]]:
    """Extract only explicit operational signals; absence is represented by []."""

    text = skill_file.read_text(encoding="utf-8")
    credentials = sorted(set(re.findall(r"\b[A-Z][A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD)\b", text)))
    domains = sorted({match.lower() for match in re.findall(r"https?://([^/\s)`]+)", text)})
    dependencies = sorted({
        package.lower()
        for package in re.findall(r"\b(?:import|pip install|uv add)\s+([A-Za-z0-9_.-]+)", text)
    })
    return dependencies, credentials, domains


def build_registry(skills_dir: Path = ROOT / "skills") -> dict:
    entries: dict[str, dict] = {}
    for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
        name = skill_file.parent.name
        meta = _parse_frontmatter(skill_file)
        origin, revision, license_name, status = _source_for(name)
        dependencies, credentials, domains = _observed_contract_fields(skill_file)
        entries[name] = {
            "name": name,
            "description": meta.get("description", ""),
            "origin": origin,
            "pinned_revision": revision,
            "license": license_name,
            "tree_hash": tree_hash(skill_file.parent),
            "dependencies": dependencies,
            "credentials": credentials,
            "network_domains": domains,
            "human_data_policy": "no-upload-without-explicit-permission",
            "routes": {
                "positive": sorted({trigger for rule in ROUTE_RULES if rule["skill"] == name for trigger in rule["triggers"]}),
                "negative": ["unrelated request without an explicit capability trigger"],
            },
            "artifact_destination": "context/ or evidence/ as defined by the active project",
            "status": status,
            "required_for_clone": name in WORLD_CLASS_SKILLS or name in CURATED_K_DENSE,
            "next_review": "2027-01-12",
        }
        if name.startswith("tooluniverse-"):
            entries[name]["review_note"] = "Held pending evidence of incremental value over existing routes."
            entries[name]["source_verification"] = "historical-attribution-not-refreshed"
        if origin["url"] == LOCAL_URL:
            entries[name]["license_note"] = "Private workspace use; redistribution rights for inherited content require separate review."
        if name == "tooluniverse-statistical-modeling":
            entries[name]["status"] = "pilot"
            entries[name]["review_note"] = "Narrow pilot only; promotion requires benchmark evidence."
        if name in CURATED_K_DENSE:
            entries[name]["review_note"] = "Curated K-Dense update; visual-generation assets and scripts remain quarantined."
            entries[name]["sync_manifest"] = K_DENSE_MANIFEST_BY_SKILL[name]
            entries[name]["sync_mode"] = "curated-tree-with-visual-quarantine"
    return {
        "schema_version": REGISTRY_SCHEMA_VERSION,
        "registry_policy": "single-source-of-truth; generated documents must not be hand-edited",
        "skills": entries,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "skills" / "registry.json")
    args = parser.parse_args()
    payload = build_registry()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "written", "skill_count": len(payload["skills"]), "output": str(args.output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
