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
