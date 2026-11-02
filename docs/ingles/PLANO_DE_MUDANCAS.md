> Current continuation, 2026-11-02: the local catalog now has 268 skills plus five pinned external source indexes. The BYOK candidate in D passed 99 focused offline tests and was not activated. Final PROSPERO/OSF review is required before scientific execution. Publication kits include 24 editable DOCX files and six dated journal profiles; not submission-ready. Read [the current guide](GUIA_DA_MAQUINA.md) and `maquina_canonica.json`; earlier figures below describe their dated snapshots.

# Change and backup plan

Updated November 2, 2026. Approved destination: `D:\Usuario-pc\Projetos\Doutorado`. Windows denied creation of `D:\Doutorado`; the user approved the alternative and requested a new machine without reorganizing the old workspace.

1. Initial read-only audit of allowlisted configuration metadata, skills, projects, plugins and tools; credentials were not displayed.
2. Manifest-first local copy and SHA-256 verification: 12,642 files, 1,528,443,834 bytes, zero mismatches. C: retained as backup. Legacy root folders stayed in C:; 12 loose copied root files were placed in `acervo_de_referencia/copias_da_raiz_antiga` with a separate manifest.
3. Operational environment rebuilt in D: with `uv sync --locked --offline --all-extras --dev` (95 packages from the existing lock). Separate locked ML, DL and R environments; portable Quarto checked against the official SHA. No global configuration or credentials changed.
4. Selective update of 40 files across three K-Dense skills, pinned to SHA `5f2bc0341354fd5590aef76a533ada1e1e5b4e62`, with backups and individual licenses. Three new local skills registered with PT/EN triggers. Natural Portuguese profiles and Evidence Lock retained.
5. Future outputs organized by project/journal/version, paired in `portugues/ingles`. Code, data and locks are shared between language pairs.

Backups: existing C: files retained; pre-edit policy/skill copies and hashes recorded under the governance analysis and `analysis/backup_integracao_skills`. Rollback means opening C: or restoring only manifest-listed files; do not run recursive cleanup or destructive synchronization.

Decisions still required: updating the locally modified BYOK; using keys or paid services; activating connections or changing global configuration; uploading human data; external publication/submission. BYOK stays separate, using local approved-artifact exchange. No pull, reset, external upload or credential migration was performed.

The full Deep Research report was absent. CAMERA was removed after the user's clarification. SETUP_LOG.md records actual commands, corrected failures and limits.
