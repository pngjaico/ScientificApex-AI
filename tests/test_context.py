from pathlib import Path

from article_machine.context import build_task_packet
from article_machine.projects import init_project


def test_build_task_packet_saves_compact_context_for_mode(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "Gut Simulation", "intestinal-digital-twin")

    packet = build_task_packet(
        project_dir,
        mode="bootstrap",
        active_hypothesis="A digital twin can estimate perfusion collapse under ischemia.",
    )

    assert packet["mode"] == "bootstrap"
    assert packet["active_hypothesis"].startswith("A digital twin")
    assert packet["project"]["lane"] == "computational-discovery"
    assert "deliverables" in packet
    assert (project_dir / packet["packet_path"]).is_file()
    rejected = build_task_packet(project_dir, mode="discovery")
    assert rejected["status"] == "blocked"
    assert "packet_path" not in rejected
