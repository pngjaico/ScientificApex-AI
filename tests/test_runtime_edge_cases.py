from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_contracts_v2 import _v2_project

from article_machine.adapters import runtime
from article_machine.commands import governance
from article_machine.contracts.compute import (
    ComputeContractV2,
    ContractValidationError,
    RuntimeContract,
    _runtime_from_payload,
    load_compute_contract,
)
from article_machine.projects import init_project
from article_machine.serialization import load_structured_file, save_structured_file
from article_machine.services import environment, runners


def _runtime_contract(**changes) -> RuntimeContract:
    values = {
        "required": True,
        "runner": "python",
        "version": "3.13",
        "timeout_seconds": 10,
        "allowed_directories": ("analysis", "scripts"),
        "lockfile": "uv.lock",
        "executable": None,
        "package_manager": "uv",
        "package_manager_version": "1.0",
        "packages": (),
        "plugins": (),
    }
    values.update(changes)
    return RuntimeContract(**values)


def _completed(stdout: str = "", stderr: str = "", returncode: int = 0):
    return SimpleNamespace(stdout=stdout, stderr=stderr, returncode=returncode)


def test_runtime_contract_rejects_each_missing_required_field() -> None:
    cases = [
        (_runtime_contract(required="yes"), "required"),
        (_runtime_contract(runner=""), "runner"),
        (_runtime_contract(version=None), "version"),
        (_runtime_contract(timeout_seconds=0), "timeout"),
        (_runtime_contract(allowed_directories=()), "allowed_directories"),
        (_runtime_contract(allowed_directories=("../escape",)), "invalid entry"),
        (_runtime_contract(lockfile=None), "lockfile"),
        (_runtime_contract(package_manager=None), "package_manager"),
        (_runtime_contract(package_manager_version=None), "package_manager_version"),
    ]
    for contract, expected in cases:
        assert any(expected in issue for issue in contract.validate("python"))


def test_compute_contract_checks_version_and_plugin_identifiers() -> None:
    runtime_contract = _runtime_contract(
        required=False, lockfile=None, package_manager=None, package_manager_version=None
    )
    contract = ComputeContractV2(1, runtime_contract, runtime_contract, runtime_contract, (" ",))
    issues = contract.validate()
    assert any("contract_version" in issue for issue in issues)
    assert any("plugin identifier" in issue for issue in issues)
    assert "source_path" not in contract.as_dict()


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        (None, "must be an object"),
        ({"allowed_directories": "analysis"}, "allowed_directories must be a list"),
        ({"packages": "numpy"}, "packages and plugins must be lists"),
        ({"plugins": "p"}, "packages and plugins must be lists"),
        ({"timeout_seconds": True}, "timeout_seconds must be an integer"),
        ({"lockfile": 7}, "lockfile must be a string"),
    ],
)
def test_runtime_payload_rejects_malformed_fields(payload, message: str) -> None:
    with pytest.raises(ContractValidationError, match=message):
        _runtime_from_payload("python", payload)


