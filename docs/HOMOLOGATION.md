# Preparação para homologação

## Ambiente

- Windows suportado.
- Desenvolvimento, homologação e produção separados.
- Docker Desktop com daemon Linux operacional.
- Python 3.12, Node.js, Rust/Cargo e Visual Studio Build Tools.

## Dados

Usar exclusivamente `services/api/tests/fixtures/synthetic_data.json` ou dados equivalentes fictícios. Não copiar documentos reais.

## Checklist técnico

1. Aplicar migrations em banco de homologação vazio.
2. Criar dados sintéticos e nenhum usuário real.
3. Validar healthcheck e compatibilidade.
4. Executar testes backend e frontend.
5. Validar isolamento por empresa com acessos positivos e negativos.
6. Testar upload em quarentena, aprovação, download, lixeira e auditoria.
7. Testar chamados, notificações e WebSocket.
8. Testar backup/restore em ambiente isolado.
9. Registrar falhas e evidências.

A publicação em produção exige autorização expressa e não faz parte deste ciclo.
