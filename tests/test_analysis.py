from pathlib import Path

from article_machine.analysis import preflight, run_r_script
from article_machine.projects import init_project


def test_preflight_blocks_when_rscript_is_unavailable(tmp_path: Path, monkeypatch) -> None:
    project_dir = init_project(tmp_path, "NMA Project", "network-meta-analysis")
    monkeypatch.setattr("article_machine.analysis.shutil.which", lambda _: None)

    report = preflight(project_dir)

    assert report["status"] == "blocked"
    assert "Rscript" in report["checks"]["rscript"]["message"]
    assert "install" in report["checks"]["rscript"]["message"].lower()


def test_preflight_warns_but_passes_when_r_is_not_required(tmp_path: Path, monkeypatch) -> None:
    project_dir = init_project(tmp_path, "Review Project", "systematic-review")
    monkeypatch.setattr("article_machine.analysis.shutil.which", lambda _: None)

    report = preflight(project_dir)

    assert report["status"] == "passed"
    assert report["checks"]["rscript"]["status"] == "warning"


def test_run_r_script_records_logs_and_session_info(tmp_path: Path, monkeypatch) -> None:
    project_dir = init_project(tmp_path, "Meta Analysis", "network-meta-analysis")
    script_path = project_dir / "analysis" / "meta.R"
    script_path.write_text("cat('meta ok')\n", encoding="utf-8")

    monkeypatch.setattr("article_machine.analysis.shutil.which", lambda _: "C:/R/bin/Rscript.exe")

    calls = []

    class Completed:
        def __init__(self, stdout: str = "", stderr: str = "") -> None:
            self.returncode = 0
            self.stdout = stdout
            self.stderr = stderr

    def fake_run(command, capture_output, text, check, cwd):
        calls.append(command)
        if "-e" in command:
            return Completed(stdout="R version 4.4.0\nsessionInfo()")
        return Completed(stdout="meta ok")

    monkeypatch.setattr("article_machine.analysis.subprocess.run", fake_run)

    report = run_r_script(project_dir, script_path)

    assert report["status"] == "passed"
    assert report["stdout_log"].endswith("stdout.log")
    assert report["session_info"].endswith("sessionInfo.txt")
    assert (project_dir / report["stdout_log"]).is_file()
    assert (project_dir / report["session_info"]).is_file()
    assert len(calls) == 2
