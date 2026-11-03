"""Expose the approved curated skills in the local agent discovery directory."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def publish(*, apply: bool = False) -> dict:
    registry = json.loads((ROOT / "skills" / "registry.json").read_text(encoding="utf-8"))
    selected = {
        name for name, entry in registry["skills"].items()
        if entry["status"] == "active" and (
            entry["origin"]["provider"] == "K-Dense AI"
            or name in {"scientific-workflow-orchestrator", "bilingual-scientific-writing", "fapesp-cnpq-projects"}
        )
    }
    issues = []
    for name in sorted(selected):
        source = ROOT / "skills" / name
        destination = ROOT / ".agents" / "skills" / name
        if destination.exists():
            if destination.resolve() != source.resolve():
                issues.append(f"{name}: existing discovery path is not the approved source; preserved")
            continue
        if not apply:
            issues.append(f"{name}: discovery link is absent")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        if os.name == "nt":
            quoted_destination = str(destination).replace("'", "''")
            quoted_source = str(source).replace("'", "''")
            command = f"New-Item -ItemType Junction -Path '{quoted_destination}' -Target '{quoted_source}' | Out-Null"
            subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], check=True, capture_output=True)
        else:
            destination.symlink_to(source, target_is_directory=True)
    return {"status": "pass" if not issues else "block", "skill_count": len(selected), "issues": issues, "apply": apply}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    report = publish(apply=args.apply)
    print(json.dumps(report))
    raise SystemExit(0 if report["status"] == "pass" else 1)
