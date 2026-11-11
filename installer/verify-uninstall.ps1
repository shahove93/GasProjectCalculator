# Verify a silent uninstall of GasProjectCalculator: installed program files and
# shortcuts are removed, while user-created marker files outside the install
# directory are preserved.
#
# Usage (from the repository root):
#   powershell -ExecutionPolicy Bypass -File installer\verify-uninstall.ps1 `
#       -UninstallLog <path>

[CmdletBinding()]
param(
    [string]$InstallDir = (Join-Path $env:LOCALAPPDATA 'Programs\GasProjectCalculator'),
    [Parameter(Mandatory = $true)][string]$UninstallLog
)

$ErrorActionPreference = 'Stop'

$uninstallLogFull = [System.IO.Path]::GetFullPath($UninstallLog)
$uninstaller = Join-Path $InstallDir 'unins000.exe'
$startMenuShortcut = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\GasProjectCalculator.lnk'
$desktopShortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) 'GasProjectCalculator.lnk'
$userDataDir = Join-Path $env:LOCALAPPDATA 'GasProjectCalculator'
$markers = @(
    (Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'GasProjectCalculator-WI02-user-marker.txt'),
    (Join-Path ([Environment]::GetFolderPath('Desktop')) 'GasProjectCalculator-WI02-user-marker.txt'),
    (Join-Path $userDataDir 'user-marker.txt')
)

Write-Output "=== WI-02 silent uninstall verification ==="
Write-Output "Timestamp: $(Get-Date -Format o)"
Write-Output "Install directory: $InstallDir"
Write-Output "Uninstall log: $uninstallLogFull"

if (-not (Test-Path -LiteralPath $uninstaller)) {
    throw "Uninstaller not found: $uninstaller"
}
Write-Output ""
Write-Output "=== User marker files before uninstall ==="
foreach ($marker in $markers) {
    Write-Output ("$marker : " + (Test-Path -LiteralPath $marker))
    if (-not (Test-Path -LiteralPath $marker)) {
        throw "User marker file missing before uninstall: $marker"
    }
}

$argumentList = @('/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART', "/LOG=`"$uninstallLogFull`"")
$argumentLine = $argumentList -join ' '
Write-Output ""
Write-Output "Command: & `"$uninstaller`" $argumentLine"
$process = Start-Process -FilePath $uninstaller -ArgumentList $argumentList -Wait -PassThru
Write-Output "Uninstaller exit code: $($process.ExitCode)"
if ($process.ExitCode -ne 0) {
    throw "Uninstaller failed with exit code $($process.ExitCode)"
}

# Inno's uninstaller can relaunch itself from %TEMP%; poll until the installed
# program files are gone.
$deadline = (Get-Date).AddSeconds(60)
while ((Test-Path -LiteralPath (Join-Path $InstallDir 'GasProjectCalculator.exe')) -and (Get-Date) -lt $deadline) {
    Start-Sleep -Milliseconds 300
}

Write-Output ""
Write-Output "=== Removal results ==="
$exeStillPresent = Test-Path -LiteralPath (Join-Path $InstallDir 'GasProjectCalculator.exe')
Write-Output ("Installed exe present after uninstall: " + $exeStillPresent)
Write-Output ("Install directory present after uninstall: " + (Test-Path -LiteralPath $InstallDir))
Write-Output ("Start Menu shortcut present after uninstall: " + (Test-Path -LiteralPath $startMenuShortcut))
Write-Output ("Desktop shortcut present after uninstall: " + (Test-Path -LiteralPath $desktopShortcut))
if ($exeStillPresent) { throw "Installed executable still present after uninstall" }
if (Test-Path -LiteralPath $startMenuShortcut) { throw "Start Menu shortcut still present after uninstall" }
if (Test-Path -LiteralPath $desktopShortcut) { throw "Desktop shortcut still present after uninstall" }
if (Test-Path -LiteralPath $InstallDir) {
    $leftover = Get-ChildItem -LiteralPath $InstallDir -Recurse -File
    Write-Output ("Remaining files in install directory: " + $leftover.Count)
    $leftover | ForEach-Object { $_.FullName } | Write-Output
    if ($leftover.Count -gt 0) { throw "Program files remain in the install directory" }
}

Write-Output ""
Write-Output "=== User file preservation ==="
foreach ($marker in $markers) {
    $exists = Test-Path -LiteralPath $marker
    Write-Output ("$marker : " + $exists)
    if (-not $exists) { throw "Uninstall deleted the user marker file: $marker" }
}
Write-Output ("User data directory preserved: " + (Test-Path -LiteralPath $userDataDir))
Write-Output "=== Silent uninstall verification complete ==="
