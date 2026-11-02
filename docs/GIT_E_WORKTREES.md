# Git, worktrees e estado limpo

Regra: **um worktree canônico, nenhuma limpeza destrutiva sem confirmação**.
Este documento registra o estado e evita que um agente confunda trabalho em
andamento com lixo.

## Worktree canônico

- Caminho: `D:\Usuario-pc\Projetos\Doutorado`
- Branch: `codex/article-machine-complete-56-ultra`
- É o único worktree de trabalho. Não criar worktrees paralelos sem
  necessidade explícita.
- O status pode estar sujo durante trabalho concorrente (Gemini/Codex). Sujeira
  não autoriza `git reset --hard`, `git clean` nem commit de terceiros.

## Worktree secundário registrado

| Caminho | Estado | Ação |
|---|---|---|
| `C:\Users\Usuario-pc\AppData\Local\Temp\article-machine-verify-323a784` | Destacado (`detached HEAD`), 747 entradas de status, arquivos removidos | Não usar; remover só com confirmação |

Ele é um worktree temporário de verificação. Não contém a raiz canônica e não
deve ser consultado por agentes. Sua remoção libera espaço em C:, mas exige
confirmação porque `git worktree remove` apaga o diretório.

## Checklist antes de dizer que o worktree está limpo

```powershell
git worktree list
git status --short
git diff --check
git diff --stat
```

- `git status --short` vazio = limpo.
- `git diff --check` sem saída = sem espaços em branco problemáticos.
- `git diff --stat` deve ser compreensível e revisado.
- Não usar `git add -A` às cegas: o workspace tem archive, dados e caches
  ignorados por regras específicas.
- Não commitar `.env`, tokens, dados de pacientes, PDFs restritos, `archive/`,
  `.venv/`, `renv/library/` ou `node_modules/`.

## Script de diagnóstico

`scripts/limpar_worktrees.ps1` lista worktrees, estado e commits exclusivos.
Por padrão é **dry-run**. Só remove com `-Executar`, e só força com `-Forcar`.

```powershell
# Diagnóstico, sem alterar nada
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\limpar_worktrees.ps1

# Remoção deliberada de um worktree temporário (pede confirmação)
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\limpar_worktrees.ps1 -Executar
```

## Regras de convivência

1. Não criar worktree novo para tarefa que cabe no worktree canônico.
2. Se precisar de isolamento, registre o caminho e o propósito em `docs/`.
3. Antes de remover, confirme que não há commit ou arquivo exclusivo.
4. Nunca rodar `git worktree prune` sem listar o que será removido.
5. O worktree canônico só é declarado limpo depois de commit revisado e
   `git status` vazio.
