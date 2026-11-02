> Continuação atual, 2026-11-02: o catálogo local tem 268 skills e cinco índices de fontes externas fixadas. O candidato BYOK em D passou em 99 testes offline focados e não foi ativado. Registro final PROSPERO/OSF revisado é obrigatório antes da execução científica. O kit editorial tem 24 DOCX editáveis e seis perfis datados de revistas; não está pronto para submissão. Consulte [o guia atual](portugues/GUIA_DA_MAQUINA.md) e `maquina_canonica.json`; números anteriores abaixo pertencem aos respectivos snapshots.

# Plano de mudanças e backups

Atualização: 2 de novembro de 2026. Destino aprovado: `D:\Usuario-pc\Projetos\Doutorado`. O Windows negou criar `D:\Doutorado`; o usuário aprovou o caminho alternativo e pediu foco na máquina nova, sem arrumar o antigo.

1. Auditoria read-only inicial de configurações por metadados permitidos, skills, projetos, plugins e ferramentas; sem exibir credenciais.
2. Cópia local com manifesto antes e SHA-256: 12.642 arquivos, 1.528.443.834 bytes, zero divergências. C: preservado como backup. Pastas legadas do root ficaram em C:; 12 cópias soltas do root foram isoladas em `acervo_de_referencia/copias_da_raiz_antiga`, com manifesto próprio.
3. Ambiente operacional reconstruído em D: por `uv sync --locked --offline --all-extras --dev` (95 pacotes do lock existente). Ambientes ML, DL e R separados, com locks próprios; Quarto portátil com SHA oficial conferido. Nenhuma configuração global ou credencial foi alterada.
4. Atualização seletiva de 40 arquivos em três skills K-Dense, pin SHA `5f2bc0341354fd5590aef76a533ada1e1e5b4e62`, com backup e licenças por skill. Três skills locais novas registradas com gatilhos PT/EN. Perfis de português natural e Evidence Lock preservados.
5. Organização daqui em diante por projeto/revista/versão e pares `portugues/ingles`. Código, dados e locks compartilhados entre os pares.

Backups: origem C: intacta quanto aos arquivos existentes; cópias pré-alteração de políticas/skills e respectivos hashes na análise de governança e em `analysis/backup_integracao_skills`. Rollback: abrir C: ou restaurar apenas arquivos listados nos manifestos; não executar limpeza recursiva ou sincronização destrutiva.

Pendências que exigem decisão específica: atualizar o BYOK com três alterações locais; usar chaves/serviços pagos; ativar conexões ou alterar configurações globais; enviar dados humanos; publicar/submeter externamente. O BYOK permanece separado, com intercâmbio local de artefatos aprovados. Não foi feito pull, reset, envio externo nem migração de credenciais.

O relatório completo de Pesquisa Aprofundada estava ausente. CAMERA foi retirado do escopo após esclarecimento do usuário. Os comandos efetivos, falhas corrigidas e limites estão em SETUP_LOG.md.
