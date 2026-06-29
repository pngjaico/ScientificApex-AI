# SKILLS CANON: SCIENTIFIC OS

## Objetivo
- Usar skills como aceleradores especializados, mas subordinar todas elas ao runtime `article_machine/`, aos modos e aos gates do projeto ativo.

## Hierarquia
1. `project.yaml` e `protocol.yaml`
2. `standards.yaml`
3. `article_machine/` runtime
4. Skills especializadas do workspace
5. Prompts livres do agente

## Camadas

### Layer 0: Project Scope
- Todo trabalho nasce ou continua em `projects/<project_id>/`.
- O agente deve descobrir o projeto ativo antes de pesquisar, escrever ou executar.

### Layer 1: Context Management
- Grandes corpora nunca devem ser despejados brutos no modelo.
- O fluxo padrão é:
  1. registrar fonte em `sources/registry.jsonl`
  2. converter ou resumir em `sources/converted/`
  3. consolidar contexto em `context/project_brief.md`
  4. gerar `context/task_packets/*.json`

### Layer 2: Standards Routing
- O tipo do projeto define guidelines e checklists:
  - `systematic-review` -> `PRISMA`, `GRADE`, `ROBIS`, `AMSTAR 2`
  - `network-meta-analysis` -> `PRISMA-NMA`, `GRADE`
  - `diagnostic-study` -> `STARD`, `QUADAS-2`
  - `clinical-trial` -> `CONSORT`
  - `observational-study` -> `STROBE`
  - `animal-study` -> `ARRIVE`
  - `prediction-model` -> `TRIPOD`
  - `health-economics` -> `CHEERS`

### Layer 3: Evidence Lock
- Todo draft factual deve ser compatível com `evidence/claim_map.jsonl`.
- Toda citação deve resolver contra `drafts/references.bib`.
- O agente deve rodar o gate antes de afirmar que o manuscrito está pronto.

### Layer 4: Computational Discovery
- Projetos `drug-discovery` e `intestinal-digital-twin` pertencem à `computational-discovery`.
- Skills prioritárias:
  - `rdkit`
  - `datamol`
  - `deepchem`
  - `diffdock`
  - `medchem`
  - `molecular-dynamics`
  - `statistical-analysis`
  - `scientific-visualization`
- Todo resultado sai com rótulo `hypothesis-generating`.

### Layer 5: Review Trinity
- Sem `Review Trinity` em `PASS`, não existe `submission`.

### Layer 6: World-Class Agent Skills
- O agente deve consultar `article-machine skills route --query "<pedido>"` quando houver dúvida sobre quais skills usar.
- Skills de ideação e planejamento:
  - `hypothesis-tournament`
  - `scientific-novelty-checker`
  - `experimental-design-planner`
- Skills de reprodutibilidade:
  - `ro-crate-provenance-export`
  - `nextflow-pipeline-runner`
  - `snakemake-pipeline-runner`
  - `cwl-workflow-bridge`
- Skills de revisão e evidência:
  - `asreview-screening-bridge`
  - `risk-of-bias-assistant`
  - `grade-sof-table-builder`
- Skills de descoberta biomédica:
  - `openalex-literature-graph`
  - `open-targets-drug-targeting`
  - `chembl-bindingdb-miner`
  - `alphafold-pdb-structure-router`
  - `in-silico-validation-governor`
- Skills de auditoria:
  - `agent-benchmark-harness`
  - `scientific-red-team-reviewer`

## Regra de Ouro
- Skills ajudam a executar.
- O runtime decide o estado metodológico.
- Se uma skill cobre a tarefa, ela deve ser usada antes de solução manual livre.
