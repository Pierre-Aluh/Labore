[CmdletBinding()]
param(
    [string]$ApiBaseUrl = "http://localhost:8000",
    [string]$DesktopVersion = "0.1.0"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$response = Invoke-RestMethod -Uri "$ApiBaseUrl/api/v1/meta/compatibility?client_version=$DesktopVersion" -Method Get
if (-not $response.compatible) { throw "Desktop $DesktopVersion não é compatível com a API $($response.api_version)." }
Write-Host "Compatível: desktop $DesktopVersion com API $($response.api_version)."
