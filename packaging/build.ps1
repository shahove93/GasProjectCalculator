# Build the GasProjectCalculator Windows x64 onedir desktop application.
#
# Usage (from the repository root or any CWD):
#   powershell -ExecutionPolicy Bypass -File packaging\build.ps1
#
# Produces: dist\GasProjectCalculator\GasProjectCalculator.exe

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $projectRoot '.venv\Scripts\python.exe'
$spec = Join-Path $PSScriptRoot 'GasProjectCalculator.spec'
$distPath = Join-Path $projectRoot 'dist'
$workPath = Join-Path $projectRoot 'build'
$artifact = Join-Path $distPath 'GasProjectCalculator\GasProjectCalculator.exe'

if (-not (Test-Path -LiteralPath $python)) {
    throw "Python interpreter not found at $python"
}

Write-Host "Project root: $projectRoot"
Write-Host "Python: $python"
Write-Host "Spec: $spec"

Push-Location -LiteralPath $projectRoot
try {
    & $python -m PyInstaller `
        --noconfirm `
        --clean `
        --distpath $distPath `
        --workpath $workPath `
        $spec
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller build failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

if (-not (Test-Path -LiteralPath $artifact)) {
    throw "Build finished but artifact is missing: $artifact"
}

$hash = (Get-FileHash -LiteralPath $artifact -Algorithm SHA256).Hash
Write-Host "Artifact: $artifact"
Write-Host "SHA256: $hash"
exit 0
