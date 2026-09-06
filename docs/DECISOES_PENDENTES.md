# DECISÕES PENDENTES

## Objetivo e Status
Este documento é o registro único das decisões ainda não aprovadas do Labore Portal. As recomendações abaixo são propostas técnicas, não requisitos fechados. Não iniciar implementação funcional enquanto as decisões obrigatórias da seção 1 não forem aprovadas.

## Aprovações Recebidas em 2026-09-05

O usuário aprovou para a Fase 01:

- Fundação somente estrutural.
- Plataforma inicial Windows com suporte vigente.
- Ambientes de desenvolvimento, homologação e produção separados, sem dados reais em desenvolvimento/testes.
- Toda tarefa futura com escopo aprovado, testes definidos, documentação atualizada e commit pequeno.

Essas aprovações correspondem às decisões P01, P02, P03 e P06. As restrições da seção “Fora do escopo” da autorização da Fase 01 também são obrigatórias nesta unidade.

Impactos:
- **Custo:** esforço de desenvolvimento, infraestrutura e operação.
- **Segurança:** risco de acesso indevido, perda, vazamento ou indisponibilidade.
- **Manutenção:** complexidade de evolução, suporte e recuperação.

## 1. Decisões Obrigatórias Antes da Fase 01

| ID | Decisão | Recomendação simples | Custo | Segurança | Manutenção |
| --- | --- | --- | --- | --- | --- |
| P01 | Escopo técnico exato da Fase 01 | Aprovar somente fundação documentalmente rastreável: estrutura do monorepo, configuração-base, healthcheck e qualidade; sem domínio, banco funcional ou upload. | Baixo; reduz retrabalho. | Médio/alto; evita superfície prematura. | Alto; cria base previsível. |
| P02 | Política de dados de desenvolvimento | Usar exclusivamente dados fictícios, arquivos sintéticos e segredos locais fora do Git. | Baixo. | Alto; reduz risco de LGPD. | Alto; facilita testes reproduzíveis. |
| P03 | Compatibilidade mínima de ambiente | Fixar versões suportadas de Windows, Node, Python, Rust/Tauri, Docker e PostgreSQL somente na Fase 01 após validação do ambiente. | Baixo. | Médio; reduz componentes sem suporte. | Alto; evita divergência entre máquinas. |
| P04 | Identidade da primeira fundação | Definir que a Fase 01 não terá autenticação de produção; apenas configuração estrutural e healthcheck não sensível. | Baixo. | Alto; evita segurança falsa. | Alto; deixa autenticação para Fase 03. |
| P05 | Limite de mudanças autorizadas | Não criar migrations, tabelas, endpoints de domínio, storage de documentos ou telas funcionais na Fase 01. | Baixo. | Alto; reduz risco de decisões prematuras. | Alto; mantém fases separadas. |
| P06 | Regra de revisão e aprovação | Cada unidade deve ter escopo, teste e aprovação antes da próxima; commits pequenos, sem alterações destrutivas. | Baixo. | Médio. | Alto; facilita rollback e auditoria. |

Estas decisões são principalmente de governança. As decisões de produto e operação abaixo podem ser fechadas depois, antes de suas respectivas fases.

## 2. Decisões Necessárias Antes de Fases Futuras

