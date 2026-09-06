# Roteiro de implantação

## Homologação local

1. Confirmar Windows suportado, Python 3.12, Node, Cargo, Docker Desktop e MSVC.
2. Copiar `config/.env.example` para um arquivo local não rastreado.
3. Iniciar PostgreSQL pelo Compose com perfil `local-infra`.
4. Aplicar migrations com `services/api/.venv/Scripts/python.exe -m alembic upgrade head` dentro de `services/api`.
5. Iniciar API com `services/api/.venv/Scripts/python.exe -m uvicorn app.main:app --reload` dentro de `services/api`.
6. Validar `/health` e `/api/v1/meta/compatibility`.
7. Executar frontend com `npm.cmd run dev`.
8. Usar somente fixtures sintéticas e validar RBAC, documentos, chamados, chat e backup.

### Resultado da homologação em 2026-09-06

- PostgreSQL Compose: saudável e aceitando conexões na porta local 5432.
- Alembic: aplicado até `0006_ticket_permissions`.
- API: `/health` retornou 200; compatibilidade `0.1.0` retornou 200; rota protegida sem sessão retornou 401.
- Frontend: Vite respondeu 200 e serviu o entrypoint React.
- RBAC: cliente recebeu 403 em rota administrativa; administrador recebeu 200.
- Documentos: upload 201 em quarentena, download antes da aprovação 404, aprovação 200 e download posterior 200.
- Chamados/chat: criação 201, participante 204, mensagem 201 e WebSocket entregando evento `message`.
- Notificações: administrador recebeu uma notificação sintética.
- Backup: dump local criado com sucesso; simulação de restore concluída sem ação destrutiva.
- Dados usados: somente usuários `example.invalid`, empresa `SYNTH-*` e arquivo sintético.

Os processos da API e do frontend permanecem ativos para inspeção local. O backup gerado está em diretório ignorado pelo Git.

## Produção futura

1. Aprovar LGPD, retenção, SLA, RPO/RTO e responsáveis.
2. Provisionar servidor dedicado, volumes, nobreak e monitoramento.
3. Configurar segredos em cofre/procedimento separado.
4. Configurar domínio e Cloudflare Tunnel sem porta de entrada.
5. Fazer backup inicial e teste de restauração.
6. Aplicar migrations revisadas em janela controlada.
7. Distribuir instalador Tauri assinado por canal aprovado.
8. Fazer homologação final com dados autorizados e somente então solicitar autorização expressa de publicação.

Este roteiro não executa nenhuma ação externa automaticamente.
