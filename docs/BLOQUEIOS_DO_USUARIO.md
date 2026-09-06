# BLOQUEIOS QUE EXIGEM AÇÃO DO USUÁRIO

## B001 - Linker MSVC para Tauri

- Data: 2026-09-05.
- Fase: 10.
- Sintoma: `cargo check --manifest-path apps/desktop/src-tauri/Cargo.toml` falha com `linker link.exe not found`.
- Causa: o Rust MSVC está instalado, mas o Visual Studio Build Tools com workload C++ não está disponível no PATH/toolchain atual.
- Ação necessária: instalar Visual Studio Build Tools para VS 2022 ou superior com `Desktop development with C++`, Windows SDK e MSVC v143; depois abrir um terminal de desenvolvedor ou garantir `link.exe` no PATH.
- Impacto: impede validar e empacotar o executável Tauri; não impede o typecheck/build Vite nem o desenvolvimento backend.
- Não executado: nenhuma instalação externa ou elevação automática foi tentada.

## B002 - PostgreSQL/Docker daemon

- Data: 2026-09-05.
- Fase: 02/13.
- Sintoma: o Docker CLI foi instalado, mas a operação do daemon Docker Desktop/WSL2 não foi confirmada neste ambiente.
- Ação necessária: iniciar Docker Desktop com backend Linux operacional e validar `docker version` com Client e Server.
- Impacto: impede aplicar migrations e executar testes de integração contra PostgreSQL; testes unitários e de contrato continuam executáveis.
