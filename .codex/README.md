# Codex project control plane

This directory configures Codex for the mixed Article Machine workspace with a
role-aware GPT-6.1 Sol / GPT-6 Luna control plane.

- The main task defaults to `gpt-6.1-sol` at `medium`, Standard service, for integration,
  high-risk judgment, and parallel synthesis in this workspace.
- At most three subagents may run beside the primary agent.
- Exploration uses GPT-6 Luna low; bounded execution uses Luna medium;
  focused analysis uses Luna high; scientific review uses Sol high.
- `workspace_explorer`, `scientific_reviewer`, and `verification_runner` are
  read-only roles; implementation stays owned by the primary agent unless a
  task explicitly assigns a non-overlapping write surface.
- The official OpenAI developer-docs MCP is declared for current model/API
  guidance. A Codex restart or new task may be required before it appears.

Two user-level CLI profiles provide a controlled A/B surface without changing
the personal default model:

```powershell
codex --profile xhigh-baseline
codex --profile ultra-benchmark
```

Both July profiles are read-only historical/comparative launch surfaces. They
identify the requested model and reasoning effort, but a benchmark report must
still record the effective runtime rather than infer it from the profile name.
Versioned templates live under
`.codex/profiles/`; the active copies live in the user-level Codex directory.

Repository behavior and scientific gates remain authoritative in `AGENTS.md`.
Large context and Ultra delegation do not replace Graphify, project scoping,
Evidence Lock, benchmarks, or Review Trinity. Begin with one worker and add
agents only for independent, verifiable work with explicit file ownership.
Escalate ambiguous or failed Luna work to Sol. Do not select Astra, Fast, max
or ultra automatically. The user may override a session's settings. Editing
these defaults does not change a running session; record its actual runtime.

## Sequential Multi-Agent Operation (Antigravity / Codex / OpenCode)
This workspace is operated sequentially by three agent environments:
1. **Google Antigravity** (interactive pair-programming assistant)
2. **OpenAI Codex** (Sol/Luna multi-agent CLI/IDE)
3. **OpenCode** (open-source desktop & CLI assistant via `opencode.json` / `abrir_opencode.cmd`)

**Handoff Protocol:**
- Operation is strictly sequential: never run multiple agents concurrently.
- On entry: inspect `git status`, `git log -1`, `.machine/handoff_sessao.json`, and the latest entry in `docs/HANDOFF_ENTRE_AGENTES.md`.
- Run `.\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict` before starting.
- On exit: validate tests, update `.machine/handoff_sessao.json`, append a log entry to `docs/HANDOFF_ENTRE_AGENTES.md`, and make a clean git commit.