def test_compute_loader_rejects_missing_invalid_version_and_plugin_list(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Bad Compute", "systematic-review")
    (project / "compute.yaml").unlink()
    with pytest.raises(ContractValidationError):
        load_compute_contract(project)
    save_structured_file(project / "compute.yaml", {"contract_version": True})
    with pytest.raises(ContractValidationError):
        load_compute_contract(project)
    save_structured_file(project / "compute.yaml", {"contract_version": 2, "required_plugins": "bad"})
    with pytest.raises(ContractValidationError):
        load_compute_contract(project)


def test_declared_executable_resolution_and_runtime_fallbacks(tmp_path: Path, monkeypatch) -> None:
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    project = workspace / "projects" / "p"
    project.mkdir(parents=True)
    (workspace / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    declared = project / "bin" / "python"
    declared.parent.mkdir()
    declared.write_text("executable", encoding="utf-8")
    (workspace / "Rscript").write_text("executable", encoding="utf-8")

    assert runtime._workspace_root(project) == workspace
    assert runtime._workspace_root(None) is None
    assert runtime.resolve_executable("python", _runtime_contract(executable="bin/python"), project) == str(
        declared.resolve()
    )
    assert runtime.resolve_executable("r", _runtime_contract(executable="Rscript"), project) == str(
        (workspace / "Rscript").resolve()
    )
    assert runtime.resolve_executable("unknown", _runtime_contract(runner="unavailable"), project) is None

    (workspace / "Rscript").unlink()
    monkeypatch.setattr(runtime.shutil, "which", lambda name: {"Rscript": "r-path", "node": "node-path"}.get(name))
    assert runtime.resolve_executable("r", _runtime_contract(runner="Rscript", version=None), project) == "r-path"
    assert runtime.resolve_executable("browser", _runtime_contract(runner="node", version=None), project) == "node-path"
    assert runtime.resolve_executable("python", _runtime_contract(runner="python", version=None), project)


def test_versioned_r_resolution_and_lockfile_confinement(tmp_path: Path, monkeypatch) -> None:
    local = tmp_path / "local"
    program_files = tmp_path / "program-files"
    versioned = local / "Programs" / "R" / "R-4.4.1" / "bin" / "x64" / "Rscript.exe"
    versioned.parent.mkdir(parents=True)
    versioned.write_text("R", encoding="utf-8")
    monkeypatch.setenv("LOCALAPPDATA", str(local))
    monkeypatch.setenv("ProgramFiles", str(program_files))
    project = tmp_path / "project"
    project.mkdir()
    assert runtime.resolve_executable("r", _runtime_contract(version="4.4.1"), project) == str(versioned.resolve())

    root = tmp_path / "workspace"
    active_project = root / "projects" / "p"
    active_project.mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    (root / "uv.lock").write_text("locked", encoding="utf-8")
    (active_project / "renv.lock").write_text("locked", encoding="utf-8")
    assert (
        runtime.resolve_lockfile(active_project, _runtime_contract(lockfile="renv.lock"))
        == (active_project / "renv.lock").resolve()
    )
    assert (
        runtime.resolve_lockfile(active_project, _runtime_contract(lockfile="uv.lock")) == (root / "uv.lock").resolve()
    )
    assert runtime.resolve_lockfile(active_project, _runtime_contract(lockfile="../../../outside.lock")) is None
    assert runtime.resolve_lockfile(active_project, _runtime_contract(lockfile=str(tmp_path / "outside.lock"))) is None
    assert runtime.resolve_lockfile(active_project, _runtime_contract(lockfile=None)) is None


@pytest.mark.parametrize(
    ("runtime_name", "output", "expected"),
    [
        ("python", "Python 3.13.5", "3.13.5"),
        ("r", "R version 4.4.1", "4.4.1"),
        ("browser", "Node.js Version 24.1.0", "24.1.0"),
    ],
)
def test_runtime_version_parses_each_supported_runtime(
    monkeypatch, runtime_name: str, output: str, expected: str
) -> None:
    monkeypatch.setattr(runtime.subprocess, "run", lambda *args, **kwargs: _completed(output))
    assert runtime.runtime_version(runtime_name, "runtime") == expected


def test_version_probes_fail_closed_on_bad_exit_output_and_exceptions(monkeypatch) -> None:
    monkeypatch.setattr(runtime.subprocess, "run", lambda *args, **kwargs: _completed(returncode=1))
    assert runtime.runtime_version("python", "python") is None
    monkeypatch.setattr(runtime.subprocess, "run", lambda *args, **kwargs: _completed("not a version"))
    assert runtime.runtime_version("python", "python") is None
    assert runtime.runtime_version("unknown", "runtime") is None

    def failed(*args, **kwargs):
        raise OSError("not launchable")

    monkeypatch.setattr(runtime.subprocess, "run", failed)
    assert runtime.runtime_version("python", "python") is None
    assert runtime.package_manager_version("python", _runtime_contract(), "python") is None
    assert runtime.package_manager_version("r", _runtime_contract(package_manager="renv"), "Rscript") is None


@pytest.mark.parametrize("manager", ["uv", "npm"])
def test_package_manager_probes_parse_versions_and_fail_closed(monkeypatch, manager: str) -> None:
    contract = _runtime_contract(package_manager=manager)
    monkeypatch.setattr(runtime.shutil, "which", lambda _: "manager.exe")
    monkeypatch.setattr(runtime.subprocess, "run", lambda *args, **kwargs: _completed("1.2.3\n"))
    assert runtime.package_manager_version("python", contract, "python") == "1.2.3"
    monkeypatch.setattr(runtime.subprocess, "run", lambda *args, **kwargs: _completed("bad"))
    assert runtime.package_manager_version("python", contract, "python") is None
    monkeypatch.setattr(runtime.subprocess, "run", lambda *args, **kwargs: _completed(returncode=1))
    assert runtime.package_manager_version("python", contract, "python") is None
    monkeypatch.setattr(runtime.shutil, "which", lambda _: None)
    assert runtime.package_manager_version("python", contract, "python") is None


def test_renv_and_unknown_package_manager_probes(monkeypatch) -> None:
    monkeypatch.setattr(runtime.subprocess, "run", lambda *args, **kwargs: _completed("1.2.3\n"))
    assert runtime.package_manager_version("r", _runtime_contract(package_manager="renv"), "Rscript") == "1.2.3"
    monkeypatch.setattr(runtime.subprocess, "run", lambda *args, **kwargs: _completed(returncode=2))
    assert runtime.package_manager_version("r", _runtime_contract(package_manager="renv"), "Rscript") is None
    assert runtime.package_manager_version("python", _runtime_contract(package_manager="other"), "python") is None


def test_environment_check_blocks_missing_runtime_and_incompatible_runtime(tmp_path: Path, monkeypatch) -> None:
    project = _v2_project(tmp_path)
    (project / "uv.lock").unlink()
    monkeypatch.setattr(environment, "resolve_executable", lambda *args: None)
    missing = environment.check_environment(project, "python")
    assert missing["status"] == "blocked"
    assert any("executable is unavailable" in issue for issue in missing["issues"])
    assert any("lockfile is missing" in issue for issue in missing["issues"])
    assert environment.check_environment(project, "invalid")["status"] == "blocked"

    monkeypatch.setattr(environment, "resolve_executable", lambda *args: "python")
    monkeypatch.setattr(environment, "runtime_version", lambda *args: "3.12.0")
    monkeypatch.setattr(environment, "package_manager_version", lambda *args: "0.9")
    mismatch = environment.check_environment(project, "python")
    assert mismatch["status"] == "blocked"
    assert any("version mismatch" in issue for issue in mismatch["issues"])


def test_environment_browser_cache_and_optional_missing_probes(tmp_path: Path, monkeypatch) -> None:
    project = _v2_project(tmp_path)
    monkeypatch.setattr(environment, "resolve_executable", lambda *args: None)
    optional = environment.check_environment(project, "r")
    assert optional["status"] == "passed"
    assert optional["executable"] is None

    compute = load_structured_file(project / "compute.yaml")
    compute["browser"].update(required=True, version="24", package_manager="npm", package_manager_version="10")
    save_structured_file(project / "compute.yaml", compute)
    browser_lock = project / "tools" / "playwright" / "package-lock.json"
    browser_lock.parent.mkdir(parents=True)
    browser_lock.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(environment, "resolve_executable", lambda *args: "node")
    monkeypatch.setattr(environment, "runtime_version", lambda *args: "24.1.0")
    monkeypatch.setattr(environment, "package_manager_version", lambda *args: "10.0.0")
    browser_cache = project.resolve().parent.parent / "tools" / "playwright" / ".playwright"
    browser_cache.mkdir(parents=True)
    (browser_cache / "chromium-test").mkdir()
    browser = environment.check_environment(project, "browser")
    assert browser["status"] == "passed"
    assert browser["browser_installed"] is True


def test_environment_preflight_plugin_bindings_and_malformed_compute(tmp_path: Path, monkeypatch) -> None:
    project = _v2_project(tmp_path)
    compute = load_structured_file(project / "compute.yaml")
    compute["required_plugins"] = ["zotero-reference-manager"]
    save_structured_file(project / "compute.yaml", compute)
    monkeypatch.setattr(environment, "check_environment", lambda *args: {"status": "passed", "issues": []})
    missing = environment.preflight_environment(project)
    assert missing["status"] == "blocked"
    assert missing["checks"]["plugins"]["missing"] == ["zotero-reference-manager"]
    bindings = project / ".machine" / "plugin_bindings.json"
    bindings.parent.mkdir(parents=True, exist_ok=True)
    plugin_root = project / "plugin-cache" / "zotero"
    (plugin_root / "skills").mkdir(parents=True)
    bindings.write_text(
        json.dumps({"bindings": {"zotero-reference-manager": [{"root": str(plugin_root), "version": "1.0.0"}]}}),
        encoding="utf-8",
    )
    passed = environment.preflight_environment(project)
    assert passed["status"] == "passed"
    assert passed["checks"]["plugins"]["status"] == "pass"
    assert json.loads((project / "analysis" / "preflight.json").read_text(encoding="utf-8"))["status"] == "passed"

    bindings.write_text('{"bindings":{"zotero-reference-manager":[]}}', encoding="utf-8")
    invalid = environment.preflight_environment(project)
    assert invalid["status"] == "blocked"
    assert invalid["checks"]["plugins"]["status"] == "blocked"

    (project / "compute.yaml").write_text("contract_version: [", encoding="utf-8")
    blocked = environment.preflight_environment(project)
    assert blocked["status"] == "blocked"
    assert blocked["checks"]["compute_contract"]["status"] == "blocked"


def test_environment_prepare_dry_run_and_requires_lockfile(tmp_path: Path, monkeypatch) -> None:
    project = _v2_project(tmp_path)
    monkeypatch.setattr(
        environment, "check_environment", lambda *args: {"status": "blocked", "lockfile_present": False}
    )
    dry_run = environment.prepare_environment(project, "python")
    assert dry_run["executed"] is False
    assert dry_run["action"].startswith("dry-run")
    denied = environment.prepare_environment(project, "python", execute=True)
    assert denied["action"].startswith("blocked")
    assert "prepare_commands" not in denied


@pytest.mark.parametrize("runtime_name", ["python", "r", "browser"])
def test_environment_prepare_executes_locked_command_with_mocked_processes(
    tmp_path: Path, monkeypatch, runtime_name: str
) -> None:
    project = _v2_project(tmp_path)
    before = {
        "contract": "EnvironmentCheckV2",
        "runtime": runtime_name,
        "status": "blocked",
        "lockfile_present": True,
        "executable": "Rscript",
    }
    after = {**before, "status": "blocked", "issues": ["still blocked after prepare"]}
    checks = iter([before, after])
    monkeypatch.setattr(environment, "check_environment", lambda *args: next(checks))
    calls = []

    def mocked_run(command, **kwargs):
        calls.append((command, kwargs))
        return _completed("prepared")

    monkeypatch.setattr(environment.subprocess, "run", mocked_run)
    result = environment.prepare_environment(project, runtime_name, execute=True)
    assert result["executed"] is True
    assert result["prepare_exit_code"] == 0
    assert result["status"] == "blocked"  # preparation does not hide failed post-checks
    assert calls
    assert all(kwargs["capture_output"] and kwargs["text"] for _, kwargs in calls)
    if runtime_name == "browser":
        assert len(calls) == 2
        assert Path(calls[0][0][0]).stem.lower() == "npm"
        assert calls[0][0][1] == "ci"
        assert "PLAYWRIGHT_BROWSERS_PATH" in calls[0][1]["env"]
    else:
        assert len(calls) == 1


def test_environment_prepare_stops_after_failure_and_records_oserror(tmp_path: Path, monkeypatch) -> None:
    project = _v2_project(tmp_path)
    before = {"status": "blocked", "lockfile_present": True}
    after = {**before, "issues": []}
    checks = iter([before, after])
    monkeypatch.setattr(environment, "check_environment", lambda *args: next(checks))
    monkeypatch.setattr(
        environment.subprocess, "run", lambda *args, **kwargs: _completed(returncode=1, stderr="failed")
    )
    failed = environment.prepare_environment(project, "browser", execute=True)
    assert len(failed["prepare_commands"]) == 1
    assert failed["prepare_exit_code"] == 1

    checks = iter([before, after])
    monkeypatch.setattr(environment, "check_environment", lambda *args: next(checks))

    def cannot_launch(*args, **kwargs):
        raise OSError("npm missing")

    monkeypatch.setattr(environment.subprocess, "run", cannot_launch)
    errored = environment.prepare_environment(project, "python", execute=True)
    assert errored["prepare_commands"][0]["exit_code"] is None
    assert errored["prepare_exit_code"] is None


def test_runner_path_containment_extensions_and_hash(tmp_path: Path) -> None:
    project = _v2_project(tmp_path)
    allowed = ("analysis", "scripts")
    script = project / "analysis" / "valid.py"
    script.write_text("print('ok')", encoding="utf-8")
    assert runners._safe_script(project, script, "python", allowed) == script.resolve()
    assert runners._sha256(script) == "e651ef002de96727cf3b1f8533ebb5c1036d12d795ec486c4cbd4ed2872fde31"

    outside = tmp_path / "outside.py"
    outside.write_text("pass", encoding="utf-8")
    with pytest.raises(ContractValidationError):
        runners._safe_script(project, outside, "python", allowed)
    with pytest.raises(ContractValidationError):
        runners._safe_script(project, project / "project.yaml", "python", allowed)
    with pytest.raises(ContractValidationError):
        runners._safe_script(project, project / "analysis" / "missing.py", "python", allowed)

    alias = project / "analysis" / "escape.py"
    try:
        alias.symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"Symlink creation is unavailable on this Windows host: {exc}")
    with pytest.raises(ContractValidationError):
        runners._safe_script(project, alias, "python", allowed)


def test_runner_records_launch_error_and_failed_exit(tmp_path: Path, monkeypatch) -> None:
    project = _v2_project(tmp_path)
    script = project / "analysis" / "fail.py"
    script.write_text("raise SystemExit(1)", encoding="utf-8")
    monkeypatch.setattr(runners, "preflight_environment", lambda _: {"status": "passed"})
    monkeypatch.setattr(runners, "resolve_executable", lambda *args: "python")

    def fail_exit(*args, **kwargs):
        return _completed("out", "err", returncode=1)

    report = runners.run_python_script(project, script, subprocess_run=fail_exit)
    assert report["status"] == "failed"
    assert report["exit_code"] == 1

    def launch_error(*args, **kwargs):
        raise OSError("runtime missing")

    report = runners.run_python_script(project, script, subprocess_run=launch_error)
    assert report["status"] == "failed"
    assert report["exit_code"] is None
    assert Path(project / report["stderr_log"]).read_text(encoding="utf-8") == "runtime missing"


def test_runner_runs_r_script_with_v2_hash_and_timeout(tmp_path: Path, monkeypatch) -> None:
    project = _v2_project(tmp_path)
    compute = load_structured_file(project / "compute.yaml")
    compute["r"].update(
        required=True,
        version="4.4",
        package_manager="renv",
        package_manager_version="1.2.3",
        lockfile="renv.lock",
    )
    save_structured_file(project / "compute.yaml", compute)
    (project / "renv.lock").write_text("{}", encoding="utf-8")
    script = project / "scripts" / "model.R"
    script.parent.mkdir(exist_ok=True)
    script.write_text("print('ok')", encoding="utf-8")
    monkeypatch.setattr(runners, "preflight_environment", lambda _: {"status": "passed"})
    monkeypatch.setattr(runners, "resolve_executable", lambda *args: "Rscript")
    calls = []

    def timeout(command, **kwargs):
        calls.append((command, kwargs))
        raise subprocess.TimeoutExpired(command, kwargs["timeout"], output="partial")

    report = runners.run_r_script(project, script, subprocess_run=timeout)
    assert report["status"] == "failed"
    assert report["timed_out"] is True
    assert calls[0][1]["timeout"] == 30
    manifest = load_structured_file(project / ".machine" / "runs" / report["run_id"] / "manifest.json")
    assert manifest["execution"]["script_sha256"]
    assert manifest["execution"]["runtime"] == "r"


def test_runner_returns_preflight_and_executable_blocks(tmp_path: Path, monkeypatch) -> None:
    project = _v2_project(tmp_path)
    script = project / "analysis" / "hello.py"
    script.write_text("pass", encoding="utf-8")
    monkeypatch.setattr(runners, "preflight_environment", lambda _: {"status": "blocked", "issues": ["gate"]})
    assert runners.run_python_script(project, script)["status"] == "blocked"
    monkeypatch.setattr(runners, "preflight_environment", lambda _: {"status": "passed"})
    monkeypatch.setattr(runners, "resolve_executable", lambda *args: None)
    assert runners.run_python_script(project, script)["status"] == "blocked"


def test_governance_benchmark_command_blocks_bad_inputs_and_writes_reports(tmp_path: Path) -> None:
    project = tmp_path / "project"
    project.mkdir()
    missing = governance.aggregate_benchmark_file(project)
    assert missing["status"] == "block"
    source = project / "input.json"
    source.write_text("[]", encoding="utf-8")
    non_object = governance.aggregate_benchmark_file(project, input_path=source)
    assert non_object["status"] == "block"
    source.write_text("{broken", encoding="utf-8")
    malformed = governance.aggregate_benchmark_file(project, input_path=source)
    assert malformed["status"] == "block"
    source.write_text('{"cases": []}', encoding="utf-8")
    output = project / "custom" / "report.json"
    report = governance.aggregate_benchmark_file(project, input_path=source, output_path=output)
    assert report["output"] == str(output)
    assert output.is_file()

    attempt = governance.record_blocked_attempt(project, "draft", {"reason": "missing evidence"})
    envelope = json.loads(attempt.read_text(encoding="utf-8"))
    assert envelope["gate_eligible"] is False
    assert envelope["payload"]["reason"] == "missing evidence"
