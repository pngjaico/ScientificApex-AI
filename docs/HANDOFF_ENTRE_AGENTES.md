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


### [2026-11-02 22:00] Handoff: Antigravity -> Codex / OpenCode
- **Agente Responsavel:** Antigravity (Google DeepMind)
- **Projeto Ativo:** `projects/NMA_OSA_VPI`
- **Fase / Modo:** Adequação Editorial e Preparação de Publicação Internacional
- **O que foi feito:**
  - Auditoria completa metodológica e científica do trabalho de AOS após cirurgia para IVF em fissurados com Prof. Dr. Nivaldo Alonso (`NMA_OSA_VPI`), equivalente à NMA dos Biomarcadores.
  - Demonstração da inadequação de NMA (ausência de RCTs head-to-head) e consolidação do desenho canônico como Metanálise de Proporções de Braço Único.
  - Correção forense de dados: exclusão de Abdel-Aziz 2019 (resgate), correção de Prada-Madrid 2011 (Furlow 1/10 e faringoplastia mista 5/10), segregação de Denadai 2018 (triagem clínica) e Rochlin 2021 (claims/CID).
  - Resultados da primária PSG estrita (5 braços, 129 pacientes, 53 eventos): Orticochea 81,1%, Flap Faríngeo 27,0%, Furlow 10,0%.
  - Audição editorial comparando 6 revistas (CPCJ, JCS, IJPO, PRS, JCMS, RBCP) com seleção do *The Cleft Palate-Craniofacial Journal* (CPCJ, SAGE, ACPA, $0 APC).
  - Estruturação canônica em `publicacoes/cleft-palate-craniofacial-journal/v01/` e espelho em `publicacoes/internacional_e_nacional/`.
  - Execução de modelagem estatística em R 4.6.1 gerando 4 figuras em 300 DPI PNG e vetorial SVG em PT e EN.
  - Geração de 4 tabelas científicas em CSV bilíngues.
  - Compilação dos pacotes DOCX formatados: `Blinded_Main_Manuscript_CPCJ.docx`, `Title_Page_CPCJ.docx`, `Cover_Letter_CPCJ.docx`, `PRISMA_2020_Checklist_CPCJ.docx` e `Manuscrito_OSA_IVF_Fissurados_Pacote_Orientador_Prof_Nivaldo_Alonso.docx`.
- **Testes / Auditoria:**
  - `article_machine machine audit --strict`: PASS
  - `pytest tests/`: 399 passed, 1 skipped (100% de integridade)
- **Proximos Passos Recomendados:**
  - [ ] Enviar pacote executivo ao Prof. Dr. Nivaldo Alonso (`Manuscrito_OSA_IVF_Fissurados_Pacote_Orientador_Prof_Nivaldo_Alonso.docx`).
  - [ ] Realizar upload dos 4 arquivos em inglês no portal de submissão da SAGE (CPCJ) após chancela.


