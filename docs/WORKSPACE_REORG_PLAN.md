# Workspace Reorganization Plan

This is a non-destructive reorganization. The root contains real research data,
legacy folders, generated outputs, and project directories. Moving all of it in
one automated pass would create broken paths and false provenance.

## Current Problems

- Git is effectively uninitialized locally: current branch has no commits and
  almost everything is untracked.
- Scientific projects and legacy source folders are mixed at the root.
- Generated graphify temporary files are present at root and under
  `graphify-out/`.
- `projects/projects/` is nested and should be reviewed before migration.
- The package runtime works through `.venv\Scripts\python.exe -m article_machine`;
  docs used to imply the console command was always available.

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

Current branch: `codex/gastrosp-top1-final`.

The root repo has no local commit history. The safe cleanup is:

1. Keep the current branch.
2. Add `.gitignore` before staging.
3. Generate workspace graph and docs.
4. Review `git status --short`.
5. Create the first local commit only after confirming no sensitive raw data is
   being staged.

Do not run `git reset --hard`, `git clean`, or broad move commands in this
workspace without an explicit reviewed file list.
