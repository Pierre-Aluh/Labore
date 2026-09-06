# Labore Portal

Fundacao do sistema de gestao documental e atendimento contabil.

## Estado atual

As fases locais autorizadas foram executadas até a documentação de implantação. A produção não foi publicada. Bloqueios de Docker/PostgreSQL e MSVC estão em `docs/BLOQUEIOS_DO_USUARIO.md`.

Arquitetura aprovada:

- Desktop: Tauri 2 + React + TypeScript.
- API: FastAPI + Python.
- Banco: PostgreSQL.
- Orquestracao: Docker Compose.
- Publicacao futura: Cloudflare Tunnel.
- Arquivos: filesystem fisico controlado no servidor.

## Estrutura

```text
apps/desktop/       App desktop Tauri + React + TypeScript (estrutura inicial)
services/api/       Servico FastAPI + Python (estrutura inicial)
infra/              Compose e configuracoes operacionais
config/             Exemplos de configuracao sem segredos

docs/               Documentacao tecnica e operacional
SPECIFICATION.md    Especificacao oficial
AGENTS.md           Regras para futuras sessoes
```

## Pre-requisitos locais

As versoes definitivas devem ser fechadas conforme `docs/DECISOES_PENDENTES.md`. A fundacao foi preparada para Windows com suporte vigente, Git, Node.js, Python, Rust/Cargo e Docker Desktop.

## Validacao da fundacao

Com as ferramentas instaladas, execute:

```powershell
git status --short
python --version
node --version
cargo --version
docker compose config
```

Os comandos de qualidade e testes serao adicionados quando os primeiros modulos executaveis forem autorizados. Nenhum dado real deve ser usado em desenvolvimento ou homologacao.

## Configuracao

Copie `config/.env.example` para uma configuracao local protegida, por exemplo `config/.env.local`, sem commitar segredos. O arquivo de exemplo nao contem credenciais reais. Para usar o Compose com esse arquivo, execute `docker compose --env-file config/.env.local --profile local-infra config`.

## Próximos passos

Consulte `docs/DEPLOYMENT_RUNBOOK.md`, `docs/PRODUCTION_READINESS.md` e `docs/BLOQUEIOS_DO_USUARIO.md` antes de homologar. Nenhuma publicação deve ocorrer sem autorização expressa.
