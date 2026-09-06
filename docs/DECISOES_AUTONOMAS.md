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

### A008 - Nenhuma credencial bancária
- Escopo: Fase 07.
- Decisão: armazenar apenas instituição e identificador mascarado; extratos são arquivos enviados pelo usuário.
- Justificativa: o escopo não autoriza integração bancária externa e não há necessidade de custodiar credenciais.
- Impacto: custo baixo; segurança alta; manutenção simples e reversível.
- Revisão: integração futura exigirá nova análise de segurança e consentimento explícito.

### A009 - Ciclo inicial de chamados
- Escopo: Fase 08.
- Decisão: permitir `open`, `closed` e `reopened`, preservando os estados de espera para a camada de mensagens da Fase 09.
- Justificativa: entregar o núcleo de atendimento sem inventar SLA não aprovado.
- Impacto: custo baixo; segurança média/alta pela auditoria; manutenção simples e extensível.
- Revisão: SLA e transições finais devem ser fechados antes da homologação.

### A010 - Notificação interna persistente
- Escopo: Fase 09.
- Decisão: persistir notificações no PostgreSQL e usar WebSocket somente como entrega em tempo real, sem depender dele para histórico.
- Justificativa: garante recuperação após indisponibilidade de rede e permite futura entrega por e-mail.
- Impacto: custo baixo/médio; segurança média/alta; manutenção alta por separar persistência e transporte.
- Revisão: canais externos ficam fora da V1.

### A011 - Interface única por papel
- Escopo: Fase 10.
- Decisão: manter um shell desktop único e derivar navegação pelo papel retornado após autenticação.
- Justificativa: atende a arquitetura aprovada e evita produtos separados por perfil.
- Impacto: custo médio; segurança depende da API como autoridade; manutenção alta por compartilhar componentes.
- Revisão: novas áreas devem respeitar permissões server-side.

### A012 - Restore explicitamente confirmado
- Escopo: Fase 11.
- Decisão: o script de restauração sempre inicia em simulação e exige `-ConfirmRestore` + `ShouldProcess`.
- Justificativa: reduz risco de substituir banco/storage por engano.
- Impacto: custo baixo; segurança operacional alta; manutenção simples.
- Revisão: qualquer automação futura deve preservar confirmação e logs.

### A013 - Compatibilidade por contrato simples
- Escopo: Fase 12.
- Decisão: expor versão da API, faixa do desktop e booleano de compatibilidade em endpoint público de metadata.
- Justificativa: evita instalar cliente incompatível sem criar dependência externa ou mecanismo de atualização prematuro.
- Impacto: custo baixo; segurança neutra por não expor dados sensíveis; manutenção simples.
- Revisão: substituir por política semver formal antes de produção.

### A014 - Homologação sem dados persistidos reais
- Escopo: Fase 13.
- Decisão: validar com fixtures `SYNTH-*`, domínios `example.invalid` e migrations offline quando PostgreSQL não estiver disponível.
- Justificativa: mantém separação de ambientes e permite progresso sem risco de dados reais.
- Impacto: custo baixo; segurança alta; manutenção alta por tornar testes reproduzíveis.
- Revisão: trocar por dados anonimizados somente mediante aprovação legal e operacional.

### A015 - Produção explicitamente fora da automação
- Escopo: Fase 14.
- Decisão: limitar a entrega a roteiros, checklists e placeholders; não publicar nem configurar serviços externos.
- Justificativa: produção exige credenciais, decisões legais, backup, assinatura e autorização expressa.
- Impacto: custo operacional futuro; segurança alta; manutenção melhor por tornar o gate explícito.
- Revisão: somente mediante autorização específica de implantação.