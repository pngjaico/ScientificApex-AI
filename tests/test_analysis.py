from __future__ import annotations

import json
from pathlib import Path
import subprocess

from article_machine.analysis import preflight
from article_machine.adapters import runtime as runtime_adapter
from article_machine.serialization import load_structured_file, save_structured_file
from article_machine.services import environment
from test_contracts_v2 import _v2_project


def test_json_suffix_writes_real_json_and_yaml_remains_readable(tmp_path: Path) -> None:
    payload = {"title": "Revisão", "enabled": True, "items": [1, 2]}
    json_path = tmp_path / "report.json"
    yaml_path = tmp_path / "report.yaml"

    save_structured_file(json_path, payload)
    save_structured_file(yaml_path, payload)

    assert json.loads(json_path.read_text(encoding="utf-8")) == payload
    assert load_structured_file(json_path) == payload
    assert load_structured_file(yaml_path) == payload


def test_historical_json_is_still_readable(tmp_path: Path) -> None:
    path = tmp_path / "historical.json"
    path.write_text('{"legacy": true, "count": 3}', encoding="utf-8")
    assert load_structured_file(path) == {"legacy": True, "count": 3}


def test_preflight_fails_closed_when_a_contract_is_malformed(tmp_path: Path) -> None:
    project = _v2_project(tmp_path)
    (project / "protocol.yaml").write_text("contract_version: [", encoding="utf-8")

    report = preflight(project)

    assert report["status"] == "blocked"
    assert report["checks"]["protocol.yaml"]["status"] == "blocked"


def test_required_runtime_probe_failure_blocks_preflight(tmp_path: Path, monkeypatch) -> None:
    project = _v2_project(tmp_path)
    monkeypatch.setattr(environment, "runtime_version", lambda runtime, executable: None)

    report = preflight(project)

    assert report["status"] == "blocked"
    assert any("python version mismatch" in issue for issue in report["issues"])


def test_version_probe_timeout_is_reported_as_unavailable(monkeypatch) -> None:
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], kwargs.get("timeout", 20))

    monkeypatch.setattr(runtime_adapter.subprocess, "run", timeout)
    assert runtime_adapter.runtime_version("python", "python") is None
