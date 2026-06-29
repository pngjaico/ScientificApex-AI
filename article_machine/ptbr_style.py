from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PTBR_STYLE_SUBSTITUTIONS: list[dict[str, str]] = [
    {
        "term": "camada contextual",
        "replacement": "análise separada usada para interpretação",
        "reason": "Evita abstração traduzida; diz o que foi feito.",
    },
    {
        "term": "camada bariátrica contextual",
        "replacement": "análise separada da cirurgia bariátrica",
        "reason": "Mantém a separação metodológica sem parecer jargão.",
    },
    {
        "term": "hub-dependência",
        "replacement": "influência de um estudo dominante na rede",
        "reason": "Explica o problema estatístico em linguagem compreensível.",
    },
    {
        "term": "eixo obesidade-metabolismo",
        "replacement": "relação entre obesidade, alterações metabólicas e risco de câncer",
        "reason": "Substitui metáfora vaga por relação causal/associativa explícita.",
    },
    {
        "term": "sinal farmacológico",
        "replacement": "associação observada para a classe medicamentosa",
        "reason": "Evita linguagem promocional e mantém tom associativo.",
    },
    {
        "term": "sinal convergente",
        "replacement": "padrão observado em diferentes análises",
        "reason": "Troca frase de aparência automatizada por descrição direta.",
    },
    {
        "term": "NMA",
        "replacement": "meta-análise em rede",
        "reason": "Em texto corrido em português, usar a expressão por extenso após definir a sigla.",
    },
]


TRANSLATIONESE_PATTERNS: list[dict[str, str]] = [
    {
        "pattern": "camada",
        "suggestion": "Use 'análise', 'grupo', 'conjunto de estudos' ou outra descrição concreta.",
    },
    {
        "pattern": "sinal",
        "suggestion": "Use 'associação', 'resultado', 'padrão observado' ou 'estimativa'.",
    },
    {
        "pattern": "eixo",
        "suggestion": "Explique a relação biológica ou epidemiológica em vez de usar metáfora.",
    },
]


TRANSLATION_CLICHES: list[dict[str, str]] = [
    {"pattern": "no contexto de", "replacement": "na análise de"},
    {"pattern": "no contexto do", "replacement": "na análise do"},
    {"pattern": "no contexto da", "replacement": "na análise da"},
    {"pattern": "em termos de", "replacement": "quanto a"},
    {"pattern": "à luz de", "replacement": "considerando"},
    {"pattern": "evidencia-se", "replacement": "os dados mostram"},
    {"pattern": "ressalta-se", "replacement": "é importante observar"},
    {"pattern": "destaca-se", "replacement": "observa-se"},
    {"pattern": "caracterizado por", "replacement": "com"},
]


UNNECESSARY_ENGLISH_TERMS: list[dict[str, str]] = [
    {"term": "framework", "replacement": "modelo de trabalho"},
    {"term": "endpoint", "replacement": "desfecho"},
    {"term": "outcome", "replacement": "desfecho"},
    {"term": "baseline", "replacement": "início do seguimento"},
    {"term": "arm-level", "replacement": "por grupo"},
    {"term": "layer", "replacement": "análise"},
    {"term": "signal", "replacement": "associação observada"},
    {"term": "hub", "replacement": "estudo dominante"},
]


MOJIBAKE_PATTERNS = ["Ã", "Â", "â€", "�"]


HR_DEFINITION_TERMS = [
    "razao de riscos instantaneos",
    "razao de risco instantaneo",
    "hazard ratio",
]


STATISTICAL_TERMS: list[dict[str, str]] = [
    {
        "term": "P-score",
        "accepted_explanations": ["probabilidade de ranqueamento", "ranking", "ordena", "ranqueamento", "ranquear"],
        "message": "P-score aparece sem explicação curta de que é uma medida de ranqueamento.",
    },
    {
        "term": "tau2",
        "accepted_explanations": ["heterogeneidade", "variabilidade entre estudos"],
        "message": "tau2 aparece sem explicação curta de heterogeneidade.",
    },
    {
        "term": "I2",
        "accepted_explanations": ["heterogeneidade", "variabilidade"],
        "message": "I2 aparece sem explicação curta de heterogeneidade.",
    },
]


