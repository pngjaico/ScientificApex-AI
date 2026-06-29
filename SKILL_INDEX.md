# Global Skill Index - Article Machine

## Layer 1 and 2: Review and Evidence
- Use literature, citation, peer-review, and evidence skills for search, screening, extraction, synthesis, and claim validation.

## Layer 3: Modeling and Bench Work
- Use statistical, R/Python, computational discovery, RDKit, DiffDock, DeepChem, molecular dynamics, and scientific visualization skills for analysis.

## Layer 4: Synthesis and Dissemination
- `scientific-writing`: abstracts and manuscripts.
- `scientific-slides`: legacy slide narrative support.
- `latex-posters`: print-first poster fallback.
- `pptx-posters`: legacy PPTX poster fallback.
- `scientific-visualization`: camera-ready data figures.
- `scientific-schematics`: technical diagrams and study flowcharts.
- `conference-deliverable-router`: official entry point for deck, poster, abstract, handout, and submission pack.
- `conference-requirements-importer`: normalizes congress rules into `conference.yaml`.
- `conference-slides-html`: HTML-first deck generation with QA and PDF/PPTX export.
- `conference-posters-html`: HTML-first vertical/horizontal poster generation with QA and export.
- `visual-backend-router`: chooses diagram, chart, hero image, and asset backends.
- `playwright-layout-qa`: browser QA for screenshots, overflow, thumbnails, and PDF.
- `pptx-export-bridge`: editable PPTX fallback without making PPTX canonical.
- `submission-ops-playwright`: dry-run and confirmed portal submission operations.
- `speaker-notes-timing`: talk timing and speaker notes for 3/5/10/15 minute profiles.
- `paper-to-talk`: converts manuscripts or claim maps into oral narratives.
- `paper-to-poster`: converts manuscripts or claim maps into poster storyboards.
- `life-science-router`: routes biomedical discovery and evidence questions through the Life Science Research plugin inside Article Machine projects.

## Congress Mode
When the user asks to prepare for a congress:
1. Import rules with `conference-requirements-importer` and `article-machine congress import`.
2. Route the output with `conference-deliverable-router`.
3. Build decks with `conference-slides-html`, `paper-to-talk`, and `speaker-notes-timing`.
4. Build posters with `conference-posters-html` and `paper-to-poster`.
5. Route visuals with `visual-backend-router`.
6. Validate layouts with `playwright-layout-qa`.
7. Export editable fallback files with `pptx-export-bridge`.
8. Use `submission-ops-playwright` for dry-run and explicitly confirmed submissions.

## Life Science Mode
When the user asks a biomedical discovery, target, variant, omics, drug, protein, pathway, microbiome, clinical, or dataset question:
1. Run `article-machine life-science plan <project_dir> --question "<question>"`.
2. Read `context/life_science/retrieval_plan.yaml`.
3. Use the selected Life Science Research plugin skills.
4. Save outputs under `evidence/life_science/`.
5. Promote only verified findings to `evidence/claim_map.jsonl`.

## World-Class Scientific Agent Layer
Use these skills naturally whenever the user's intent matches. Do not attempt the workflow manually first.

### Ideation and Design
- `hypothesis-tournament`: generate, criticize, rank, and evolve scientific hypotheses.
- `scientific-novelty-checker`: verify novelty before claims such as novel, first, or unprecedented.
- `experimental-design-planner`: convert a hypothesis into controls, endpoints, bias controls, and validation design.

### Reproducibility and Workflow Standards
- `ro-crate-provenance-export`: package runs with FAIR-style provenance, hashes, environment, commands, inputs, and outputs.
- `nextflow-pipeline-runner`: use scalable, containerized, HPC/cloud-ready workflows.
- `snakemake-pipeline-runner`: use readable Python/R-friendly rule-based workflows.
- `cwl-workflow-bridge`: export command workflows to vendor-neutral Common Workflow Language.

### Evidence Synthesis Quality
- `asreview-screening-bridge`: active-learning screening with audit trail and human reviewer control.
- `risk-of-bias-assistant`: route and support RoB 2, ROBINS-I, QUADAS-2, PROBAST, ROBIS, AMSTAR 2, and related tools.
- `grade-sof-table-builder`: build GRADE certainty and Summary of Findings tables.

### Biomedical Discovery
- `openalex-literature-graph`: map scholarly metadata, topics, venues, authors, and citation neighborhoods.
- `open-targets-drug-targeting`: target-disease evidence, tractability, safety, known drugs, and prioritization.
- `chembl-bindingdb-miner`: ChEMBL/BindingDB/PubChem compound, activity, binding, and medchem triage.
- `alphafold-pdb-structure-router`: AlphaFold/PDB/UniProt structure selection, confidence, and docking readiness.
- `in-silico-validation-governor`: assign validation labels and prevent overclaiming for computational results.

### Evaluation and Red Team
- `agent-benchmark-harness`: benchmark the machine, skills, outputs, and regression cases before claiming quality.
- `scientific-red-team-reviewer`: stress-test claims, manuscripts, protocols, decks, posters, and discovery results.

### Upstream Scientific Agent Skills Sync
- `experimental-design` and `statistical-power`: upstream study design and sample-size planning; use with the local `experimental-design-planner` gate.
- `nextflow`, `bulk-rnaseq`, `pathway-enrichment`, and `pacsomatic`: reproducible omics and workflow execution routes.
- `liteparse`, `paper-lookup`, `research-lookup`, and `exa-search`: document parsing, metadata lookup, and current web retrieval routes; still promote only verified findings into Evidence Lock.
- `arbor` and `autoskill`: optimization and skill-generation helpers; require benchmark evidence before claiming improvement.
- `onekgpd`, `bids`, `hugging-science`, and `tamarind`: specialized biomedical data/model routes; database or platform output is not final proof by itself.

## Natural Skill Routing
- Use `article-machine skills route --query "<user request>"` when unsure which skills apply.
- Use `article-machine skills audit` after adding or editing skills.
- If a routed skill applies, read and use that skill before solving the task directly.
