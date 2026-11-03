# Guia Obrigatório de Execução do Modo Ativo / Active Mode Execution Guide

- **Projeto / Project:** `mandaqui-ifabp-programa-2026` (`observational-study`)
- **Modo Ativo / Active Mode:** `bootstrap`

## 1. Skills Obrigatórias neste Modo (Leia antes de executar)
- **`workspace-graph-navigator`** → `.agents/skills/workspace-graph-navigator/SKILL.md`
- **`project-entry-navigator`** → `.agents/skills/project-entry-navigator/SKILL.md`
- **`scientific-workflow-orchestrator`** → `.agents/skills/scientific-workflow-orchestrator/SKILL.md`
- **`hypothesis-tournament`** → `skills/hypothesis-tournament/SKILL.md`
- **`scientific-novelty-checker`** → `skills/scientific-novelty-checker/SKILL.md`
- **`guideline-router`** → `skills/guideline-router/SKILL.md`
- **`deep-thinking-governor`** → `skills/deep-thinking-governor/SKILL.md`
- **`tooluniverse-epidemiological-analysis`** → `skills/tooluniverse-epidemiological-analysis/SKILL.md`
- **`datasus-research-engine`** → `skills/datasus-research-engine/SKILL.md`

## 2. Comandos Canônicos da Máquina para este Modo
- `python -m article_machine methodology validate-protocol projects/mandaqui-ifabp-programa-2026`
- `python -m article_machine workflow plan projects/mandaqui-ifabp-programa-2026 --query "..." --language pt-BR`
- `python -m article_machine study build projects/mandaqui-ifabp-programa-2026`

## 3. Caminhos de Escrita Permitidos neste Modo
- `projects/mandaqui-ifabp-programa-2026/project.yaml`
- `projects/mandaqui-ifabp-programa-2026/protocol.yaml`
- `projects/mandaqui-ifabp-programa-2026/standards.yaml`
- `projects/mandaqui-ifabp-programa-2026/compute.yaml`
- `projects/mandaqui-ifabp-programa-2026/context/`

## 4. Regras Invioláveis Anti-Poluição (Qualquer Agente)
- NEVER create loose files in the workspace root or directly in projects/<project_id>/ root.
- Every output file MUST reside inside one of the canonical subdirectories (sources/, context/, screening/, extraction/, evidence/, analysis/, figures/, drafts/, deliverables/, publicacoes/, reviews/, exports/).
- Every scientific/editorial deliverable MUST have paired PT-BR (portugues/) and EN (ingles/) files.
- Never stage .env, API tokens, .RData/.Rhistory, or raw patient data dumps.
