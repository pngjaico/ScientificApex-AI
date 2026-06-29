---
name: ptbr-article-writing
description: Use when drafting, rewriting, naturalizing, or auditing scientific manuscripts, abstracts, thesis chapters, posters, decks, or Article Machine outputs in Brazilian Portuguese, especially when the text risks sounding translated from English, uses anglicisms, needs IMRAD, structured abstract discipline, ABNT, Vancouver/ICMJE/NLM, APA, IEEE, Chicago, citation/reference formatting, ptbr-audit, Evidence Lock, or Portuguese style review.
---

# PT-BR Article Writing

## Overview

Escreva primeiro em português brasileiro acadêmico. Não traduza um molde em inglês; reconstrua a frase a partir do objetivo, método, resultado e limite real da evidência.

## Mandatory Flow

1. Identifique o projeto ativo em `projects/<project_id>/` e leia `project.yaml`, `protocol.yaml`, `standards.yaml` e `compute.yaml` quando a tarefa envolver evidência, análise, descoberta, manuscrito ou entrega científica.
2. Atualize ou consulte um Task Packet antes de redigir texto substantivo.
3. Gere um perfil de escrita com:

```powershell
article-machine style ptbr-brief --deliverable "<tipo>" --audience "<leitor>" --output "<project_dir>/context/ptbr_generation_brief.md"
```

4. Use o perfil, o protocolo, o mapa de claims e as regras do periódico/congresso para escrever. Não invente fato para melhorar fluidez.
5. Para texto existente com cheiro de tradução, rode:

```powershell
article-machine style ptbr-naturalize "<entrada.md>" --output "<saida.md>" --json-output "<relatorio.json>"
```

6. Audite antes de chamar de pronto:

```powershell
article-machine style ptbr-audit "<arquivo.md>" --output "<audit.md>" --json-output "<audit.json>"
```

7. Se houver conteúdo factual, rode o fluxo de Evidence Lock/Review Trinity aplicável. Texto bonito sem claim seguro continua reprovado.

Use o caminho `.venv\Scripts\article-machine.exe` quando o comando não estiver no PATH.

## Citation Style Extension

Antes de formatar citações ou referências:

1. Identifique o estilo exigido pelo periódico, congresso, banca ou instituição.
2. Leia `references/citation-and-reference-styles.md`.
3. Não misture famílias: ABNT autor-data/numeric, Vancouver numeric, APA autor-data, IEEE numeric e Chicago notas/autor-data têm lógicas diferentes.
4. Confirme a edição vigente da norma ou manual. ABNT deve ser verificada em fonte institucional/ABNT; gerador automático não é prova.
5. Corrija metadados antes da pontuação: autor, título, periódico, ano, volume, número, páginas/eLocation, DOI, PMID/PMID Central, URL e data de acesso quando exigida.
6. Sincronize `drafts/references.bib`, citações no texto e `evidence/claim_map.jsonl`. Citação perfeita para fonte errada continua erro científico.

Pare se o usuário pedir "ABNT" genericamente para submissão biomédica sem informar o destino. ABNT costuma reger trabalhos acadêmicos no Brasil; muitos periódicos biomédicos exigem Vancouver/ICMJE/NLM mesmo quando o texto está em português.

## Writing Standard

| Elemento | Faça | Bloqueie |
|---|---|---|
| Resumo | Objetivo, método, resultados principais e conclusão proporcional | Resumo que promete mais do que o corpo mostra |
| Introdução | Problema, lacuna e objetivo no fim da seção | Nariz de cera, revisão extensa sem pergunta clara |
| Métodos | Delineamento, fonte, período, população, análise e critérios | "Foi utilizada uma abordagem robusta" sem detalhe operacional |
| Resultados | Números, medidas, intervalos e direção do efeito | Interpretação antes de apresentar o achado |
| Discussão | Principal achado, comparação, limites e implicação prudente | Conclusão causal sem desenho causal |
| Conclusão | Responder ao objetivo com incerteza explícita | "Mais estudos são necessários" como frase vazia |

