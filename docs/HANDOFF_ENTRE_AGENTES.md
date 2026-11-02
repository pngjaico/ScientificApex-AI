# PROTOCOLO DE INTERCAMBIO ENTRE AGENTES
## Antigravity (Google) | Codex (OpenAI) | OpenCode (Open-Source)

> **Regra Fundamental de Operacao:**  
> A operacao entre os tres ambientes e **estritamente sequencial** ("um agente por vez, nunca concorrente").  
> Nenhum agente deve executar edicoes simultaneas no workspace. Toda transicao e baseada em arquivos de estado e historico do Git.

---

### 1. Mapa dos Ambientes e Arquivos de Configuracao

Cada um dos tres ambientes possui seu canal de entrada e descoberta nativo, mas todos compartilham as mesmas regras canonicas:

| Ambiente | Motor Principal | Ponto de Entrada / Launcher | Configuracao Especifica | Arquivos de Regras Lidos |
| :--- | :--- | :--- | :--- | :--- |
| **Antigravity** | Google DeepMind (Gemini / Claude Opus) | Interface Antigravity IDE | `.agents/skills/`, regras internas | `AGENTS.md`, `.agents/AGENTS.md`, `.AGENTES` |
| **Codex** | OpenAI (GPT-6.1 Sol / GPT-6 Luna) | `abrir_codex.cmd` (`codex --cd .`) | `.codex/config.toml`, `.codex/agents/*.toml` | `AGENTS.md`, `.codex/README.md`, `.AGENTES` |
| **OpenCode** | Open-Source CLI / Desktop | `abrir_opencode.cmd` / `OpenCode.exe` | `opencode.json` | `AGENTS.md`, `opencode.json`, `.AGENTES` |

---

### 2. Protocolo de Entrada (Incoming Agent Checklist)

Ao iniciar uma sessao em qualquer um dos 3 agentes, o agente deve seguir obrigatoriamente estes passos antes de qualquer modificacao:

1. **Inspecionar o Historico Git Recente:**
   ```powershell
   git status
   git log -1 --stat
   ```
   *Verificar se o workspace esta limpo e qual foi o ultimo commit realizado pelo agente anterior.*

2. **Ler o Estado de Handoff:**
   - Inspecionar `.machine/handoff_sessao.json` para capturar:
     - `active_project`: o projeto ativo atual (`projects/<project_id>/`).
     - `current_mode`: modo atual do fluxo (ex.: `analysis`, `drafting`, `review-trinity`).
     - `last_session`: resumo do que o agente anterior completou.
     - `next_recommended_actions`: proximos passos imediatos.
   - Ler a ultima secao do log em `docs/HANDOFF_ENTRE_AGENTES.md`.

3. **Executar Auditoria de Governanca (Sanity Check):**
   ```powershell
   .\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict
   ```
   *Deve retornar `status: pass` com 0 issues.*

4. **Consultar o Grafo Operacional (Graph-First):**
   Para navegacao, arquitetura ou busca de skills, usar:
   ```powershell
   .\.venv\Scripts\python.exe -m graphify query "<pergunta operacional>" --budget 1200
   ```
   *Nao realizar varreduras recursivas cegas no root.*

5. **Delimitar o Escopo de Escrita:**
   - Focar o trabalho exclusivamente dentro de `projects/<project_id>/`.
   - Modificacoes no nucleo (`article_machine/`, `skills/`, `.codex/`, `docs/`) apenas quando a tarefa for explicitamente de infraestrutura.

---

### 3. Protocolo de Saida e Transicao (Outgoing Agent Checklist)

Antes de encerrar a sessao para que outro agente possa assumir:

1. **Validar o Codigo / Testes:**
   - Se modificou codigo Python ou testes:
     ```powershell
     .\.venv\Scripts\python.exe -m pytest tests/
     ```
   - Se modificou skills ou governanca:
     ```powershell
     .\.venv\Scripts\python.exe -m article_machine machine audit --workspace-root . --strict
     ```

2. **Garantir Regras Cientificas:**
   - Manter `Evidence Lock` para qualquer claim.
   - Se gerou ou editou entregas/manuscritos, garantir o par bilingue `portugues/` e `ingles/`.

3. **Atualizar o Estado de Handoff:**
   - Atualizar os campos em `.machine/handoff_sessao.json` (agente, resumo, recomendacoes).
   - Adicionar uma nova entrada na secao de historico deste documento (`docs/HANDOFF_ENTRE_AGENTES.md`).

4. **Realizar Commit de Checkpoint:**
   ```powershell
   git add <arquivos modificados>
   git commit -m "handoff(<agente>): <resumo claro das entregas>"
   ```
   *Nunca incluir `.env`, `.venv`, caches temporarios ou dados brutos desprotegidos.*

---

### 4. Modelo de Registro de Sessao (Template de Handoff)

Copie e preencha este bloco ao final de cada intervencao:

```markdown
### [YYYY-MM-DD HH:MM] Handoff: <Agente de Saida> -> <Agente Alvo / Qualquer>
- **Agente Responsavel:** <Antigravity | Codex | OpenCode>
- **Projeto Ativo:** projects/<project_id>/
- **Fase / Modo:** <bootstrap | corpus-build | analysis | drafting | review-trinity | governanca>
- **O que foi feito:**
  - Item 1...
  - Item 2...
- **Testes / Auditoria:**
  - `machine audit --strict`: <PASS / FAIL>
  - `pytest`: <X passed, Y skipped>
- **Commit Git:** <hash ou mensagem do commit>
- **Proximos Passos Recomendados:**
  - [ ] Acao 1...
  - [ ] Acao 2...
- **Alertas / Cuidados para o Proximo Agente:**
  - Nao alterar...
```

---

### 5. Historico de Transicoes

### [2026-11-02 17:25] Handoff: Antigravity -> Codex / OpenCode
- **Agente Responsavel:** Antigravity (Google DeepMind)
- **Projeto Ativo:** `projects/article-machine-governance-2026`
- **Fase / Modo:** Governanca e Intercambio Multiagente
- **O que foi feito:**
  - Criacao do protocolo canonico de intercambio entre agentes em `docs/HANDOFF_ENTRE_AGENTES.md`.
  - Criacao do estado de maquina `.machine/handoff_sessao.json`.
  - Criacao de `opencode.json` e launcher `abrir_opencode.cmd` para integracao total do OpenCode.
  - Sincronizacao de `AGENTS.md`, `.agents/AGENTS.md` e `.codex/README.md` com as regras de troca de contexto.
  - Execucao completa da suite de testes: 328 testes passaram (1 skipped).
  - Execucao da auditoria estrita da maquina: status PASS com 0 issues.
- **Testes / Auditoria:**
  - `article_machine machine audit --strict`: PASS
  - `pytest tests/`: 328 passed, 1 skipped
- **Commit Git:** Checkpoint de unificacao e integracao multiagente.
- **Proximos Passos Recomendados:**
  - [ ] Qualquer agente (Codex, OpenCode ou Antigravity) pode assumir o projeto ativo `projects/article-machine-governance-2026` ou trabalhar em subpastas de `projects/`.
  - [ ] Seguir o checklist de entrada ao iniciar a proxima sessao.
- **Alertas / Cuidados para o Proximo Agente:**
  - Manter operacao sequencial (nunca abrir dois agentes ao mesmo tempo).
  - Sempre consultar o grafo operacional com `graphify query` antes de navegar.
