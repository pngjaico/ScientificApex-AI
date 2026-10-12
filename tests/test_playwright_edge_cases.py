from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from article_machine import playwright_ops
from article_machine.cli import main
from article_machine.deliverables import import_conference_requirements
from article_machine.projects import init_project
from article_machine.serialization import save_structured_file


def test_locked_browser_unavailable_blocks_without_cli_fallback(tmp_path: Path, monkeypatch) -> None:
    html = tmp_path / "deck.html"
    html.write_text("<html><body>Draft</body></html>", encoding="utf-8")
    monkeypatch.setattr(
        playwright_ops,
        "playwright_available",
        lambda: {"status": "blocked", "message": "Locked browser runtime unavailable."},
    )
    monkeypatch.setattr(
        playwright_ops,
        "_run_playwright_cli",
        lambda *_args, **_kwargs: pytest.fail("must not bypass the unavailable locked runtime"),
    )

    report = playwright_ops.qa_html(html, tmp_path / "qa", "default")

    assert report["status"] == "blocked"
    assert report["message"] == "Locked browser runtime unavailable."
    assert not (tmp_path / "qa" / "layout-qa.png").exists()


def test_locked_cli_missing_node_is_reported_as_blocked(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        playwright_ops,
        "playwright_available",
        lambda: {"status": "pass", "node_path": "missing-node", "cli_path": str(tmp_path / "playwright" / "cli.js")},
    )

    def missing_executable(*_args, **_kwargs):
        raise FileNotFoundError("missing-node")

    monkeypatch.setattr(playwright_ops.subprocess, "run", missing_executable)
    report = playwright_ops._run_playwright_cli(["--version"], tmp_path / "output", timeout=7)

    assert report["status"] == "blocked"
    assert "could not be launched" in report["message"]
    assert report["message"].endswith("missing-node")


def test_locked_script_passes_requested_timeout_to_subprocess(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "qa"
    monkeypatch.setattr(
        playwright_ops,
        "playwright_available",
        lambda: {
            "status": "pass",
            "node_path": "node",
            "playwright_path": str(tmp_path / "tools" / "node_modules" / "playwright"),
        },
    )
    observed = {}

    class Completed:
        returncode = 0
        stdout = '{"status":"pass"}'
        stderr = ""

    def fake_run(command, **kwargs):
        observed["command"] = command
        observed.update(kwargs)
        return Completed()

    monkeypatch.setattr(playwright_ops.subprocess, "run", fake_run)
    report = playwright_ops._run_playwright_script("console.log('{}')", output, timeout=7)

    assert report["status"] == "pass"
    assert observed["timeout"] == 7
    assert observed["cwd"] == output
    assert Path(observed["command"][1]).is_file()


def test_strict_public_export_blocks_ambiguous_requirements_before_browser_calls(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    project = init_project(tmp_path, "Strict Export Gate", "systematic-review")
    import_conference_requirements(
        project,
        source="Prepare a short presentation.",
        kind="deck",
        slug="strict-deck",
    )
    deliverable = project / "deliverables" / "strict-deck"
    save_structured_file(deliverable / "qa_report.json", {"status": "pass", "issues": []})
    monkeypatch.setattr(
        playwright_ops,
        "export_html_pdf",
        lambda *_args, **_kwargs: pytest.fail("strict validation must run before Playwright export"),
    )

    exit_code = main(["deck", "export", str(deliverable), "--strict"])
    payload = json.loads(capsys.readouterr().out)

    assert payload["status"] == "blocked"
    assert payload["contract"]["status"] == "block"
    assert any("requirements confidence" in issue.lower() for issue in payload["issues"])
    assert not (deliverable / "exports" / "export-v001").exists()
    assert exit_code == 1


def test_cli_timeout_exception_is_not_silently_retried(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        playwright_ops,
        "playwright_available",
        lambda: {
            "status": "pass",
            "node_path": "node",
            "playwright_path": str(tmp_path / "node_modules" / "playwright"),
            "cli_path": str(tmp_path / "node_modules" / "playwright" / "cli.js"),
        },
    )

    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(["node", "playwright"], timeout=1)

    monkeypatch.setattr(playwright_ops.subprocess, "run", timeout)

    report = playwright_ops._run_playwright_cli(["--version"], tmp_path / "output", timeout=1)
    assert report["status"] == "blocked"
    assert "timeout" in report["message"]




def _enable_locked_script_runtime(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        playwright_ops,
        "playwright_available",
        lambda: {
            "status": "pass",
            "node_path": "node",
            "playwright_path": str(tmp_path / "node_modules" / "playwright"),
        },
    )


def test_locked_script_timeout_returns_structured_block(tmp_path: Path, monkeypatch) -> None:
    _enable_locked_script_runtime(tmp_path, monkeypatch)

    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(["node", "script.js"], 5, output=b"partial", stderr=b"late")

    monkeypatch.setattr(playwright_ops.subprocess, "run", timeout)
    report = playwright_ops._run_playwright_script("console.log('{}')", tmp_path / "output", timeout=5)

    assert report["status"] == "blocked"
    assert report["timed_out"] is True
    assert report["timeout_seconds"] == 5
    assert report["stdout"] == "partial"
    assert report["stderr"] == "late"


def test_locked_script_launch_oserror_returns_structured_block(tmp_path: Path, monkeypatch) -> None:
    _enable_locked_script_runtime(tmp_path, monkeypatch)

    def cannot_launch(*_args, **_kwargs):
        raise OSError("node executable missing")

    monkeypatch.setattr(playwright_ops.subprocess, "run", cannot_launch)
    report = playwright_ops._run_playwright_script("console.log('{}')", tmp_path / "output")

    assert report["status"] == "blocked"
    assert report["timed_out"] is False
    assert "node executable missing" in report["stderr"]


@pytest.mark.parametrize("stdout", ["", "  \n", "not-json", "[]", "null", '"text"', "{}"])
def test_locked_script_rejects_empty_invalid_and_nonobject_json(tmp_path: Path, monkeypatch, stdout: str) -> None:
    _enable_locked_script_runtime(tmp_path, monkeypatch)

    class Completed:
        returncode = 0
        stderr = ""

        def __init__(self, output: str) -> None:
            self.stdout = output

    monkeypatch.setattr(playwright_ops.subprocess, "run", lambda *_args, **_kwargs: Completed(stdout))
    report = playwright_ops._run_playwright_script("console.log('report')", tmp_path / "output")

    assert report["status"] == "blocked"
    assert report["message"]


def test_locked_script_accepts_nonempty_json_object_report(tmp_path: Path, monkeypatch) -> None:
    _enable_locked_script_runtime(tmp_path, monkeypatch)

    class Completed:
        returncode = 0
        stdout = '{"status":"pass","checked":true}\n'
        stderr = "warning"

    monkeypatch.setattr(playwright_ops.subprocess, "run", lambda *_args, **_kwargs: Completed())
    report = playwright_ops._run_playwright_script("console.log('report')", tmp_path / "output")

    assert report == {"status": "pass", "checked": True, "stderr": "warning"}
