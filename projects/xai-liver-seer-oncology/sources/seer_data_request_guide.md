# Guia de Acesso Gratuito à Base do NCI SEER

## Projeto: `xai-liver-seer-oncology`
**Machine Learning Explicável (XAI) e Predição Conformal para Ressecção vs Transplante no Carcinoma Hepatocelular**

---

## 1. O que é a base SEER e por que ela é 100% gratuita?
O programa **SEER (Surveillance, Epidemiology, and End Results)** é mantido pelo **National Cancer Institute (NCI / NIH)** dos Estados Unidos e cobre cerca de 48% da população norte-americana.
* **Custo:** **US$ 0,00** (totalmente financiado pelo governo dos EUA para pesquisa biomédica).
* **Sem taxas administrativas:** Não há cobrança de taxas de recuperação de custos.
* **Aprovação:** O NCI libera as credenciais para qualquer pesquisador acadêmico após o preenchimento online do *Research Data Agreement*.

---

## 2. Passo a Passo para Obter o Acesso (2 minutos)

1. **Acesse a página de solicitação do NCI:**
   👉 [https://seer.cancer.gov/data/access.html](https://seer.cancer.gov/data/access.html)
2. **Selecione o tipo de acesso:**
   * Clique em **"SEER Research Data"** (dados de pesquisa padrão com todas as variáveis clínicas, histológicas, estadiamento e sobrevida).
3. **Preencha seus dados de identificação acadêmica:**
   * Nome: João Vitor Fiches Machado
   * Instituição: sua afiliação universitária / hospitalar
   * E-mail: preferencialmente e-mail institucional
4. **Assine eletronicamente o DUA (Data-Use Agreement):**
   * Compromisso de não tentar reidentificar pacientes e citar o SEER no artigo.
5. **Recebimento das Credenciais:**
   * O NCI envia por e-mail suas credenciais e o link para download do software oficial **SEER*Stat** (geralmente em até 1 a 2 dias úteis, 100% gratuito).

---

## 3. Extração da Coorte de Carcinoma Hepatocelular no SEER*Stat

Ao abrir o software `SEER*Stat`:
1. Selecione **New Matrix Session** ou **Case Listing Session**.
2. Na aba **Selection (Filtros)**:
   * `Site and Morphology.Site recode ICD-O-3/WHO 2008` = **Liver** (`C22.0`)
   * `Histologic Type ICD-O-3` = **8170/3 - 8175/3** (Hepatocellular Carcinoma)
   * `Age at diagnosis` >= 18 anos
   * `RX Summ--Surg Prim Site (1998+)` in [30-59 (Ressecção), 61 (Transplante)]
3. Na aba **Table (Variáveis)**:
   * Patient ID, Year of diagnosis, Age, Sex, Race
   * CS tumor size, CS extension, Vascular invasion, AFP, Fibrosis score
   * Derived AJCC Stage Group 8th ed
   * RX Summ--Surg Prim Site
   * Survival months, Vital status recode, SEER cause-specific death classification
4. **Exportar:** Clique em `Matrix -> Export` e salve o arquivo como `.csv` ou `.txt` na pasta:
   `projects/xai-liver-seer-oncology/sources/seer/`
