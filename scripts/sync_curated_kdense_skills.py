"""Auditably synchronize the approved K-Dense skill subset from one commit.

The exact full commit SHA is mandatory. Existing files are backed up before
replacement; files absent upstream are retained locally and never deleted.
"""

from __future__ import annotations

import argparse
from io import BytesIO
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / ".agents" / "skills" / "scientific-agent-skills"
CURATED_SKILLS = (
    "research-lookup",
    "database-lookup",
    "citation-management",
    "literature-review",
    "statistical-analysis",
    "peer-review",
    "clinical-reports",
    "venue-templates",
    "scientific-writing",
    "scientific-critical-thinking",
)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(MIRROR), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _revision(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("--revision must be a full 40-character lowercase commit SHA")
    resolved = _git("rev-parse", "--verify", f"{value}^{{commit}}")
    if resolved != value:
        raise ValueError("--revision did not resolve to the exact requested commit")
    return resolved


def _quarantined(relative: Path) -> bool:
    lowered = relative.as_posix().lower()
    filename = relative.name.lower()
    if filename.startswith("generate_schematic"):
        return True
    return lowered.startswith("assets/") and relative.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def synchronize(output: Path, *, revision: str, apply: bool, skills: tuple[str, ...] = CURATED_SKILLS) -> dict:
    if not skills or len(set(skills)) != len(skills) or not set(skills).issubset(CURATED_SKILLS):
        raise ValueError("skills must be a non-empty unique subset of the curated allowlist")
    revision = _revision(revision)
    upstream_head = _git("rev-parse", "origin/main")
    license_bytes = subprocess.run(
        ["git", "-C", str(MIRROR), "show", f"{revision}:LICENSE.md"],
        check=True,
        capture_output=True,
    ).stdout
    license_text = license_bytes.decode("utf-8", errors="replace")
    license_name = "MIT" if license_text.startswith("MIT License") else "NOASSERTION"
    output.parent.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "schema_version": 2,
        "provider": "K-Dense AI",
        "origin": "https://github.com/K-Dense-AI/scientific-agent-skills",
        "revision": revision,
        "observed_origin_main": upstream_head,
        "license": license_name,
        "license_file": "LICENSE.md",
        "license_sha256": _sha256(license_bytes),
        "curated_skills": list(skills),
        "skills": {},
        "apply": apply,
    }
    for skill in skills:
        archive = subprocess.run(
            ["git", "-C", str(MIRROR), "archive", "--format=zip", revision, f"skills/{skill}"],
            check=True,
            capture_output=True,
        ).stdout
        target = ROOT / "skills" / skill
        copied: list[str] = []
        overwritten: list[str] = []
        excluded: list[str] = []
        files: dict[str, dict[str, str]] = {}
        quarantined: list[dict[str, str]] = []
        upstream_paths: set[str] = set()
        with zipfile.ZipFile(BytesIO(archive)) as bundle:
            for member in sorted((item for item in bundle.infolist() if not item.is_dir()), key=lambda item: item.filename):
                prefix = f"skills/{skill}/"
                if not member.filename.startswith(prefix):
                    continue
                relative = Path(member.filename[len(prefix):])
                if relative.is_absolute() or ".." in relative.parts:
                    raise RuntimeError(f"unsafe path in upstream archive: {member.filename}")
                upstream_paths.add(relative.as_posix())
                if _quarantined(relative):
                    excluded.append(relative.as_posix())
                    quarantined.append({
                        "path": relative.as_posix(),
                        "reason": "visual-generation asset or script excluded by curation policy",
                        "upstream_sha256": _sha256(bundle.read(member)),
                    })
                    continue
                destination = target / relative
                upstream_bytes = bundle.read(member)
                upstream_hash = _sha256(upstream_bytes)
                record = {"upstream_sha256": upstream_hash}
                if destination.is_file():
                    overwritten.append(relative.as_posix())
                    local_bytes = destination.read_bytes()
                    record["previous_local_sha256"] = _sha256(local_bytes)
                    backup = ROOT / ".machine" / "skill-backups" / "kdense" / revision / skill / relative
                    record["backup_path"] = backup.relative_to(ROOT).as_posix()
                    record["backup_sha256"] = _sha256(local_bytes)
                    if apply:
                        if backup.exists():
                            saved_hash = _sha256(backup.read_bytes())
                            if saved_hash != record["backup_sha256"] and upstream_hash != record["previous_local_sha256"]:
                                raise RuntimeError(f"backup already exists with different content: {backup}")
                            record["backup_sha256"] = saved_hash
                            record["previous_local_sha256"] = saved_hash
                        else:
                            backup.parent.mkdir(parents=True, exist_ok=True)
                            backup.write_bytes(local_bytes)
                else:
                    copied.append(relative.as_posix())
                files[relative.as_posix()] = record
                if apply:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_bytes(upstream_bytes)
        retained_local = []
        if target.exists():
            for local_path in sorted(path for path in target.rglob("*") if path.is_file()):
                relative = local_path.relative_to(target).as_posix()
                if relative not in upstream_paths:
                    retained_local.append({
                        "path": relative,
                        "sha256": _sha256(local_path.read_bytes()),
                        "reason": "not present in selected upstream tree; retained without deletion",
                    })
                elif relative in excluded:
                    retained_local.append({
                        "path": relative,
                        "sha256": _sha256(local_path.read_bytes()),
                        "reason": "upstream path quarantined; existing local file retained",
                    })
        manifest["skills"][skill] = {
            "copied": copied,
            "overwritten": overwritten,
            "excluded": excluded,
            "quarantined": quarantined,
            "files": files,
            "removed": [],
            "retained_local": retained_local,
        }
    output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Copy approved non-quarantined files into skills/.")
    parser.add_argument("--revision", required=True, help="Exact full commit SHA to synchronize")
    parser.add_argument("--skills", nargs="+", choices=CURATED_SKILLS, default=CURATED_SKILLS,
                        help="Subset of the approved skills to synchronize")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    selection = "all" if tuple(args.skills) == CURATED_SKILLS else "-".join(args.skills)
    output = args.output or ROOT / "skills" / "registry.sources" / f"kdense-curated-{selection}-{args.revision[:7]}.json"
    manifest = synchronize(output, revision=args.revision, apply=args.apply, skills=tuple(args.skills))
    print(json.dumps({"status": "applied" if args.apply else "planned", "skills": len(manifest["skills"]), "output": str(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
