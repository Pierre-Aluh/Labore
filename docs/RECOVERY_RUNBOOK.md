# Roteiro de recuperação

1. Isolar o servidor e registrar horário/incidente.
2. Identificar o último pacote de backup íntegro.
3. Executar `restore.ps1` sem `-ConfirmRestore` para simular.
4. Confirmar destino, versão e autorização operacional.
5. Executar restauração em ambiente isolado.
6. Validar migration, healthcheck, contagem de metadados e amostra de hashes.
7. Validar permissões, auditoria e notificações.
8. Somente após validação, reabrir acesso ao ambiente.

RPO/RTO finais e responsável operacional continuam pendentes de decisão do escritório.
