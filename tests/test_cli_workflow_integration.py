from __future__ import annotations

import json

from article_machine.cli import main
from article_machine.projects import init_project
import article_machine.services.plugins as plugin_service
import article_machine.cli as cli_module


def test_public_workflow_plan_cli_writes_packet_without_advancing_project(tmp_path, capsys) -> None:
    project = init_project(tmp_path, "CLI Workflow", "systematic-review")
    project_file = project / "project.yaml"
    before = project_file.read_bytes()

    exit_code = main(
        [
            "workflow", "plan", str(project),
            "--query", "Compare intervention effects and alternative explanations",
            "--language", "en",
        ]
    )
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["status"] == "planned"
    assert payload["gate_eligible"] is False
    assert project_file.read_bytes() == before
    assert (project / "context" / "scientific_workflow_plan.json").is_file()
    assert (project / "context" / "scientific_workflow_packet.md").is_file()


def test_public_plugin_audit_is_local_and_does_not_claim_live_authentication(
    tmp_path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(plugin_service, "discover_plugin_candidates", lambda *_args, **_kwargs: [])

    exit_code = main(["plugins", "audit", "--workspace-root", str(tmp_path)])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert payload["contract"] == "ScientificPluginAuditV1"
    assert payload["status"] == "inspected"
    assert payload["plugins"]
    assert all(item["credentials_verified"] is False for item in payload["plugins"])
    assert all(item["live_calls_verified"] is False for item in payload["plugins"])
    assert all(item["human_data_upload_authorized"] is False for item in payload["plugins"])


def test_public_environment_prepare_dry_run_never_requests_install(tmp_path, monkeypatch, capsys) -> None:
    project = init_project(tmp_path, "CLI Environment", "systematic-review")
    calls = []

    def fake_prepare(project_dir, runtime, *, execute=False):
        calls.append((project_dir, runtime, execute))
        return {"contract": "EnvironmentPrepareV2", "status": "blocked", "executed": execute, "action": "dry-run"}

    monkeypatch.setattr(cli_module, "prepare_environment", fake_prepare)

    exit_code = main(["env", "prepare", str(project), "--runtime", "browser", "--dry-run"])
    payload = json.loads(capsys.readouterr().out)

    assert exit_code == 1
    assert calls == [(project, "browser", False)]
    assert payload["executed"] is False
    assert not (tmp_path / "tools" / "playwright" / "node_modules").exists()


def test_draft_and_export_cli_block_before_evidence_or_stage_checks(tmp_path, monkeypatch, capsys) -> None:
    project = init_project(tmp_path, "CLI Blocked Artifacts", "systematic-review")
    monkeypatch.setattr(cli_module, "validate_evidence_lock", lambda *_: (_ for _ in ()).throw(AssertionError("draft gate ran")))
    monkeypatch.setattr(cli_module, "audit_stage", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("export stage audit ran")))

    draft_exit = main(["draft", str(project)])
    draft = json.loads(capsys.readouterr().out)
    export_exit = main(["export", str(project)])
    export = json.loads(capsys.readouterr().out)

    assert draft_exit == export_exit == 1
    assert draft["contract"] == export["contract"] == "CommandModeGate"
    assert draft["status"] == export["status"] == "block"
    assert draft["current_mode"] == export["current_mode"] == "bootstrap"
    assert not (project / "exports" / "project_summary.json").exists()
