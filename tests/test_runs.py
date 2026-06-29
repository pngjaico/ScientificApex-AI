from pathlib import Path

from article_machine.projects import init_project
from article_machine.runs import close_run, open_run, record_artifact, replay_run


def test_run_manifest_records_artifacts_and_replay_metadata(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Replay Project", "systematic-review")
    artifact = project_dir / "analysis" / "summary.txt"
    artifact.write_text("summary", encoding="utf-8")

    manifest = open_run(project_dir, mode="analysis", prompt="Run analysis")
    record_artifact(project_dir, manifest["run_id"], artifact)
    closed = close_run(project_dir, manifest["run_id"], status="passed")
    replay = replay_run(project_dir, manifest["run_id"])

    assert closed["status"] == "passed"
    assert replay["run_id"] == manifest["run_id"]
    assert replay["artifacts"][0]["path"] == "analysis/summary.txt"
    assert replay["artifacts"][0]["sha256"]
