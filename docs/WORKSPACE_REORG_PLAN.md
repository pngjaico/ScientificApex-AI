# Workspace Reorganization Plan

This is a non-destructive reorganization. The root contains real research data,
legacy folders, generated outputs, and project directories. Moving all of it in
one automated pass would create broken paths and false provenance.

## Current Problems

- Git is initialized and the current branch is two commits ahead of
  `origin/main`, but the worktree contains many pre-existing modified and
  untracked files. It has not been proven reproducible from a clean clone.
- Scientific projects and legacy source folders are mixed at the root.
- Generated graphify temporary files are present at root and under
  `graphify-out/`.
- The package runtime works through `.venv\Scripts\python.exe -m article_machine`;
  docs used to imply the console command was always available. Graphifyy 0.9.8
  is now a pinned development dependency for the same venv.
- Several required critical skills exist locally but are not tracked in Git;
  their contracts need explicit review before they can be called reproducible.

## Clean Target Layout

```text
Doutorado/
  article_machine/              # Python package
  tests/                        # package tests
  scripts/                      # workspace maintenance scripts
  docs/                         # agent and method documentation
  skills/                       # workspace scientific skills
  projects/<project_id>/        # active Article Machine projects
  sources/                      # shared source intake only
  graphify-out/                 # workspace operational graph
  legacy/                       # future destination for manually migrated folders
```

## Migration Rules

- Do not move anything with patient data, PDFs, raw sources, or manually curated
  analysis until a migration manifest exists.
- Every move needs: old path, new path, reason, affected project, and validation
  command.
- Do not merge duplicate project folders by name alone. Compare
  `project.yaml`, evidence manifests, and latest modified files first.
- Generated caches should be ignored or cleaned, not committed.

## Manual Review Queue

These root folders are likely legacy or raw-source areas and should be triaged
before moving:

- `Correção Orientador/`
- `Doutorado/`
- `Leitor de Artigos/`
- `PDFS DR ANDRÉ/`
- `REVISÃO LIGA/`
- `Revisões Sistemáticas/`
- `Submissão Final/`
- `NMA_OSA_VPI/` at root versus `projects/NMA_OSA_VPI/`

## Branch Cleanup Policy

The safe cleanup is:

1. Keep the current branch unless the user explicitly requests another branch.
2. Add or verify `.gitignore` before staging.
3. Run `machine audit --strict`, regenerate the workspace graph, and run tests.
4. Review `git status --short` and an explicit candidate-file manifest.
5. Stage only reviewed code, contracts, tests, and policy files; exclude raw
   data, full texts, local runs, secrets, caches, and environment state.
6. Commit only after confirming the staged diff is complete and contains no
   sensitive scientific inputs.

Do not run `git reset --hard`, `git clean`, or broad move commands in this
workspace without an explicit reviewed file list.
