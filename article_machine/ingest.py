from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import shutil


def register_source(project_dir: Path, source: str, source_kind: str) -> dict:
    project_dir = Path(project_dir)
    registry_path = project_dir / "sources" / "registry.jsonl"
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "registered_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "source_kind": source_kind,
    }

    if source_kind == "file":
        src = Path(source)
        if src.exists():
            destination = project_dir / "sources" / "raw" / src.name
            shutil.copy2(src, destination)
            entry["copied_to"] = destination.relative_to(project_dir).as_posix()

    with registry_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
