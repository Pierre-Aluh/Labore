# AGENTS

## 1. Propósito
Este arquivo orienta futuras sessões do Codex no projeto Labore Portal.

## 2. Mandatos Arquiteturais
- Manter arquitetura: Tauri 2 + React + TypeScript, FastAPI, PostgreSQL, Docker Compose, Cloudflare Tunnel e storage físico.
- Não substituir tecnologias sem aprovação explícita do usuário.
- Não criar produtos separados por perfil: app desktop único com UI por permissão.

## 3. Regras de Escopo
- Executar trabalho por unidades pequenas e aprovadas.
- Não iniciar funcionalidades fora do escopo autorizado da sessão.
- Se houver lacuna de requisito, registrar como pendência, não inventar regra definitiva.

## 4. Regras de Implementação
- Toda operação de documento deve passar pela API.
- Proibido acesso direto do cliente às pastas do servidor.
- Proibido armazenar binários de documentos no PostgreSQL.
- Alterações de banco apenas via migration revisada.

## 5. Regras de Segurança
- Aplicar RBAC com menor privilégio.
- Isolar rigorosamente dados por empresa.
- Validar autenticação/autorização em HTTP e WebSocket.
- Não logar senha, token ou payload sensível.
- Não usar dados reais de clientes em desenvolvimento/testes.
- Não implementar MFA nesta versão sem solicitação explícita.

## 6. Regras de Auditoria
Registrar ao menos:
- Ações em arquivos (upload/download/view/update/delete/restore).
- Eventos de autenticação e sessão.
- Ações administrativas (usuários, empresas, papéis, permissões).
- Ciclo de chamados (abrir, responder, atribuir, encerrar, reabrir).

## 7. Regras de Qualidade e Testes
- Toda mudança funcional deve vir com testes apropriados.
- Toda migration deve ter validação automatizada.
- Alterações críticas de autorização exigem testes de acesso negativo e positivo.

## 8. Regras de Documentação
- Atualizar documentação junto com mudanças aprovadas.
- Preservar coerência entre SPECIFICATION.md e docs/*.md.
- Registrar decisões pendentes explicitamente em docs/DECISOES_PENDENTES.md.
- Não transformar uma recomendação em requisito fechado sem aprovação do usuário.
- Toda alteração documental deve indicar se fecha, refina ou mantém uma decisão pendente.

## 9. Regras de Git
- Commits pequenos, claros e recuperáveis.
- Não reverter trabalho do usuário sem autorização explícita.
- Evitar comandos destrutivos e reescrita de histórico sem aprovação.

## 10. Limites de Sessão
- Se o usuário solicitar apenas documentação/planejamento, não implementar código.
- Se houver conflito entre pedido imediato e arquitetura mandatória, pedir confirmação antes de prosseguir.
- Em caso de risco destrutivo (dados, banco, arquivos, histórico), parar e solicitar validação do usuário.

## 11. Checklist Antes de Implementar Qualquer Unidade
1. Escopo aprovado?
2. Requisito de segurança definido?
3. Regras de autorização definidas?
4. Impacto em auditoria coberto?
5. Plano de testes definido?
6. Documentação alvo identificada?

## 12. Pendências Estruturais Permanentes
- Regras finais de status de documentos/movimentações/competências.
- Limites e política antivírus de upload.
- Retenção e restauração de lixeira.
- Estratégia final de atualização Tauri.
- SLA e critérios operacionais de chamados.
- Política legal detalhada de LGPD/retenção.

## 13. Estado Atual do Projeto
- A Fase 01 foi concluída e a autorização contínua para as Fases 02 a 14 foi recebida em 2026-09-05.
- Implementar fases somente na ordem definida em SPECIFICATION.md e ROADMAP.md, com testes, documentação, decisão autônoma e commit por fase.
- Não publicar em produção, configurar serviços externos, usar credenciais reais ou usar dados reais de clientes.
- A matriz de cobertura dos 24 capítulos está em docs/DECISOES_PENDENTES.md.
