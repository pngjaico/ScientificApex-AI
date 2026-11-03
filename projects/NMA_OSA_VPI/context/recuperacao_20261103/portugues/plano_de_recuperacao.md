# Plano de recuperação metodológica OSA/IVF

Versão 0.1, 03/11/2026. Emenda proposta para conferência com o protocolo submetido. Não é protocolo registrado, síntese executada ou manuscrito final.

## Registro e histórico

O autor informou nesta sessão que o trabalho foi submetido ao PROSPERO e aguarda confirmação para publicação. Não foi possível conferir ID, recibo, data, versão ou status externo. O contrato local `prepared-not-submitted` está potencialmente desatualizado: não deve ser interpretado como prova de que nunca houve submissão. Também não há base para declarar registro final, registro prospectivo ou correspondência entre cadastro e métodos executados.

O usuário autorizou continuar os reparos locais enquanto o comprovante está indisponível. Esta autorização não cria um ID, não resolve a cronologia, não constitui aprovação dos coautores e não autoriza publicação externa. Não fazer novo cadastro duplicado. Preservar os contratos e as versões anteriores; a informação relatada pelo autor fica no manifesto deste pacote até conferência documental.

A regra local e `protocol-registration-governor` exigem registro final verificado para execução científica. O código adicionalmente verifica se o registro antecedeu o trabalho. Não modificar o validador, não apagar histórico e não criar outro projeto para simular prospectividade. A fase atual prepara correções, instrumentos e emenda. Busca sistemática nova, adjudicação final, extração definitiva, nova síntese e submissão permanecem condicionadas à resolução documentada desse requisito.

## Pergunta e estimandos propostos

Pergunta principal: qual a frequência de AOS identificada por PSG após cirurgia secundária para IVF em pessoas com fissura palatina, considerando técnica, definição diagnóstica e seguimento?

- Estimando primário: proporção com AOS entre participantes efetivamente avaliados por PSG em uma coorte cirúrgica elegível, em horizonte e limiar explicitados. Informar também a proporção da população elegível que foi testada.
- Incidência de novo: estimando separado, apenas quando ausência de AOS no basal e seguimento estiverem documentados.
- Efeito comparativo entre técnicas: estimando separado, apenas com comparação dentro do estudo e avaliação adequada de confundimento/desenho.
- Diferença entre fontes de aferição: descrição contextual. Não estimar sensibilidade, subdetecção multiplicativa ou mecanismo de subnotificação por simples divisão de proporções de estudos distintos.

Esses itens são propostas de reparação informadas pelo conhecimento dos resultados anteriores. Não serão chamados de pré-especificação original. A versão submetida ao PROSPERO deverá determinar o que é manutenção, esclarecimento ou mudança pós-hoc.

## Elegibilidade e reconstrução do corpus

Manter população fissura/IVF e procedimentos secundários como núcleo. Coortes mistas só entram na primária se os dados dos fissurados forem separáveis. Separar diagnóstico PSG, triagem clínica e códigos administrativos. Manter braços de técnica ambígua fora da estimativa específica por técnica, com motivo rastreável. Coortes de resgate não informam risco de ocorrência após a cirurgia original. Não excluir um estudo apenas por ser antigo, por resultado discordante ou por desfazer a conclusão atual.

Não presumir elegibilidade dos candidatos citados no parecer. Conferir texto completo, técnica, população, denominador, PSG, janela e possível duplicação. Verificar especialmente a relação entre as amostras de Liao 2002/2004. Mapear record_id → report_id → study_id → cohort_id → arm_id → timepoint_id. Reconstruir PRISMA a partir dos registros, sem ajustar números para reproduzir o fluxograma anterior.

Proposta de busca: recuperar primeiro exportações e estratégias originais de PubMed, Embase, Scopus, Web of Science e CENTRAL. Se uma base não foi efetivamente consultada, corrigir o relato. Atualização deve ter data de execução, plataforma, estratégia completa, limites e exportação por base. Busca de auditoria e consultas pontuais anteriores não contam como nova busca sistemática.

