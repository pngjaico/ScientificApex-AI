from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

from .runs import close_run, open_run, record_artifact
from .serialization import load_structured_file, save_structured_file


def _relative(project_dir: Path, path: Path) -> str:
    return path.relative_to(project_dir).as_posix()


def preflight(project_dir: Path) -> dict:
    project_dir = Path(project_dir)
    rscript = shutil.which("Rscript")
    compute = load_structured_file(project_dir / "compute.yaml")
    r_required = bool(compute.get("r", {}).get("required"))
    r_check = {
        "status": "pass" if rscript else ("blocked" if r_required else "warning"),
        "path": rscript,
        "message": (
            f"Rscript detected at {rscript}."
            if rscript
            else (
                "Rscript is not available. Install R for Windows and ensure `Rscript` is on PATH before running `.R`, `.Rmd`, or `.qmd` pipelines."
                if r_required
                else "Rscript is not available, but this project does not currently require R. The gate remains open."
            )
        ),
    }
    report = {
        "status": "passed" if (rscript or not r_required) else "blocked",
        "checks": {
            "rscript": r_check,
            "project_files": {
                "status": "pass",
                "message": "project.yaml, protocol.yaml, standards.yaml, and compute.yaml are expected in the active project root.",
            },
        },
    }
    save_structured_file(project_dir / "analysis" / "preflight.json", report)
    return report


def run_r_script(project_dir: Path, script_path: Path) -> dict:
    project_dir = Path(project_dir)
    script_path = Path(script_path)
    gate = preflight(project_dir)
    if gate["status"] != "passed":
        return gate

    rscript = shutil.which("Rscript")
    manifest = open_run(project_dir, mode="analysis", prompt=f"Run R script {script_path.name}")
    run_dir = project_dir / ".machine" / "runs" / manifest["run_id"] / "analysis" / "r" / script_path.stem
    run_dir.mkdir(parents=True, exist_ok=True)

    script_result = subprocess.run(
        [rscript, str(script_path)],
        capture_output=True,
        text=True,
        check=False,
        cwd=project_dir,
    )
    stdout_log = run_dir / "stdout.log"
    stderr_log = run_dir / "stderr.log"
    stdout_log.write_text(script_result.stdout or "", encoding="utf-8")
    stderr_log.write_text(script_result.stderr or "", encoding="utf-8")

    session_result = subprocess.run(
        [rscript, "-e", "sessionInfo()"],
        capture_output=True,
        text=True,
        check=False,
        cwd=project_dir,
    )
    session_info = run_dir / "sessionInfo.txt"
    session_info.write_text(session_result.stdout or "", encoding="utf-8")

    record_artifact(project_dir, manifest["run_id"], stdout_log)
    record_artifact(project_dir, manifest["run_id"], stderr_log)
    record_artifact(project_dir, manifest["run_id"], session_info)

    status = "passed" if script_result.returncode == 0 else "failed"
    close_run(project_dir, manifest["run_id"], status=status)
    return {
        "status": status,
        "run_id": manifest["run_id"],
        "stdout_log": _relative(project_dir, stdout_log),
        "stderr_log": _relative(project_dir, stderr_log),
        "session_info": _relative(project_dir, session_info),
    }