AI_TONE_TERMS = [
    "robusto",
    "inovador",
    "transformador",
    "disruptivo",
    "definitivo",
    "prova causal",
    "100% perfeito",
    "perfeito",
    "salvação",
    "publicável",
]


LONG_SENTENCE_WORD_LIMIT = 42
NOMINALIZATION_LIMIT = 5


PTBR_STYLE_SOURCE_NOTES: list[dict[str, str]] = [
    {
        "source": "Revista de Saúde Pública - instruções aos autores",
        "url": "https://rsp.fsp.usp.br/pt-br/instrucoes-aos-autores/",
        "lesson": "Resumo estruturado em Objetivo, Métodos, Resultados e Conclusão; revisão editorial privilegia clareza, brevidade, objetividade e solidez.",
    },
    {
        "source": "Revista de Saúde Pública - categorias de artigos",
        "url": "https://rsp.fsp.usp.br/pt-br/categorias-de-artigos/",
        "lesson": "Revisão sistemática deve descrever busca, critérios de seleção e síntese dos resultados.",
    },
    {
        "source": "Revista de Saúde Pública - preparo do manuscrito",
        "url": "https://rsp.fsp.usp.br/pt-br/preparo-do-manuscrito/",
        "lesson": "Resultados devem seguir sequência lógica e o texto deve restringir a descrição aos dados importantes.",
    },
    {
        "source": "SciELO - exemplo de revisão sistemática em português",
        "url": "https://scielo.pt/scielo.php?pid=S1645-00862022000100110&script=sci_arttext",
        "lesson": "Resumo natural em português usa verbos diretos: realizou-se, utilizou-se, foram analisados, constatou-se, conclui-se.",
    },
    {
        "source": "BioSCIENCE - revisão em português sobre cirurgia bariátrica e câncer colorretal",
        "url": "https://bioscience.org.br/bioscience/index.php/bioscience/article/view/551",
        "lesson": "Resumo biomédico brasileiro usa rótulos objetivos: Introdução, Objetivo, Método, Resultados e Conclusão.",
    },
    {
        "source": "EQUATOR Network - PRISMA 2020",
        "url": "https://www.equator-network.org/reporting-guidelines/prisma/",
        "lesson": "Revisões sistemáticas e meta-análises devem seguir checklist de relato; há tradução brasileira do PRISMA 2020.",
    },
    {
        "source": "LA-BORA! gov - Linguagem Simples",
        "url": "https://www.gov.br/servidor/pt-br/assuntos/laboragov/curadoria-tematica/linguagem-simples",
        "lesson": "Vá direto ao ponto, evite siglas, estrangeirismos e jargões, use frases curtas e troque substantivos abstratos por verbos de ação.",
    },
    {
        "source": "Guia de Edição de Serviços do Gov.br",
        "url": "https://www.gov.br/pt-br/guia-de-edicao-de-servicos-do-gov.br/escrevendo-o-seu-texto",
        "lesson": "Use voz ativa, sentenças curtas, ordem direta, palavras nativas e consistência terminológica.",
    },
    {
        "source": "Manual de Comunicação do Senado - linguagem simples",
        "url": "https://www12.senado.leg.br/manualdecomunicacao/estilos/palavras-mais-simples",
        "lesson": "Explique termos técnicos, jargões, estrangeirismos e siglas; use ordem direta e parágrafos claros com um assunto.",
    },
]


SECTION_PATTERNS: dict[str, list[str]] = {
    "introducao": [
        "A obesidade se associa a alterações metabólicas que podem influenciar o risco de câncer colorretal.",
        "O problema clínico deve ser apresentado sem promessa causal antes dos dados.",
    ],
    "objetivo": [
        "Avaliar a associação entre {exposure} e {outcome}.",
        "Comparar {interventions} quanto a {outcome}.",
    ],
    "metodos": [
        "Foi realizada revisão sistemática com meta-análise em rede.",
        "A busca foi realizada em {databases}, com critérios de inclusão e exclusão definidos previamente.",
        "A seleção dos estudos foi feita por revisores independentes quando aplicável.",
    ],
    "resultados": [
        "Foram incluídos {n_studies} estudos.",
        "A estimativa deve ser apresentada com medida, intervalo de confiança e interpretação curta.",
    ],
    "conclusao": [
        "Os achados sugerem associação, não prova causal.",
        "A conclusão deve responder ao objetivo e explicitar a incerteza.",
    ],
}


