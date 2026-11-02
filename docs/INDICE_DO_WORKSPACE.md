# Índice do workspace

Raiz canônica: `D:\Usuario-pc\Projetos\Doutorado`.
C: permanece intacto como backup histórico. Nada é excluído deste workspace sem
manifesto, verificação de hash e autorização explícita.

Verificado em 2026-11-02. Este índice descreve onde cada coisa mora; ele não
substitui `AGENTS.md`, `.AGENTES` nem os contratos de cada projeto.

## Ordem de leitura

1. [`LEIA-ME_PRIMEIRO.md`](../LEIA-ME_PRIMEIRO.md) — porta de entrada.
2. [`AGENTS.md`](../AGENTS.md) — regras operacionais do agente.
3. [`.AGENTES`](../.AGENTES) — política canônica, catálogos e limites.
4. [`docs/ARQUITETURA_FINAL.md`](ARQUITETURA_FINAL.md) — camadas da máquina.
5. [`docs/ESTADO_DOS_PROJETOS.md`](ESTADO_DOS_PROJETOS.md) — painel gerado dos 18 projetos.
6. [`docs/AMBIENTES_E_LOCKS.md`](AMBIENTES_E_LOCKS.md) — ambientes, locks e restauração.
7. [`docs/FLUXOS_CIENTIFICOS.md`](FLUXOS_CIENTIFICOS.md) — os quatro fluxos.
8. [`docs/AGENT_OPERATION_MAP.md`](AGENT_OPERATION_MAP.md) — handoff operacional.

## Mapa da raiz

| Caminho | Papel | Regra |
|---|---|---|
| `article_machine/` | Runtime Python: contratos, CLI, gates, Evidence Lock, Review Trinity. | Fonte de verdade do comportamento. Alterar só com teste. |
| `projects/` | Trabalho científico, um diretório por projeto. | Nunca trabalhar fora de um projeto ativo. |
| `modelos/` | Modelos reutilizáveis: ML clínico, estatística, manuscrito, NMA, publicação, protocolo. | Código e locks compartilhados; sem dados humanos. |
| `skills/` | Biblioteca de skills + `registry.json` com proveniência. | Skill nova precisa de entrada no registro e hash da árvore. |
| `scripts/` | Automação operacional e utilitários. | Scripts novos devem ser idempotentes e documentados. |
| `tests/` | Suíte pytest. | Não editar teste para acomodar bug; corrigir o código. |
| `docs/` | Documentação humana e de agente, em PT-BR e inglês. | Entregas novas em `docs/portugues/` e `docs/ingles/`. |
| `.agents/` | Espelho local de políticas e skills para agentes. | Manter coerente com `AGENTS.md`; não é fonte científica. |
| `.codex/` | Configuração local de modelos, papéis e subagentes. | Não alterar sem pedido explícito. |
| `.github/workflows/` | CI: `quality-gate.yml`. | Workflows novos exigem permissões mínimas e ações pinadas. |
| `.machine/` | Estado do runtime, bindings de plugins, docs geradas. | Gerado; não editar à mão. |
| `archive/` | Legado migrado de C: com manifesto e SHA-256. | Fora do Git. Não excluir. |
| `acervo_de_referencia/` | Cópias antigas da raiz e PDFs de referência. | Somente leitura; não é evidência atual. |
| `ferramentas/` | Ferramentas portáteis (Quarto 1.10.20). | Binários; não versionar. |
| `graphify-out/` | Grafo operacional gerado. | Regenerar com `scripts/generate_workspace_graph.py`. |
| `integracoes/` | Catálogos científicos e integrações externas. | Ler manifestos; não promover achado sem Evidence Lock. |
| `sources/` | Notas e fontes soltas da raiz antiga. | Novas fontes vão em `projects/<id>/sources/`. |
| `tools/` | Playwright e automação de navegador. | Reproduzível via `npm ci`; não é conteúdo científico. |
| `.venv/` | Ambiente Python local. | Reproduzível por `uv sync --locked --all-extras --dev`. |
| `archive/legado_C_2026-11/` | Cópia do que só existia em C:. | Ver `LEIA-ME.md` dentro do archive. |

## Anatomia de um projeto

