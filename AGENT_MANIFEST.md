# AGENT MANIFEST: SCIENTIFIC OS RUNTIME

Este manifesto define como qualquer agente deve operar esta máquina científica.

## Missão
- Trabalhar como um `Scientific OS` agent-native para revisão, manuscrito, meta-análise, tese, projetos `in silico` e descoberta computacional.
- Priorizar rastreabilidade, baixo risco de alucinação, reprodutibilidade e conformidade metodológica.
- Nunca pular diretamente do pedido do usuário para texto final sem passar pelos modos, gates e artefatos estruturados do projeto ativo.

## Núcleo Operacional
- O runtime oficial vive em `article_machine/`.
- O trabalho sempre acontece dentro de `projects/<project_id>/`.
- O entrypoint padrão é a CLI `article-machine`.
- Cada execução relevante deve gravar manifestos em `.machine/runs/<run_id>/manifest.json`.

## Regras Absolutas
- Todo projeto deve possuir `project.yaml`, `protocol.yaml`, `standards.yaml` e `compute.yaml`.
- Todo manuscrito factual deve usar `{{claim:claim-id}}` e ser validado pelo `Evidence Lock`.
- O agente deve construir `Task Packets` curtos por modo antes de produzir análise ou texto longo.
- Nenhum projeto entra em `submission` sem `Review Trinity` em `PASS`.
- Resultados `in silico` são sempre rotulados como `hypothesis-generating` até validação externa.
- O agente deve usar skills aplicáveis antes de improvisar workflows já cobertos.
- Qualquer afirmação de "perfeito", "melhor" ou "production-grade" requer evidência de benchmark.

## Roteamento Natural de Skills
- Use `article-machine skills route --query "<pedido>"` quando a intenção exigir roteamento explícito.
- Use `article-machine skills audit` após criar ou alterar skills.
- Use `docs/AGENT_OPERATION_MAP.md` como handoff mínimo: entrada, auditoria,
  graph, projeto ativo, roteamento, Task Packet e Evidence Lock.
- Navegação de workspace usa `workspace-graph-navigator` antes de varredura ampla.
- Entrada/retomada de projeto usa `project-entry-navigator` antes de evidência, análise, descoberta ou draft.
- Reorganização, staging, graphing amplo e qualquer risco a fontes brutas usam `content-preservation-guardian`.
- Hipóteses, novidade e desenho experimental usam `hypothesis-tournament`, `scientific-novelty-checker` e `experimental-design-planner`.
- Reprodutibilidade e workflows usam `ro-crate-provenance-export`, `nextflow-pipeline-runner`, `snakemake-pipeline-runner` ou `cwl-workflow-bridge`.
- Revisões sistemáticas usam `asreview-screening-bridge`, `risk-of-bias-assistant` e `grade-sof-table-builder`.
- Protocolo, extração e revisão viva usam `protocol-registration-governor`, `extraction-schema-governor` e `living-review-monitor`.
- Fontes específicas usam `pubmed-database`, `clinical-trials-database`, `literature-search-europepmc`, `literature-search-openalex`, `literature-search-arxiv`, `literature-search-biorxiv`, `crossref-unpaywall-resolver`, `semantic-scholar-citation-graph` e `opencitations-citation-audit`.
- Zotero, BibTeX, `references.bib`, chaves de citação e full text local usam `zotero-reference-manager`.
- Descoberta biomédica usa `openalex-literature-graph`, `open-targets-drug-targeting`, `chembl-bindingdb-miner`, `alphafold-pdb-structure-router` e `life-science-router`.
- Sequenciamento/NGS usa `ngs-analysis-router` antes de qualquer instalação, referência grande, execução ou upload cloud.
- Workflows `tooluniverse-*` instalados ampliam literatura profunda, meta-análise, epidemiologia, diagnóstico, datasets, guidelines, trial design, farmacovigilância, validação de alvo, variantes, integração biológica e drug repurposing, sempre subordinados ao Evidence Lock.
- Resultados computacionais passam por `in-silico-validation-governor`.
- Decisões fortes, claims frágeis e pedidos de "perfeito" usam `deep-thinking-governor`.
- Avaliação da própria máquina usa `agent-benchmark-harness`.
- Texto científico com cara de IA usa `anti-ai-writing-governor`, sem bypass de detector e sem perda de evidência.
- Upgrade de skills usa `skill-upgrade-governor`.
- Antes de submissão ou claim forte, use `scientific-red-team-reviewer`.

- Resposta a pareceristas, rebuttal, integridade de referencias/citacoes e consistencia interna de manuscrito usam `manuscript-integrity-response-governor`.
- DOCX/PPTX/LaTeX editaveis, relatorios de leitura, slides de defesa/reuniao e pacotes academicos com QA de layout usam `academic-office-deliverables`.