## Natural Portuguese Rules

- Prefira ordem direta: sujeito, verbo, complemento.
- Use verbos concretos no lugar de substantivos abstratos quando a frase ficar pesada.
- Defina siglas na primeira menção e evite sigla no resumo se ela não for inevitável.
- Troque anglicismos dispensáveis: `endpoint` -> desfecho; `baseline` -> início do seguimento; `framework` -> modelo de trabalho ou estrutura metodológica.
- Use "os achados sugerem", "foi observada associação" ou "a estimativa indicou" quando o desenho não permite causalidade.
- Mantenha termos internacionais quando forem a forma reconhecida da medida, mas explique em português: razão de riscos instantâneos (hazard ratio, HR).
- Corte frases longas antes de polir adjetivos. Uma frase com duas relações metodológicas deve virar duas frases.

## Evidence And Claims

- Use `{{claim:claim-id}}` para qualquer afirmação factual em `drafts/manuscript.md`.
- Não transforme cautela metodológica em fraqueza estilística. Incerteza bem escrita é melhor do que precisão falsa.
- Não apague números, intervalos, datas, nomes de bases, critérios de inclusão, ferramentas de risco de viés ou limitações para deixar o texto mais "natural".
- Se uma frase ficar feia porque a evidência é incompleta, preserve a feiura metodológica e registre a pendência.

## Calibration Reference

Leia `references/portuguese-academic-style.md` quando:

- for escrever manuscrito, resumo expandido, tese, poster ou deck em português;
- o texto tiver muitos anglicismos, voz passiva ou nominalizações;
- o usuário pedir "não parecer tradução";
- o periódico/congresso exigir resumo, IMRAD, PRISMA, Vancouver, DeCS/MeSH ou estrutura específica.

Leia `references/citation-and-reference-styles.md` quando:

- o usuário pedir ABNT, NBR 6023, NBR 10520, NBR 14724, NBR 6028, Vancouver, ICMJE, NLM, Citing Medicine, APA, IEEE, Chicago, AMA ou "normas de referência";
- for converter bibliografia entre estilos;
- houver conflito entre norma institucional, instruções de periódico e saída de gerador bibliográfico;
- precisar auditar se as citações no texto batem com a lista de referências.

## Common Mistakes

| Erro | Correção |
|---|---|
| Traduzir "we found that" como "nós encontramos que" | "Observou-se que", "Os dados mostraram" ou "Foi identificada associação" |
| Usar "no contexto de" para qualquer coisa | Nomeie a análise, população ou cenário real |
| Chamar todo resultado de "sinal" | Use associação, estimativa, resultado, padrão observado ou achado |
| Dizer "robusto", "inovador", "definitivo" | Mostre desenho, amostra, precisão e limite |
| Reescrever conclusão para soar forte | Ajuste a força à evidência; se necessário, reduza a conclusão |
| Auditar só ortografia | Rode `ptbr-audit` e Evidence Lock; estilo e verdade são gates separados |
| Aplicar ABNT 6023:2018 por hábito | Verifique a edição vigente; em 2025 a NBR 6023 recebeu atualização/substituição |
| Chamar todo estilo numérico de Vancouver | Vancouver biomédico deve seguir ICMJE/NLM/Citing Medicine ou a instrução do periódico |
| Deixar Zotero/gerador decidir sozinho | Use gerador só como rascunho; confira metadados e regra do destino |

## Stop Conditions

Pare e reporte falha claramente se:

- `Rscript` for necessário pelo projeto e estiver ausente;
- o texto factual não tiver claim map ou fonte verificável;
- o `ptbr-audit` retornar `block`;
- houver mojibake, caracteres quebrados ou perda de acentos;
- o usuário pedir submissão, poster, slides ou resumo fora do pipeline de deliverables.
- a norma bibliográfica exigida não estiver identificada ou entrar em conflito com a regra do destino.
