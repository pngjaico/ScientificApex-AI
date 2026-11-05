# Pacote de Solicitação de Dados UNOS/OPTN (STAR Files / SRTR Data Request)

## Projeto: `xai-liver-ecd-allocation-unos`
**Machine Learning Explicável (XAI) e Predição Conformal para Alocação de Órgãos Marginais (ECD) no Transplante Hepático**

---

## 1. Informações Institucionais e Justificativa de Pesquisa

- **Título do Projeto:** Explainable Machine Learning (XAI) and Conformal Prediction for Expanded Criteria Donor (ECD) Allocation in Liver Transplantation: Outperforming the Donor Risk Index (DRI) using the UNOS/OPTN Population Registry
- **Investigador Principal:** João Vitor Fiches Machado e equipe
- **Destino Científico:** Sessão Plenária de Transplante Hepático — Gastrão 2027; Submissão a *Liver Transplantation* / *Transplantation* / *American Journal of Transplantation*.
- **Enquadramento Ético (IRB/CEP):** Isenção de consentimento e aprovação ética formal nos termos da regulamentação federal norte-americana **45 CFR 46.104(d)(4)** (pesquisa secundária com base de dados pública desidentificada e anonimizada) e normas CONEP/Brasil para bases de dados de domínio público sem identificação nominal de participantes.
- **Acordo de Uso de Dados (DUA):** Compromisso de conformidade integral com o *OPTN Data Use Agreement*, garantindo sigilo, não-tentativa de reidentificação de doadores, receptores ou centros transplantadores, e uso estritamente restrito aos fins de pesquisa declarados.

---

## 2. Resumo da Justificativa Científica (Research Rationale)

O transplante hepático enfrenta uma crise persistente de escassez de órgãos, levando ao descarte anual de centenas de enxertos de doadores falecidos com critérios expandidos (ECD) ou doação após parada circulatória (DCD). Os escores clássicos de alocação linear—especialmente o *Donor Risk Index (DRI)* de Feng et al. (2006) e o *Balance of Risk (BAR score)* de Dutkowski et al. (2012)—falham em capturar sinergias biológicas e interações não-lineares protetoras entre características do doador e do receptor (ex.: receptores de baixa gravidade com lab MELD < 20 tolerando enxertos idosos ou com isquemia prolongada sem comprometimento da sobrevida).

O objetivo desta solicitação é obter a coorte completa de transplantes hepáticos de doador falecido (2010 a 2025) para desenvolver, validar prospectivamente (corte temporal 2021–2025) e calibrar algoritmos de *gradient boosting* (LightGBM/XGBoost com restrições de monotonicidade clínica) combinados à predição conformal de incerteza (MAPIE, com 95% de cobertura garantida) e interpretabilidade explicável (TreeSHAP), comparando formalmente o Benefício Líquido Clínico em Análise de Curva de Decisão (DCA) contra o DRI e BAR score.

---

## 3. Especificação das Tabelas e Arquivos Solicitados (UNOS STAR)

Solicitamos os seguintes arquivos do pacote padrão **OPTN/SRTR Standard Transplant Analysis and Research (STAR)**:

| Tabela / Arquivo STAR | Conteúdo Principal | Chave de Vinculação |
| :--- | :--- | :--- |
| **`TX_LI` (Liver Transplant)** | Registros de todos os procedimentos de transplante hepático, datas, características basais do receptor, variáveis operatórias e seguimento longitudinal de enxerto e paciente. | `TRR_ID_CODE`, `PX_ID`, `DONOR_ID` |
| **`DONOR_DECEASED` (Deceased Donor)** | Perfil clínico completo do doador falecido (DBD e DCD), causas de óbito, dados de biópsia hepática, exames laboratoriais, suporte inotrópico e tempos de preservação. | `DONOR_ID` |
| **`CAND_LI` (Liver Candidate)** | Trajetória do candidato em lista de espera, pontuações de MELD/MELD-Na no momento da alocação e parâmetros clínicos de gravidade. | `PX_ID` |

---

## 4. Dicionário de Variáveis Mapeadas

