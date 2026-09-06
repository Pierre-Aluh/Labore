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