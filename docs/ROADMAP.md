# ROADMAP

## 1. Diretriz
Evolução em fases pequenas, verificáveis e aprovadas.

A Fase 01 só começa após aprovação explícita do usuário e fechamento das decisões classificadas como obrigatórias antes dela em docs/DECISOES_PENDENTES.md.

## 2. Fases Macro
1. Fase 01 - Fundação do projeto.
2. Fase 02 - Banco de dados e migrations.
3. Fase 03 - Autenticação e sessões.
4. Fase 04 - Gestão de empresas, usuários, papéis e permissões.
5. Fase 05 - Documentos e armazenamento físico controlado.
6. Fase 06 - Movimentação contábil.
7. Fase 07 - Extratos bancários e investimentos.
8. Fase 08 - Chamados.
9. Fase 09 - Chat em tempo real.
10. Fase 10 - Interfaces e painel administrativo.
11. Fase 11 - Backups e recuperação.
12. Fase 12 - Instalador e atualização desktop.
13. Fase 13 - Testes, segurança e homologação.
14. Fase 14 - Implantação.

## 3. Critério de Entrada em Fase
- Documentação da fase anterior aprovada.
- Escopo delimitado em tarefas pequenas.
- Riscos principais mapeados.

## 4. Critério de Saída de Fase
- Entregáveis concluídos e testados.
- Revisão técnica finalizada.
- Documentação atualizada.
- Aprovação do usuário.

## 5. Dependências Críticas
- Fase 03 depende da base de dados de Fase 02.
- Fases 05, 06 e 07 dependem de RBAC maduro (Fase 04).
- Fase 09 depende de chamados sólidos (Fase 08).
- Fase 12 depende de estabilidade funcional das fases anteriores.

## 6. Riscos de Execução
- Crescimento de escopo sem aprovação.
- Falta de testes em fluxos críticos.
- Lacunas de segurança em upload/download.
- Processo de backup sem ensaio de restauração.

## 7. Pendências de Planejamento
- SLA de atendimento por departamento.
- Dimensionamento por volume real.
- Estratégia final de atualização do desktop.
- Política detalhada de backup externo.
- Decisões obrigatórias e decisões futuras estão classificadas em docs/DECISOES_PENDENTES.md.

## 8. Estado de Execução

- Fase 01: concluída.
- Fase 02: concluída em 2026-09-05, com schema conceitual e migration inicial testados localmente sem banco real.
- Fase 03: concluída em 2026-09-05, com Argon2id, sessões opacas, revogação e bloqueio temporário testados.
- Fase 04: concluída em 2026-09-05, com catálogo RBAC, vínculos e rotas administrativas protegidas.
- Próxima fase: Fase 05, documentos e armazenamento físico controlado.
