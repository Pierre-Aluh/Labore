# LABORE PORTAL
## Sistema de Gestão Documental e Atendimento Contábil
### VERSAO 1.0

> Status: especificação documental em revisão. Nenhuma implementação funcional está autorizada nesta etapa.

## 1. Objetivo
Definir a especificação técnica oficial do Labore Portal para orientar construção, operação e evolução do produto sem ambiguidades arquiteturais.

Objetivos centrais:
- Digitalizar o fluxo documental entre escritório contábil e clientes.
- Reduzir dispersão de atendimento (WhatsApp/e-mail/telefone) via chamados e chat interno.
- Garantir rastreabilidade, segurança e segregação de dados por empresa.
- Manter documentos como arquivos comuns no disco do servidor, sem dependência de formato proprietário.

Escopo desta versão:
- Aplicativo desktop único com interface por permissões.
- API FastAPI com autenticação, autorização, auditoria e operações de arquivos.
- PostgreSQL para metadados e regras de negócio.
- Publicação externa via Cloudflare Tunnel.

Fora do escopo desta versão:
- MFA obrigatório.
- Aplicativos móveis nativos.
- Armazenamento de binários de documentos no banco.

## 2. Arquitetura
Arquitetura mandatória:
- Desktop: Tauri 2 + React + TypeScript.
- Backend: FastAPI (Python).
- Banco: PostgreSQL.
- Orquestração no servidor: Docker Compose.
- Exposição externa: Cloudflare Tunnel.
- Arquivos: sistema de arquivos físico local do servidor.

Fluxo macro:
1. Usuário abre o app desktop e autentica.
2. App comunica por HTTPS com domínio publicado via Cloudflare.
3. Cloudflare encaminha ao Tunnel ativo no servidor local do escritório.
4. API processa regras, persiste metadados no PostgreSQL e lê/escreve arquivos em storage físico.

Diretrizes técnicas:
- Não expor porta de entrada pública no servidor local.
- Toda operação remota de arquivo ocorre exclusivamente pela API.
- Separar claramente camada de domínio, aplicação, infraestrutura e interface.

## 3. Usuários
Perfis funcionais iniciais:
- Cliente.
- Colaborador do escritório.
- Administrador.

Modelo de identidade:
- Usuário pode estar associado a uma ou mais empresas.
- Colaborador pode atuar em um ou mais departamentos.
- Administrador tem privilégios de gestão, sem isenção de auditoria.

## 4. Permissões
Modelo obrigatório: RBAC.

Papéis iniciais sugeridos:
- Administrador, Contador, Fiscal, Departamento Pessoal, Atendimento, Cliente.

Ações mínimas por recurso:
- Visualizar.
- Enviar/Criar.
- Baixar.
- Alterar.
- Excluir (com retenção e auditoria).

Restrições:
- Menor privilégio por padrão.
- Isolamento rigoroso por empresa.
- Permissões avaliadas em toda requisição HTTP e em toda ação de WebSocket.

## 5. Empresas
Conceitos:
- Empresa é o eixo de segregação de dados e permissões.
- Usuários clientes acessam apenas empresas vinculadas.
- Competência (mes/ano) organiza recepção e entrega documental.

Requisitos:
- Cadastro de empresas com identificador interno estável.
- Vínculo usuário-empresa via tabela dedicada.
- Busca por empresa com filtros por status e departamento responsável.

## 6. Documentos
Princípios:
- Documento binário nunca é salvo no PostgreSQL.
- Banco armazena apenas metadados e trilha de auditoria.

Categorias iniciais:
- Movimentação contábil.
- Extratos.
- Investimentos.
- Documentos da contabilidade (Fiscal/Contábil/DP e extensível).

Metadados mínimos:
- ID do documento.
- Empresa.
- Competência.
- Categoria/subcategoria/tipo.
- Nome original e nome normalizado.
- Caminho controlado (logical path).
- Hash de integridade.
- Tamanho, MIME inferido, extensão.
- Usuário remetente.
- Timestamps e estado.

Formatos inicialmente considerados:
- PDF, XML, XLSX, XLS, CSV, OFX, TXT, JPG, JPEG, PNG, ZIP.

