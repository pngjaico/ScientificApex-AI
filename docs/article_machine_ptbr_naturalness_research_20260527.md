# Pesquisa De Calibragem PT-BR Da Article Machine

Data: 2026-05-27

Escopo: camada estrutural de escrita científica em português brasileiro. Esta pesquisa não avalia a NMA nem seus resultados; ela define regras para a máquina escrever textos acadêmicos naturais, claros e auditáveis.

## Fontes Consultadas

- Revista de Saúde Pública, instruções aos autores: a revista explicita estrutura de resumo e descreve revisão de redação científica orientada por clareza, brevidade, objetividade e solidez. Fonte: https://rsp.fsp.usp.br/pt-br/instrucoes-aos-autores/
- Revista de Saúde Pública, categorias de artigos: revisões sistemáticas devem declarar busca, critérios de seleção e síntese dos resultados. Fonte: https://rsp.fsp.usp.br/pt-br/categorias-de-artigos/
- Revista de Saúde Pública, preparo do manuscrito: os resultados devem seguir sequência lógica e o texto deve restringir a descrição aos dados importantes. Fonte: https://rsp.fsp.usp.br/pt-br/preparo-do-manuscrito/
- EQUATOR/PRISMA 2020: revisões sistemáticas e meta-análises exigem checklist de relato, transparência de método e apresentação proporcional dos achados. Fonte: https://www.equator-network.org/reporting-guidelines/prisma/
- SciELO, exemplo de revisão sistemática em português: resumos biomédicos naturais usam verbos diretos e evitam metáforas metodológicas vagas. Fonte: https://scielo.pt/scielo.php?pid=S1645-00862022000100110&script=sci_arttext
- BioSCIENCE, exemplo de revisão sobre cirurgia bariátrica e câncer colorretal: a estrutura Introdução, Objetivo, Método, Resultados e Conclusão funciona bem em português biomédico. Fonte: https://bioscience.org.br/bioscience/index.php/bioscience/article/view/551
- LA-BORA!/Gov.br, Linguagem Simples: recomenda ir direto ao ponto, reduzir siglas, estrangeirismos e jargões, usar frases curtas e preferir verbos de ação. Fonte: https://www.gov.br/servidor/pt-br/assuntos/laboragov/curadoria-tematica/linguagem-simples
- Guia de Edição de Serviços do Gov.br: reforça voz ativa, ordem direta, palavras nativas e consistência de termos. Fonte: https://www.gov.br/pt-br/guia-de-edicao-de-servicos-do-gov.br/escrevendo-o-seu-texto
- Manual de Comunicação do Senado: recomenda explicar termos técnicos, siglas, jargões e estrangeirismos. Fonte: https://www12.senado.leg.br/manualdecomunicacao/estilos/palavras-mais-simples

## Regras Derivadas

- O texto deve nascer em português, não ser tradução de um esqueleto em inglês.
- Termos técnicos podem permanecer, mas a primeira aparição precisa explicar a medida ou sigla.
- Anglicismos dispensáveis devem ser substituídos: `framework`, `endpoint`, `outcome`, `baseline`, `layer`, `signal`, `hub`.
- Expressões vagas devem ser reescritas: "camada contextual", "sinal convergente", "hub-dependência", "eixo obesidade-metabolismo".
- Frases longas ou cheias de substantivos abstratos devem virar frases menores com sujeito e verbo.
- A conclusão deve ser proporcional ao desenho do estudo. Em evidência observacional, usar "associação", "sugeriu", "foi compatível com" e evitar "prova".
- O arquivo final em Word deve ser auditado diretamente como `.docx`, porque problemas de formatação e extração podem aparecer depois do Markdown.

## Implementação Na Máquina

- `article_machine.ptbr_style.audit_text` bloqueia HR sem definição, jargão proibido, anglicismo dispensável e mojibake.
- `article_machine.ptbr_style.audit_text` gera avisos para frases longas, clichês de tradução e excesso de nominalização.
- `article_machine.ptbr_style.naturalize_text` aplica substituições conservadoras sem alterar números.
- `article-machine style ptbr-naturalize` cria uma versão inicial reescrita e um relatório JSON com a comparação entre original e revisado.
- `article-machine style ptbr-brief` gera um perfil de escrita antes de produzir o entregável.
- O Review Trinity pode bloquear textos em português quando `ptbr_style_policy.enabled: true` estiver ativo no projeto.

## Limite Metodológico

Esta camada melhora a forma, mas não valida evidência científica. Ela não decide inclusão de artigo, risco de viés, GRADE, CINeMA ou coerência da rede. Para isso, a Article Machine ainda precisa passar por Evidence Lock, Review Trinity e pelos módulos metodológicos do projeto.
