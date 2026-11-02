# Organização e limpeza do workspace

Política vigente: **nada é excluído sem autorização explícita**. Esta rodada
apenas organiza, documenta e verifica. C: continua intacto; D: é a raiz
canônica.

## Princípios

1. Conteúdo científico bruto (PDFs, dados clínicos, dumps, manuscritos) nunca
   é apagado, movido ou renomeado sem manifesto e hash.
2. Caches e ambientes são reproduzíveis, mas continuam no disco até haver uma
   janela de limpeza aprovada.
3. Arquivos gerados são separados de fontes: `graphify-out/`, `.machine/`,
   `renv/library/`, `.venv/`, `node_modules/` não são conteúdo canônico.
4. Archive legado fica fora do Git e dentro de `archive/`.
5. Segredos ficam em local ignorado pelo Git, nunca em documento ou skill.
6. Mudanças estruturais são registradas em `docs/` com data e escopo.

## Inventário atual (2026-11-02)

| Área | Tamanho | Natureza | Ação atual |
|---|---:|---|---|
| `projects/` | 2.810 MB | Trabalho científico e artefatos | Preservar; organizar por projeto. |
| `archive/` | 2.585 MB | Legado de C: com manifesto | Preservar; fora do Git. |
| `integracoes/` | 838 MB | Catálogos e integrações externas | Preservar; ler manifesto. |
| `ferramentas/` | 639 MB | Quarto portátil | Preservar; binário. |
| `modelos/` | 612 MB | Modelos + biblioteca renv local | Lock versionado; biblioteca reproduzível. |
| `.venv/` | 506 MB | Ambiente Python local | Reproduzível por `uv sync`. |
| `skills/` | 99 MB | Skills + registro | Versionar; auditoria de proveniência. |
| `.git/` | 76 MB | Histórico | Não tocar. |
| `graphify-out/` | 56 MB | Grafo gerado | Regenerar quando necessário. |
| `tools/` | 17 MB | Playwright local | Reproduzível por `npm ci`. |
| `acervo_de_referencia/` | 9 MB | Cópias antigas | Somente leitura. |
| `.machine/` | 2,4 MB | Estado do runtime | Gerado. |

Itens reproduzíveis de maior peso, mantidos nesta rodada:

| Item | Tamanho | Como reconstruir |
|---|---:|---|
| `projects/.../byok/upstream_ro/web/node_modules` | 865,5 MB | `npm ci` no diretório do pacote |
| `projects/.../byok/upstream_ro/server/node_modules` | 273,9 MB | `npm ci` no diretório do pacote |
| `modelos/meta_analise_em_r/renv/library` | 358,7 MB | `renv::restore()` |
| `.venv` | 505,5 MB | `uv sync --locked --all-extras --dev` |
| Caches Python (`.mypy_cache`, `__pycache__`) | 4,3 MB | Reexecutar ferramentas |
| `tools/playwright/node_modules` | 16,8 MB | `npm ci --prefix tools/playwright` |

Nenhum desses itens foi removido. A presença deles não compromete a
organização porque está coberta pelo `.gitignore` e separada do conteúdo
científico.

## Classificação dos arquivos

| Classe | Exemplos | Versionar? | Apagar? |
|---|---|---|---|
| Fonte científica | PDFs, protocolos, extrações, manuscritos | Sim, conforme política do projeto | Nunca sem manifesto |
| Dado clínico bruto | PSG, HC DADOS, planilhas de pacientes | Não | Nunca neste workspace |
| Código e contratos | `article_machine/`, `project.yaml`, `compute.yaml` | Sim | Só com revisão |
| Lock | `uv.lock`, `renv.lock` | Sim | Nunca à mão |
| Ambiente | `.venv/`, `renv/library/`, `node_modules/` | Não | Só com autorização |
| Gerado | `graphify-out/`, `.machine/`, painel | Depende | Regerar, não editar |
| Legado | `archive/legado_C_2026-11/` | Não | Nunca sem backup verificado |
| Segredo | `.env`, tokens | Não | Nunca imprimir/commitar |

## Higiene contínua (sem exclusão)

- `.gitignore` cobre `archive/`, `.venv/`, `renv/library/`, caches, locks de
  backup e temporários.
- `docs/ESTADO_DOS_PROJETOS.md` é gerado por
  `scripts/estado_dos_projetos.py`; rode `--check` no pre-commit.
- `skills/registry.json` é a fonte de proveniência; skill nova precisa de
  entrada e hash.
- `graphify-out/GRAPH_REPORT.md` é o mapa operacional; regenerar após mudanças
  estruturais.
- Nomes de entrega: `tipo_assunto_YYYY-MM-DD_vNN.ext`, com `portugues/` e
  `ingles/`.
- O archive tem `MANIFESTO_DE_MIGRACAO.json`, `inventario_completo.csv` e
  `RELATORIO_DE_COPIA.json`; qualquer verificação futura usa esses arquivos.

## Limpeza futura (não executada)

Se e quando o usuário autorizar, a ordem segura é:

1. **Congelar** um manifesto com caminhos, tamanhos e hashes dos itens a
   remover.
2. **Verificar** que o item é reproduzível: `uv.lock`, `package-lock.json` ou
   `renv.lock` presente e restaurável.
3. **Reinstalar** em um diretório de teste e rodar a suíte.
4. **Remover** apenas caches e ambientes, nunca `archive/` ou dados brutos.
5. **Registrar** o resultado em `docs/` e atualizar o painel.

Candidatos, em ordem de menor risco:

| Ordem | Item | Ganho | Pré-requisito |
|---:|---|---:|---|
| 1 | `.mypy_cache`, `__pycache__`, `.pytest_cache`, `.ruff_cache` | ~4 MB | Nenhum |
| 2 | `graphify-out` transitório | ~50 MB | Regenerar o grafo |
| 3 | `tools/playwright/node_modules` | ~17 MB | `npm ci` |
| 4 | `byok/**/node_modules` | ~1,14 GB | `npm ci` nos dois pacotes |
| 5 | `.venv` | ~506 MB | `uv sync --locked` |
| 6 | `renv/library` | ~359 MB | `renv::restore()` |

**Não são candidatos:** `archive/`, `projects/**/evidence`, `projects/**/sources`,
PDFs, dados clínicos, manuscritos, `acervo_de_referencia/`, `ferramentas/quarto`.

## Verificação

```powershell
# Estado do Git e arquivos recentes
git status --short

# Painel de projetos atualizado
.\.venv\Scripts\python.exe scripts\estado_dos_projetos.py --check

# Suíte
.\.venv\Scripts\python.exe -m pytest

# Integridade do archive
Get-Content archive\legado_C_2026-11\RELATORIO_DE_COPIA.json

# Ambiente R
cd modelos\meta_analise_em_r
Rscript analysis\00_pacotes_do_ambiente.R
```

## O que não fazer

- Não apagar `archive/` para "liberar espaço": ele é a única cópia de 4.303
  arquivos que só existiam em C:.
- Não mover projetos ou renomear pastas com links em documentos e manifests.
- Não reescrever `graphify-out/`, locks ou `.machine/` à mão.
- Não commitar `.env`, tokens, dados de pacientes ou PDFs com direitos
  restritos.
- Não rodar limpeza enquanto outro agente estiver escrevendo no mesmo diretório.
