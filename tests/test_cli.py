from pathlib import Path

from article_machine.cli import main
from article_machine.projects import init_project


def _seed_claims(project_dir: Path) -> None:
    (project_dir / "sources" / "converted" / "study-001.md").write_text(
        "Remission improved by 15%.\n",
        encoding="utf-8",
    )
    (project_dir / "evidence" / "claim_map.jsonl").write_text(
        (
            '{"claim_id":"claim-supported","statement":"Intervention improved remission.",'
            '"source_path":"sources/converted/study-001.md","source_excerpt":"Remission improved by 15%.",'
            '"reference_key":"smith2024","status":"supported"}\n'
        ),
        encoding="utf-8",
    )
    (project_dir / "drafts" / "references.bib").write_text(
        "@article{smith2024,\n  title={Study 1},\n  year={2024}\n}\n",
        encoding="utf-8",
    )


def test_cli_init_creates_project(tmp_path: Path) -> None:
    exit_code = main(
        [
            "init",
            "CLI Project",
            "--type",
            "systematic-review",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert (tmp_path / "projects" / "cli-project" / "project.yaml").exists()


def test_cli_congress_import_and_deck_plan(tmp_path: Path) -> None:
    project_dir = init_project(tmp_path, "CLI Deck", "systematic-review")
    _seed_claims(project_dir)

    import_exit = main(
        [
            "congress",
            "import",
            str(project_dir),
            "--source",
            "# Event\n\nOral presentation. Duration: 5 minutes. Maximum 5 slides.\n",
            "--kind",
            "deck",
            "--slug",
            "cli-deck",
        ]
    )
    plan_exit = main(["deck", "plan", str(project_dir / "deliverables" / "cli-deck")])

    assert import_exit == 0
    assert plan_exit == 0
    assert (project_dir / "deliverables" / "cli-deck" / "conference.yaml").exists()
    assert (project_dir / "deliverables" / "cli-deck" / "storyboard.yaml").exists()
