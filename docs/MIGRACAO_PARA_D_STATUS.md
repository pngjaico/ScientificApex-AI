# Migração para D: — estado em 2026-11-02

Este documento registra o que já está em D:, o que foi verificado e o que
ainda impede declarar a migração concluída. O histórico do plano está em
[`MIGRACAO_PARA_D.md`](MIGRACAO_PARA_D.md).

## Situação

| Item | Estado |
|---|---|
| Raiz canônica | `D:\Usuario-pc\Projetos\Doutorado` |
| C: | **Intacto** (nenhum arquivo excluído) |
| Conteúdo só existente em C: | Copiado para `archive/legado_C_2026-11/` |
| Cópia verificada | **4.303 arquivos, 0 falhas de SHA-256** |
| Tamanho do archive | 2,52 GiB |
| Projetos em D: | 18, todos com `project.yaml` |
| Ambiente Python | `.venv` com `uv.lock`; extra `analysis` adicionado |
| Ambiente R científico | Lock completo (69 principais + fecho transitivo; ver `AGENTS.md`), `renv::status()` sincronizado |
| Git | Nada commitado nesta rodada |

## O que foi feito

1. Inventário de C: e D: por caminho, tamanho e SHA-256.
2. Separação do que era idêntico, só de C:, conflitante ou reproduzível.
3. Cópia do que só existia em C: para `archive/legado_C_2026-11/`.
4. Verificação independente de cobertura: todo registro tem cópia no archive
   ou original em D:.
5. Isolamento de `segredos/.env` e dos 70 conflitos.
6. Fechamento do ambiente R científico:
   `metafor 5.2.1`, `meta 8.5.0`, `netmeta 3.7.0`, `clubSandwich 0.7.0`,
   `robvis 0.3.1`, `PRISMA2020 1.1.5`, `pROC 1.19.1`, `rms 8.2.0`, além de
   ML clínico (`tidymodels`, `xgboost`, `lightgbm`, `ranger`, `DALEX`,
   `shapviz`), NMA diagnóstica/dose-resposta (`mada`, `dosresmeta`) e figuras
   científicas (`ggplot2`, `patchwork`, `ggpubr`, `survminer`).
7. Atualização do `renv.lock` para o ambiente consolidado (69 pacotes
   principais e mais de 300 no fecho transitivo; ver `AGENTS.md`) e replicação
   em `modelos/meta_analise_em_r/ambiente/renv.lock`.
8. Criação do painel `docs/ESTADO_DOS_PROJETOS.md` e do índice
   `docs/INDICE_DO_WORKSPACE.md`.
9. Política de organização sem exclusão em
   `docs/ORGANIZACAO_E_LIMPEZA.md`.

## O que foi adicionado ao ambiente

### Python

- Extra `analysis`: `pandera`, `mapie`, `lifelines`, `pdfplumber`.
- Desenvolvimento: `pre-commit`, `detect-secrets`.
- `uv.lock` atualizado.

### R

- Script único de atualização e travamento:
  `scripts/atualizar_ambiente_meta_analise.R` (instala, sincroniza, roda o
  validador e confere `renv::status()`).
- Declaração e validação dos pacotes:
  `modelos/meta_analise_em_r/analysis/00_pacotes_do_ambiente.R`.
- `renv/settings.json` com `snapshot.type = "all"` para registrar as
  dependências recursivas.
- `renv.lock` completo (69 pacotes principais e mais de 300 no fecho
  transitivo; ver `AGENTS.md`), com cópia em
  `modelos/meta_analise_em_r/ambiente/renv.lock`.

## O que falta

| Pendência | Bloqueio | Próximo passo |
|---|---|---|
| Excluir C: | Sem backup independente e teste de restauração | Testar clone limpo e restaurar o archive |
| Teste de clone limpo | Precisa de rede e tempo | `git clone` em pasta temporária + `uv sync --locked --all-extras --dev` + `pytest` |
| CI de segurança | Workflow único atual | Adicionar CodeQL, gitleaks, dependency-review e actionlint |
| Metadados de 3 projetos | `project_type`/`current_mode` ausentes | Preencher os contratos |
| Backup 3-2-1 | Sem destino externo confirmado | Definir HD/nuvem e testar restauração |
| Revisão semântica | Depende de humano | Ler as entregas PT-BR/EN |

## Checklist antes de excluir C:

- [ ] Archive com hash verificado e cópia independente em outro disco.
- [ ] Clone limpo de D: instala e passa nos testes.
- [ ] `renv::restore()` funciona a partir do lock.
- [ ] Nenhum caminho crítico aponta para C:.
- [ ] Confirmação explícita do usuário.
- [ ] Registro da exclusão em `docs/`.

Enquanto o checklist não estiver completo, C: permanece como está.

## Links

- [`archive/legado_C_2026-11/LEIA-ME.md`](../archive/legado_C_2026-11/LEIA-ME.md)
- [`docs/INDICE_DO_WORKSPACE.md`](INDICE_DO_WORKSPACE.md)
- [`docs/ORGANIZACAO_E_LIMPEZA.md`](ORGANIZACAO_E_LIMPEZA.md)
- [`docs/ESTADO_DOS_PROJETOS.md`](ESTADO_DOS_PROJETOS.md)