```
projects/<project_id>/
  project.yaml          # identidade, tipo, modo atual, release
  protocol.yaml         # pergunta, PICO, critérios, registro
  standards.yaml        # diretrizes de relato aplicáveis
  compute.yaml          # R/Python/browser, locks e permissões
  sources/registry.jsonl
  context/              # Task Packet, briefs, planos
  evidence/             # claim_map.jsonl, extrações, screening
  analysis/             # código e resultados reproduzíveis
  drafts/               # manuscript.md + references.bib
  reviews/              # Review Trinity
  figures/
  deliverables/<slug>/  # congressos: HTML canônico, QA antes de exportar
  publicacoes/<revista>/<identificador>/
  .machine/runs/<run_id>/manifest.json
```

Entregas novas de publicação usam nove áreas numeradas e subpastas
`portugues/` e `ingles/`, com nomes de arquivo em português. Congressos
continuam em `deliverables/`.

## Onde colocar cada artefato

| Artefato | Destino | Proibido |
|---|---|---|
| Fonte nova de literatura | `projects/<id>/sources/registry.jsonl` + `evidence/` | Soltar PDF bruto na raiz. |
| Claim científico | `projects/<id>/evidence/claim_map.jsonl` | Claim sem fonte verificável. |
| Código de análise | `projects/<id>/analysis/` | Rodar fora do projeto ativo. |
| Manuscrito | `projects/<id>/drafts/manuscript.md` | Texto final sem Evidence Lock. |
| Artigo para revista | `projects/<id>/publicacoes/<revista>/<id>/` | Criar entrega editorial fora do pipeline. |
| Congresso | `projects/<id>/deliverables/<slug>/` | Slide/pôster fora de `deliverables/`. |
| Modelo reutilizável | `modelos/<area>/` | Dados humanos no modelo. |
| Legado de C: | `archive/legado_C_2026-11/` | Mover ou apagar sem manifesto. |
| Credencial | `.env` local ou cofre | Commitar, imprimir ou copiar para skill. |

## Comandos canônicos

```powershell
# Runtime
.\.venv\Scripts\python.exe -m article_machine --help
.\.venv\Scripts\python.exe -m article_machine preflight projects\<id>
.\.venv\Scripts\python.exe -m article_machine context build projects\<id> --mode analysis --hypothesis "..."
.\.venv\Scripts\python.exe -m article_machine draft projects\<id>
.\.venv\Scripts\python.exe -m article_machine review projects\<id>

# Grafo operacional
.\.venv\Scripts\python.exe scripts\generate_workspace_graph.py

# Painel de projetos
.\.venv\Scripts\python.exe scripts\estado_dos_projetos.py

# Testes
.\.venv\Scripts\python.exe -m pytest

# Ambiente R de meta-análise (rodar da raiz para atualizar e travar)
Rscript scripts\atualizar_ambiente_meta_analise.R

# Validar o ambiente já instalado
cd modelos\meta_analise_em_r
Rscript analysis\00_pacotes_do_ambiente.R
```

## Arquivos gerados (não editar à mão)

- `graphify-out/*` — grafo e relatório operacional.
- `.machine/generated-skill-docs/*` — documentação de skills.
- `docs/ESTADO_DOS_PROJETOS.md` — painel dos projetos.
- `uv.lock` e `*/renv.lock` — locks; atualizar pela ferramenta, nunca à mão.
- `*/renv/library/` e `.venv/` — ambientes reproduzíveis, fora do Git.

## Convivência com outro agente (Gemini/Codex)

1. Antes de editar arquivo compartilhado, rode `git status --short` e confira
   `LastWriteTime` dos arquivos vizinhos.
2. Prefira criar arquivo novo a reescrever arquivo em uso.
3. Não apague, mova ou renomeie nada sem manifesto e confirmação.
4. Não faça commit nem push sem pedido explícito.
5. Se um arquivo mudar durante a edição, releia antes de aplicar a mudança.
6. Registre alterações estruturais em `docs/` com data e escopo.

## Pendências conhecidas

- Três projetos sem `project_type` ou `state.current_mode` declarados:
  `OncoMetabolic_CRC_NMA`, `congress-winners-2026` e
  `GastroSP_Gold_NMA_Biomarkers`. O painel os marca com `?`.
- CI de segurança (CodeQL, gitleaks, dependency-review, actionlint) ainda não
  foi adicionado; o workflow existente é `quality-gate.yml`.
- C: segue preservado; a exclusão depende de teste de restauração e backup
  independente.
