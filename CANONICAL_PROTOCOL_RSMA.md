# CANONICAL PROTOCOL: RS-MA / NMA

## Objetivo
- Operar revisões sistemáticas, meta-análises e network meta-analyses com gates explícitos, outputs auditáveis e compatibilidade com R.

## Fluxo Canônico

### 1. Bootstrap
- Inicializar o projeto com `article-machine init`.
- Definir `project_type = systematic-review` ou `network-meta-analysis`.
- Gerar `project.yaml`, `protocol.yaml`, `standards.yaml` e `compute.yaml`.

### 2. Protocol Freeze
- Preencher `research_question`, `objectives`, critérios de inclusão e exclusão.
- Bloquear avanço se o protocolo estiver incompleto.

### 3. Corpus Build
- Registrar toda fonte em `sources/registry.jsonl`.
- Preservar fontes originais em `sources/raw/`.
- Salvar versões destiladas em `sources/converted/`.

### 4. Screening
- Produzir decisões de elegibilidade e notas de exclusão.
- Para revisões diagnósticas, usar `QUADAS-2`.
- Para revisões de intervenção, usar `RoB 2` e `ROBINS-I` conforme o desenho.

### 5. Extraction
- Alimentar `evidence/claim_map.jsonl`.
- Toda linha deve conter:
  - `claim_id`
  - `statement`
  - `source_path`
  - `source_excerpt`
  - `reference_key`
  - `status`

### 6. Analysis
- Para NMA e síntese quantitativa com R:
  - rodar `article-machine preflight`
  - executar scripts com `article-machine run-r`
  - registrar `stdout.log`, `stderr.log`, `sessionInfo.txt`

### 7. Drafting
- Construir `drafts/manuscript.md` usando `{{claim:claim-id}}`.
- Popular `drafts/references.bib`.
- Rodar `Evidence Lock`.

### 8. Review Trinity
- `methodological`
- `quantitative`
- `editorial`

### 9. Submission
- Só avançar quando `reviews/review_report.json` estiver em `PASS`.

## Standards
- `systematic-review` -> `PRISMA`, `GRADE`, `ROBIS`, `AMSTAR 2`
- `network-meta-analysis` -> `PRISMA-NMA`, `GRADE`
- `diagnostic-study` -> `STARD`, `QUADAS-2`

## Princípios
- Sem claim suportado, não há texto final.
- Sem referência resolvida, não há submissão.
- Sem manifest, não há reprodutibilidade.
- Sem `sessionInfo()`, não há confiança em saída R.
