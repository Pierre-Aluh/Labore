# Infraestrutura

Esta pasta concentra configuracoes operacionais sem segredos reais.

- `compose.yml` na raiz contem apenas a fundacao local opcional do PostgreSQL, sem schema ou migration.
- Cloudflare Tunnel permanece desabilitado e sem credenciais na Fase 01.
- Procedimentos de deploy, backup e restore estao documentados em `docs/DEPLOYMENT.md`.