## Modos Obrigatórios
1. `bootstrap`
2. `protocol-freeze`
3. `corpus-build`
4. `screening`
5. `extraction`
6. `analysis`
7. `discovery`
8. `drafting`
9. `review-trinity`
10. `submission`

## Gatilhos de Gate
- `protocol-freeze`: requer `research_question` e ao menos um objetivo em `protocol.yaml`.
- `screening` e `extraction`: requerem `sources/registry.jsonl` não vazio.
- `discovery`: permitido apenas para projetos com `lane = computational-discovery`.
- `review-trinity`: requer `drafts/manuscript.md`.
- `submission`: requer `reviews/review_report.json` com `aggregate_status = pass`.

## Política de Evidência
- Nenhuma afirmação científica deve existir sem `claim_id`, `source_excerpt`, `reference_key` e status `supported`.
- `drafts/references.bib` deve conter todas as chaves citadas no `claim_map.jsonl`.
- Falhas no `Evidence Lock` bloqueiam `drafting`, `review-trinity` e `submission`.

## Política de R e Computação
- `Rscript` é pré-condição verificável, nunca detalhe implícito.
- Quando R for necessário, usar `article-machine preflight` antes de qualquer execução.
- Toda execução R deve registrar `stdout.log`, `stderr.log`, `sessionInfo.txt` e manifestos de run.

## Revisão Final
- `Methodological Reviewer`: protocolo, standards, viés, reprodutibilidade.
- `Quantitative Reviewer`: estatística, R, benchmarking, incerteza.
- `Editorial Reviewer`: claim map, referências, coerência textual e submissão.

## Resultado Esperado
- Um agente novo deve conseguir abrir este workspace, inicializar ou retomar um projeto, passar pelos modos com gates reais e entregar saídas auditáveis sem depender de contexto implícito.

<!-- ARTICLE_MACHINE_REGISTRY_START -->
## Skill registry (generated)

- `academic-office-deliverables` (active)
- `agent-benchmark-harness` (active)
- `alphafold-pdb-structure-router` (active)
- `anti-ai-writing-governor` (active)
- `asreview-screening-bridge` (active)
- `author-identity-resolver` (active)
- `bilingual-scientific-writing` (active)
- `catalogos-cientificos-sob-demanda` (active)
- `chembl-bindingdb-miner` (active)
- `citation-management` (active)
- `clinical-reports` (active)
- `clinical-trials-database` (active)
- `content-preservation-guardian` (active)
- `crossref-unpaywall-resolver` (active)
- `cwl-workflow-bridge` (active)
- `database-lookup` (active)
- `database-retrieval-governor` (active)
- `deep-thinking-governor` (active)
- `evidence-lock-hardener` (active)
- `experimental-design-planner` (active)
- `extraction-schema-governor` (active)
- `fapesp-cnpq-projects` (active)
- `grade-sof-table-builder` (active)
- `guideline-router` (active)
- `hypothesis-tournament` (active)
- `in-silico-validation-governor` (active)
- `life-science-router` (active)
- `literature-review` (active)
- `literature-search-arxiv` (active)
- `literature-search-biorxiv` (active)
- `literature-search-europepmc` (active)
- `literature-search-openalex` (active)
- `living-review-monitor` (active)
- `manuscript-integrity-response-governor` (active)
- `meta-analise-medica` (active)
- `metodos-ml-clinico` (active)
- `nextflow-pipeline-runner` (active)
- `ngs-analysis-router` (active)
- `open-targets-drug-targeting` (active)
- `openalex-literature-graph` (active)
- `opencitations-citation-audit` (active)
- `peer-review` (active)
- `project-entry-navigator` (active)
- `protocol-registration-governor` (active)
- `ptbr-article-writing` (active)
- `publicacao-medica-organizada` (active)
- `pubmed-database` (active)
- `query-string-governor` (active)
- `research-lookup` (active)
- `retraction-integrity-checker` (active)
- `risk-of-bias-assistant` (active)
- `ro-crate-provenance-export` (active)
- `scientific-critical-thinking` (active)
- `scientific-novelty-checker` (active)
- `scientific-red-team-reviewer` (active)
- `scientific-workflow-orchestrator` (active)
- `scientific-writing` (active)
- `semantic-scholar-citation-graph` (active)
- `skill-upgrade-governor` (active)
- `snakemake-pipeline-runner` (active)
- `stage-audit-governor` (active)
- `statistical-analysis` (active)
- `topic-ideation-tournament` (active)
- `venue-templates` (active)
- `workspace-graph-navigator` (active)
- `zotero-reference-manager` (active)
<!-- ARTICLE_MACHINE_REGISTRY_END -->
