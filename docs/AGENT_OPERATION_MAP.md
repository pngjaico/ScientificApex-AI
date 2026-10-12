# Agent Operation Map

This is the shortest safe path for an agent entering the Article Machine
workspace. It is operational, not motivational.

## Entry Flow

1. Read `docs/AGENT_START_HERE.md`.
2. Read `.agents/AGENTS.md` for the local graph-first policy.
3. Run `.\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict`.
4. Read `graphify-out/GRAPH_REPORT.md` before broad navigation.
5. Query the graph for navigation/routing questions even if the user did not ask for graph use.
6. Select or create one active `projects/<project_id>/`.
7. Read `project.yaml`, `protocol.yaml`, `standards.yaml`, and `compute.yaml`.
8. Run `.\.venv\Scripts\python.exe -m article_machine skills route --query "<task>"`.
9. Build context with `article_machine context build` before analysis, discovery, or drafting.
10. Validate Evidence Lock before calling claims or drafts ready.

## Routing Gates

- Workspace graph, broad navigation, architecture map, and agent handoff:
  `workspace-graph-navigator`.
- Active project selection, project resume, bootstrap, and contract-file entry:
  `project-entry-navigator`.
- Cleanup, reorganization, staging, migration, raw content, and legacy-folder risk:
  `content-preservation-guardian`.
- References, BibTeX, citation keys, local attachments, and Zotero full text:
  `zotero-reference-manager`.
- Biomedical discovery, public datasets, targets, variants, structures, compounds,
  trials, and literature provider routing: `life-science-router`.
- BCL, FASTQ, BAM/CRAM, VCF, count matrices, and sequencing assay routing:
  `ngs-analysis-router`.
- Strong decisions, fragile claims, "perfect", "best", premortem, steelman, and
  assumption audits: `deep-thinking-governor`.
- Skill installs, new APIs, external repositories, and capability upgrades:
  `skill-upgrade-governor`.
- Production-grade, world-class, best, or "ready" claims about the machine:
  `agent-benchmark-harness`.

## Artifact Destinations

- Raw or shared inputs: `sources/`, unless a project-specific source belongs
  under `projects/<project_id>/sources/`.
- Search plans and task packets: `projects/<project_id>/context/`.
- Evidence promoted to claims: `projects/<project_id>/evidence/`.
- NGS run envelopes and computational run records: `projects/<project_id>/analysis/`.
- Draft manuscripts and references: `projects/<project_id>/drafts/`.
- Reviews, audits, red-team notes, and benchmark results:
  `projects/<project_id>/reviews/`.

## Hard Stops

- Do not work on evidence, analysis, discovery, or manuscript text without an
  active project.
- Do not promote Life Science, Zotero, ToolUniverse, or NGS outputs directly to
  manuscript claims without Evidence Lock.
- Do not run full-root semantic graph extraction by default.
- Do not move legacy folders, patient/source dumps, PDFs, or raw full text
  without a migration manifest.
- Do not call the machine perfect, production-grade, or world-class without
  an acceptance-level report that passes
  `.\.venv\Scripts\python.exe -m article_machine benchmark validate <project_dir>`
  and includes residual-risk notes.
