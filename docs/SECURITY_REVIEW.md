# Revisão de segurança da Fase 13

Controles verificados por testes locais:

- Hash Argon2id sem senha em claro.
- Token de sessão armazenado somente como hash.
- Expiração e revogação de sessão.
- RBAC negado por padrão.
- Isolamento de empresa em operações de domínio.
- Sanitização e prevenção de traversal no storage.
- Limite de tamanho e quarentena de upload.
- Auditoria de ações sensíveis.
- WebSocket rejeita sessão ausente, expirada ou revogada.
- Fixture de homologação usa domínios `example.invalid` e identificadores `SYNTH-*`.

Pendências antes de produção: scanner antivírus, revisão jurídica LGPD, teste de restore, MSVC/assinatura desktop e operação Cloudflare real.
