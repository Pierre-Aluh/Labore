# ARCHITECTURE

## 1. Escopo
Este documento define a arquitetura técnica do Labore Portal e os limites de decisão para implementação.

## 2. Stack Obrigatória
- Desktop: Tauri 2 + React + TypeScript.
- Backend/API: FastAPI + Python.
- Banco de dados: PostgreSQL.
- Orquestração de serviços: Docker Compose.
- Publicação externa: Cloudflare Tunnel.
- Armazenamento de arquivos: filesystem local do servidor.

Cloudflare Tunnel é a camada de publicação externa; não é permitido expor diretamente a API por uma porta de entrada pública.

## 3. Topologia
Fluxo lógico:
1. Aplicativo desktop autentica via HTTPS.
2. Tráfego entra pelo domínio Cloudflare.
3. Cloudflare encaminha para Tunnel com conexão de saída no servidor local.
4. API FastAPI processa regras e integra PostgreSQL + storage físico.

Restrições:
- Não publicar porta de entrada do servidor na internet.
- Não permitir montagem de compartilhamento de rede cliente-servidor como canal de upload/download.

## 4. Componentes
- Desktop App: interface única por papel/permissão.
- API FastAPI/App Layer: autenticação, autorização, validação, orquestração de casos de uso.
- Domínio: regras de documentos, competências, pendências, chamados e auditoria.
- Persistência relacional: metadados e transações de negócio.
- Storage service: escrita/leitura de binários com caminhos controlados.
- Audit service: trilha de eventos protegida contra alteração indevida; imutabilidade técnica e retenção final ainda serão definidas.
- Notification service: eventos internos e push em tempo real.
- Realtime service: WebSocket autenticado para chat/notificações.

## 5. Separação de Responsabilidades
- Desktop não conhece estrutura física real de diretórios.
- API é único ponto autorizado para operações remotas.
- Banco armazena metadados, nunca binários.
- Storage guarda binários, nunca regras de autorização.

## 6. Princípios Arquiteturais
- Segurança por padrão.
- Menor privilégio e isolamento por empresa.
- Observabilidade mínima (logs, auditoria, métricas essenciais).
- Portabilidade operacional (backup e restauração claros).
- Simplicidade operacional para equipe não técnica.

## 7. Modelo de Módulos (Backend)
Sugestão de bounded modules:
- auth
- users
- companies
- rbac
- departments
- competencies
- documents
- accounting_movements
- bank_accounts_and_statements
- tickets
- chat
- notifications
- audit
- sessions

## 8. Modelo de Módulos (Desktop)
Sugestão de domínios de UI:
- autenticação
- dashboard
- documentos
- movimentações
- extratos
- chamados/chat
- notificações
- administração

## 9. Eventos de Domínio Relevantes
- document_uploaded
- document_deleted_soft
- document_restored
- movement_marked_complete
- ticket_created
- ticket_replied
- ticket_closed
- notification_created
- user_locked_temporarily

## 10. Resiliência
- Requisições idempotentes quando aplicável.
- Timeouts e retries com política conservadora.
- Falhas de storage não podem corromper consistência de metadados.
- Estratégia transacional para metadados + escrita de arquivo, incluindo comportamento de falha e reconciliação.

## 11. Decisões Pendentes
- Estratégia final de comunicação assíncrona interna (fila dedicada ou eventos in-process na V1).
- Regras finais de versionamento de API e compatibilidade de cliente.
- Estratégia detalhada de atualização automática do desktop.
