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

## 14. Implementação da Fase 04

- `POST/GET /api/v1/admin/companies`: cadastro e consulta de empresas com permissão.
- `POST /api/v1/admin/users`: criação de usuário, papel e vínculos de empresa com permissão.
- `POST /api/v1/admin/departments`: cadastro de departamento com permissão.
- `GET /api/v1/admin/roles`: consulta do catálogo de papéis com permissão.
- Rotas administrativas retornam 401 sem sessão e 403 sem permissão.

## 15. Implementação da Fase 05

- `POST /api/v1/documents`: upload multipart autenticado e autorizado, sempre em quarentena.
- `GET /api/v1/documents/{document_id}/download`: download somente de documento disponível e acessível à empresa.
- `POST /api/v1/documents/{document_id}/approve`: aprovação explícita e auditada.
- O caminho físico nunca é recebido do cliente e não há endpoint de filesystem.

## 16. Implementação da Fase 06

- `POST /api/v1/movements`: cria movimentação e associa documentos por tipo.
- `GET /api/v1/movements/{movement_id}`: consulta status e itens ausentes.
- `POST /api/v1/movements/{movement_id}/complete`: recusa conclusão com HTTP 409 quando faltar arquivo obrigatório.

## 17. Implementação da Fase 07

- `POST /api/v1/bank-accounts`: cadastra conta com identificador mascarado.
- `GET /api/v1/companies/{company_id}/bank-accounts`: lista contas acessíveis.
- `POST /api/v1/bank-accounts/{account_id}/statements/{document_id}`: associa extrato à conta.
- `POST /api/v1/investment-requirements`: cria requisito de investimento por competência.

## 18. Implementação da Fase 08

- `POST /api/v1/tickets`: abre chamado vinculado à empresa e departamento opcional.
- `GET /api/v1/tickets/companies/{company_id}`: lista chamados acessíveis.
- `POST /api/v1/tickets/{ticket_id}/participants`: atribui participante vinculado à empresa.
- `POST /api/v1/tickets/{ticket_id}/close` e `/reopen`: controlam o ciclo auditado.
- Mensagens e WebSocket são implementados na Fase 09.

## 19. Implementação da Fase 09

- `POST/GET /api/v1/tickets/{ticket_id}/messages`: mensagens persistentes e autorizadas.
- `GET /api/v1/notifications`: notificações internas do usuário.
- `POST /api/v1/notifications/{notification_id}/read`: marca notificação própria como lida.
- `WS /api/v1/ws/tickets/{ticket_id}?token=...`: canal autenticado de tempo real; sessão expirada/revogada é rejeitada.

## 20. Implementação da Fase 12

- `GET /api/v1/meta/compatibility?client_version=...` informa compatibilidade sem expor dados de negócio.
- O endpoint não substitui autorização de recursos.
- O desktop mantém atualização automática desativada até assinatura e rollback serem homologados.
