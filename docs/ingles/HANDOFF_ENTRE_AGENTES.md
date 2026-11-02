# INTER-AGENT HANDOFF PROTOCOL
## Antigravity (Google) | Codex (OpenAI) | OpenCode (Open-Source)

> **Fundamental Operational Rule:**  
> Operation across the three environments is **strictly sequential** ("one agent at a time, never concurrent").  
> No agent may perform simultaneous modifications in the workspace. All transitions rely on explicit state files and Git history.

---

### 1. Environment Map and Configuration Points

Each of the three environments has its native discovery channel, but all share the canonical rules:

| Environment | Primary Engine | Entry Point / Launcher | Specific Config | Configuration / Rule Files Read |
| :--- | :--- | :--- | :--- | :--- |
| **Antigravity** | Google DeepMind (Gemini / Claude Opus) | Antigravity IDE UI | `.agents/skills/`, internal rules | `AGENTS.md`, `.agents/AGENTS.md`, `.AGENTES` |
| **Codex** | OpenAI (GPT-6.1 Sol / GPT-6 Luna) | `abrir_codex.cmd` (`codex --cd .`) | `.codex/config.toml`, `.codex/agents/*.toml` | `AGENTS.md`, `.codex/README.md`, `.AGENTES` |
| **OpenCode** | Open-Source CLI / Desktop | `abrir_opencode.cmd` / `OpenCode.exe` | `opencode.json` | `AGENTS.md`, `opencode.json`, `.AGENTES` |

---

### 2. Incoming Agent Checklist

When starting a session in any of the 3 environments, follow these steps before making changes:

1. **Inspect Recent Git History:**
   ```powershell
   git status
   git log -1 --stat
   ```
   *Verify that the workspace is clean and inspect the last commit made by the previous agent.*

2. **Read the Handoff State:**
   - Inspect `.machine/handoff_sessao.json`:
     - `active_project`: current active project (`projects/<project_id>/`).
     - `current_mode`: current phase (e.g., `analysis`, `drafting`, `review-trinity`).
     - `last_session`: summary of what the previous agent completed.
     - `next_recommended_actions`: immediate next steps.
   - Read the latest log entry in `docs/HANDOFF_ENTRE_AGENTES.md`.

3. **Run Governance Sanity Check:**
   ```powershell
   .\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict
   ```
   *Must return `status: pass` with 0 issues.*

4. **Query the Operational Graph (Graph-First):**
   ```powershell
   .\.venv\Scripts\python.exe -m graphify query "<operational question>" --budget 1200
   ```
   *Do not perform blind root directory recursive scans.*

5. **Bound Your Write Surface:**
   - Focus edits strictly within `projects/<project_id>/`.
   - Edit root infrastructure (`article_machine/`, `skills/`, `.codex/`, `docs/`) only when explicitly requested.

---

### 3. Outgoing Agent Checklist

Before concluding your session for another agent to take over:

1. **Validate Code and Tests:**
   - Python code / tests: `.\.venv\Scripts\python.exe -m pytest tests/`
   - Governance / skills: `.\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict`

2. **Ensure Scientific Integrity:**
   - Maintain Evidence Lock for all claims.
   - Maintain PT-BR / EN paired deliverables.

3. **Update Handoff State:**
   - Update `.machine/handoff_sessao.json`.
   - Append an entry to `docs/HANDOFF_ENTRE_AGENTES.md`.

4. **Commit Checkpoint:**
   ```powershell
   git add <modified files>
   git commit -m "handoff(<agent>): <clear summary of changes>"
   ```
   *Never commit `.env`, `.venv`, transient caches, or unprotected human data.*

---

### 4. Transition Log

See `docs/HANDOFF_ENTRE_AGENTES.md` for historical transition logs.
