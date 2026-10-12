# Article Machine Agent Playbook

This file is the practical prompt layer for agents. It is intentionally blunt:
the machine is only useful when it blocks weak evidence, stale routing, and
unsupported claims.

## Agent Prompt Contract

Use this frame at the start of non-trivial scientific work:

```text
Active project: projects/<project_id>
Mode requested: <bootstrap|protocol-freeze|corpus-build|screening|extraction|analysis|discovery|drafting|review-trinity|submission>
Question or task: <one sentence>
Primary evidence source: <files, registry, DOI, database, or none yet>
Expected artifact: <task packet, manifest, analysis output, draft, review, deliverable>
Hard stop: no unsupported claim, no unlogged source, no mode jump.
```

Then run:

```powershell
.\.venv\Scripts\python.exe -m article_machine preflight projects\<project_id>
.\.venv\Scripts\python.exe -m article_machine skills route --query "<task>"
.\.venv\Scripts\python.exe -m article_machine context build projects\<project_id> --mode <mode> --hypothesis "<if applicable>"
```

## Better Defaults For Agents

- If the user asks for research ideas, route to `topic-ideation-tournament` or
  `hypothesis-tournament`; do not freestyle a ranked list without explicit
  novelty, feasibility, data availability, and red-team notes.
- If the user asks for novelty, route to `scientific-novelty-checker` before
  saying novel, first, unprecedented, or gap.
- If the user asks for a biomedical database result, run the Life Science plan
  and keep outputs under `evidence/life_science/`; do not promote them to final
  claims until Evidence Lock can cite source and reference.
- If the user asks for slides, poster, abstract, or submission, use the
  deliverables pipeline. Never build congress artifacts outside
  `projects/<project_id>/deliverables/<slug>/`.
- If the user asks whether the machine is good, better, production-ready, or
  world-class, use `agent-benchmark-harness` and show failures.

## Project Mode Gate

Do not advance modes by vibes. Use:

```powershell
.\.venv\Scripts\python.exe -m article_machine stage audit projects\<project_id> --target-mode <mode>
.\.venv\Scripts\python.exe -m article_machine guard check projects\<project_id>
```

If these block, report the exact blocker. Do not soften it.

## Drafting Prompt

Before drafting:

```powershell
.\.venv\Scripts\python.exe -m article_machine draft projects\<project_id>
```

Draft only claims that have `{{claim:claim-id}}` markers and matching entries in
`evidence/claim_map.jsonl`. If the evidence map is empty, write a methods or
limitations scaffold, not factual conclusions.

## Review Prompt

Before submission:

```powershell
.\.venv\Scripts\python.exe -m article_machine review projects\<project_id>
.\.venv\Scripts\python.exe -m article_machine journal report projects\<project_id>
```

Submission is blocked until Review Trinity, Evidence Lock, journal route, and
benchmark evidence pass. A pretty PDF is not a submission-ready artifact.

## Graph Prompt

Use the workspace graph first for navigation:

```powershell
python scripts\generate_workspace_graph.py
python -m graphify query "How should a new agent choose an active project?"
```

For the deterministic handoff path, read `docs/AGENT_OPERATION_MAP.md` and
follow its entry flow before touching evidence, analysis, discovery, or drafts.

For a deep graph of one scientific project, run graphify inside that project
folder or pass the project path. Do not run deep semantic extraction on the root
unless you intentionally want to process caches, legacy folders, and large PDFs.
