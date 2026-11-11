# Verify a silent per-user install of the new СС.Расчет installer.
#
# Usage (from the repository root):
#   powershell -ExecutionPolicy Bypass -File installer\verify-install.ps1 `
#       -InstallerPath installer\Output\GasProjectCalculator-Setup-1.0.0.exe `
#       [-DesktopIcon] -InstallLog <path>
#
# Prints the exact command, exit code, registry (HKCU) evidence, installed file
# list, and shortcut target/arguments so the output can be captured as evidence.
# The display name is compared against the exact brand name, built from code
# points so this script stays ASCII-only and safe for PowerShell 5.1.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$InstallerPath,
    [switch]$DesktopIcon,
    [Parameter(Mandatory = $true)][string]$InstallLog
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$expectedAppName = -join @(
    [char]0x0421, [char]0x0421, [char]0x002E, [char]0x0420, [char]0x0430,
    [char]0x0441, [char]0x0447, [char]0x0435, [char]0x0442
)
$appKeyName = '{A3E4B6C1-7F2D-4B8E-9C1A-5D6E7F8091A2}_is1'
$hkcuKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$appKeyName"
$hklmKey = "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$appKeyName"
$fallbackDir = Join-Path $env:LOCALAPPDATA 'Programs\GasProjectCalculator'

$installer = (Resolve-Path -LiteralPath $InstallerPath).Path
$installLogFull = [System.IO.Path]::GetFullPath($InstallLog)
$logParent = Split-Path -Parent $installLogFull
if (-not (Test-Path -LiteralPath $logParent)) {
    New-Item -ItemType Directory -Force -Path $logParent | Out-Null
}

Write-Output "=== RD-03 silent install verification ==="
Write-Output "Timestamp: $(Get-Date -Format o)"
Write-Output "Installer: $installer"
Write-Output ("Installer SHA256: " + (Get-FileHash -LiteralPath $installer -Algorithm SHA256).Hash)
Write-Output "Install log: $installLogFull"
Write-Output "Desktop icon task requested: $([bool]$DesktopIcon)"

$argumentList = @('/VERYSILENT', '/SUPPRESSMSGBOXES', '/NORESTART', "/LOG=`"$installLogFull`"")
if ($DesktopIcon) {
    $argumentList += '/TASKS="desktopicon"'
}
$argumentLine = $argumentList -join ' '
Write-Output ""
Write-Output "Command: & `"$installer`" $argumentLine"
$process = Start-Process -FilePath $installer -ArgumentList $argumentList -Wait -PassThru
Write-Output "Installer exit code: $($process.ExitCode)"
if ($process.ExitCode -ne 0) {
    throw "Installer failed with exit code $($process.ExitCode)"
}

# Registry evidence: a per-user install must live under HKCU, never HKLM.
Write-Output ""
Write-Output "=== Registry evidence (per-user) ==="
Write-Output ("HKCU uninstall key: " + $hkcuKey)
Write-Output ("HKCU key exists: " + (Test-Path -LiteralPath $hkcuKey))
Write-Output ("HKLM uninstall key: " + $hklmKey)
Write-Output ("HKLM key exists: " + (Test-Path -LiteralPath $hklmKey))
if (-not (Test-Path -LiteralPath $hkcuKey)) {
    throw "Per-user uninstall registry key was not created under HKCU"
}
if (Test-Path -LiteralPath $hklmKey) {
    throw "Unexpected machine-wide uninstall registry key under HKLM"
}
$entry = Get-ItemProperty -LiteralPath $hkcuKey
Write-Output ("DisplayName: " + $entry.DisplayName)
Write-Output ("DisplayVersion: " + $entry.DisplayVersion)
Write-Output ("Publisher: " + $entry.Publisher)
Write-Output ("InstallLocation: " + $entry.InstallLocation)
Write-Output ("UninstallString: " + $entry.UninstallString)
if ($entry.DisplayName -ne $expectedAppName) {
    throw "Registry DisplayName does not match the exact brand name: '$($entry.DisplayName)'"
}

$appName = $entry.DisplayName
$installDir = if ($entry.InstallLocation) { $entry.InstallLocation.TrimEnd('\') } else { $fallbackDir }
$startMenuShortcut = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\$appName.lnk"
$desktopShortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) "$appName.lnk"

$exe = Join-Path $installDir 'GasProjectCalculator.exe'
Write-Output ""
Write-Output "=== Installed files ==="
Write-Output "Install directory: $installDir"
Write-Output ("Install directory exists: " + (Test-Path -LiteralPath $installDir))
if (-not (Test-Path -LiteralPath $exe)) {
    throw "Installed executable missing: $exe"
}
$files = Get-ChildItem -LiteralPath $installDir -Recurse -File
Write-Output ("Installed file count: " + $files.Count)
Write-Output ("Installed total bytes: " + (($files | Measure-Object -Property Length -Sum).Sum))
Write-Output "Installed file list:"
$files | ForEach-Object { $_.FullName.Substring($installDir.Length + 1) } | Sort-Object | Write-Output
Write-Output ("Installed exe SHA256: " + (Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash)

function Write-ShortcutInfo([string]$path) {
    Write-Output "Shortcut: $path"
    Write-Output ("  exists: " + (Test-Path -LiteralPath $path))
    if (Test-Path -LiteralPath $path) {
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($path)
        Write-Output ("  name: " + (Split-Path -Leaf $path))
        Write-Output ("  target: " + $shortcut.TargetPath)
        Write-Output ("  arguments: " + $shortcut.Arguments)
        Write-Output ("  working directory: " + $shortcut.WorkingDirectory)
        Write-Output ("  icon: " + $shortcut.IconLocation)
        if ($shortcut.TargetPath -ne $exe) {
            throw "Shortcut target '$($shortcut.TargetPath)' is not the installed exe '$exe'"
        }
        if ($shortcut.WorkingDirectory -ne $installDir) {
            throw "Shortcut working directory '$($shortcut.WorkingDirectory)' is not the install directory '$installDir'"
        }
    }
}

Write-Output ""
Write-Output "=== Shortcuts ==="
Write-ShortcutInfo $startMenuShortcut
Write-ShortcutInfo $desktopShortcut
$desktopExists = Test-Path -LiteralPath $desktopShortcut
Write-Output ("Desktop shortcut expected: " + $([bool]$DesktopIcon) + "; actual: " + $desktopExists)
if ($desktopExists -ne [bool]$DesktopIcon) {
    throw "Desktop shortcut presence does not match the requested task state"
}
if (-not (Test-Path -LiteralPath $startMenuShortcut)) {
    throw "Start Menu shortcut was not created"
}
Write-Output "=== Silent install verification complete ==="
