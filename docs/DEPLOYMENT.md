# DEPLOYMENT

## 1. Objetivo
Definir modelo de implantação e operação do servidor local do escritório.

## 2. Ambiente Alvo
- Máquina dedicada no escritório.
- Docker Compose para API, banco e serviços auxiliares.
- Storage físico local para documentos.
- Publicação externa via Cloudflare Tunnel.

O banco e o storage devem usar volumes persistentes separados. O Tunnel pode ser executado como serviço do sistema ou container, conforme decisão operacional futura.

## 3. Estrutura Operacional Sugerida
- LABORE_SERVER/app
- LABORE_SERVER/config
- LABORE_SERVER/database
- LABORE_SERVER/storage/clientes
- LABORE_SERVER/backup
- LABORE_SERVER/logs
- LABORE_SERVER/compose.yml
- LABORE_SERVER/iniciar.bat
- LABORE_SERVER/parar.bat
- LABORE_SERVER/backup.bat
- LABORE_SERVER/restaurar.bat

## 4. Princípios de Implantação
- Não expor porta pública diretamente.
- Externalizar configuração sensível.
- Garantir persistência de volumes de banco e storage.
- Registrar versão de deploy e changelog operacional.

## 5. Cloudflare Tunnel
Diretriz:
- Túnel de saída ativo no servidor.
- DNS e domínio gerenciados no Cloudflare.
- Credenciais e configuração fora do repositório.

Pendente:
- Definição da conta, domínio e política operacional de rotação de credenciais.

## 6. Backup e Recuperação
- Backup consistente do PostgreSQL.
- Backup do storage de documentos.
- Cópia para mídia local separada.
- Cópia externa criptografada, sem incluir segredos operacionais em claro.
- Testes de restauração periódicos.

## 7. Migração de Servidor
Fluxo esperado:
1. Executar backup consistente.
2. Copiar pacote para nova máquina.
3. Restaurar banco e storage.
4. Subir serviços.
5. Validar saúde funcional.

## 8. Disponibilidade
Riscos principais:
- Queda de energia.
- Queda de internet.
- Falha de disco.

Mitigações mínimas:
- Nobreak.
- Disco dedicado para backup.
- Monitoramento básico de serviços.

## 9. Decisões Pendentes
- RPO/RTO formais.
- Ferramenta final de monitoramento.
- Frequência oficial de backup e restauração de teste.
- Procedimento de gestão e restauração de segredos de produção.

## 10. Implementação da Fase 11

- `infra/scripts/backup.ps1` cria dump PostgreSQL e arquivo do storage.
- `infra/scripts/restore.ps1` simula por padrão e exige `-ConfirmRestore` para agir.
- Pacotes comuns não incluem segredos.
- O roteiro de recuperação está em `docs/RECOVERY_RUNBOOK.md`.
