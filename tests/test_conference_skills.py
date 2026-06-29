from pathlib import Path


REQUIRED_CONFERENCE_SKILLS = [
    "conference-deliverable-router",
    "conference-requirements-importer",
    "conference-slides-html",
    "conference-posters-html",
    "visual-backend-router",
    "playwright-layout-qa",
    "pptx-export-bridge",
    "submission-ops-playwright",
    "speaker-notes-timing",
    "paper-to-talk",
    "paper-to-poster",
]


def test_conference_skills_exist_with_skill_frontmatter() -> None:
    workspace = Path(__file__).resolve().parents[1]
    for skill_name in REQUIRED_CONFERENCE_SKILLS:
        skill_path = workspace / "skills" / skill_name / "SKILL.md"
        assert skill_path.exists(), skill_name
        text = skill_path.read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert f"name: {skill_name}" in text
        assert "description: Use when" in text
