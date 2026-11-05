"""Portable tests for document extraction and its optional Tesseract integration."""

from __future__ import annotations

from pathlib import Path

import docx
import pytest
from PIL import Image, ImageDraw

import article_machine.services.document_extraction as extraction_service
from article_machine.projects import init_project
from article_machine.services.document_extraction import (
    collapse_doubled_glyphs,
    extract_document,
    extract_project_documents,
    resolve_tesseract,
    text_quality,
)


def _write_minimal_pdf(path: Path) -> None:
    """Write a valid one-page, blank PDF using only the Python standard library."""
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << >> /Contents 4 0 R >>",
        b"<< /Length 0 >>\nstream\n\nendstream",
    ]
    content = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, body in enumerate(objects, start=1):
        offsets.append(len(content))
        content.extend(f"{number} 0 obj\n".encode("ascii"))
        content.extend(body)
        content.extend(b"\nendobj\n")
    xref_offset = len(content)
    content.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    content.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        content.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    content.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(content)


def _tesseract_or_skip() -> dict:
    tess = resolve_tesseract()
    if not tess.get("available"):
        pytest.skip("SKIPPED: Tesseract executable is not installed or unavailable.")
    missing = {"por", "eng"} - set(tess.get("languages", []))
    if missing:
        pytest.skip(f"SKIPPED: Tesseract language data missing: {', '.join(sorted(missing))}.")
    return tess


def test_resolve_tesseract_when_portuguese_and_english_are_available() -> None:
    tess = _tesseract_or_skip()
    assert "tesseract" in Path(tess["cmd"]).name.lower()
    assert {"por", "eng"}.issubset(tess["languages"])


def test_collapse_doubled_glyphs_and_quality() -> None:
    raw = "CCEERRTTIIFFIICCAADDOO DDEE PPUUBBLLIICCAAÇÇÃÃOO"
    assert collapse_doubled_glyphs(raw) == "CERTIFICADO DE PUBLICAÇÃO"

    empty_q = text_quality("")
    assert empty_q["chars"] == 0
    assert empty_q["score"] == 0.0

    good_q = text_quality("Synthetic software parser validation with several readable words.")
    assert good_q["score"] > 0.65
    assert good_q["alpha_ratio"] > 0.8


def test_extract_image_with_tesseract_ocr_when_por_and_eng_are_available(tmp_path: Path) -> None:
    _tesseract_or_skip()
    img_path = tmp_path / "placa_sintetica.png"
    img = Image.new("RGB", (900, 180), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 60), "ARTICLE MACHINE OCR TEST 2026", fill=(0, 0, 0))
    img.save(img_path)

    manifest = extract_document(img_path, tmp_path / "extracted_img", ocr="force", lang="por+eng")

    assert manifest["status"] == "pass"
    assert manifest["page_count_total"] == 1
    assert Path(manifest["output_dir"]).is_dir()
    text_md = (Path(manifest["output_dir"]) / "text.md").read_text(encoding="utf-8")
    assert "ARTICLE" in text_md or "MACHINE" in text_md


def test_forced_pdf_ocr_route_with_mocked_engine(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Exercise real PDF rendering and OCR routing without requiring Tesseract."""
    pdf_path = tmp_path / "pdf_sintetico.pdf"
    _write_minimal_pdf(pdf_path)
    monkeypatch.setattr(
        extraction_service,
        "resolve_tesseract",
        lambda: {"available": True, "cmd": "mock-tesseract", "default_lang": "por+eng", "issues": []},
    )
    calls: list[str] = []

    def fake_ocr(image: Image.Image, tess: dict, lang: str) -> tuple[str, float]:
        calls.append(lang)
        assert image.size[0] > 0 and image.size[1] > 0
        assert tess["cmd"] == "mock-tesseract"
        return "Synthetic OCR route was reached for this blank PDF page.", 92.0

    monkeypatch.setattr(extraction_service, "_ocr_pil_image", fake_ocr)
    manifest = extract_document(pdf_path, tmp_path / "extracted_pdf", ocr="force", lang="por+eng")

    assert manifest["status"] == "pass"
    assert manifest["page_count_total"] == 1
    assert manifest["pages_by_method"] == {"ocr": 1}
    assert manifest["pages_needing_verification"] == [1]
    assert calls == ["por+eng"]
    text_md = (Path(manifest["output_dir"]) / "text.md").read_text(encoding="utf-8")
    assert "Synthetic OCR route" in text_md


def test_extract_docx_with_synthetic_software_table(tmp_path: Path) -> None:
    doc_path = tmp_path / "validacao_parser.docx"
    doc = docx.Document()
    doc.add_heading("Synthetic Parser Validation", level=1)
    doc.add_paragraph("This software fixture checks native text and table extraction only.")
    table = doc.add_table(rows=3, cols=2)
    data = [["Component", "Status"], ["PDF parser", "fixture"], ["OCR route", "mocked"]]
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            table.cell(row_index, col_index).text = value
    doc.save(str(doc_path))

    manifest = extract_document(doc_path, tmp_path / "extracted_docx")

    assert manifest["status"] == "pass"
    assert manifest["table_count"] == 1
    csv_path = Path(manifest["output_dir"]) / "tables" / "docx_t01.csv"
    assert csv_path.exists()
    csv_content = csv_path.read_text(encoding="utf-8-sig")
    assert "PDF parser" in csv_content
    assert "mocked" in csv_content


def test_extract_project_documents_for_machine_governance_with_synthetic_pdf(tmp_path: Path) -> None:
    project = init_project(tmp_path, "PDF Extraction Test", "machine-governance")
    source_pdf = project / "sources" / "documento_sintetico.pdf"
    _write_minimal_pdf(source_pdf)
    original_bytes = source_pdf.read_bytes()

    index = extract_project_documents(project, ocr="off", table_strategy="off")

    assert index["status"] == "pass"
    assert index["file_count"] == 1
    assert (project / "sources" / "extracted" / "index.json").is_file()
    assert source_pdf.read_bytes() == original_bytes

    cached = extract_project_documents(project, ocr="off", table_strategy="off")
    assert cached["status"] == "pass"


def test_unregistered_scientific_project_is_blocked_before_extraction(tmp_path: Path) -> None:
    project = init_project(tmp_path, "Unregistered Scientific Project", "systematic-review")
    source_pdf = project / "sources" / "documento_sintetico.pdf"
    _write_minimal_pdf(source_pdf)
    original_bytes = source_pdf.read_bytes()
    extracted_root = project / "sources" / "extracted"

    result = extract_project_documents(project, ocr="off", table_strategy="off")

    assert result["status"] == "blocked"
    assert any("registration" in issue.lower() or "registro" in issue.lower() for issue in result["issues"])
    assert not extracted_root.exists()
    assert source_pdf.read_bytes() == original_bytes
