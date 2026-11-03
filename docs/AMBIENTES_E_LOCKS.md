# Ambientes, locks e restauração

Referência única para saber qual ambiente usar, qual lock manda e como
reconstruir sem quebrar a máquina. O `AGENTS.md` continua sendo a política
vigente; este documento é o mapa operacional.

## Resumo

| Ambiente | Versão | Gerenciador | Lock | Restauração |
|---|---|---|---|---|
| Python da raiz | 3.13 | uv 0.11.31 | `uv.lock` | `uv sync --locked --all-extras --dev` |
| ML clínico (Python) | 3.13 | uv | `modelos/aprendizado_de_maquina_clinico/uv.lock` | `cd modelos/aprendizado_de_maquina_clinico && uv sync --locked` |
| ML clínico — variante | 3.13 | uv | `.../ambientes/aprendizado_maquina/uv.lock` | `cd .../aprendizado_maquina && uv sync --locked` |
| Aprendizado profundo | 3.13 | uv | `.../ambientes/aprendizado_profundo/uv.lock` | `cd .../aprendizado_profundo && uv sync --locked` |
| R científico | 4.6.1 | renv 1.3.1 | `modelos/meta_analise_em_r/renv.lock` | `Rscript scripts/atualizar_ambiente_meta_analise.R` |
| R — estatística e figuras | 4.6.1 | renv | `modelos/estatistica_e_figuras/ambiente/renv.lock` | `renv::restore()` nesse projeto |
| Quarto | 1.10.20 | portátil | `ferramentas/quarto-1.10.20` | não reinstalar; usar o binário local |
| Playwright | 1.61.1 | npm 11.17.0 | `tools/playwright/package-lock.json` | `npm ci --prefix tools/playwright` |
| BYOK web/server | — | npm | `package-lock.json` em cada pacote | `npm ci` no diretório do pacote |

## R científico

- Executável canônico:
  `C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe`.
- Não usar o R 4.5.0 que aparece no PATH.
- O lock de referência tem 85 pacotes principais e 342 no fecho
  transitivo CRAN. O número exato é auditado; consulte `AGENTS.md` e o próprio
  `renv.lock`.
- O script `scripts/atualizar_ambiente_meta_analise.R` instala binários,
  sincroniza a biblioteca local do R, grava o snapshot com
  `snapshot.type = "all"` e falha se `renv::status()` não ficar sincronizado.
- Validação dos pacotes principais:

```powershell
& "C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe" --vanilla modelos/meta_analise_em_r/analysis/00_pacotes_do_ambiente.R
```

- Atualização completa (rodar da raiz, com o workspace livre):

```powershell
& "C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe" --vanilla scripts/atualizar_ambiente_meta_analise.R
```

- Pacotes deliberadamente fora do lock base: `dmetar`, `gemtc`, `BUGSnet`,
  `highcharter`, `chattr`, `ellmer`, `keras`, `tensorflow` e `torch` em R.
  O motivo de cada exclusão está no `AGENTS.md`.

## Python

- A raiz usa `uv`, não `pip`.
- Extras disponíveis:
  - `office`: `python-docx`.
  - `analysis`: `pandera`, `mapie`, `lifelines`, `pdfplumber`.
- Desenvolvimento: `pytest`, `ruff`, `mypy`, `pre-commit`, `detect-secrets`,
  `pip-audit`, `cyclonedx-bom`, `graphifyy`.
- O comando confiável é sempre
  `.\.venv\Scripts\python.exe -m article_machine ...`.
- O extra `analysis` não entra no `uv sync` padrão; use
  `uv sync --locked --all-extras --dev` para instalá-lo.

### ML Clínico e Deep Learning (`modelos/aprendizado_de_maquina_clinico`)
- **Python 3.13 isolado com `uv.lock` sincronizado.**
- **Stack Tabular e Conformal:** `scikit-learn` (1.9.1), `xgboost` (3.4.1), `lightgbm` (4.7.0), `mapie` (1.6.0), `lifelines` (0.30.3), `optuna` (4.9.0), `shap` (0.54.1), `pandera` (0.35.0), `pandas` (2.3.3), `statsmodels` (0.15.0), `matplotlib` (3.11.2), `seaborn` (0.13.2), `plotly` (6.9.0).
- **Subambiente de Deep Learning (`ambientes/aprendizado_profundo`):** `torch` (2.15.0+cpu), `torchvision`, `torchmetrics` com `uv.lock` dedicado.
- **Restauração:** `uv sync --directory modelos/aprendizado_de_maquina_clinico` e `uv sync --directory modelos/aprendizado_de_maquina_clinico/ambientes/aprendizado_profundo`.
- **Execução canônica:** `modelos/aprendizado_de_maquina_clinico/.venv/Scripts/python.exe <script.py>`.

## Quarto e relatórios

- Binário portátil: `ferramentas/quarto-1.10.20/bin/quarto.exe`.
- Verificação: `.\ferramentas\quarto-1.10.20\bin\quarto.exe --version`.
- Renderização científica usa R 4.6.1 e os locks acima; não usar o Quarto
  global como fonte de verdade.

## Navegador

- Playwright local em `tools/playwright` (versão 1.61.1).
- Reinstalação:
  `npm ci --prefix tools/playwright` e depois
  `npx --prefix tools/playwright playwright install`.
- QA visual de HTML e submissão continuam exigindo autorização e snapshot
  fresco; o navegador não é evidência científica.

## Lacunas conhecidas

| Lacuna | Efeito | Ação |
|---|---|---|
| `modelos/estatistica_e_figuras` sem `compute.yaml` | Contrato incompleto para preflight | Criar contrato quando o modelo for promovido |
| `modelos/manuscrito` sem lockfile R | Dependências declaradas, mas não travadas | Criar `renv.lock` próprio ou reutilizar o consolidado |
| BYOK sem build autenticado | Não há prova de execução ponta a ponta | Testar em janela isolada, sem credenciais no Git |
| R 4.5.0 no PATH | Risco de usar versão errada | Sempre chamar o caminho absoluto de 4.6.1 |

## Regras

1. Não rodar `renv::snapshot()` nem `uv lock` enquanto outro agente estiver
   atualizando o mesmo ambiente.
2. Não editar lock à mão.
3. Toda atualização de ambiente termina com validação e registro em `docs/`.
4. Dados humanos, tokens e credenciais nunca entram em lock, skill ou Git.
