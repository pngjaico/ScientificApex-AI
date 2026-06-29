from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None


def _normalize(value: Any) -> Any:
    return deepcopy(value)


def dump_structured_data(data: dict[str, Any]) -> str:
    payload = _normalize(data)
    if yaml is not None:
        return yaml.safe_dump(  # pragma: no branch
            payload,
            allow_unicode=True,
            sort_keys=False,
        )
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def load_structured_text(text: str) -> dict[str, Any]:
    content = (text or "").strip()
    if not content:
        return {}
    if yaml is not None:
        loaded = yaml.safe_load(content)
        return loaded if isinstance(loaded, dict) else {}
    loaded = json.loads(content)
    return loaded if isinstance(loaded, dict) else {}


def load_structured_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return load_structured_text(path.read_text(encoding="utf-8"))


def save_structured_file(path: Path, data: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dump_structured_data(data), encoding="utf-8")
    return path
