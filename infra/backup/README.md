# Backup e recuperação

Os scripts `infra/scripts/backup.ps1` e `infra/scripts/restore.ps1` são locais e não publicam dados.

## Backup

```powershell
./infra/scripts/backup.ps1 -OutputRoot ./backup -StorageRoot ./storage/clientes -EnvFile ./config/.env.local
```

O pacote contém dump consistente do PostgreSQL, arquivo compactado do storage quando disponível e metadata sem segredos.

## Restauração

Primeiro simule:

```powershell
./infra/scripts/restore.ps1 -BackupDirectory ./backup/labore-YYYYMMDD-HHMMSS -EnvFile ./config/.env.local
```

A restauração real é destrutiva e exige confirmação explícita:

```powershell
./infra/scripts/restore.ps1 -BackupDirectory ./backup/labore-YYYYMMDD-HHMMSS -EnvFile ./config/.env.local -ConfirmRestore -WhatIf:$false
```

Não incluir `.env`, tokens, credenciais Cloudflare ou outros segredos em pacotes comuns. Custódia de segredos permanece separada.
