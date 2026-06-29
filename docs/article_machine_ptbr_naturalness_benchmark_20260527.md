# Benchmark Estrutural PT-BR

Data: 2026-05-27

Objetivo: verificar se a Article Machine impede, detecta ou corrige marcas comuns de texto científico em português com aparência de tradução literal.

## Casos De Teste

| Caso | Entrada problemática | Resultado esperado |
|---|---|---|
| Jargão traduzido | "camada contextual", "sinal convergente", "hub-dependência" | Bloqueio e sugestão concreta |
| HR sem definição | "HR 0,70" na primeira menção | Bloqueio e recomendação de "razão de riscos instantâneos (hazard ratio, HR)" |
| Anglicismo dispensável | `framework`, `endpoint`, `outcome`, `baseline`, `layer`, `signal`, `hub` | Bloqueio e equivalente em português |
| Codificação quebrada | sequências típicas de mojibake ou caractere de substituição | Bloqueio |
| Tradução literal | "no contexto de", "em termos de", "à luz de", "evidencia-se" | Aviso e sugestão de frase mais direta |
| Excesso abstrato | muitas palavras em `-ção`, `-mento`, `-dade`, `-ência` | Aviso para reescrever com verbos |
| DOCX final | texto problemático dentro de `.docx` | Leitura e auditoria do conteúdo do Word |

## Critério De Aceite

- Testes unitários da camada PT-BR devem passar.
- O comando `style ptbr-audit` deve retornar erro quando houver achado bloqueante.
- O comando `style ptbr-naturalize` deve preservar números e reduzir os achados do texto original.
- O Review Trinity deve falhar quando o projeto exigir `ptbr_style_policy` e os textos em português tiverem bloqueios.

## Resultado Atual

O benchmark foi transformado em testes automatizados em `tests/test_ptbr_style.py`.

Validação em 2026-05-27:

- `pytest -q`: passou.
- `compileall article_machine projects\OncoMetabolic_CRC_NMA\scripts`: passou.
- `article-machine style ptbr-audit` nos seis entregáveis PT-BR principais, incluindo `.docx`: passou com zero achados.
- `article-machine review projects\OncoMetabolic_CRC_NMA`: passou.
- `article-machine guard check projects\OncoMetabolic_CRC_NMA`: passou.

Esses resultados validam a camada estrutural de linguagem. Não validam automaticamente a qualidade da evidência científica de qualquer manuscrito futuro.