### A. Preditores do Doador (Tabela `DONOR_DECEASED`)
- `DON_AGE`: Idade do doador (anos).
- `DON_TY`: Tipo de doador (`C` = Falecido DBD, `D` = Parada circulatória DCD).
- `COD_CAD_DON`: Causa do óbito (1=Anóxia, 2=AVC/CVA, 3=Trauma craniano, 4=Tumor SNC, 5=Outros).
- `MACRO_FAT_LIV_DON`: Percentual de esteatose macrovacuolar na biópsia do fígado do doador.
- `HIST_CARD_ARREST_DON`: Histórico de parada cardiorrespiratória com manobras de RCP.
- `SODIUM_SERUM_DON`: Pico de sódio sérico pré-captação (mEq/L).
- `COLD_ISCH_TM`: Tempo de isquemia fria em horas (CIT).
- `WARM_ISCH_TM`: Tempo de isquemia morna do doador em minutos (relevante para DCD).
- `DON_HGT_CM`, `DON_WGT_KG`: Altura e peso do doador (para cálculo de BMI e razões de matching).
- `SGOT_DON`, `SGPT_DON`: Transaminases séricas (AST/ALT) do doador.
- `INOTROP_SUPPORT_DON`: Uso e número de agentes inotrópicos vasoativos.

### B. Preditores do Receptor e Transplante (Tabela `TX_LI` e `CAND_LI`)
- `CAN_AGE_AT_TX`: Idade do receptor na data do transplante.
- `CAN_GENDER`: Sexo biológico do receptor.
- `CAN_ABO`: Grupo sanguíneo ABO do receptor.
- `DON_ABO`: Grupo sanguíneo ABO do doador (para compatibilidade ABO).
- `CAN_HGT_CM`, `CAN_WGT_KG`: Estatura e peso do receptor no transplante.
- `CAN_DGN`: Diagnóstico primário de doença hepática (MASH, Álcool, HCV, Colestática, HCC).
- `CAN_LAST_LAB_MELD`: MELD laboratorial do receptor na data do transplante.
- `CAN_LAST_SRTR_LAB_MELD`: MELD-Na laboratorial do receptor na data do transplante.
- `CAN_PREV_ABDOM_SURG`: Cirurgia abdominal prévia (Sim/Não).
- `CAN_PORTAL_VEIN_THROMB`: Presença e grau de trombose de veia porta.
- `CAN_VENTILATOR`: Uso de ventilação mecânica no momento do transplante.
- `CAN_DIAL`: Hemodiálise ou terapia renal substitutiva nos 7 dias pré-transplante.
- `CAN_MED_COND`: Condição médica no transplante (1=UTI, 2=Hospitalizado não-UTI, 3=Ambulatorial).
- `SHARE_TY`: Tipo de compartilhamento/alocação (Local, Regional, Nacional; DSA vs Acuity Circle).
- `REGION`: Região geográfica da UNOS (1 a 11).

### C. Desfechos Clínicos Primários e Secundários (Tabela `TX_LI`)
- `GSTATUS`: Status do enxerto (1 = Perda do enxerto/falência, 0 = Enxerto funcionante).
- `GTIME`: Tempo até a perda do enxerto (dias).
- `PSTATUS`: Status vital do paciente (1 = Óbito, 0 = Vivo).
- `PTIME`: Tempo até o óbito (dias).
- `COD`: Causa primária de óbito ou falência do enxerto.

---

## 5. Passos Práticos para Envio da Solicitação

1. **Acesso ao Portal UNOS/SRTR:** Acesse o portal oficial [https://www.srtr.org/requesting-srtr-data/](https://www.srtr.org/requesting-srtr-data/) ou [https://optn.transplant.hrsa.gov/data/request-data/](https://optn.transplant.hrsa.gov/data/request-data/).
2. **Preenchimento do Formulário:** Copie os campos de justificativa e o dicionário de variáveis acima para o formulário online da OPTN/SRTR.
3. **Assinatura do Data Use Agreement (DUA):** Assine digitalmente o DUA institucional.
4. **Depósito dos Arquivos Recebidos:** Assim que a UNOS disponibilizar o link para download (geralmente arquivos compactados `.csv.gz`, `.sas7bdat` ou `.dta`), salve os arquivos na pasta:
   `projects/xai-liver-ecd-allocation-unos/sources/unos_star/`
