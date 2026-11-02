# Leia-me do grafo operacional

Esta pasta é **gerada**. Ela não é fonte científica e não substitui
`AGENTS.md`, `.AGENTES`, os contratos de projeto nem o Evidence Lock.

## Comece por aqui

| Ordem | Arquivo | Para quê |
|---:|---|---|
| 1 | [`GRAPH_REPORT.md`](GRAPH_REPORT.md) | Relatório textual: comunidades, nós centrais, fluxo do agente, atalhos por intenção e receitas de consulta. |
| 2 | [`graph.html`](graph.html) | Grafo interativo. Layout fixo, física desligada por padrão, busca e filtro por comunidade. |
| 3 | [`workspace_graph_manifest.json`](workspace_graph_manifest.json) | Contagens, estado do Git na geração, camadas indexadas e limitações. |
| 4 | [`graph.json`](graph.json) | Grafo legível por máquina (Graphify/NetworkX). |
| 5 | [`arvore_da_maquina/portugues/LEIA-ME.md`](arvore_da_maquina/portugues/LEIA-ME.md) | Mapa estrutural da raiz inteira: 26 mil caminhos, sem ler conteúdo; ramos protegidos são opacos. |

`cache/` e `converted/` são transitórios. Não editar à mão.

## Consultas que funcionam

```powershell
# Onde está o painel de projetos
.\.venv\Scripts\python.exe -m graphify query "onde esta o painel de projetos" --budget 1200

# Como restaurar o ambiente R
.\.venv\Scripts\python.exe -m graphify query "como restaurar o ambiente R e o lock renv" --budget 1200

# Organizar sem excluir conteúdo bruto
.\.venv\Scripts\python.exe -m graphify query "como organizar o workspace sem excluir conteudo bruto" --budget 1200

# Qual projeto está em análise
.\.venv\Scripts\python.exe -m graphify query "qual projeto esta no modo analysis" --budget 1200
```

As consultas em português funcionam porque o relatório indexa frases-gatilho
(`Natural Language Gateway Phrases`) que apontam para os nós certos.

## Como regenerar

```powershell
# 1. Grafo operacional (documentos, projetos, skills, runtime, ambientes)
.\.venv\Scripts\python.exe scripts\generate_workspace_graph.py

# 2. Mapa estrutural da raiz (somente metadados; não lê conteúdo)
.\.venv\Scripts\python.exe scripts\mapear_arvore_da_maquina.py
```

O gerador operacional valida o contrato de comunidades: todo nó novo precisa
pertencer a exatamente uma comunidade. Se um nó ficar sem classificação, a
geração falha de propósito em vez de produzir um grafo incompleto.

## Regras de leitura

1. O grafo é **operacional**, não é prova científica. Arestas `INFERRED` são
   inferências de navegação ou risco.
2. Se o grafo contradisser os arquivos atuais, os arquivos vencem; regenere.
3. Não rode extração semântica da raiz inteira por padrão: há caches, PDFs,
   dados brutos e legado. Use o grafo operacional ou grafos por projeto.
4. `graph.html` é para navegação humana; `graph.json` é para automação.
5. O grafo não contém credenciais, conteúdo de pacientes nem texto integral de
   PDFs.
