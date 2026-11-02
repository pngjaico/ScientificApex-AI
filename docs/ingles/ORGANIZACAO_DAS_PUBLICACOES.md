# Publication organization

Use projects/<id>/publicacoes/<journal>/<identifier>/ with nine numbered areas: protocol, retrieval/references, authorized data, analyses, tables, figures, manuscript, review and submission. Directory names remain Portuguese: 01_protocolo through 09_submissao. Every area contains portugues/ingles; both versions use the same Portuguese filename, tipo_assunto_YYYY-MM-DD_vNN.ext.

organizar_publicacoes.py accepts --raiz, --projeto, --revista and --identificador. Dry-run is default; --criar explicitly creates. Existing targets and traversal are rejected. verificar_pares detects missing file pairs; numerical, citation and semantic fidelity require additional review.

Code/data/locks are shared. Runtime contract paths remain standardized. Conference outputs stay in deliverables/. Root modelos/ contains paired PROTOCOLO.md and LEIA-ME.md plus real ML/DL/R locks. No old C: output was reorganized. Organization does not establish scientific or submission readiness.