## 7. Movimentações
Movimentação contábil é entidade própria.

Campos mínimos:
- Empresa.
- Competência.
- Observação opcional.
- Estado conceitual (pendente, incompleta, recebida); transições e semântica final permanecem pendentes.

Arquivos obrigatórios por movimentação:
- DOCUMENTO.
- COBRANCA/MEIO DE PAGAMENTO.
- COMPROVANTE.

Regras:
- Não concluir envio completo se faltar item obrigatório.
- Interface deve indicar explicitamente itens ausentes.
- Alterações de estado devem ser auditadas.

## 8. Extratos
Modelagem:
- Extrato vinculado a empresa, competência e conta bancária (quando cadastrada).
- Investimentos/rendimentos tratados como classe rastreável de documentos esperados.

Objetivo operacional:
- Identificar rapidamente o que foi recebido e o que está pendente por conta e competência.

## 9. Competências
Conceito central:
- Competência representa mes/ano de referência contábil.

Funções:
- Organizar documentos e pendências por empresa.
- Consolidar status geral da competência.
- Permitir visão de completude para triagem do escritório.

Status previstos (a validar regra final):
- Completa.
- Incompleta.
- Em análise.

## 10. Chamados
Capacidades:
- Abertura de chamado por cliente com assunto, descrição e departamento opcional/obrigatório conforme política.
- Participação de um ou mais colaboradores.
- Encerramento por cliente ou colaborador autorizado.
- Reabertura sob critérios definidos.

Dados mínimos:
- Protocolo/ID.
- Empresa.
- Solicitante.
- Departamento.
- Estado.
- Datas de abertura/última interação/encerramento.

## 11. Chat
Requisito técnico:
- Mensageria em tempo real por WebSockets autenticados.

Regras:
- Mensagens associadas a chamado.
- Participação controlada por permissão.
- Registro persistente obrigatório no servidor.
- Anexos em chat passam pelo mesmo pipeline seguro de upload.

Exportação:
- Exportação TXT/PDF prevista.
- Política de exportação automática x manual permanece pendente.

## 12. Notificações
Canal inicial:
- Notificação interna no aplicativo desktop.

Eventos mínimos:
- Resposta em chamado.
- Novo documento entregue.
- Aviso de documentação incompleta.
- Alterações relevantes de status.

Diretriz:
- Mecanismo desenhado para futura extensão a e-mail sem comprometer arquitetura atual.

## 13. Auditoria
Obrigatória desde a primeira versão.

Eventos mínimos auditáveis:
- Arquivos: upload, download, visualização, alteração, movimentação, exclusão, restauração.
- Acesso: login, logout, falhas, bloqueios, revogações.
- Administração: criação/edição/desativação de usuários, empresas, papéis e permissões.
- Atendimento: abertura, resposta, atribuição, encerramento e reabertura de chamados.

Campos mínimos de log:
- Usuário.
- Data/hora UTC.
- Ação.
- Entidade alvo.
- Empresa contexto.
- Resultado (sucesso/falha) e motivo.

## 14. Armazenamento
Estratégia:
- Armazenamento físico em diretórios do servidor.
- Organização por identificadores internos estáveis de empresa, ano, competência, categoria e entidade. Nomes de empresa não devem ser a única chave física.

Requisitos:
- Nomenclatura normalizada e previsível.
- Prevenção de path traversal.
- Separação entre path físico e path lógico persistido em metadados.
- Lixeira com retenção antes de remoção definitiva.

## 15. Backup
Escopo do backup:
- Banco PostgreSQL (backup consistente).
- Storage de documentos.
- Configurações essenciais não secretas (Compose, exemplos de variáveis, scripts operacionais). Segredos devem ser protegidos e tratados conforme procedimento separado.

Política mínima:
- Backup local em mídia separada.
- Backup externo criptografado.
- Retenção definida por janela temporal.
- Testes periódicos de restauração.

Requisito de portabilidade:
- Procedimento claro para migração de servidor por restauração, sem copiar arquivos de banco em uso.

## 16. Segurança
Controles obrigatórios:
- Senha com hash forte (Argon2id ou equivalente aprovado).
- Sessão com expiração e revogação.
- Limite de tentativas e bloqueio temporário.
- Autorização por RBAC em todas as operações.
- HTTPS no acesso externo.
- Validação de tipo/tamanho de upload e sanitização de nome.
- Proibição de logs com dados sensíveis.

