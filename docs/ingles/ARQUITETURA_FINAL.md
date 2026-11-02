> Current continuation, 2026-11-02: the local catalog now has 268 skills plus five pinned external source indexes. The BYOK candidate in D passed 99 focused offline tests and was not activated. Final PROSPERO/OSF review is required before scientific execution. Publication kits include 24 editable DOCX files and six dated journal profiles; not submission-ready. Read [the current guide](GUIA_DA_MAQUINA.md) and `maquina_canonica.json`; earlier figures below describe their dated snapshots.

# Final scientific-machine architecture

Canonical local workspace: `D:\Usuario-pc\Projetos\Doutorado`. C: retained as backup/history; K-Dense BYOK stays separate. Status: locally validated only within the tested scope, with explicit remaining work. No clinical, production, guaranteed-publication or remote-CI readiness is claimed.

## Layers

1. Codex coordinates requirements, execution and review; configuration does not prove the active session model/effort. AGENTS.md defines project scope and gates.
2. Article Machine 0.3.0 handles contracts, Task Packets, routing, Evidence Lock, Review Trinity and mode-gated exports.
3. Operational Graphify navigates code/projects; it is not scientific evidence. Skills load by intent without a new giant global-context library.
4. Three registered local skills: meta-analise-medica, metodos-ml-clinico, publicacao-medica-organizada. Three upstream skills selectively updated at a verified pin, pilot status: scikit-learn, pytorch-lightning, scientific-visualization. Licenses, backups and hashes recorded.
5. Isolated execution: operational Python/uv.lock; ML with scikit-learn 1.9.1; DL with PyTorch 2.15.0+cpu; R 4.6.1 with metafor 5.2-1/renv 1.3.1; portable Quarto 1.10.20 under ferramentas/. Each stack has a separate lock. Do not rely on R 4.5.0 on PATH.
6. Retrieval/bibliography uses official APIs and exposed tools with source provenance. Zotero binding exists but local API is unavailable. BYOK receives only approved local artifacts with a manifest; no implicit credential/human-data transfer.

## Workflows and publication

[FLUXOS_CIENTIFICOS.md](FLUXOS_CIENTIFICOS.md) specifies A question→search/deduplication→Zotero→appraisal/extraction→manuscript; B protocol/dataset→SAP→R→tables/figures→Quarto; C review→PRISMA→RoB/GRADE→R meta-analysis; D clinical dataset→baseline→ML/DL→nested/external validation/calibration→TRIPOD+AI/PROBAST+AI→article.

Future outputs live under projects/<id>/publicacoes/<journal>/<identifier>/ with nine numbered areas and portugues/ingles pairs. Portuguese filenames, both language versions required. Code/data/locks shared; lexical preservation does not establish scientific equivalence. Reusable models are in modelos/aprendizado_de_maquina_clinico, meta_analise_em_r and manuscrito. Conference outputs remain in deliverables/ with QA and confirmed submission.

## Capability evidence

Full suite: 275 passed, 1 skipped. Strict machine, skill provenance and generated-document checks: PASS. Organizer: 9 tests PASS. Demonstrations include R meta-analysis/regression, independent Python numerical agreement, nested/calibrated ML and exactly repeated deterministic DL. Both Quarto HTML versions rendered; 11 file pairs checked, numbers/citations preserved and PT-BR style passed. All synthetic; this is not clinical validation or a completed systematic review.

## Remaining limits

Browser preflight blocked because Playwright cache/dependencies were not migrated. HTML UI visual QA was SKIPPED because Work local browsing is disabled; PNG plots were inspected and HTML structurally checked. Zotero API and BYOK update remain pending. External validation, real grouped data, RoB/GRADE judgments, editorial acceptance and submission depend on each study. New files remain uncommitted; no clean-clone/remote-CI proof. Global changes, paid services and publication require authorization.

Evidence: `projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/verificacao_final/`, locks, manifests and paired resultados_finais folders. Organized demonstration: governance project/publicacoes/demonstracao-interna/2026-11-02_v01.