def _strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def _norm(value: str) -> str:
    value = _strip_accents(value).lower()
    value = value.replace("‑", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", value)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _line_excerpt(text: str, line_number: int) -> str:
    lines = text.splitlines()
    if not lines:
        return ""
    idx = min(max(line_number - 1, 0), len(lines) - 1)
    return lines[idx].strip()


def _looks_like_reference_line(excerpt: str) -> bool:
    stripped = excerpt.strip()
    if re.match(r"^\d+\.\s+\S+", stripped):
        return True
    return bool(re.search(r"\bdoi:\s*10\.\d{4,9}/", stripped, flags=re.IGNORECASE))


def _issue(
    *,
    code: str,
    severity: str,
    message: str,
    line: int,
    term: str = "",
    suggestion: str = "",
    excerpt: str = "",
    path: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "code": code,
        "severity": severity,
        "line": line,
        "message": message,
    }
    if term:
        payload["term"] = term
    if suggestion:
        payload["suggestion"] = suggestion
    if excerpt:
        payload["excerpt"] = excerpt
    if path:
        payload["path"] = path
    return payload


def _iter_term_matches(text: str, term: str) -> list[tuple[int, int]]:
    normalized_text = _norm(text)
    normalized_term = _norm(term)
    if not normalized_term:
        return []

    matches = []
    for match in re.finditer(rf"(?<!\w){re.escape(normalized_term)}(?!\w)", normalized_text):
        matches.append((match.start(), match.end()))
    return matches


def _has_hr_definition(text: str, first_hr_offset: int) -> bool:
    window = _norm(text[max(0, first_hr_offset - 220): first_hr_offset + 220])
    return any(term in window for term in HR_DEFINITION_TERMS)


def _sentence_word_count(sentence: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ-]+\b", sentence))


def _preserve_initial_case(replacement: str, matched: str) -> str:
    if not replacement or not matched:
        return replacement
    if matched[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def _replace_phrase(text: str, phrase: str, replacement: str) -> str:
    return re.sub(
        re.escape(phrase),
        lambda match: _preserve_initial_case(replacement, match.group(0)),
        text,
        flags=re.IGNORECASE,
    )


def _replace_word(text: str, term: str, replacement: str) -> str:
    return re.sub(
        rf"\b{re.escape(term)}\b",
        lambda match: _preserve_initial_case(replacement, match.group(0)),
        text,
        flags=re.IGNORECASE,
    )


def _nominalization_count(sentence: str) -> int:
    suffixes = (
        "cao",
        "coes",
        "mento",
        "mentos",
        "dade",
        "dades",
        "encia",
        "encias",
        "izacao",
        "izacoes",
    )
    words = re.findall(r"\b[\wÀ-ÿ-]+\b", _norm(sentence))
    return sum(1 for word in words if word.endswith(suffixes))


def _split_sentences(text: str) -> list[tuple[str, int]]:
    matches = list(re.finditer(r"[^.!?\n]+(?:[.!?]|\n|$)", text))
    return [(match.group(0).strip(), match.start()) for match in matches if match.group(0).strip()]


def _statistical_term_is_explained(text: str, term: str, accepted_explanations: list[str]) -> bool:
    normalized = _norm(text)
    term_norm = _norm(term)
    term_offset = normalized.find(term_norm)
    if term_offset < 0:
        return True
    window = normalized[max(0, term_offset - 180): term_offset + 220]
    return any(_norm(explanation) in window for explanation in accepted_explanations)


def read_text_for_audit(path: str | Path) -> str:
    path = Path(path)
    if path.suffix.lower() == ".docx":
        try:
            from docx import Document
        except Exception as exc:  # pragma: no cover - dependency is available in project env
            raise RuntimeError("python-docx is required to audit .docx files") from exc
        document = Document(path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs]
        for table in document.tables:
            for row in table.rows:
                paragraphs.extend(cell.text for cell in row.cells)
        return "\n".join(item for item in paragraphs if item)
    return path.read_text(encoding="utf-8")


def naturalize_text(text: str) -> str:
    result = text
    for item in TRANSLATION_CLICHES:
        result = _replace_phrase(result, item["pattern"], item["replacement"])
    for item in UNNECESSARY_ENGLISH_TERMS:
        result = _replace_word(result, item["term"], item["replacement"])

    replacements = sorted(PTBR_STYLE_SUBSTITUTIONS, key=lambda item: len(item["term"]), reverse=True)
    for item in replacements:
        term = item["term"]
        if _norm(term) == "nma":
            continue
        result = _replace_phrase(result, term, item["replacement"])

    result = re.sub(
        r"\bO achado mais forte não é uma prova causal de uma droga específica\b",
        "O achado não autoriza afirmar que uma droga específica previne o desfecho",
        result,
        flags=re.IGNORECASE,
    )
    result = re.sub(r"\bNMA farmacol[oó]gica\b", "meta-análise em rede farmacológica", result, flags=re.IGNORECASE)
    result = re.sub(r"\bNMA\b", "meta-análise em rede", result)

    normalized = _norm(result)
    first_hr = re.search(r"\b(?:ahr|hr)\b", normalized)
    if first_hr and not _has_hr_definition(result, first_hr.start()):
        result = re.sub(
            r"\bHR\b",
            "razão de riscos instantâneos (hazard ratio, HR)",
            result,
            count=1,
        )
    if text and text[0].isupper() and result and result[0].islower():
        result = result[0].upper() + result[1:]
    return result


def build_generation_brief(*, deliverable: str, audience: str = "pesquisador") -> str:
    source_lines = "\n".join(
        f"- {item['source']}: {item['lesson']} ({item['url']})" for item in PTBR_STYLE_SOURCE_NOTES
    )
    intro_patterns = "\n".join(f"- {item}" for item in SECTION_PATTERNS["introducao"])
    methods_patterns = "\n".join(f"- {item}" for item in SECTION_PATTERNS["metodos"])
    results_patterns = "\n".join(f"- {item}" for item in SECTION_PATTERNS["resultados"])
    conclusion_patterns = "\n".join(f"- {item}" for item in SECTION_PATTERNS["conclusao"])

    return f"""
# Perfil De Geração Científica PT-BR

Entrega: {deliverable}
Leitor principal: {audience}

## Ordem Obrigatória

Escreva primeiro em português brasileiro. Não traduza template inglês. Use linguagem científica natural, como artigo biomédico brasileiro: frase direta, sujeito claro, números explícitos e conclusão proporcional à evidência.

Quando o texto for resumo estruturado, use Objetivo, Métodos, Resultados e Conclusão. Introdução pode entrar antes do Objetivo quando o congresso exigir.

## Medidas E Siglas

- Defina HR na primeira menção como razão de riscos instantâneos (hazard ratio, HR).
- Use meta-análise em rede por extenso antes de usar NMA.
- Explique P-score como medida de ranqueamento.
- Explique tau2 e I2 como heterogeneidade quando aparecerem fora de tabela.

## Frases Modelo

Introdução:
{intro_patterns}

Métodos:
{methods_patterns}

Resultados:
{results_patterns}

Conclusão:
{conclusion_patterns}

## Proibições De Estilo

- Não use camada contextual, sinal convergente, sinal farmacológico, hub-dependência ou eixo obesidade-metabolismo sem explicar.
- Não use linguagem promocional: robusto, definitivo, perfeito, publicável, prova causal.
- Não diga que cirurgia bariátrica é superior aos fármacos na mesma rede; diga que foi analisada separadamente.

## Barreira De Naturalidade

- Não entregue texto com mojibake ou caracteres quebrados.
- Evite anglicismos dispensáveis: framework, endpoint, outcome, baseline, arm-level, layer, signal, hub.
- Troque clichês de tradução por frases diretas: "no contexto de" -> "na análise de"; "em termos de" -> "quanto a"; "à luz de" -> "considerando".
- Evite frases com muitas palavras abstratas terminadas em -ção, -mento, -dade ou -ência. Use sujeito e verbo.
- Se uma frase tiver mais de uma ideia metodológica, divida em duas.

## Base De Calibragem

{source_lines}
""".strip() + "\n"


def audit_text(text: str, *, path: str | Path | None = None) -> dict[str, Any]:
    path_str = str(path) if path is not None else None
    issues: list[dict[str, Any]] = []

    for pattern in MOJIBAKE_PATTERNS:
        offset = text.find(pattern)
        if offset >= 0:
            line = _line_number(text, offset)
            issues.append(
                _issue(
                    code="mojibake",
                    severity="block",
                    term=pattern,
                    line=line,
                    message="Texto contém sinal de mojibake ou codificação quebrada.",
                    suggestion="Regrave o arquivo como UTF-8 e regenere o entregável.",
                    excerpt=_line_excerpt(text, line),
                    path=path_str,
                )
            )

    for item in PTBR_STYLE_SUBSTITUTIONS:
        term = item["term"]
        if _norm(term) == "nma":
            continue
        for start, _end in _iter_term_matches(text, term):
            line = _line_number(text, start)
            issues.append(
                _issue(
                    code="forbidden_term",
                    severity="block",
                    term=term,
                    line=line,
                    message=f"Termo com aparência de tradução literal: {term}.",
                    suggestion=item["replacement"],
                    excerpt=_line_excerpt(text, line),
                    path=path_str,
                )
            )

    normalized_text = _norm(text)
    first_hr = re.search(r"\b(?:ahr|hr)\b", normalized_text)
    if first_hr and not _has_hr_definition(text, first_hr.start()):
        line = _line_number(text, first_hr.start())
        issues.append(
            _issue(
                code="hr_without_first_definition",
                severity="block",
                term="HR",
                line=line,
                message="HR aparece sem definição em português na primeira menção.",
                suggestion="Use 'razão de riscos instantâneos (hazard ratio, HR)' na primeira menção.",
                excerpt=_line_excerpt(text, line),
                path=path_str,
            )
        )

    for match in re.finditer(r"(?<!\w)nma(?!\w)", normalized_text):
        start = match.start()
        prefix = normalized_text[max(0, start - 8): start]
        if prefix.endswith("prisma-"):
            continue
        line = _line_number(text, start)
        issues.append(
            _issue(
                code="unexpanded_nma",
                severity="warn",
                term="NMA",
                line=line,
                message="NMA aparece em texto corrido; prefira meta-análise em rede após definir a sigla.",
                suggestion="meta-análise em rede",
                excerpt=_line_excerpt(text, line),
                path=path_str,
            )
        )

    for item in UNNECESSARY_ENGLISH_TERMS:
        for start, _end in _iter_term_matches(text, item["term"]):
            line = _line_number(text, start)
            excerpt = _line_excerpt(text, line)
            if _looks_like_reference_line(excerpt):
                continue
            issues.append(
                _issue(
                    code="unnecessary_english",
                    severity="block",
                    term=item["term"],
                    line=line,
                    message=f"Anglicismo dispensável em texto científico em português: {item['term']}.",
                    suggestion=item["replacement"],
                    excerpt=excerpt,
                    path=path_str,
                )
            )

    for item in TRANSLATION_CLICHES:
        for start, _end in _iter_term_matches(text, item["pattern"]):
            line = _line_number(text, start)
            issues.append(
                _issue(
                    code="translation_cliche",
                    severity="warn",
                    term=item["pattern"],
                    line=line,
                    message=f"Clichê de tradução ou frase vaga: {item['pattern']}.",
                    suggestion=item["replacement"],
                    excerpt=_line_excerpt(text, line),
                    path=path_str,
                )
            )

    for item in STATISTICAL_TERMS:
        if not _statistical_term_is_explained(text, item["term"], item["accepted_explanations"]):
            start = _norm(text).find(_norm(item["term"]))
            line = _line_number(text, max(start, 0))
            issues.append(
                _issue(
                    code="statistical_term_without_context",
                    severity="warn",
                    term=item["term"],
                    line=line,
                    message=item["message"],
                    suggestion="Inclua explicação breve na primeira aparição.",
                    excerpt=_line_excerpt(text, line),
                    path=path_str,
                )
            )

    for item in TRANSLATIONESE_PATTERNS:
        pattern = item["pattern"]
        for start, _end in _iter_term_matches(text, pattern):
            line = _line_number(text, start)
            issues.append(
                _issue(
                    code="translationese_pattern",
                    severity="warn",
                    term=pattern,
                    line=line,
                    message=f"Possível abstração excessiva: {pattern}.",
                    suggestion=item["suggestion"],
                    excerpt=_line_excerpt(text, line),
                    path=path_str,
                )
            )

    for term in AI_TONE_TERMS:
        for start, _end in _iter_term_matches(text, term):
            line = _line_number(text, start)
            issues.append(
                _issue(
                    code="promotional_or_overclaim_tone",
                    severity="warn",
                    term=term,
                    line=line,
                    message=f"Termo pode soar promocional ou forte demais: {term}.",
                    suggestion="Troque por linguagem associativa e específica.",
                    excerpt=_line_excerpt(text, line),
                    path=path_str,
                )
            )

    for sentence, offset in _split_sentences(text):
        word_count = _sentence_word_count(sentence)
        if word_count > LONG_SENTENCE_WORD_LIMIT:
            line = _line_number(text, offset)
            issues.append(
                _issue(
                    code="long_sentence",
                    severity="warn",
                    line=line,
                    message=f"Frase longa demais para texto científico em português ({word_count} palavras).",
                    suggestion=f"Divida a frase em duas ou mais frases abaixo de {LONG_SENTENCE_WORD_LIMIT} palavras.",
                    excerpt=sentence[:220],
                    path=path_str,
                )
            )
        nominalizations = _nominalization_count(sentence)
        if nominalizations >= NOMINALIZATION_LIMIT:
            line = _line_number(text, offset)
            issues.append(
                _issue(
                    code="nominalization_overload",
                    severity="warn",
                    line=line,
                    message=f"Excesso de substantivos abstratos na mesma frase ({nominalizations}).",
                    suggestion="Troque parte dos substantivos por verbos concretos e divida a frase.",
                    excerpt=sentence[:220],
                    path=path_str,
                )
            )

    status = "block" if any(issue["severity"] == "block" for issue in issues) else "pass"
    return {
        "path": path_str,
        "status": status,
        "issue_count": len(issues),
        "issues": issues,
    }


def audit_paths(paths: list[str | Path]) -> dict[str, Any]:
    reports = []
    for raw_path in paths:
        path = Path(raw_path)
        text = read_text_for_audit(path)
        reports.append(audit_text(text, path=path))

    status = "block" if any(report["status"] == "block" for report in reports) else "pass"
    return {
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files_checked": len(reports),
        "issue_count": sum(report["issue_count"] for report in reports),
        "reports": reports,
    }


def render_markdown_report(reports: list[dict[str, Any]], *, title: str = "Auditoria De Estilo PT-BR") -> str:
    status = "block" if any(report["status"] == "block" for report in reports) else "pass"
    issues = [issue for report in reports for issue in report["issues"]]
    counts = Counter(issue["code"] for issue in issues)

    lines = [
        f"# {title}",
        "",
        f"Status geral: {status}",
        f"Arquivos avaliados: {len(reports)}",
        f"Problemas encontrados: {len(issues)}",
        "",
        "## Resumo Por Tipo",
        "",
    ]
    if counts:
        for code, count in sorted(counts.items()):
            lines.append(f"- {code}: {count}")
    else:
        lines.append("- Nenhum problema encontrado.")

    lines.extend(["", "## Achados", ""])
    if not issues:
        lines.append("Nenhum achado bloqueante ou aviso foi identificado.")
    else:
        for report in reports:
            report_issues = report["issues"]
            if not report_issues:
                continue
            file_label = report.get("path") or "<texto>"
            lines.extend(["", f"### {file_label}", ""])
            for issue in report_issues:
                lines.append(
                    f"- L{issue['line']} [{issue['severity']}] {issue['code']}: {issue['message']}"
                )
                if issue.get("term"):
                    lines.append(f"  - termo: {issue['term']}")
                if issue.get("suggestion"):
                    lines.append(f"  - sugestão: {issue['suggestion']}")
                if issue.get("excerpt"):
                    lines.append(f"  - trecho: {issue['excerpt']}")

    lines.extend(
        [
            "",
            "## Regras Aplicadas",
            "",
            "- Explicar HR na primeira menção como razão de riscos instantâneos (hazard ratio, HR).",
            "- Evitar jargão traduzido sem explicação.",
            "- Preferir frases curtas, sujeito claro e linguagem associativa.",
            "- Em textos em português, escrever primeiro em português em vez de traduzir template inglês.",
        ]
    )
    return "\n".join(lines).strip() + "\n"


def write_audit_reports(paths: list[str | Path], output: Path | None, json_output: Path | None) -> dict[str, Any]:
    payload = audit_paths(paths)
    markdown = render_markdown_report(payload["reports"])

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8")
    if json_output is not None:
        json_output.parent.mkdir(parents=True, exist_ok=True)
        json_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload
