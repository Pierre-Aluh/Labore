# DECISÕES AUTÔNOMAS

Registro de decisões técnicas tomadas durante a execução autorizada das fases. Cada entrada deve conter escopo, justificativa, impacto e possibilidade de revisão.

## 2026-09-05

### A001 - Virtualenv local para o backend
- Escopo: Fase 02 e fases backend.
- Decisão: usar `services/api/.venv`, sem dependências globais.
- Justificativa: isolamento entre ambientes e reprodutibilidade no Windows.
- Impacto: custo baixo; segurança melhor por reduzir interferência global; manutenção simples.
- Revisão: pode ser substituído por ambiente CI/containerizado sem alterar a arquitetura.

### A002 - SQLAlchemy 2 + Alembic
- Escopo: Fase 02.
- Decisão: usar SQLAlchemy 2 para modelagem e Alembic para migrations PostgreSQL.
- Justificativa: suporte atual, migrations explícitas e compatibilidade com FastAPI.
- Impacto: custo baixo/médio; segurança favorecida por queries parametrizadas; manutenção alta por schema versionado.
- Revisão: possível sem alterar PostgreSQL ou a API pública.

### A003 - Schema inicial abrangente sem seed
- Escopo: Fase 02.
- Decisão: criar em uma migration as tabelas conceituais necessárias às fases autorizadas, sem inserir usuários, papéis ou dados de negócio.
- Justificativa: mantém o schema versionado e permite que as fases seguintes adicionem comportamento sem recriar fundação; evita dados iniciais não aprovados.
- Impacto: custo baixo/médio; segurança favorecida pela ausência de contas padrão; manutenção simples por uma origem de schema rastreável.
- Revisão: novas alterações devem usar migrations posteriores, nunca editar a migration aplicada.

### A004 - Sessão opaca revogável
- Escopo: Fase 03.
- Decisão: emitir token aleatório ao cliente e persistir apenas seu SHA-256, com expiração de 12 horas e revogação server-side.
- Justificativa: permite revogação imediata e reduz exposição de dados no token; é compatível com desktop e WebSocket futuro.
- Impacto: custo baixo/médio; segurança alta; manutenção simples por usar a tabela `sessions` já prevista.
- Revisão: duração e mecanismo de transporte podem mudar sem alterar o modelo de identidade.

### A005 - RBAC por recurso e ação
- Escopo: Fase 04.
- Decisão: autorizar por pares `resource/action`, com vínculos explícitos de usuário-papel e empresa-usuário; negar por padrão.
- Justificativa: evita autorização baseada apenas em rótulo e permite menor privilégio por departamento.
- Impacto: custo médio; segurança alta; manutenção alta por centralizar a regra.
- Revisão: novos recursos entram por migration e testes de acesso positivo/negativo.

### A006 - Quarentena antes da disponibilidade
- Escopo: Fase 05.
- Decisão: todo upload começa como `quarantined`; download exige aprovação explícita.
- Justificativa: não disponibilizar arquivos antes de uma futura política de antivírus/quarentena.
- Impacto: custo baixo agora; segurança alta; manutenção média por exigir etapa operacional.
- Revisão: pode ser conectado a scanner futuro sem alterar o contrato de documento.

### A007 - Completude derivada da movimentação
- Escopo: Fase 06.
- Decisão: o status da movimentação é derivado dos tipos associados; `received` exige exatamente os três tipos obrigatórios.
- Justificativa: impede que o status seja alterado manualmente para esconder pendências.
- Impacto: custo baixo; segurança e integridade operacional altas; manutenção simples por regra centralizada.
- Revisão: novos tipos exigem migration e atualização explícita da regra.