## Extração e adjudicação

Usar o esquema compartilhado `esquema_extracao.csv`. Registrar idade na cirurgia separadamente da idade na PSG, tipo de IAH/oIAH/IDR, limiar original, critérios de gravidade, acompanhamento e perdas. Não converter limiares diferentes em um critério único sem dados individuais suficientes. Extrair números absolutos; não reconstruir eventos por arredondamento de percentuais sem confirmação.

Cada decisão final terá avaliador, data, fonte e localização. A conferência exige duas avaliações independentes e resolução de discordâncias documentada. Uma primeira extração automatizada ou duas leituras do mesmo assistente não serão apresentadas como dois revisores humanos independentes. Trechos devem ser mínimos e vinculados à página/tabela original.

## Decisão de síntese

1. Não estabelecer antecipadamente que NMA ou metanálise de proporções é obrigatória. A ausência absoluta de ensaios randomizados foi uma alegação incorreta; sua existência também não basta para formar rede válida.
2. Antes de combinar, avaliar compatibilidade clínica, definições, horizonte, seleção para PSG e independência das coortes. Distinguir número de estudos de número de braços e subgrupos etários.
3. Com um estudo por técnica, apresentar a estimativa daquele estudo. Não estimar heterogeneidade entre estudos por meio dos seus subgrupos etários nem usar Q entre técnicas como prova de superioridade.
4. Se houver estudos independentes e compatíveis, justificar modelo e intervalos antes de executar a síntese reparada. Documentar métodos distintos para proporção de estudo, braço único e síntese. Wilson é intervalo de escore; Clopper-Pearson é intervalo exato. Não misturar seus rótulos.
5. Se compatibilidade ou independência forem insuficientes, manter síntese descritiva estruturada. Se existirem comparações adequadas, avaliar síntese comparativa separada; só considerar NMA após demonstrar conectividade e plausibilidade de transitividade.
6. Definir regra para tempos repetidos e amostras sobrepostas antes da nova análise. Apresentar tempos por estudo; não impor a janela uniforme de 6 a 12 meses aos dados existentes.

## Viés, certeza e automação

Selecionar a ferramenta pelo estimando e desenho: não aplicar automaticamente ROBINS-I a toda proporção nem classificar estudo excluído como risco crítico por estar fora do PICO. Registrar perguntas/domínios, justificativas e locadores. Confirmar a ferramenta adequada para evidência de frequência antes de fechar os julgamentos.

Definir abordagem e nível inicial da certeza, justificar cada decisão e separar claims, screening e PSG misto. Não tratar “viés de publicação não detectado” como ausência demonstrada. Não repetir rótulos GRADE anteriores como avaliados de novo.

Todos os gráficos e tabelas devem derivar dos resultados e julgamentos versionados; remover valores científicos fixos nos scripts de figura. Capturar ambiente, dependências, entradas, hashes, comandos, falhas e saídas. Manter a execução anterior como histórico; não sobrescrever evidência ou código original silenciosamente.

## Texto, entregas e encerramento

O arquivo pareado `substituicoes_textuais.md` contém propostas de correção imediata baseadas no parecer, sem transformar métodos propostos em métodos realizados. Não afirmar busca nas cinco bases até conferir; não manter multiplicador de subdetecção, ranking causal, algoritmo mandatório ou declaração de IA padronizada sem histórico verificado.

Entregas finais esperadas: protocolo/emenda reconciliados; busca e seleção auditáveis; extração e decisões verificadas; análises justificadas ou síntese descritiva; RoB e certeza documentados; fonte canônica PT/EN; tabelas/figuras computadas; DOCX gerados dessa fonte; referências e declarações verificadas; Evidence Lock e revisão final contra hashes finais.

Limites atuais: registro externo, protocolo submetido, revisão humana independente, exportações originais e textos completos candidatos não estão certificados por este pacote. Não há novo resultado clínico. Não há autorização de submissão externa.
