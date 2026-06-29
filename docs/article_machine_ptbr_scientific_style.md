# Guia De Estilo Científico PT-BR

Este guia é obrigatório para entregáveis científicos em português gerados pela Article Machine: resumo expandido, resumo de congresso, métodos, conclusão, brief para orientador e cartas em português.

## Regra Central

Escrever primeiro em português acadêmico brasileiro. Não traduzir um template inglês. O texto deve parecer escrito por pesquisador brasileiro: direto, específico, com sujeito claro e sem abstrações que escondem o método.

## Termos A Evitar

| Evitar | Usar |
|---|---|
| camada contextual | análise separada usada para interpretação |
| camada bariátrica contextual | análise separada da cirurgia bariátrica |
| hub-dependência | influência de um estudo dominante na rede |
| eixo obesidade-metabolismo | relação entre obesidade, alterações metabólicas e risco de câncer |
| sinal farmacológico | associação observada para a classe medicamentosa |
| sinal convergente | padrão observado em diferentes análises |
| NMA | meta-análise em rede, salvo tabelas ou sigla já definida |

## Medidas Estatísticas

- Na primeira menção, escrever: "razão de riscos instantâneos (hazard ratio, HR)".
- Depois da definição, "HR" pode ser usado em tabelas e frases de resultado.
- Para texto corrido, preferir "razão de risco" quando a frase ficar mais natural.
- P-score deve ser apresentado como medida de ranqueamento.
- tau2 e I2 devem ser explicados como medidas de heterogeneidade quando aparecerem em texto corrido.

## Frase E Tom

- Preferir frases curtas, com uma ideia principal por frase.
- Evitar excesso de substantivos abstratos.
- Não usar tom promocional: "robusto", "inovador", "definitivo" ou "prova causal" sem base metodológica.
- Usar linguagem associativa para evidência observacional: "foi associado", "sugeriu", "apontou", "foi compatível com".
- Explicar o motivo metodológico da separação de análises em vez de chamar isso de "camada".

## Checklist Antes De Entregar

- HR foi explicado em português na primeira aparição?
- Siglas foram definidas antes do uso em texto corrido?
- Há jargão traduzido sem explicação?
- Há termos estatísticos sem explicação curta?
- Há frases longas que poderiam virar duas frases?
- O texto evita prometer causalidade quando a evidência é observacional?
- O arquivo final foi lido como `.docx` quando o entregável principal é Word?
- Há sinais de codificação quebrada, como sequências típicas de mojibake ou caracteres de substituição?
- Há anglicismos dispensáveis, como `framework`, `endpoint`, `outcome`, `baseline`, `layer`, `signal` ou `hub`?
- Há excesso de frases do tipo "no contexto de", "em termos de", "à luz de", "evidencia-se" e "ressalta-se"?
- Há muitas palavras abstratas terminadas em `-ção`, `-mento`, `-dade` ou `-ência` na mesma frase?

## Camada Estrutural De Naturalidade

A Article Machine deve tratar textos em português como produção primária, não como tradução posterior. Para isso, a camada PT-BR aplica quatro barreiras antes de liberar resumo, método, conclusão, carta ou brief:

1. Bloqueio de codificação quebrada: qualquer sinal de mojibake ou caractere de substituição invalida o texto.
2. Bloqueio de inglês desnecessário: termos como `framework`, `endpoint`, `outcome`, `baseline`, `arm-level`, `layer`, `signal` e `hub` devem ser substituídos por equivalentes em português, salvo quando o termo estrangeiro for parte formal da medida ou da sigla.
3. Aviso de tradução literal: expressões como "no contexto de", "em termos de", "à luz de", "evidencia-se" e "ressalta-se" não são proibidas em absoluto, mas a máquina deve sugerir formulação mais direta.
4. Aviso de excesso de nominalização: frases carregadas de substantivos abstratos devem ser reescritas com verbos e sujeito explícito.

Títulos de artigos em referências Vancouver não devem ser traduzidos nem corrigidos pelo auditor. O bloqueio de inglês vale para o texto autoral em português, não para títulos bibliográficos preservados.