### [2026-11-02 23:42] Handoff: Antigravity -> Codex / OpenCode
- **Agente Responsavel:** Antigravity (Google DeepMind)
- **Projeto Ativo:** `projects/NMA_OSA_VPI`
- **Fase / Modo:** Calibracao Pos-Hostile Red Team Review e Sincronizacao Google Docs / Word JCS
- **O que foi feito:**
  - Conducao de revisao hostil Red Team formal (`projects/NMA_OSA_VPI/reviews/red_team_hostile_review_jcs.md`) sob a skill `scientific-red-team-reviewer`.
  - Aplicacao de todas as correcoes pertinentes no manuscrito em ingles e portugues:
    * Calibracao epistemologica do titulo: substituicao de "Incidence" por "Frequency and Detection Rate" em razao da ausencia de polissonografia basal pre-operatoria universal de novo na literatura primaria.
    * Expurgo integral de adjetivacoes infladas e marcas de IA ("forensic", "crucially", "critical insights", "perilous illusion") e remocao da discussao defensiva sobre NMA da Introducao.
    * Adicao dos criterios formais da AASM na secao de Metodos: IAH >= 1,5 eventos/h para coortes pediatricas, IAH >= 5,0 eventos/h para adultos, e seguimento estavel de 6 a 12 meses.
    * Insercao de ressalvas de imprecisao amostral severa em Furlow (k=1, N=10, IC 95%: 1,8% a 40,4%) como hipotese geradora preliminar e alerta de validade externa para Orticochea (serie de centro unico em Bogota).
    * Reestruturacao pragmatica das recomendacoes clinicas para algoritmo estratificado por risco (PSG mandatria para Orticochea, retrognatismo grave, Robin ou sindromes; triagem clinica e oximetria noturna para retalho faringeo e palatoplastia padrao).
  - Eliminacao de sobreposicoes visuais e esteticas nos scripts R (`gerar_analises_e_figuras_publicacao.R`), realocando rotulos da Tabela Forest para coluna independente (`x = 106%`), ajustando caixas PRISMA (espacamento horizontal de 0,3 unidades) e margens do ROBINS-I.
  - Sincronizacao completa do Google Docs em ingles (`15njWq0Los5BExW6EwqORbAABiIHGfB6-HJPh6Jf0DOg`) e portugues (`1vtckKNiceaQ4EaYIYdSsViBitdbtWa7fd0YS7jUjvKk`): insercao inline de todas as 4 figuras em 300 DPI na secao de Resultados, tabelas com largura auto-ajustada e reposicionamento do memorando executivo para o final na versao em portugues.
  - Recompilacao dos 5 pacotes Word `.docx` de submissao e orientador com as correcoes integradas (`build_submission_docx_jcs.py`).
  - Reindexacao do grafo operacional (1.325 nos, 2.662 arestas).
  - Ausencia absoluta de travessoes (`—` ou `–`) em todos os documentos.
- **Testes / Auditoria:**
  - `article_machine machine audit --strict`: PASS (100% de conformidade)
  - `pytest tests/`: 400 passed, 1 skipped (100% de integridade)
- **Proximos Passos Recomendados:**
  - [ ] Enviar o link do Google Docs ou o `.docx` atualizado ao Prof. Dr. Nivaldo Alonso para revisao final.
  - [ ] Confirmar o e-mail e ORCID do Dr. Marcel Gutierrez antes da submissao formal.
  - [ ] Prosseguir para submissao no Editorial Manager do *The Journal of Craniofacial Surgery*.



### [2026-11-03] Handoff: Codex -> proximo agente
- Projeto: `projects/NMA_OSA_VPI`. Auditoria interna dos documentos JCS de 02/11, por pedido do autor.
- Parecer PT/EN: `reviews/peer_review_20261103/{portugues,ingles}/parecer_peer_review.md`; 13 achados, 4 bloqueios centrais. Nao tratar como pronto para submissao.
- Verificados: discrepancias de limiar/seguimento Zhao; contagens CSV/DOI; texto/XML de cinco DOCX; candidatos bibliograficos e ensaio randomizado que contradizem declaracoes do texto. Sem nova extracao/sintese; originais preservados por hash.
- Machine audit strict PASS; workflow planner BLOCK por contratos legados; audit-language BLOCK por assinatura numerica lexical. Nao alegar reproducao cientifica ou equivalencia bilingue certificada.
- Grafo operacional atualizado; suas alteracoes geradas permanecem fora do checkpoint para nao versionar mistura de superficies alheias. Arquivos untracked preexistentes de implementacao/testes preservados. Suite completa nao reexecutada: tarefa documental, sem mudanca no runtime da maquina.
- English: Internal author-requested review found 13 issues and 4 central blockers. Read the paired review before further work. No manuscript edits, new synthesis, live Docs check or submission. Existing PASS artifacts do not establish scientific readiness.
