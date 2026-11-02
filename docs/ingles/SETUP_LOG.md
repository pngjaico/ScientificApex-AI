> Current continuation, 2026-11-02: the local catalog now has 268 skills plus five pinned external source indexes. The BYOK candidate in D passed 99 focused offline tests and was not activated. Final PROSPERO/OSF review is required before scientific execution. Publication kits include 24 editable DOCX files and six dated journal profiles; not submission-ready. Read [the current guide](GUIA_DA_MAQUINA.md) and `maquina_canonica.json`; earlier figures below describe their dated snapshots.

# Execution and installation log

Consolidated 2026-11-02. Scope: new D: scientific machine; no hardware audit, publication, key usage or human data. Global configuration and BYOK unchanged.

| Command/action | Scope | Result | Evidence/limit |
|---|---|---|---|
| ZIP README→AGENTS→plan→criteria→legacy | Package | PASS; Deep Research absent | Hardware advice not executed |
| Sanitized inventory, graphify query, codex --version | Read-only | PASS | Corrections retained; CLI 0.165.0-alpha.1.2 |
| Create D:\Doutorado | Initial destination | FAIL: Windows denied access | User approved D:\Usuario-pc\Projetos\Doutorado |
| migrar_para_d.py | Source-preserving copy | PASS: 12,642 files / 1,528,443,834 bytes | Equal SHA-256, manifest before copy |
| Copy corrections | D: only | PASS | Tracked template restored; NMA_OSA_VPI: 92 files / 1,779,862 bytes, hashes equal; 12 loose copies isolated with manifest |
| uv sync --locked --offline --all-extras --dev | Operational venv | PASS: 95 packages | Existing lock, environment rebuilt |
| uv lock / uv sync --locked --no-build | Separate ML/DL | PASS | scikit-learn 1.9.1, PyTorch 2.15.0+cpu; real locks |
| Local CRAN library; renv::snapshot | Isolated R 4.6.1 | PASS after two corrected failures | Dependencies completed; 16-package lock; metafor 5.2-1/renv 1.3.1 |
| Official portable Quarto ZIP/hash/extraction | ferramentas/quarto-1.10.20 | PASS | SHA 08a6d026877e5fb2c89e5f7e01c018847412993309cb49056e5427014ea5d868 |
| GitHub API/Crossref | Public metadata | Partial FAIL, recovered | GH timeout; six HEADs via git ls-remote. PRISMA 429 then web confirmation; two TRIPOD+AI/PROBAST+AI DOIs verified |
| K-Dense fetch/curation | 3 skills / 40 files | Static/provenance PASS; pilot | SHA 5f2bc0341354fd5590aef76a533ada1e1e5b4e62, licenses/backups |
| 3 local skills/PT-EN routes | D: registry | PASS | 267 entries; 16 focused tests, six routes; outside 65 critical until versioning |
| R demonstrations/bilingual plots | Synthetic | PASS | Meta/regression, figures/tables, independent Python estimate/CI agreement for tau2=0 |
| clinical_ml_baseline.py | Isolated ML | PASS | 180 synthetic rows, nested CV/calibration; grouped/time/external validation pending |
| executar_dl_sintetico.py | Isolated CPU DL | Persisted assertions/results PASS | 100 iterations, exact repeat; gradient/optimizer mechanics only |
| quarto render Portuguese/English | Two reports | PASS | Embedded images/references; 11 file pairs |
| workflow audit-language / style ptbr-audit | PT/EN reports | PASS | Numbers/citations preserved; human semantic review required |
| PNG inspection/UI attempt | QA | PNG inspected; HTML visual SKIPPED | Work local browsing disabled; HTML structural PASS |
| test_organizar_publicacoes.py | Temporary tests | PASS: 9 tests | Dry-run, traversal, collision, 18 subfolders, orphan detection |
| python -m pytest | Final D: full suite | PASS: 275 passed, 1 skipped | verificacao_final/testes_completos.log; Windows symlink skip |
| Strict machine/provenance/generated-doc checks | Integration | PASS | verificacao_final/resultado_verificacao.json |
| Zotero readiness/browser preflight | Services | SKIPPED/BLOCKED | API unavailable; Playwright not restored; no library access |
| Local BYOK packet with hashes/PT-EN tasks | Handoff | PREPARED; execution SKIPPED | governance/intercambio_kdense/demonstracao_2026-11-02 |

Initial D: suite had 256 pass, 1 skip, 1 fail from an omitted tracked template. Byte-for-byte restoration preceded the successful full rerun. Initial ML/Quarto skips predated the D: installations and executions. Earlier snapshots were retained.

No commit, remote upload, submission or clinical-result promotion. Some local environments/results remain Git-ignored. C: is backup. New outputs are bilingual with Portuguese filenames.

Evidence: projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/. Official sources: https://github.com/quarto-dev/quarto-cli/releases/tag/v1.10.20 ; https://scikit-learn.org/stable/install.html ; https://docs.pytorch.org/ ; https://wviechtb.github.io/metafor/ ; https://rstudio.github.io/renv/ .

Final supplement: 140 structural project directories restored from metadata. Graph export reconciled after verifying only intentionally absent legacy/cache roots; backup retained. New skills/documents indexed: 1,071 nodes/2,157 edges. Prediction defaults updated to TRIPOD+AI/PROBAST+AI; three templates generated with the actual initializer, validated contracts and locks. 14 focused template/graph tests passed after these changes.

Definitive rerun after defaults/templates: **275 passed, 1 skipped**, 81.23 s. Evidence: verificacao_final/testes_completos_apos_templates.log.
