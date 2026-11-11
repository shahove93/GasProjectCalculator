# Build the GasProjectCalculator Windows x64 installer with Inno Setup.
#
# Usage (from the repository root or any CWD):
#   powershell -ExecutionPolicy Bypass -File installer\build-installer.ps1
#
# The Inno Setup compiler is resolved from -IsccPath, then $env:ISCC_PATH, then
# two verified local (non-installed) locations. A candidate is only accepted
# when its companion ISCmplr.dll is present, because ISCC.exe alone cannot
# compile. The compiler binary is never committed.
#
# Prerequisite: the packaged onedir application must exist; build it first with
#   powershell -ExecutionPolicy Bypass -File packaging\build.ps1

[CmdletBinding()]
param(
    [string]$IsccPath = $env:ISCC_PATH
)

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$fallbackCandidates = @(
    'C:\Users\user\AppData\Local\Temp\edr-windows-build\inno\ISCC.exe',
    'C:\Users\user\AppData\Local\Programs\Antigravity IDE\resources\app\node_modules\innosetup\bin\ISCC.exe'
)
$appDir = Join-Path $projectRoot 'dist\GasProjectCalculator'
$appExe = Join-Path $appDir 'GasProjectCalculator.exe'
$issPath = Join-Path $PSScriptRoot 'GasProjectCalculator.iss'
$outputDir = Join-Path $PSScriptRoot 'Output'

function Test-Iscc([string]$candidate) {
    if ([string]::IsNullOrWhiteSpace($candidate)) { return $false }
    if (-not (Test-Path -LiteralPath $candidate)) { return $false }
    $compiler = Join-Path (Split-Path -Parent $candidate) 'ISCmplr.dll'
    return (Test-Path -LiteralPath $compiler)
}

if (-not (Test-Iscc $IsccPath)) {
    if (-not [string]::IsNullOrWhiteSpace($IsccPath)) {
        Write-Warning "ISCC candidate '$IsccPath' is missing or incomplete (ISCmplr.dll not found); trying fallbacks."
    }
    $IsccPath = $null
    foreach ($candidate in $fallbackCandidates) {
        if (Test-Iscc $candidate) { $IsccPath = $candidate; break }
    }
    if (-not $IsccPath) {
        throw "No complete Inno Setup compiler found. Pass -IsccPath or set `$env:ISCC_PATH to an ISCC.exe that has ISCmplr.dll next to it."
    }
}
if (-not (Test-Path -LiteralPath $appExe)) {
    throw "Packaged application not found at $appExe. Run packaging\build.ps1 first."
}

$appExeHash = (Get-FileHash -LiteralPath $appExe -Algorithm SHA256).Hash
Write-Host "Project root: $projectRoot"
Write-Host "Inno Setup: $IsccPath"
Write-Host "Script: $issPath"
Write-Host "Packaged exe: $appExe"
Write-Host "Packaged exe SHA256: $appExeHash"

Push-Location -LiteralPath $PSScriptRoot
try {
    & $IsccPath $issPath
    if ($LASTEXITCODE -ne 0) {
        throw "ISCC build failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

$artifact = Get-ChildItem -LiteralPath $outputDir -Filter 'GasProjectCalculator-Setup-*.exe' -File |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
if ($null -eq $artifact) {
    throw "ISCC finished but no installer artifact was found in $outputDir"
}

$hash = (Get-FileHash -LiteralPath $artifact.FullName -Algorithm SHA256).Hash
Write-Host "Installer artifact: $($artifact.FullName)"
Write-Host "Installer size: $($artifact.Length) bytes"
Write-Host "Installer SHA256: $hash"
exit 0
