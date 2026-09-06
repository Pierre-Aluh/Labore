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
