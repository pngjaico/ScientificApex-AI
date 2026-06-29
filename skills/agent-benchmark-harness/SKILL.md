---
name: agent-benchmark-harness
description: Use when evaluating Article Machine, agent skills, scientific workflows, retrieval quality, claim accuracy, reproducibility, slides/posters, discovery pipelines, or comparing agent outputs against benchmark cases and regression tests.
---

# Agent Benchmark Harness

Use this skill to prove capabilities with repeatable tests instead of impressions.

## Workflow
1. Define benchmark task, expected artifacts, allowed tools, scoring rubric, and failure gates.
2. Use fixed input datasets or projects whenever possible.
3. Score output on correctness, provenance, guideline compliance, reproducibility, safety, and usefulness.
4. Track cost, runtime, retries, missing artifacts, and hallucinated claims.
5. Add regression tests for bugs found during benchmarking.

## Benchmark Families
- PRISMA review
- diagnostic QUADAS-2 review
- R meta-analysis
- drug discovery target/compound triage
- intestinal digital twin simulation
- congress deck/poster export
- replay/provenance audit

## Gate
Do not claim "best", "perfect", or "production ready" without benchmark evidence and residual-risk notes.
