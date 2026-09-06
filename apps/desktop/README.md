# Desktop

Aplicativo único Tauri 2 + React + TypeScript, com navegação derivada do papel recebido após login.

## Validação local

```powershell
npm.cmd run typecheck
npm.cmd run test
npm.cmd run build
& "$env:USERPROFILE\.cargo\bin\cargo.exe" check --manifest-path apps/desktop/src-tauri/Cargo.toml
```

A última validação exige Visual Studio Build Tools com C++/MSVC e Windows SDK. O bloqueio atual está registrado em `docs/BLOQUEIOS_DO_USUARIO.md`.

Atualização automática e assinatura permanecem desabilitadas até a estratégia da Fase 12 ser homologada.
