param([ValidateSet('backup','inspect','restore')][string]$Action)
$ErrorActionPreference='Stop'
$root='D:\Antigravity\GasProjectCalculator'
$work='C:\Users\user\AppData\Local\Temp\opencode\vp-02-isolated'
$backup=Join-Path $work 'backup'
$install=Join-Path $work 'install'
$reg='HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\{A3E4B6C1-7F2D-4B8E-9C1A-5D6E7F8091A2}_is1'
$key=$reg.Replace('HKCU\','HKCU:\')
$links=@((Join-Path ([Environment]::GetFolderPath('Programs')) 'СС.Расчет.lnk'),(Join-Path ([Environment]::GetFolderPath('Desktop')) 'СС.Расчет.lnk'))
function Snapshot {
  $userInstall=Join-Path $env:LOCALAPPDATA 'Programs\GasProjectCalculator'
  @(Get-ChildItem -LiteralPath $userInstall -Recurse -File | Sort-Object FullName | ForEach-Object {
    [pscustomobject]@{path=$_.FullName;size=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash}
  })
}
if($Action -eq 'backup') {
  if(Test-Path -LiteralPath $backup){throw 'Backup already exists; refusing to replace'}
  New-Item -ItemType Directory -Path $backup | Out-Null
  $keyExists=Test-Path -LiteralPath $key
  if($keyExists){ & reg.exe export $reg (Join-Path $backup 'uninstall.reg') /y; if($LASTEXITCODE){throw 'Registry export failed'} }
  $state=@{keyExists=$keyExists;links=@()}
  for($i=0;$i -lt $links.Count;$i++) {
    $exists=Test-Path -LiteralPath $links[$i]
    if($exists){Copy-Item -LiteralPath $links[$i] -Destination (Join-Path $backup "$i.lnk")}
    $state.links+=@{path=$links[$i];exists=$exists;hash=$(if($exists){(Get-FileHash -LiteralPath $links[$i]).Hash}else{$null})}
  }
  $state | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $backup 'state.json')
  Snapshot | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $backup 'user-install.json')
  Get-CimInstance Win32_Process | Where-Object {$_.ExecutablePath -like '*Programs\GasProjectCalculator\GasProjectCalculator.exe'} | Select-Object ProcessId,ExecutablePath | ConvertTo-Json | Set-Content (Join-Path $backup 'user-processes.json')
  Write-Output 'Backup complete before any installation; user install full hashes and HKCU/shortcut backups persisted.'
}
if($Action -eq 'inspect') {
  Get-ItemProperty -LiteralPath $key | Select-Object DisplayName,DisplayVersion,InstallLocation | Format-List
  $shell=New-Object -ComObject WScript.Shell
  foreach($link in $links){ if(Test-Path -LiteralPath $link){Write-Output "$link -> $($shell.CreateShortcut($link).TargetPath)"}else{Write-Output "$link absent"} }
}
if($Action -eq 'restore') {
  $state=Get-Content (Join-Path $backup 'state.json') -Raw | ConvertFrom-Json
  if(Test-Path -LiteralPath $key) {
    $location=(Get-ItemProperty -LiteralPath $key).InstallLocation.TrimEnd('\')
    if($location -ne $install){throw "Refusing to remove registry state owned by $location"}
    Remove-Item -LiteralPath $key -Recurse
  }
  if($state.keyExists){& reg.exe import (Join-Path $backup 'uninstall.reg'); if($LASTEXITCODE){throw 'Registry restore failed'}}
  for($i=0;$i -lt $links.Count;$i++) {
    if($state.links[$i].exists){Copy-Item -LiteralPath (Join-Path $backup "$i.lnk") -Destination $links[$i] -Force}
    elseif(Test-Path -LiteralPath $links[$i]){
      $shell=New-Object -ComObject WScript.Shell
      if($shell.CreateShortcut($links[$i]).TargetPath -ne (Join-Path $install 'GasProjectCalculator.exe')){throw 'Unexpected shortcut owner'}
      Remove-Item -LiteralPath $links[$i]
    }
    if($state.links[$i].exists -and (Get-FileHash -LiteralPath $links[$i]).Hash -ne $state.links[$i].hash){throw 'Shortcut hash differs'}
  }
  $before=Get-Content (Join-Path $backup 'user-install.json') -Raw | ConvertFrom-Json
  $after=Snapshot
  $differences=Compare-Object ($before | ConvertTo-Json -Depth 4) ($after | ConvertTo-Json -Depth 4)
  if($differences){throw 'User install files differ'}
  if($state.keyExists){
    & reg.exe export $reg (Join-Path $backup 'restored.reg') /y
    if((Get-FileHash (Join-Path $backup 'restored.reg')).Hash -ne (Get-FileHash (Join-Path $backup 'uninstall.reg')).Hash){throw 'Registry export differs'}
  }
  Write-Output "RESTORED: HKCU exact export, shortcut SHA256, all $($after.Count) user install files unchanged"
  $original=Get-Content (Join-Path $backup 'user-processes.json') -Raw | ConvertFrom-Json
  foreach($p in $original){Get-Process -Id $p.ProcessId -ErrorAction Stop | Select-Object Id,ProcessName}
}