Essa camada não substitui revisão humana. Ela impede que a primeira versão chegue ao orientador com aparência de texto traduzido, genérico ou excessivamente abstrato.

## Auditor Automático

Use:

```powershell
.\.venv\Scripts\python.exe -m article_machine style ptbr-audit <arquivos.md> --output <relatorio.md> --json-output <relatorio.json>
```

Projetos podem tornar a checagem obrigatória no Review Trinity com:

```yaml
ptbr_style_policy:
  enabled: true
  audit_paths:
    - deliverables/publication_pack_20260526/congress_abstract_pt.md
    - deliverables/publication_pack_20260526/professor_brief_pt.md
```

Para gerar um briefing de escrita antes de qualquer novo texto em português:

```powershell
.\.venv\Scripts\python.exe -m article_machine style ptbr-brief --deliverable "resumo expandido" --audience "orientador" --output <brief.md>
```

O auditor aceita `.md`, `.txt` e `.docx`. Em entregáveis para professor ou congresso, auditar o DOCX final é obrigatório.

Para produzir uma primeira reescrita automática de um texto com marcas de tradução literal:

```powershell
.\.venv\Scripts\python.exe -m article_machine style ptbr-naturalize <entrada.md> --output <saida.md> --json-output <relatorio.json>
```

A reescrita automática é uma triagem, não uma versão final. Se o relatório ainda vier com `block`, o texto deve ser corrigido antes de entrar no Review Trinity.

## Base De Calibragem

As regras acima foram calibradas em fontes brasileiras/lusófonas de escrita biomédica e em diretrizes internacionais de relato:

- Revista de Saúde Pública: exige resumos estruturados em Objetivo, Métodos, Resultados e Conclusão, e descreve revisão de redação científica voltada a clareza, brevidade, objetividade e solidez. Fonte: https://rsp.fsp.usp.br/pt-br/instrucoes-aos-autores/
- Revista de Saúde Pública, categorias de artigos: revisões sistemáticas devem descrever busca, critérios de seleção e síntese dos resultados. Fonte: https://rsp.fsp.usp.br/pt-br/categorias-de-artigos/
- Revista de Saúde Pública, preparo do manuscrito: resultados devem seguir sequência lógica e a descrição dos dados deve se restringir aos dados importantes. Fonte: https://rsp.fsp.usp.br/pt-br/preparo-do-manuscrito/
- SciELO, revisão sistemática em português sobre obesidade: usa verbos diretos como "realizou-se", "foram analisados", "constatou-se" e "conclui-se". Fonte: https://scielo.pt/scielo.php?pid=S1645-00862022000100110&script=sci_arttext
- BioSCIENCE, revisão em português sobre cirurgia bariátrica e câncer colorretal: usa estrutura biomédica direta em Introdução, Objetivo, Método, Resultados e Conclusão. Fonte: https://bioscience.org.br/bioscience/index.php/bioscience/article/view/551
- EQUATOR/PRISMA 2020: confirma PRISMA como guideline para revisões sistemáticas e meta-análises. Fonte: https://www.equator-network.org/reporting-guidelines/prisma/
- LA-BORA!/Gov.br, Linguagem Simples: reforça frases curtas, uso de palavras conhecidas, redução de siglas, jargões e estrangeirismos, e troca de substantivos abstratos por verbos de ação. Fonte: https://www.gov.br/servidor/pt-br/assuntos/laboragov/curadoria-tematica/linguagem-simples
- Guia de Edição de Serviços do Gov.br: reforça voz ativa, ordem direta, sentenças curtas, palavras nativas e consistência terminológica. Fonte: https://www.gov.br/pt-br/guia-de-edicao-de-servicos-do-gov.br/escrevendo-o-seu-texto
- Manual de Comunicação do Senado: recomenda explicar termos técnicos, siglas, jargões e estrangeirismos, além de organizar parágrafos com assunto claro. Fonte: https://www12.senado.leg.br/manualdecomunicacao/estilos/palavras-mais-simples

Essas fontes não devem ser copiadas. Elas servem para calibrar estrutura, naturalidade e proporção da linguagem.
