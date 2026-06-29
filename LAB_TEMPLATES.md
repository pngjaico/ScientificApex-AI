# LAB TEMPLATES: SCIENTIFIC OS SPELLBOOK

## 00. Bootstrap
**Prompt:**
> Ative a máquina científica para o projeto [NOME] do tipo [TIPO].

**Efeito esperado**
- `article-machine init`
- criação do projeto
- geração do contexto inicial

## 01. Protocol Freeze
**Prompt:**
> Congele o protocolo do projeto [NOME]. Defina a pergunta, os objetivos, os critérios e prepare o gate `protocol-freeze`.

**Efeito esperado**
- revisar `protocol.yaml`
- gerar `Task Packet`
- tentar avançar para `protocol-freeze`

## 02. Systematic Review
**Prompt:**
> Inicie a revisão sistemática para [TEMA] no projeto [NOME].

**Efeito esperado**
- lane `evidence-writing`
- `PRISMA` + `GRADE` + `ROBIS` + `AMSTAR 2`
- corpus, triagem, extração, claim map, manuscrito, review trinity

## 03. Network Meta-Analysis
**Prompt:**
> Inicie uma network meta-analysis para [TEMA] no projeto [NOME].

**Efeito esperado**
- `PRISMA-NMA`
- suporte explícito a scripts R
- outputs em `analysis/` e manuscrito rastreável

## 04. Drug Discovery
**Prompt:**
> Inicie um projeto de descoberta de drogas para [ALVO] no projeto [NOME].

**Efeito esperado**
- lane `computational-discovery`
- perfil `drug-discovery`
- benchmarking, análise, relatório, manuscrito com limites explícitos

## 05. Intestinal Digital Twin
**Prompt:**
> Inicie um projeto de intestino in silico para [PERGUNTA] no projeto [NOME].

**Efeito esperado**
- lane `computational-discovery`
- perfil `intestinal-digital-twin`
- model spec, análise de sensibilidade, relatório técnico e draft

## 06. R Analysis
**Prompt:**
> Rode o script R [CAMINHO] no projeto [NOME] e registre tudo no manifest.

**Efeito esperado**
- `article-machine preflight`
- `article-machine run-r`
- logs e `sessionInfo.txt`

## 07. Review Trinity
**Prompt:**
> Rode a Review Trinity no projeto [NOME].

**Efeito esperado**
- parecer metodológico
- parecer quantitativo
- parecer editorial
- `reviews/review_report.json`

## 08. Submission
**Prompt:**
> Prepare o projeto [NOME] para submissão.

**Efeito esperado**
- Evidence Lock em `PASS`
- Review Trinity em `PASS`
- export em `exports/`
