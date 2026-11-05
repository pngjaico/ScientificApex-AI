# Scientific workflow packet

Language: pt-BR
Task: Torneio de temas de doutorado: I-FABP, lactato e CTA, comparando pergunta clínica, viabilidade e independência do mestrado

## Execution assignments
- question: Sol -> `context/question_and_alternatives.md`; Protocol question, competing hypotheses, feasibility
- protocol: Sol -> `protocol.yaml`; Design, endpoints, estimand, registration, deviations
- retrieval: Luna -> `context/retrieval/`; Dated queries, source identifiers, deduplication, provider caveats
- screening: Luna -> `evidence/screening/`; Traceable decisions; ambiguous eligibility returns to Sol
- extraction: Luna -> `evidence/extraction_manifest.json`; Schema validation, locators, units, missing data
- methods: Sol -> `reviews/methods_review.json`; Bias, confounding, transitivity, sensitivity assumptions
- analysis: Luna -> `analysis/manifest.json`; Execute approved plan with locked runtime and hashes
- interpretation: Sol -> `evidence/claim_map.jsonl`; Support assessment, counterevidence, claim calibration
- writing: Sol -> `drafts/manuscript.md`; Native target-language prose and preserved claim/reference keys
- review: Sol -> `reviews/review_report.json`; Methodological, quantitative, editorial, independent red-team

Read the selected skills and project contracts. Check the next allowed mode before execution.
Each worker returns artifact paths, hashes, exact tests and unresolved issues.
Planning is not an approval of claims or analysis.
