# Instalador e atualização

A configuração Tauri está preparada, mas o bundle está desativado até a validação do linker MSVC, assinatura de artefatos e política de distribuição.

## Requisitos antes de ativar

- Visual Studio Build Tools/MSVC e Windows SDK.
- Certificado de assinatura custodiado fora do repositório.
- Artefatos gerados em pipeline controlado.
- Manifesto de atualização hospedado em ambiente aprovado.
- Rollback validado.

`update-manifest.example.json` contém somente placeholders e não deve ser usado para publicação.
