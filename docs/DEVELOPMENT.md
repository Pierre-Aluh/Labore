# DEVELOPMENT

## 1. Objetivo
Definir normas de desenvolvimento para execução incremental e segura do projeto.

## 2. Fluxo de Trabalho Obrigatório
- Planejar.
- Implementar unidade pequena.
- Testar.
- Revisar.
- Commit.
- Seguir para próxima unidade.

Durante a etapa documental atual, o fluxo termina na revisão e aprovação da documentação; nenhuma implementação deve começar sem autorização explícita.

## 3. Regras de Escopo
- Não alterar arquitetura sem aprovação explícita.
- Não implementar funcionalidades fora da unidade aprovada.
- Não instalar dependências sem justificativa técnica.

## 4. Regras de Banco
- Nenhuma alteração sem migration.
- Migration revisada e testada.
- Evitar alterações destrutivas sem plano de rollback.

## 5. Regras de Arquivos
- Nunca armazenar binários no PostgreSQL.
- Nunca permitir acesso direto de cliente ao filesystem.
- Toda ação de arquivo exige autenticação, autorização, validação e auditoria.

## 6. Regras de Segurança
- Não registrar segredos em logs/código/testes.
- Usar apenas dados fictícios em dev/teste.
- Seguir menor privilégio em todas as features.

## 7. Regras de Qualidade
- Testes apropriados por mudança.
- Cobertura de fluxos críticos de segurança.
- Revisão de risco de regressão por módulo.

## 8. Git e Versionamento
- Commits pequenos e descritivos.
- Não reescrever histórico compartilhado sem aprovação.
- Não desfazer trabalho do usuário sem autorização.

## 9. Critérios de Pronto por Unidade
- Requisito implementado conforme especificação.
- Testes passando.
- Auditoria e permissões validadas.
- Documentação atualizada.

Para documentação, o critério de pronto inclui matriz de cobertura dos capítulos aplicáveis e registro das pendências em docs/DECISOES_PENDENTES.md.

## 10. Decisões Pendentes
- Política formal de branching.
- Política de versionamento semântico para backend e desktop.
- Matriz de aprovação por tipo de mudança.
- Convenção final de branches e revisão não devem bloquear a documentação; devem ser fechadas antes do primeiro ciclo de código compartilhado.

## 11. Estado da Fase 01

- Dependências de runtime não foram instaladas nesta fundação.
- O ambiente verificado não possui Python, Docker ou Cargo acessíveis; npm está bloqueado pela política de execução do PowerShell.
- Git e Node estão disponíveis e foram usados apenas para validações locais.
- A validação do Compose e a execução de testes ficam pendentes até as ferramentas correspondentes estarem disponíveis.
- Nenhum dado real, segredo ou credencial de produção pode entrar no repositório.

## 12. Estado da Execução Contínua

- Fase 02 concluída com 3 testes aprovados e compilação Python aprovada.
- O schema foi validado por metadata e migration, mas ainda não foi aplicado a um PostgreSQL porque o daemon Docker não foi usado nesta unidade.
- A Fase 03 poderá iniciar sobre esta base, mantendo migrations versionadas.

## 13. Validação de Integração Pendente

- Os testes de autenticação executados nesta fase são unitários e de contrato HTTP.
- O fluxo completo contra PostgreSQL deve ser executado quando o serviço local estiver operacional, usando somente dados sintéticos.

## 14. Fase 10 Desktop

- Dependências frontend: React, Vite, TypeScript, Tauri API/CLI e Vitest.
- Validações concluídas: `npm.cmd run typecheck`, `npm.cmd run test` e `npm.cmd run build`.
- Validação pendente: `cargo check` requer linker MSVC disponível.

## 15. Fase 11 Operação

- Scripts PowerShell são validados por parser e testes de contrato.
- Não executar restore real em desenvolvimento sem pacote sintético e confirmação operacional.

## 16. Fase 13 Homologação

- Suíte backend: 37 testes aprovados.
- Frontend: typecheck, Vitest e build aprovados.
- Alembic: geração offline da cadeia até `head` aprovada.
- Fixture sintética em `services/api/tests/fixtures/synthetic_data.json`.
- Aplicação real das migrations aguarda PostgreSQL/Docker operacional.

## 17. Homologação local executada

- PostgreSQL, API e Vite foram executados localmente em 2026-09-06.
- Fluxos sintéticos de RBAC, documentos, chamados, mensagens, notificações e WebSocket foram exercitados.
- Backup e simulação de restore foram executados; restore destrutivo não foi executado.
- `config/.env.local`, `backup/` e dados sintéticos locais permanecem fora do Git.

## 18. Correção de painéis por perfil

- O login agora consulta `/api/v1/auth/me` para obter papéis e empresas.
- Cliente possui views consumindo documentos, upload, chamados, mensagens e notificações.
- Colaborador possui API `/workspace` para empresas, documentos, chamados e resumo operacional.
- Administrador possui consultas de empresas, usuários, papéis e auditoria.
- Typecheck, build e suíte backend continuam aprovados após a alteração.

## 19. Tela inicial do cliente

- A tela inicial pós-login do cliente usa a referência visual fornecida em `public/assets/client-home-reference.png`.
- A logo exibida usa `public/assets/labore-logo.png`.
- Suporte, documentos, envio, financeiro e notificações permanecem atalhos funcionais para as views/API correspondentes.