Requisito LGPD:
- Tratar dados pessoais sob princípios de minimização e necessidade.
- Requisitos legais específicos permanecem pendentes para validação jurídica.

## 17. API
Princípios:
- API versionada (prefixo /api/v1).
- Contratos explícitos de request/response.
- Erros padronizados com códigos e mensagens compreensíveis.

Capacidades por domínio:
- Auth e sessão.
- Empresas e vínculos.
- RBAC e departamentos.
- Documentos/movimentações/extratos.
- Chamados/chat/notificações.
- Auditoria e administração.

Regras:
- Toda operação de arquivo exige autenticação, autorização, validação e auditoria.
- Download via endpoint autorizado e auditado; nunca por acesso direto a disco.

## 18. Banco de dados
Tecnologia:
- PostgreSQL para dados estruturados e metadados.

Entidades conceituais iniciais:
- users, companies, company_users.
- roles, permissions, role_permissions.
- departments.
- competencies, competency_requirements.
- bank_accounts.
- documents, document_categories.
- accounting_movements, movement_documents.
- tickets, ticket_participants, ticket_messages, ticket_attachments.
- notifications, audit_logs, sessions.

Governança:
- Toda mudança por migration revisada, testada e versionada.
- Proibido armazenar conteúdo binário de documentos no banco.

## 19. Desktop
Tecnologia:
- Tauri 2 + React + TypeScript em base única de aplicativo.

Princípios de UX:
- Fluxo orientado a tarefa (não à árvore física de disco).
- Interface por papel e permissões no pós-login.
- Baixo consumo de recursos para máquinas modestas.
- Mensagens claras em falhas de rede/servidor.

## 20. Servidor
Contexto operacional:
- Máquina dedicada no escritório com Docker Compose.

Estrutura operacional sugerida:
- app, config, database, storage/clientes, backup, logs, compose.yml, scripts de iniciar/parar/backup/restaurar.

Disponibilidade:
- Dependência de energia e internet local exige nobreak e monitoramento básico.
- O Tunnel deve ser considerado parte da operação do servidor, mas a forma final de execução (container ou serviço do sistema) permanece pendente.

## 21. Instalação
Diretrizes:
- Processo de instalação simples para escritório e clientes.
- Configuração externalizada (variáveis e arquivos de ambiente).
- Guia de instalação com checklist de pré-requisitos.

Pontos a detalhar na fase de implantação:
- Certificados/domínio Cloudflare.
- Provisionamento inicial de administrador.
- Rotina inicial de backup e validação.

## 22. Atualização
Princípios:
- Atualizações controladas por versão.
- Compatibilidade entre versão do desktop e API por política definida.
- Rollback planejado para servidor e cliente.

Pendente:
- Estratégia final de atualização do app Tauri (canal, assinatura, cadência).

## 23. Testes
Estratégia mínima por camada:
- Backend: testes unitários, integração e autorização.
- Desktop: testes de interface por fluxo crítico.
- Segurança: testes de autorização e upload seguro.
- Operação: testes de backup/restore e migração.

Critérios:
- Toda alteração funcional deve acompanhar testes apropriados.
- Mudanças de schema exigem migration + validação automatizada.

## 24. Roadmap
Fases propostas:
1. Fundação do projeto.
2. Banco de dados e migrations.
3. Autenticação e sessões.
4. Gestão de empresas, usuários, papéis e permissões.
5. Documentos e armazenamento físico controlado.
6. Movimentação contábil.
7. Extratos bancários e investimentos.
8. Chamados.
9. Chat em tempo real.
10. Interfaces e painel administrativo.
11. Backups e recuperação.
12. Instalador e atualização desktop.
13. Testes, segurança e homologação.
14. Implantação.

## Governança das Decisões
As decisões pendentes estão classificadas, com recomendações e impactos, em [docs/DECISOES_PENDENTES.md](docs/DECISOES_PENDENTES.md). Esse documento é a referência única para pendências; os documentos de domínio devem apenas resumir as decisões relevantes.
