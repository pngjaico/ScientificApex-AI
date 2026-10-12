from pathlib import Path

from article_machine import playwright_ops


def test_playwright_cli_uses_locked_workspace_package_not_npx(tmp_path: Path, monkeypatch) -> None:
    check = {
        "status": "pass",
        "node_path": "node",
        "cli_path": str(tmp_path / "tools" / "playwright" / "node_modules" / "playwright" / "cli.js"),
    }
    monkeypatch.setattr(playwright_ops, "playwright_available", lambda: check)
    calls = []

    class Completed:
        returncode = 0
        stdout = "ok"
        stderr = ""

    def fake_run(command, **kwargs):
        calls.append(command)
        return Completed()

    monkeypatch.setattr(playwright_ops.subprocess, "run", fake_run)
    report = playwright_ops._run_playwright_cli(["--version"], tmp_path)

    assert report["status"] == "pass"
    assert calls[0][:2] == ["node", check["cli_path"]]
    assert "npx" not in calls[0]


def test_qa_html_falls_back_to_playwright_cli_when_node_api_is_unavailable(tmp_path: Path, monkeypatch) -> None:
    html_path = tmp_path / "deck.html"
    html_path.write_text("<html><body><section>ok</section></body></html>", encoding="utf-8")

    monkeypatch.setattr(
        playwright_ops,
        "_run_playwright_script",
        lambda script, output_dir, timeout=120: {
            "status": "blocked",
            "stderr": "Cannot find module 'playwright'",
        },
    )

    cli_calls = []

    def fake_cli(args, output_dir, timeout=120):
        cli_calls.append(args)
        screenshot = tmp_path / "qa" / "layout-qa.png"
        screenshot.parent.mkdir(parents=True, exist_ok=True)
        screenshot.write_bytes(b"png")
        return {"status": "pass", "path": str(screenshot)}

    monkeypatch.setattr(playwright_ops, "_run_playwright_cli", fake_cli)

    report = playwright_ops.qa_html(html_path, tmp_path / "qa", "5-min")

    assert report["status"] == "pass"
    assert report["overflow_elements"] == []
    assert "screenshot" in cli_calls[0]


def test_qa_html_treats_transparent_background_as_missing_for_contrast(tmp_path: Path, monkeypatch) -> None:
    html_path = tmp_path / "deck.html"
    html_path.write_text("<html><body><section>ok</section></body></html>", encoding="utf-8")
    captured = {}

    def fake_script(script: str, output_dir: Path, timeout: int = 120) -> dict:
        captured["script"] = script
        return {
            "status": "pass",
            "overflow_elements": [],
            "contrast": {"status": "pass", "minimum_ratio": 12.0},
        }

    monkeypatch.setattr(playwright_ops, "_run_playwright_script", fake_script)

    report = playwright_ops.qa_html(html_path, tmp_path / "qa", "5-min")

    assert report["status"] == "pass"
    assert "if (alpha === 0) return null;" in captured["script"]


def test_export_html_pdf_uses_playwright_cli(tmp_path: Path, monkeypatch) -> None:
    html_path = tmp_path / "deck.html"
    pdf_path = tmp_path / "deck.pdf"
    html_path.write_text("<html><body>ok</body></html>", encoding="utf-8")

    monkeypatch.setattr(
        playwright_ops,
        "_run_playwright_script",
        lambda script, output_dir, timeout=120: {
            "status": "blocked",
            "stderr": "Cannot find module 'playwright'",
        },
    )

    def fake_cli(args, output_dir, timeout=120):
        pdf_path.write_bytes(b"%PDF-1.4\n")
        return {"status": "pass", "path": str(pdf_path)}

    monkeypatch.setattr(playwright_ops, "_run_playwright_cli", fake_cli)

    report = playwright_ops.export_html_pdf(html_path, pdf_path, "5-min")

    assert report["status"] == "pass"
    assert pdf_path.exists()
