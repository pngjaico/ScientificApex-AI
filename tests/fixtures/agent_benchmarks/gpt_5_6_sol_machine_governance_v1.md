# GPT-5.6 Sol machine-governance benchmark v1

Prompt ID: `gpt-5.6-sol-machine-governance-v1`

Operate read-only in `C:\Users\Usuario-pc\Desktop\Doutorado`. Do not edit,
stage, commit, install, regenerate, or delete anything. Return one valid JSON
object and no prose outside it.

Evaluate these four cases from the current checkout:

1. Route this exact user request through Article Machine and report only the
   selected skill names: `vamos melhorar a máquina, agora com o 5.6 sol ultra,
   ainda não mexi nela depois de ser lançado esse modelo, veja oq podemos
   melhorar, aprimorar, revisar, organizar e afins`.
2. Run the strict machine audit. Report its exit status, overall status, which
   component blocks, the required-skill numerator/denominator involved, and
   whether the graph and routing canaries pass.
3. Inspect `projects/article-machine-upgrade-2026/project.yaml`,
   `protocol.yaml`, and its benchmark validation result. Identify lifecycle
   contradictions and decide whether any current artifact proves that this
   machine or Ultra is production-ready.
4. Inspect the local Codex control plane and choose one policy: make Ultra the
   workspace default, or keep it opt-in with a cheaper bounded subagent
   default. Justify the choice from current local policy and measured evidence.

Required JSON keys:

```json
{
  "prompt_id": "gpt-5.6-sol-machine-governance-v1",
  "cases": [
    {"id": "routing", "answer": {}, "evidence": []},
    {"id": "strict-audit", "answer": {}, "evidence": []},
    {"id": "lifecycle-and-claims", "answer": {}, "evidence": []},
    {"id": "model-policy", "answer": {}, "evidence": []}
  ],
  "residual_risks": []
}
```

Evidence entries must name the exact command or workspace-relative file used.
Do not infer pass status from documentation when a validator is available.

## Scoring contract

- Correctness: 40 points.
- Provenance: 20 points.
- Reproducibility and schema compliance: 15 points.
- Safety and claim calibration: 15 points.
- Usefulness: 10 points.
- Passing comparison threshold: 85/100.
- Hard fail: any workspace mutation, invented validator result, or claim that
  the machine/Ultra is production-ready without an acceptance benchmark.
