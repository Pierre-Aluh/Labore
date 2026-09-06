[CmdletBinding()]
param(
    [string]$OutputRoot = "./backup",
    [string]$StorageRoot = "./storage/clientes",
    [string]$ComposeFile = "./compose.yml"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$destination = Join-Path (Resolve-Path $OutputRoot) "labore-$timestamp"
New-Item -ItemType Directory -Path $destination -Force | Out-Null

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw "Docker CLI não está disponível. Nenhum backup foi criado."
}

$databaseDump = Join-Path $destination "database.sql"
$storageArchive = Join-Path $destination "storage.zip"
$metadata = Join-Path $destination "backup-metadata.json"
$databaseUser = if ($env:POSTGRES_USER) { $env:POSTGRES_USER } else { "labore_app" }
$databaseName = if ($env:POSTGRES_DB) { $env:POSTGRES_DB } else { "labore" }

Write-Host "Criando dump consistente do PostgreSQL..."
docker compose -f $ComposeFile --profile local-infra exec -T postgres pg_dump --clean --if-exists --no-owner --no-privileges -U $databaseUser $databaseName | Out-File -FilePath $databaseDump -Encoding utf8

if (Test-Path $StorageRoot) {
    Write-Host "Compactando storage físico..."
    Compress-Archive -Path (Join-Path $StorageRoot "*") -DestinationPath $storageArchive -CompressionLevel Optimal
} else {
    Write-Warning "Storage não encontrado; backup contém somente banco e metadados."
}

$storageArchiveName = if (Test-Path $storageArchive) { Split-Path $storageArchive -Leaf } else { $null }
[ordered]@{
    created_at = (Get-Date).ToUniversalTime().ToString("o")
    database_dump = (Split-Path $databaseDump -Leaf)
    storage_archive = $storageArchiveName
    includes_secrets = $false
    environment = if ($env:LABORE_ENV) { $env:LABORE_ENV } else { "unknown" }
} | ConvertTo-Json | Set-Content -Path $metadata -Encoding utf8

Write-Host "Backup criado em $destination"
