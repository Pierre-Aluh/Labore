# DATABASE

## 1. Objetivo
Definir diretrizes de modelagem e governança do PostgreSQL para o Labore Portal.

## 2. Princípios
- PostgreSQL guarda dados estruturados e metadados.
- Binários de documentos não devem ser armazenados no banco.
- Toda alteração de schema passa por migration versionada.
- Integridade referencial obrigatória.

## 3. Entidades Conceituais
- users
- companies
- company_users
- roles
- permissions
- role_permissions
- departments
- competencies
- competency_requirements
- bank_accounts
- document_categories
- documents
- accounting_movements
- movement_documents
- tickets
- ticket_participants
- ticket_messages
- ticket_attachments
- notifications
- audit_logs
- sessions

## 4. Convenções de Modelagem
- Chave primária: UUID ou BIGINT (decisão final pendente).
- Timestamps em UTC.
- Soft delete quando necessário, sem confundir exclusão lógica com purge definitivo.
- Índices por empresa_id, competencia, status e created_at.
- Constraints para coerência de status e relacionamentos obrigatórios.

## 5. Documentos (Metadados)
Campos mínimos previstos:
- id
- company_id
- competency_id
- category_id
- subtype
- original_filename
- normalized_filename
- logical_path
- checksum_hash
- file_size_bytes
- mime_type
- uploaded_by_user_id
- uploaded_at
- status
- deleted_at (quando soft delete)

## 6. Movimentações
- accounting_movements representa a movimentação.
- movement_documents associa tipos obrigatórios: DOCUMENTO, COBRANCA, COMPROVANTE.
- Regra de completude depende da presença dos três tipos.

## 7. Chamados e Chat
- tickets como agregador de atendimento.
- ticket_messages com autoria e timestamp.
- ticket_attachments referencia documentos com autorização equivalente.
- ticket_participants controla visibilidade e atuação.

## 8. Auditoria
audit_logs deve registrar:
- actor_user_id
- action
- target_type
- target_id
- company_id
- outcome
- created_at
- metadata redigida sem dados sensíveis.

## 9. Sessões
sessions deve suportar:
- emissão/revogação.
- expiração.
- invalidação por segurança.
- rastreio mínimo para incidentes.

## 10. Migrations
Política obrigatória:
- Migration pequena e revisável.
- Script reversível quando tecnicamente viável.
- Teste automatizado de apply/rollback em ambiente de homologação.

## 11. Decisões Pendentes
- Estratégia final de IDs (UUID v7 vs BIGINT), classificada em docs/DECISOES_PENDENTES.md.
- Matriz completa de status e transições, classificada em docs/DECISOES_PENDENTES.md.
- Política de particionamento de audit_logs e documentos por volume, a decidir somente após dimensionamento.
- Modelo final de empresa, competência e requisito esperado, incluindo unicidade e período.

## 12. Implementação da Fase 02

- Base declarativa em `services/api/app/models.py`.
- Migration inicial em `services/api/migrations/versions/0001_initial_schema.py`.
- UUIDs PostgreSQL com `pgcrypto` e JSONB para metadados de auditoria.
- Não foram criados dados iniciais, usuários, migrations destrutivas ou binários.
- A migration deve ser aplicada somente em banco local/homologação controlado.

## 13. Implementação da Fase 04

- A migration `0002_seed_rbac` cria papéis, permissões e departamentos iniciais de forma idempotente.
- Não há usuário administrador padrão nem senha inicial.
- Vínculos `company_users` e `user_roles` suportam isolamento por empresa e RBAC.

## 14. Implementação da Fase 06

- `accounting_movements` representa a movimentação, e `movement_documents` associa os arquivos.
- Os tipos obrigatórios são `DOCUMENTO`, `COBRANCA` e `COMPROVANTE`.
- O status `received` só é permitido quando os três tipos estão associados.

## 15. Implementação da Fase 07

- `bank_accounts` guarda somente instituição e identificador mascarado.
- `documents.bank_account_id` vincula extratos à conta sem armazenar credenciais bancárias.
- `competency_requirements` representa investimentos esperados por competência.
