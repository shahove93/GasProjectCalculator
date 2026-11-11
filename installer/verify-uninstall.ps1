# Verify a silent uninstall of СС.Расчет: installed program files, shortcuts and
# the per-user uninstall registry key are removed, while user-created marker
# files outside the install directory are preserved.
#
# Usage (from the repository root):
#   powershell -ExecutionPolicy Bypass -File installer\verify-uninstall.ps1 `
#       -UninstallLog <path>
#
# The display name and install location are read from the HKCU uninstall key,
# so this script stays ASCII-only and safe for PowerShell 5.1.

[CmdletBinding()]
param(
    [string]$InstallDir,
    [Parameter(Mandatory = $true)][string]$UninstallLog
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$expectedAppName = -join @(
    [char]0x0421, [char]0x0421, [char]0x002E, [char]0x0420, [char]0x0430,
    [char]0x0441, [char]0x0447, [char]0x0435, [char]0x0442
)
$appKeyName = '{A3E4B6C1-7F2D-4B8E-9C1A-5D6E7F8091A2}_is1'
$hkcuKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$appKeyName"
$fallbackDir = Join-Path $env:LOCALAPPDATA 'Programs\GasProjectCalculator'

if (-not $InstallDir) {
    if (Test-Path -LiteralPath $hkcuKey) {
        $InstallDir = (Get-ItemProperty -LiteralPath $hkcuKey).InstallLocation
    }
    if (-not $InstallDir) { $InstallDir = $fallbackDir }
}
$InstallDir = $InstallDir.TrimEnd('\')

$appName = $expectedAppName
if (Test-Path -LiteralPath $hkcuKey) {
    $appName = (Get-ItemProperty -LiteralPath $hkcuKey).DisplayName
}
$uninstallLogFull = [System.IO.Path]::GetFullPath($UninstallLog)
$logParent = Split-Path -Parent $uninstallLogFull
if (-not (Test-Path -LiteralPath $logParent)) {
    New-Item -ItemType Directory -Force -Path $logParent | Out-Null
}
$uninstaller = Join-Path $InstallDir 'unins000.exe'
$startMenuShortcut = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\$appName.lnk"
$desktopShortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) "$appName.lnk"
$userDataDir = Join-Path $env:LOCALAPPDATA 'GasProjectCalculator'
$markers = @(
    (Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'RD-03-user-marker.txt'),
    (Join-Path ([Environment]::GetFolderPath('Desktop')) 'RD-03-user-marker.txt'),
    (Join-Path $userDataDir 'RD-03-user-marker.txt')
)

Write-Output "=== RD-03 silent uninstall verification ==="
Write-Output "Timestamp: $(Get-Date -Format o)"
Write-Output "Display name: $appName"
Write-Output "Install directory: $InstallDir"
Write-Output "Uninstall log: $uninstallLogFull"
Write-Output ("HKCU uninstall key: " + $hkcuKey)

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
Write-Output ("HKCU uninstall key present after uninstall: " + (Test-Path -LiteralPath $hkcuKey))
if ($exeStillPresent) { throw "Installed executable still present after uninstall" }
if (Test-Path -LiteralPath $startMenuShortcut) { throw "Start Menu shortcut still present after uninstall" }
if (Test-Path -LiteralPath $desktopShortcut) { throw "Desktop shortcut still present after uninstall" }
if (Test-Path -LiteralPath $hkcuKey) { throw "Uninstall registry key still present after uninstall" }
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