| ID | Fechar antes de | Decisão | Recomendação simples | Custo | Segurança | Manutenção |
| --- | --- | --- | --- | --- | --- | --- |
| F01 | Fase 02 | Estratégia de IDs | Usar UUID v7 para entidades expostas e relacionais, se o suporte da versão escolhida estiver validado. | Baixo/médio. | Médio; reduz enumeração. | Médio/alto; bom para distribuição. |
| F02 | Fase 02 | Modelo final de competências e status | Definir máquina de estados explícita, com transições auditadas e status agregados derivados dos requisitos. | Médio. | Médio; evita ocultar pendências. | Alto; reduz regras espalhadas. |
| F03 | Fase 02 | Retenção de auditoria e particionamento | Começar sem particionamento, mas indexar por empresa/data e reservar particionamento por volume. | Baixo inicial. | Alto; preserva rastreabilidade. | Alto; evita complexidade cedo. |
| F04 | Fase 03 | Sessões e tokens | Preferir sessão opaca revogável no servidor, com cookie seguro quando aplicável ao cliente, expiração e rotação definidas. | Médio. | Alto; facilita revogação. | Médio; exige armazenamento de sessão. |
| F05 | Fase 03 | Política de senha e bloqueio | Argon2id, limite de tentativas, bloqueio temporário e mensagens que não revelem existência de usuário. | Baixo/médio. | Alto. | Médio. |
| F06 | Fase 04 | Matriz RBAC e escopo por empresa | Definir permissões por ação e recurso, com testes positivos e negativos para cada papel. | Médio. | Alto. | Alto; autorização centralizada. |
| F07 | Fase 05 | Tipos e limites de upload | Começar com lista fechada dos formatos já considerados, limite conservador por arquivo e limite total configurável. | Médio. | Alto; reduz abuso. | Alto; configuração central. |
| F08 | Fase 05 | Antivírus e quarentena | Receber em área de quarentena, verificar antes de disponibilizar e registrar resultado; bloquear quando o scanner não estiver disponível. | Médio/alto; exige serviço/processo. | Alto. | Médio; dependência operacional. |
| F09 | Fase 05 | Lixeira e retenção | Soft delete por 30 dias inicialmente, restauração autorizada e purge automático somente após aprovação da política legal. | Baixo/médio. | Alto; reduz remoção acidental. | Alto; rotina clara. |
| F10 | Fase 05 | Convenção física de storage | Usar IDs internos controlados por empresa/competência/categoria, nomes sanitizados e arquivo temporário com publicação atômica. | Baixo. | Alto; reduz traversal e colisão. | Alto; independente de nomes comerciais. |
| F11 | Fase 05 | Consistência banco/arquivo | Criar metadado somente após publicação segura do arquivo; rotina de reconciliação para falhas parciais. | Médio. | Alto; evita referências inválidas. | Alto; diagnóstico operacional claro. |
| F12 | Fase 06/07 | Requisitos esperados e pendências | Modelar requisitos por empresa/competência, conta e categoria, com status derivado e exceções justificadas. | Médio. | Médio. | Alto; suporta novos tipos. |
| F13 | Fase 08 | Ciclo de chamados e SLA | Definir estados, atribuição por departamento, prioridade, prazo, reabertura e encerramento antes do CRUD. | Médio. | Médio. | Alto; evita regras ad hoc. |
| F14 | Fase 09 | Exportação de conversas | Manter exportação manual sob demanda, autorizada e auditada; não salvar cópias automáticas em máquinas clientes. | Baixo/médio. | Alto. | Alto; reduz vazamento e suporte. |
| F15 | Fase 09 | WebSocket e revogação | Validar sessão no handshake e periodicamente; encerrar conexão ao revogar/expirar autorização. | Médio. | Alto. | Médio. |
| F16 | Fase 10 | Notificações | Persistir notificações internas e entregar em tempo real como otimização; e-mail fica fora da V1. | Médio. | Médio. | Alto; canal futuro desacoplado. |
| F17 | Fase 11 | Backup, RPO/RTO e retenção | Definir RPO/RTO com o escritório, backup diário do banco, cópia do storage, mídia separada e teste periódico de restore. | Médio/alto; storage externo tem custo. | Alto; criptografar fora do servidor. | Alto; recuperação verificável. |
| F18 | Fase 11 | Segredos de produção | Não incluir segredos em backup comum; documentar custódia, rotação e restauração separadamente. | Baixo/médio. | Alto. | Médio. |
| F19 | Fase 12 | Atualização Tauri | Usar artefatos assinados, canal estável controlado e rollback documentado; atualização automática só após homologação. | Médio. | Alto; assinatura evita binário adulterado. | Alto; reduz suporte manual. |
| F20 | Fase 12/14 | Cloudflare Tunnel | Começar com serviço do sistema no servidor dedicado, credencial protegida e domínio separado por ambiente; containerizar somente se operação justificar. | Baixo/médio. | Alto. | Alto; menos camadas em ambiente Windows. |
| F21 | Fase 13 | Testes de segurança e operação | Exigir testes de isolamento entre empresas, autorização negativa, upload, restore e migração antes da homologação. | Médio. | Alto. | Alto; regressões detectadas cedo. |
| F22 | Fase 14 | LGPD, retenção e consentimentos | Validar com responsável jurídico antes de produção; documentar base legal, retenção, descarte e atendimento a titulares. | Médio; pode exigir consultoria. | Alto. | Alto; evita retrabalho legal. |
| F23 | Fase 14 | Dimensionamento | Medir clientes, usuários, documentos, tamanho médio, crescimento e concorrência antes de fixar hardware final. | Baixo inicialmente. | Médio. | Alto; evita subdimensionamento. |

## 3. Cobertura dos 24 Capítulos da Especificação

