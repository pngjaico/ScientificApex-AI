# Relatório de Revisão Clínica por Pares (Clinical Peer Review Report)

**Manuscrito:** Machine Learning Explicável (XAI) e Predição Conformal de Incerteza para Ressecção versus Transplante Hepático no Carcinoma Hepatocelular  
**Autores:** João Vitor Fiches Machado et al.  
**Projeto:** `projects/xai-liver-seer-oncology` (OSF: `uzwr2`)  
**Periódico Alvo:** *Annals of Surgery* / *American Journal of Transplantation*  
**Parecer:** **Aceite com Revisões Menores (Accept with Minor Revisions)**

---

## 1. Avaliação do Mérito Científico e Cirúrgico

O presente estudo aborda um dos dilemas mais prementes e controversos da cirurgia hepatobiliopancreática contemporânea: a indicação precisa entre ressecção hepática parcial e transplante hepático ortotópico em pacientes com carcinoma hepatocelular (HCC).

Desde 1996, os Critérios de Milão de Mazzaferro estabeleceram um dogma rígido baseado em diâmetro tumoral estático (nódulo único <= 5 cm ou até 3 nódulos <= 3 cm). Embora esses critérios tenham garantido excelentes sobrevidas pós-transplante, eles penalizam desproporcionalmente pacientes com tumores ligeiramente expandidos, mas com biologia favorável, enquanto falham em predizer recidiva precoce em pacientes dentro de Milão com invasão microvascular agressiva.

A principal inovação desta investigação reside na aplicação de árvores de gradiente boosting com restrições monotônicas clínicas e predição conformal de incerteza (MAPIE) em uma coorte real massiva de **10.165 cirurgias curativas** extraídas do National Cancer Institute (SEER). A demonstração de uma AUROC temporal de **0,6773** frente a **0,5000** dos Critérios de Milão na validação externa independente representa um avanço tangível no suporte à decisão clínica.

---

## 2. Comentários Específicos aos Autores

### Introdução
- A contextualização histórica e as limitações dos sistemas lineares (Milão e TNM 8ª Edição) estão bem embasadas.
- O rationale para a inclusão de restrições monotônicas é clinicamente louvável, pois impede que o algoritmo aprenda paradoxos espúrios dos dados (por exemplo, que um tumor maior reduza o risco de óbito).

### Métodos
- O desenho do estudo segue rigorosamente a diretriz TRIPOD+AI (2024).
- O particionamento temporal em desenvolvimento (2000-2015, N = 6.962) e teste independente (2016-2021, N = 3.203) reflete práticas cirúrgicas modernas com excelente separação de eras.
- O uso de cobertura conformal de 95% fornece uma salvaguarda ética fundamental para cirurgiões e comitês de tumor board.

### Resultados e Figuras
- As Figuras 1, 2 e 3 em 300 DPI apresentam excelente clareza visual e conformidade editorial internacional.
- A Análise de Curva de Decisão (DCA) comprova que o modelo oferece ganho clínico líquido em toda a janela de limiares terapêuticos de 10% a 50%.
- A identificação do transplante hepático como fator protetor predominante (SHAP = 0,5586) é totalmente congruente com a fisiopatologia do HCC, uma vez que o transplante trata simultaneamente o tumor e o parênquima cirrótico subjacente.

### Discussão e Recomendações
- **Recomendação 1:** Discutir a aplicabilidade do modelo em cenários com escassez crítica de enxertos (como no sistema brasileiro do SUS ou europeu do Eurotransplant), enfatizando que o modelo serve para estratificar o benefício potencial da alocação de órgãos e não para burlar listas públicas de espera.
- **Recomendação 2:** Incluir menção às terapias de ponte (*bridging therapy*) e *downstaging* com quimioembolização (TACE) ou ablação por radiofrequência, que são rotineiramente empregadas enquanto o paciente aguarda em lista.

---

## 3. Recomendação Editorial

O manuscrito possui qualidade técnica e relevância clínica indiscutíveis. Recomenda-se a aprovação final após a incorporação das recomendações menores de discussão e contextualização de lista de espera.
