# Prontidão para produção

## Bloqueios atuais

- Docker/WSL2 e PostgreSQL precisam ser validados operacionalmente.
- Cargo/Tauri precisa de Visual Studio Build Tools/MSVC.
- Instalador e atualização precisam de assinatura e rollback homologados.
- Scanner antivírus e política de quarentena precisam de decisão operacional.
- RPO/RTO, backup externo e custódia de segredos precisam de aprovação.
- LGPD, retenção legal, consentimentos e SLA precisam de validação responsável.
- Cloudflare Tunnel real, domínio e certificados não foram configurados.

## Critérios mínimos antes de publicação

- Migrations aplicadas e rollback ensaiado em homologação.
- Testes positivos e negativos de isolamento por empresa.
- Backup e restore testados com evidência.
- Auditoria revisada e protegida contra alteração indevida.
- Upload/download e lixeira testados.
- WebSocket e revogação de sessão testados.
- Desktop compilado, assinado e compatível com a API.
- Plano de suporte e recuperação aprovado.
- Autorização expressa do usuário para produção.