| Capítulo | Documento(s) interno(s) | Cobertura | Observação |
| --- | --- | --- | --- |
| 1. Objetivo | ARCHITECTURE, ROADMAP | Completa | Objetivo e escopo consistentes. |
| 2. Arquitetura | ARCHITECTURE, DEPLOYMENT | Completa | Tunnel e fronteira da API explícitos. |
| 3. Usuários | SECURITY, DATABASE | Parcial | Perfis existem; ciclo de vida fica para Fase 04. |
| 4. Permissões | SECURITY, DATABASE, DEVELOPMENT | Parcial | RBAC definido; matriz final depende da Fase 04. |
| 5. Empresas | DATABASE, SECURITY, API | Parcial | Isolamento definido; regras cadastrais serão fechadas na Fase 04. |
| 6. Documentos | STORAGE, DATABASE, API, SECURITY | Completa | Upload, metadados, acesso e auditoria cobertos. |
| 7. Movimentações | DATABASE, API, ROADMAP | Parcial | Entidade e arquivos cobertos; estados finais pendentes. |
| 8. Extratos | DATABASE, API, ROADMAP | Parcial | Contas e pendências previstas; regras de contas esperadas pendentes. |
| 9. Competências | DATABASE, API, ROADMAP | Parcial | Conceito coberto; máquina de estados pendente. |
| 10. Chamados | API, DATABASE, ROADMAP | Parcial | Entidades e operações cobertas; SLA e transições pendentes. |
| 11. Chat | API, ARCHITECTURE, SECURITY | Completa | WebSocket, persistência e autorização cobertos. |
| 12. Notificações | API, ARCHITECTURE | Parcial | Canal interno coberto; entrega/retry e preferências futuras. |
| 13. Auditoria | SECURITY, DATABASE, ARCHITECTURE | Completa | Eventos e metadados cobertos; retenção detalhada pendente. |
| 14. Armazenamento | STORAGE, ARCHITECTURE | Completa | Caminho controlado, integridade e reconciliação cobertos. |
| 15. Backup | DEPLOYMENT, STORAGE | Parcial | Estratégia existe; RPO/RTO e retenção pendentes. |
| 16. Segurança | SECURITY, DEVELOPMENT, ARCHITECTURE | Completa | Baseline e regras de desenvolvimento cobertos. |
| 17. API | API, ARCHITECTURE | Parcial | Domínios cobertos; contratos detalhados ficam por fase. |
| 18. Banco de dados | DATABASE, DEVELOPMENT | Completa | Entidades, migrations e governança cobertas. |
| 19. Desktop | ARCHITECTURE, ROADMAP | Parcial | Papel do app definido; instalação/atualização ficam para Fases 12/14. |
| 20. Servidor | DEPLOYMENT, ARCHITECTURE | Completa | Topologia, estrutura e operação cobertas. |
| 21. Instalação | DEPLOYMENT, ROADMAP | Parcial | Diretrizes existem; checklist executável fica para Fase 14. |
| 22. Atualização | DEPLOYMENT, ROADMAP | Parcial | Princípios existem; estratégia Tauri pendente até Fase 12. |
| 23. Testes | DEVELOPMENT, ROADMAP, SECURITY | Completa | Critérios e classes de teste cobertos. |
| 24. Roadmap | ROADMAP, DEVELOPMENT | Completa | Fases, dependências e critérios cobertos. |

## 4. Inconsistências e Requisitos Ausentes

1. A especificação dizia que o audit service era imutável sem mecanismo definido. Agora consta como protegido contra alteração indevida, com retenção pendente.
2. O backup não separava configurações de segredos. Agora apenas configurações não secretas entram no pacote comum.
3. O caminho de storage usava o nome da empresa como referência. A recomendação agora usa IDs estáveis.
4. A transação entre arquivo e metadado estava superficial. Foram incluídos arquivo temporário, publicação atômica e reconciliação.
5. Anexos de chamados não tinham fronteira suficiente. Agora usam o mesmo storage e pipeline autorizado.
6. O Cloudflare Tunnel não tinha decisão operacional sobre serviço ou container. Essa escolha foi explicitada como pendente.
7. As pendências agora estão separadas entre pré-Fase 01 e fases futuras.

Requisitos ainda ausentes e que devem ser tratados antes da implementação correspondente:
- Critérios mensuráveis de disponibilidade, RPO e RTO.
- Catálogo final de transições de status e permissões.
- Contratos detalhados de paginação, ordenação, upload multipart e compatibilidade de API.
- Política formal de classificação de dados, retenção e descarte legal.
- Checklist executável de instalação, restore e migração.
- Métricas operacionais e alertas mínimos.