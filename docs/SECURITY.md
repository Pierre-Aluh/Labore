# SECURITY

## 1. Objetivo
Estabelecer baseline de segurança da informação para o Labore Portal.

## 2. Controles de Identidade e Acesso
- Login por usuário/e-mail e senha.
- Hash de senha forte (Argon2id recomendado).
- Bloqueio temporário por tentativas falhas sucessivas.
- Sessões com expiração, renovação e revogação.
- RBAC obrigatório em API e WebSocket.

## 3. Isolamento de Dados
- Isolamento estrito por empresa em todas as consultas.
- Proibição de acesso cruzado por falha de filtro de tenant.
- Revisões de autorização em endpoints críticos.

## 4. Segurança de Upload e Download
- Upload apenas por endpoint autenticado/autorizado.
- Sanitização de nome de arquivo.
- Bloqueio de path traversal.
- Validação de tipo, extensão e tamanho.
- Cálculo de hash de integridade.
- Download somente por endpoint autorizado e auditado.
- Arquivo recebido deve poder permanecer em quarentena até validação antivírus, conforme política a aprovar.

## 5. Proteção de Segredos
- Segredos fora do código-fonte.
- Uso de variáveis de ambiente e arquivos protegidos.
- Nunca registrar senha, token ou conteúdo sensível em logs.

## 6. Comunicação Segura
- HTTPS obrigatório no acesso externo.
- Publicação via Cloudflare Tunnel, sem porta de entrada pública.

## 7. Auditoria de Segurança
Eventos mínimos:
- login/logout/falha/bloqueio.
- criação/revogação de sessão.
- eventos administrativos sensíveis.
- ações de arquivo e atendimento.
- acesso administrativo à própria trilha de auditoria.

## 8. Privacidade e LGPD
- Usar somente dados fictícios em desenvolvimento/testes.
- Coleta mínima necessária de dados pessoais.
- Requisitos legais específicos devem ser validados com responsável jurídico.

## 9. Requisitos Não Inclusos na V1
- MFA não será implementado nesta versão.

## 10. Decisões Pendentes
- Política formal de antivírus para upload, classificada em docs/DECISOES_PENDENTES.md.
- Regras de retenção legal e descarte seguro.
- Matriz de classificação de dados e níveis de acesso.

## 11. Implementação da Fase 03

- Senhas usam Argon2id via `argon2-cffi`.
- Sessões usam tokens opacos aleatórios; somente o hash SHA-256 é persistido.
- Sessões expiram, podem ser revogadas e são rejeitadas após expiração.
- Cinco falhas consecutivas geram bloqueio temporário de 15 minutos.
- Login bem-sucedido, falho e logout geram eventos de auditoria sem senha ou token.
- Não foi criado usuário padrão e MFA permanece fora da versão atual.

## 12. Implementação da Fase 04

- Autorização centralizada por recurso e ação.
- Permissões são negadas quando não há vínculo explícito entre usuário, papel e permissão.
- Rotas administrativas não possuem bypass por nome de perfil.
- Criação de usuário exige senha mínima de 12 caracteres e armazena somente hash Argon2id.
- Consultas administrativas devem continuar recebendo filtros de empresa nas fases de domínio.

## 13. Implementação da Fase 05

- Upload valida extensão, sanitiza nome, limita tamanho e usa quarentena.
- Download verifica sessão, permissão, vínculo com empresa e estado disponível.
- Falhas de persistência removem o arquivo físico criado e fazem rollback dos metadados.
- Não há antivírus integrado nesta fase; a aprovação é deliberadamente separada e a política continua pendente.

## 14. Implementação da Fase 08

- Participantes só podem ser associados se estiverem vinculados à mesma empresa.
- Fechamento, reabertura, atribuição e abertura geram auditoria.
- O chamado não permite acesso por ID sem validação de vínculo empresarial.

## 15. Implementação da Fase 09

- WebSocket valida token opaco, revogação, expiração e participação no chamado.
- Mensagens HTTP e WebSocket geram auditoria sem conteúdo sensível em metadata.
- Notificações são criadas apenas para participantes do chamado, excluindo o autor.
- Exportação automática para máquinas clientes não foi criada; exportação manual permanece futura.

## 16. CORS local

- CORS não é aberto globalmente.
- As origens locais permitidas são explícitas e limitadas às portas do Vite de homologação.
- Origens de produção deverão ser configuradas separadamente, sem usar curingas.
