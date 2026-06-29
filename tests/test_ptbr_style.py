from __future__ import annotations

import json
from pathlib import Path

from docx import Document

from article_machine.cli import main
from article_machine.ptbr_style import (
    audit_text,
    build_generation_brief,
    naturalize_text,
    read_text_for_audit,
    render_markdown_report,
)


def test_ptbr_style_flags_forbidden_translationese_and_missing_hr_definition() -> None:
    report = audit_text(
        "A camada contextual mostrou HR 0,70. "
        "Esse sinal convergente reforca o eixo obesidade-metabolismo."
    )

    codes = {issue["code"] for issue in report["issues"]}

    assert report["status"] == "block"
    assert "forbidden_term" in codes
    assert "hr_without_first_definition" in codes
    assert "translationese_pattern" in codes


def test_ptbr_style_accepts_defined_hr_and_natural_portuguese() -> None:
    report = audit_text(
        "Na primeira mencao, a medida foi descrita como razao de riscos "
        "instantaneos (hazard ratio, HR). A cirurgia bariatrica foi analisada "
        "separadamente da rede farmacologica."
    )

    assert report["status"] == "pass"
    assert report["issues"] == []


def test_ptbr_style_accepts_prisma_nma_and_pscore_ranqueamento_context() -> None:
    report = audit_text(
        "A revisão seguiu PRISMA-NMA. P-score é uma medida de ranqueamento. "
        "A razão de riscos instantâneos (hazard ratio, HR) foi usada no resultado."
    )

    codes = {issue["code"] for issue in report["issues"]}

    assert "unexpanded_nma" not in codes
    assert "statistical_term_without_context" not in codes


def test_ptbr_style_markdown_report_summarizes_counts() -> None:
    report = audit_text("A hub-dependencia apareceu sem explicacao. HR 0,90.")
    rendered = render_markdown_report([report], title="Auditoria PT-BR")

    assert "# Auditoria PT-BR" in rendered
    assert "Status geral: block" in rendered
    assert "influência de um estudo dominante na rede" in rendered


def test_cli_ptbr_audit_writes_json_and_markdown_reports(tmp_path: Path) -> None:
    source = tmp_path / "resumo.md"
    source.write_text("A camada contextual apresentou HR 0,70.", encoding="utf-8")
    markdown = tmp_path / "audit.md"
    json_report = tmp_path / "audit.json"

    exit_code = main(
        [
            "style",
            "ptbr-audit",
            str(source),
            "--output",
            str(markdown),
            "--json-output",
            str(json_report),
        ]
    )

    assert exit_code == 1
    assert "camada contextual" in markdown.read_text(encoding="utf-8")
    payload = json.loads(json_report.read_text(encoding="utf-8"))
    assert payload["status"] == "block"


def test_cli_ptbr_brief_writes_generation_profile(tmp_path: Path) -> None:
    output = tmp_path / "brief.md"

    exit_code = main(
        [
            "style",
            "ptbr-brief",
            "--deliverable",
            "resumo expandido",
            "--audience",
            "orientador",
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    text = output.read_text(encoding="utf-8")
    assert "Perfil De Geração Científica PT-BR" in text
    assert "resumo expandido" in text


def test_ptbr_generation_brief_enforces_native_brazilian_scientific_style() -> None:
    brief = build_generation_brief(deliverable="resumo de congresso", audience="orientador")

    assert "Escreva primeiro em português brasileiro" in brief
    assert "Objetivo, Métodos, Resultados e Conclusão" in brief
    assert "razão de riscos instantâneos (hazard ratio, HR)" in brief
    assert "não traduza template inglês" in brief.lower()
    assert "Barreira De Naturalidade" in brief
    assert "framework, endpoint, outcome, baseline" in brief
    assert "Revista de Saúde Pública" in brief


def test_naturalize_text_replaces_ai_style_without_changing_numbers() -> None:
    source = (
        "A camada contextual mostrou sinal convergente do eixo obesidade-metabolismo. "
        "GLP1-RA teve HR 0,727 e P-score 0,8926."
    )

    result = naturalize_text(source)

    assert "camada contextual" not in result.lower()
    assert "sinal convergente" not in result.lower()
    assert "eixo obesidade-metabolismo" not in result.lower()
    assert "0,727" in result
    assert "0,8926" in result
    assert "razão de riscos instantâneos (hazard ratio, HR)" in result


def test_ptbr_audit_reads_docx_content(tmp_path: Path) -> None:
    docx_path = tmp_path / "resumo.docx"
    doc = Document()
    doc.add_paragraph("A camada contextual apresentou HR 0,70.")
    doc.save(docx_path)

    text = read_text_for_audit(docx_path)
    report = audit_text(text, path=docx_path)

    assert "camada contextual" in text
    assert report["status"] == "block"


def test_ptbr_style_blocks_mojibake_and_unnecessary_english_terms() -> None:
    report = audit_text(
        "O framework avaliou o endpoint no baseline. "
        "A conclusÃ£o foi registrada no resumo."
    )

    codes = {issue["code"] for issue in report["issues"]}

    assert report["status"] == "block"
    assert "mojibake" in codes
    assert "unnecessary_english" in codes


def test_ptbr_style_allows_english_terms_inside_vancouver_references() -> None:
    report = audit_text(
        "## Referências\n\n"
        "1. Wu CC, Su CC. Reduced risks using a target trial emulation framework. "
        "Diabetes Metab. 2025;51:101695. doi:10.1016/j.diabet.2025.101695"
    )

    assert report["status"] == "pass"
    assert report["issues"] == []


def test_ptbr_style_flags_nominalization_overload_and_translation_cliches() -> None:
    report = audit_text(
        "No contexto da operacionalização da avaliação da implementação da interpretação "
        "da caracterização da associação, evidencia-se a necessidade de contextualização."
    )

    codes = {issue["code"] for issue in report["issues"]}

    assert "nominalization_overload" in codes
    assert "translation_cliche" in codes


def test_naturalize_text_replaces_common_translation_cliches_and_english_terms() -> None:
    source = "No contexto do framework, o endpoint foi avaliado no baseline."

    result = naturalize_text(source)

    assert "No contexto" not in result
    assert "framework" not in result
    assert "endpoint" not in result
    assert "baseline" not in result
    assert "Na análise" in result
    assert "modelo de trabalho" in result
    assert "desfecho" in result
    assert "início do seguimento" in result


def test_naturalize_text_preserves_sentence_initial_capitalization() -> None:
    source = "Os estudos foram avaliados. No contexto do framework, o endpoint foi analisado."

    result = naturalize_text(source)

    assert ". Na análise do modelo de trabalho" in result
    assert "o desfecho foi analisado" in result


def test_cli_ptbr_naturalize_writes_cleaner_text_and_report(tmp_path: Path) -> None:
    source = tmp_path / "entrada.md"
    target = tmp_path / "saida.md"
    report_path = tmp_path / "relatorio.json"
    source.write_text("A camada contextual avaliou HR 0,70 no baseline.", encoding="utf-8")

    exit_code = main(
        [
            "style",
            "ptbr-naturalize",
            str(source),
            "--output",
            str(target),
            "--json-output",
            str(report_path),
        ]
    )

    assert exit_code == 0
    output_text = target.read_text(encoding="utf-8")
    assert "camada contextual" not in output_text
    assert "baseline" not in output_text
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert payload["status"] in {"pass", "block"}
