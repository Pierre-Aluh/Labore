[CmdletBinding(SupportsShouldProcess)]
param(
    [Parameter(Mandatory = $true)] [string]$BackupDirectory,
    [string]$StorageRoot = "./storage/clientes",
    [string]$ComposeFile = "./compose.yml",
    [string]$EnvFile = "./config/.env.local",
    [switch]$ConfirmRestore
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$backup = Resolve-Path $BackupDirectory
$metadataPath = Join-Path $backup "backup-metadata.json"
$databaseDump = Join-Path $backup "database.sql"
$storageArchive = Join-Path $backup "storage.zip"
if (-not (Test-Path $metadataPath) -or -not (Test-Path $databaseDump)) { throw "Pacote de backup incompleto." }

Write-Host "Modo de restauração: banco e storage serão substituídos."
Write-Host "Pacote: $backup"
if (-not $ConfirmRestore) {
    Write-Host "Simulação concluída. Use -ConfirmRestore somente após validar o pacote e o destino."
    exit 0
}
if (-not $PSCmdlet.ShouldProcess($backup, "Restaurar banco e storage")) { exit 0 }

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw "Docker CLI não está disponível." }
$databaseUser = if ($env:POSTGRES_USER) { $env:POSTGRES_USER } else { "labore_app" }
$databaseName = if ($env:POSTGRES_DB) { $env:POSTGRES_DB } else { "labore" }
Get-Content -Raw $databaseDump | docker compose --env-file $EnvFile -f $ComposeFile --profile local-infra exec -T postgres psql -U $databaseUser $databaseName
if (Test-Path $storageArchive) {
    New-Item -ItemType Directory -Path $StorageRoot -Force | Out-Null
    Expand-Archive -Path $storageArchive -DestinationPath $StorageRoot -Force
}
Write-Host "Restauração concluída. Execute os healthchecks e valide auditoria antes de liberar o ambiente."
