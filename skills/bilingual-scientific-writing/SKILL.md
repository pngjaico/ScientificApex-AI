---
name: bilingual-scientific-writing
description: Use when drafting, reviewing or translating scientific manuscripts in English or português brasileiro, writing abstracts, bilingual terminology glossaries, or checking semantic fidelity between languages.
---

# Bilingual scientific writing

Declare the target language (`en` or `pt-BR`) and journal/style before writing.
Write natively in that language. In PT-BR use the local ptbr-article-writing skill;
in English use the curated scientific-writing and venue-templates instructions.
Never assume translating prose validates the science.

Build a glossary at context/terminology_glossary.json: concept ID, English term,
PT-BR term, abbreviation, definition and source. Keep study IDs, claim IDs, DOI,
reference keys, endpoints, comparator direction and numeric values unchanged.
Preserve decimal meaning: 0.05 in English may render 0,05 in PT-BR; never alter
effect size, CI bounds, p values, n, units or inequality direction.

Audit claim strength across versions: association is not causation, exploratory
is not confirmatory, non-significance is not equivalence, and model performance
is not clinical benefit. Retain limitations, uncertainty and AI disclosure.

Use `article-machine workflow audit-language <project> --language en|pt-BR`
for deterministic marker/citation/numeric preservation against an explicit
`--reference` draft. The audit is a lexical regression aid; an independent
scientific reader must still verify semantic fidelity and natural style.

Drafts and bilingual audits stay under drafts/ and reviews/. Each final language
version requires Evidence Lock and editorial/methodological review before use.
