# Scientific work in English and PT-BR

This workspace uses GPT-6.1 Sol medium for coordination and final integration,
Luna low for navigation, Luna medium for assigned execution, Luna high for
focused analysis, and Sol high for critical scientific review. Standard service
is the default. Record observed model/effort; a config edit does not change an
already running session.

## Start a project

```powershell
.\.venv\Scripts\python.exe -m article_machine init "Review topic" --type systematic-review
.\.venv\Scripts\python.exe -m article_machine workflow plan projects/review-topic --query "Review the intervention and compare competing explanations" --language en
.\.venv\Scripts\python.exe -m article_machine workflow plan projects/review-topic --query "Revisar a intervenção e comparar explicações concorrentes" --language pt-BR
```

The plan writes `context/scientific_workflow_plan.json` and a readable packet.
It records allowed modes, guideline routes, artifacts and ownership. It does
not freeze a protocol, perform a search or approve an analysis. Complete the
question, eligibility, endpoints, estimand, analysis and registration fields
before advancing. Protocol deviations need dates and rationale.

## Choose the scientific design

| Work | Main checks |
| --- | --- |
| Systematic review / pairwise meta-analysis | PRISMA, prospective registration, independent screening, bias, heterogeneity and sensitivity |
| Network meta-analysis | PRISMA-NMA, transitivity, consistency, connectedness, ranking uncertainty |
| Diagnostic accuracy | STARD / QUADAS-2, threshold effects, reference standard, paired comparisons |
| Cohort / observational | STROBE, confounding, missingness, estimand and causal limits |
| RCT | CONSORT / RoB 2, prespecified outcomes, allocation, attrition and multiplicity |
| Animal work | ARRIVE / SYRCLE, experimental unit, blinding, exclusions and pseudoreplication |
| Prediction model | TRIPOD / PROBAST, leakage, calibration, external validation and utility |
| Computational discovery | Explicit hypothesis-generating label, benchmark, negative controls and experimental validation plan |

These are workflow routes, not certification that the local machine has passed
every scientific design. Read current reporting guidelines for the real project.

## Delegate bounded tasks

Start with one worker. Each assignment names objective, inputs, allowed tools,
owned files, artifacts, verification and stop conditions. Luna may extract
metadata, validate extraction schemas, implement an approved analysis, run tests
and compare evidence against clear criteria. Sol retains design, ambiguous
eligibility, bias adjudication, statistical decisions and interpretation. Return
Luna failures or ambiguities to Sol. A separate Sol reviewer verifies claims.

Rank hypotheses by novelty evidence, feasibility, falsifiability, confounding
and expected information gain. Keep competing explanations and the negative
result plan. Use a dated source-backed novelty search before claiming novelty.

## Write and translate

Declare `en` or `pt-BR`. Build a terminology glossary with concept IDs,
definitions, abbreviations and sources. Write naturally in the selected
language and preserve endpoints, effect direction, values, units, uncertainty,
claim IDs, reference keys and disclosure. For PT-BR use the local editorial
profile; for English use scientific-writing and venue-templates.

```powershell
.\.venv\Scripts\python.exe -m article_machine workflow audit-language projects/review-topic --language pt-BR --draft drafts/pt.md --reference drafts/en.md
```

The audit checks lexical preservation. It cannot prove semantic equivalence,
methodological validity or citation support. Both language versions need
Evidence Lock and independent editorial review. Decimal-localization and
thousands separators require human attention when ambiguous.

## Providers and plugins

`plugins audit` inspects package availability and version ambiguity locally.
Literature/database plugins, PubMed, Europe PMC, Crossref/OpenAlex and Zotero
support retrieval and references. NGS uses project-specific compute preflight.
Available packages do not prove authentication or successful live calls.
When multiple versions exist use an explicit `.machine/plugin_bindings.json`.
Keep optional external services optional; do not upload human data implicitly.

Consensus and Scite were discovered as optional literature/citation pilots.
They require account connection and a project benchmark before adoption.
Academic writing/review connectors and document tools can help editorial work;
their outputs remain review artifacts until evidence and claims are verified.

## Completion and evidence

Execution uses ComputeContractV2, locked environments and recorded runs. Sources
need identifiers, hashes, observation dates and locators. V1 reports remain
historical. Stage transitions, draft, review and export fail when their required
checks are blocked. Benchmark scores declared by an output producer cannot
establish acceptance: deterministic file-backed tests have a narrow scope,
while scientific judgments require independent evaluation.

Review Trinity requires actual independent reviewer artifacts, not merely an
enabled flag or the existence of an analysis manifest. Save methodological and
quantitative assessments in `reviews/methodological_review.json` and
`reviews/quantitative_review.json`, respectively, using
`MethodologicalReviewEvidenceV1` and `QuantitativeReviewEvidenceV1`.
Each assessment identifies the reviewer, records `reviewed_at`, includes a
substantive `assessment`, declares `independent=true`, and binds `input_snapshot`
to `article_machine.policy.gates.workspace_snapshot(project_dir)`.
The red-team report must bind its own snapshot too. Changed scientific inputs
invalidate the reviews; rerunning a wrapper does not renew the independent work.
These declarations support an audit trail, not cryptographic proof of reviewer
identity or proof that the scientific judgment is correct.
