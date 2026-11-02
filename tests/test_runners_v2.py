import subprocess
from pathlib import Path

from test_contracts_v2 import _v2_project

from article_machine.serialization import load_structured_file, save_structured_file
from article_machine.services.runners import run_python_script


def _ready_project(tmp_path: Path) -> Path:
    project = _v2_project(tmp_path)
    protocol = load_structured_file(project / "protocol.yaml")
    protocol["research_question"] = "Does the runner preserve provenance?"
    protocol["objectives"] = ["Validate execution."]
    save_structured_file(project / "protocol.yaml", protocol)
    from registration_fixtures import reviewed_registration_fixture
    reviewed_registration_fixture(project)
    return project


def test_run_python_records_hashes_logs_exit_code_and_environment(tmp_path: Path) -> None:
    project = _ready_project(tmp_path)
    script = project / "analysis" / "hello.py"
    script.write_text("print('ok')\n", encoding="utf-8")
    report = run_python_script(project, script)
    assert report["status"] == "passed"
    assert report["exit_code"] == 0
    manifest = load_structured_file(project / ".machine" / "runs" / report["run_id"] / "manifest.json")
    assert manifest["execution"]["script_sha256"]
    assert (project / report["environment_log"]).is_file()


def test_run_python_rejects_scripts_outside_allowed_directories(tmp_path: Path) -> None:
    project = _ready_project(tmp_path)
    script = project / "unsafe.py"
    script.write_text("print('unsafe')\n", encoding="utf-8")
    report = run_python_script(project, script)
    assert report["status"] == "blocked"
    assert "analysis/ or scripts/" in report["issues"][0]


def test_run_python_timeout_is_recorded_and_closes_run(tmp_path: Path) -> None:
    project = _ready_project(tmp_path)
    script = project / "analysis" / "slow.py"
    script.write_text("pass\n", encoding="utf-8")

    def timeout(command, **kwargs):
        assert kwargs["timeout"] == 30
        raise subprocess.TimeoutExpired(command, kwargs["timeout"])

    report = run_python_script(project, script, subprocess_run=timeout)

    assert report["status"] == "failed"
    assert report["timed_out"] is True
    manifest = load_structured_file(project / ".machine" / "runs" / report["run_id"] / "manifest.json")
    assert manifest["execution"]["script_sha256"]
    assert manifest["execution"]["timed_out"] is True
