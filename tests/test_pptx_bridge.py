from pathlib import Path
import zipfile

from article_machine.pptx_bridge import export_editable_pptx
from article_machine.serialization import save_structured_file


def test_pptx_export_embeds_article_machine_metadata(tmp_path: Path) -> None:
    storyboard_path = tmp_path / "storyboard.yaml"
    conference_path = tmp_path / "conference.yaml"
    output_path = tmp_path / "deck.pptx"
    save_structured_file(
        storyboard_path,
        {
            "scenes": [
                {
                    "title": "Finding",
                    "body": "Treatment improved remission.",
                    "speaker_notes": "Keep interpretation cautious.",
                    "source_claim_ids": ["claim-001"],
                }
            ]
        },
    )
    save_structured_file(
        conference_path,
        {
            "event_name": "Congress",
            "authors": ["A. Researcher"],
            "affiliations": ["Lab"],
            "profile": "5-min",
            "qr": {"url": "https://example.org"},
        },
    )

    report = export_editable_pptx(storyboard_path, output_path, "deck", conference_path=conference_path)

    assert report["status"] == "pass"
    with zipfile.ZipFile(output_path) as pptx:
        names = set(pptx.namelist())
        metadata = pptx.read("docProps/article-machine.json").decode("utf-8")
        assert "docProps/article-machine.json" in names
        assert "ppt/notes/article-machine-notes.md" in names
        assert "claim-001" in metadata
        assert "A. Researcher" in metadata


def test_poster_pptx_export_is_single_slide(tmp_path: Path) -> None:
    storyboard_path = tmp_path / "storyboard.yaml"
    conference_path = tmp_path / "conference.yaml"
    output_path = tmp_path / "poster.pptx"
    save_structured_file(
        storyboard_path,
        {
            "scenes": [
                {
                    "scene_id": "header",
                    "role": "header",
                    "title": "Poster title",
                    "body": "Poster subtitle",
                    "span": 12,
                    "source_claim_ids": [],
                },
                {
                    "scene_id": "methods",
                    "role": "methods",
                    "title": "Methods",
                    "body": "Systematic review and frequentist diagnostic network meta-analysis.",
                    "span": 6,
                    "source_claim_ids": ["claim-001"],
                },
            ]
        },
    )
    save_structured_file(
        conference_path,
        {
            "event_name": "Congress Poster",
            "authors": ["A. Researcher"],
            "affiliations": ["Lab"],
            "profile": "digital 16:9 landscape",
            "qr": {"url": "https://example.org"},
        },
    )

    report = export_editable_pptx(storyboard_path, output_path, "poster", conference_path=conference_path)

    assert report["status"] == "pass"
    assert report["slide_count"] == 1
    with zipfile.ZipFile(output_path) as pptx:
        names = set(pptx.namelist())
        assert "ppt/slides/slide1.xml" in names
        assert "ppt/slides/slide2.xml" not in names
