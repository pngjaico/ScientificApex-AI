# Organização das publicações

O módulo `projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/organizar_publicacoes.py` cria uma estrutura vazia de organização dentro de um projeto existente. O padrão é `--dry-run`; a criação exige `--criar`. O destino existente é recusado, e a ferramenta não move, renomeia nem copia arquivos.

## Uso

Na raiz do workspace:

```powershell
python projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/organizar_publicacoes.py --projeto projeto-id --revista revista-slug --identificador v01 --raiz .
python projects/article-machine-governance-2026/analysis/codex-first-2026-11-01/organizar_publicacoes.py --projeto projeto-id --revista revista-slug --identificador v01 --raiz . --criar
```

`--raiz` precisa ser explícito e conter `projects/<projeto-id>/`. IDs de projeto e revista são slugs simples; identificadores aceitam letras, números, ponto, hífen e sublinhado, sem separadores de caminho.

## Estrutura criada

O destino é `projects/<projeto>/publicacoes/<revista-slug>/<identificador>/` com:

1. `01_protocolo/`
2. `02_busca_e_referencias/`
3. `03_dados_autorizados/`
4. `04_analises/`
5. `05_tabelas/`
6. `06_figuras/`
7. `07_manuscrito/`
8. `08_revisao/`
9. `09_submissao/`

Inclui `manifesto.json` e `LEIA-ME.md`. O manifesto aponta para `project.yaml`, `protocol.yaml`, `evidence/claim_map.jsonl`, `drafts/` e `analysis/` canônicos. Não renomeia nem substitui esses contratos. Entregáveis de congresso continuam em `deliverables/` e no pipeline próprio; a publicação guarda apenas um índice ou referência aprovada, sem duplicar o pacote canônico.

## Nomes e checkpoints

Use `tipo_assunto_YYYY-MM-DD_vNN.ext`, por exemplo `tabela_fluxo_2026-11-01_v01.csv`. Mantenha versões anteriores sem sobrescrever. A pasta `03_dados_autorizados/` não é autorização para tratar ou copiar dados humanos: primeiro confirme base legal, consentimento/ética quando aplicável, desidentificação e permissão do projeto.

Antes de circular uma versão, faça checkpoints com o responsável pelo projeto e com os requisitos atuais da revista: protocolo e análise congelados; rastreabilidade com claims e referências; revisão metodológica e de privacidade; revisão editorial/coautores; conferência das instruções da revista; aprovação final do pacote e dos metadados. A organização facilita revisão; não promete que o material esteja publicável ou aceito.

Modelos em português ficam em `analysis/codex-first-2026-11-01/templates/modelos_em_portugues/`. Eles apontam para os scripts flat didáticos existentes sem os renomear.


## Regra final bilíngue
Cada uma das nove áreas agora contém `portugues/` e `ingles/`. Toda entrega deve ter os dois arquivos pareados, com o mesmo nome base em português. `verificar_pares` recusa órfãos; números, referências e semântica exigem auditoria adicional. Dados/código/locks são compartilhados. Os modelos bilíngues canônicos ficam em `modelos/` na raiz D:.
