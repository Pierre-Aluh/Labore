# API

## 1. Objetivo
Definir diretrizes de contrato para a API do Labore Portal.

## 2. Princípios de Contrato
- Versionamento por prefixo: /api/v1.
- JSON como formato padrão.
- Respostas e erros consistentes.
- Autenticação e autorização em toda rota protegida.

## 3. Domínios de Endpoints (Planejados)
- auth
- users
- companies
- roles/permissions
- departments
- competencies
- documents
- accounting-movements
- bank-accounts/statements
- tickets
- notifications
- audit
- health/readiness (operacional, sem exposição de segredos).

## 4. Autenticação e Sessão
- Endpoint de login.
- Emissão de sessão/token com validade definida.
- Endpoint de logout/revogação.
- Política de refresh ou renovação controlada (detalhar na implementação).

## 5. Documentos
Operações previstas:
- Upload.
- Download.
- Listagem filtrada por empresa/competência/categoria.
- Soft delete.
- Restauração em janela de retenção.
- Consulta de pendências por empresa e competência.

Regras:
- Sem acesso direto ao filesystem.
- Toda operação com trilha de auditoria.

## 6. Movimentações
Operações previstas:
- Criar movimentação por competência.
- Vincular arquivos por tipo obrigatório.
- Consultar completude e pendências.

## 7. Chamados e Chat
- CRUD de chamados conforme permissão.
- Participantes por departamento/papel.
- Mensagens em tempo real via WebSocket autenticado.
- Histórico persistente no servidor.
- Anexos devem usar referência controlada ao storage e não criar um canal paralelo de arquivos.

## 8. Notificações
- Listar notificações do usuário.
- Marcar lidas.
- Geração automática por eventos de domínio.

## 9. Auditoria
- Endpoints administrativos para consulta de trilha.
- Filtros por período, usuário, empresa, entidade e ação.

## 10. Padrão de Erro
Exemplo conceitual:
- code: identificador estável da falha.
- message: texto amigável.
- details: informações técnicas sem expor segredos.
- correlation_id: rastreio operacional.

## 11. WebSocket
- Handshake autenticado.
- Controle de autorização por canal/chamado.
- Eventos versionados.
- Revogação ou expiração de sessão deve impedir continuidade de conexão autorizada.

## 12. Decisões Pendentes
- Modelo final de token/sessão, classificado em docs/DECISOES_PENDENTES.md.
- Catálogo final de códigos de erro.
- Estratégia de compatibilidade entre versões de cliente e API.
- Contratos finais de paginação, ordenação, filtros e upload multipart.

## 13. Implementação da Fase 03

- `GET /health` é o endpoint operacional não protegido.
- `POST /api/v1/auth/login` recebe credenciais e retorna sessão opaca.
- `POST /api/v1/auth/logout` revoga a sessão Bearer apresentada.
- `GET /api/v1/auth/me` valida a sessão e retorna somente identidade básica.
- Nenhum endpoint de negócio foi criado nesta fase.
