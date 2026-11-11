# Verify a silent per-user install of the GasProjectCalculator installer.
#
# Usage (from the repository root):
#   powershell -ExecutionPolicy Bypass -File installer\verify-install.ps1 `
#       -InstallerPath installer\Output\GasProjectCalculator-Setup-1.0.0.exe `
#       [-DesktopIcon] -InstallLog <path>
#
# Prints the exact command, exit code, installed file list, and shortcut
# target/arguments so the output can be captured as evidence.

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$InstallerPath,
    [switch]$DesktopIcon,
    [Parameter(Mandatory = $true)][string]$InstallLog
)

$ErrorActionPreference = 'Stop'

$installer = (Resolve-Path -LiteralPath $InstallerPath).Path
$installLogFull = [System.IO.Path]::GetFullPath($InstallLog)
$installDir = Join-Path $env:LOCALAPPDATA 'Programs\GasProjectCalculator'
$startMenuShortcut = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\GasProjectCalculator.lnk'
$desktopShortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) 'GasProjectCalculator.lnk'

Write-Output "=== WI-02 silent install verification ==="
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
        Write-Output ("  target: " + $shortcut.TargetPath)
        Write-Output ("  arguments: " + $shortcut.Arguments)
        Write-Output ("  working directory: " + $shortcut.WorkingDirectory)
        Write-Output ("  icon: " + $shortcut.IconLocation)
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
