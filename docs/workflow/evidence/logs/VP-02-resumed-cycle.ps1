$ErrorActionPreference = 'Stop'
$root = 'D:\Antigravity\GasProjectCalculator'
$work = 'C:\Users\user\AppData\Local\Temp\opencode\vp-02-resume-cycle'
$install = Join-Path $work 'install'
$backup = Join-Path $work 'backup'
$reg = 'HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\{A3E4B6C1-7F2D-4B8E-9C1A-5D6E7F8091A2}_is1'
$key = $reg.Replace('HKCU\','HKCU:\')
$links = @((Join-Path ([Environment]::GetFolderPath('Programs')) 'СС.Расчет.lnk'), (Join-Path ([Environment]::GetFolderPath('Desktop')) 'СС.Расчет.lnk'))
$userInstall = Join-Path $env:LOCALAPPDATA 'Programs\GasProjectCalculator'
$logPrefix = Join-Path $root 'docs\workflow\evidence\logs\VP-02-resumed-cycle'
function Snapshot {
    @(Get-ChildItem -LiteralPath $userInstall -Recurse -File | Sort-Object FullName | ForEach-Object {
        [ordered]@{path=$_.FullName;size=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash}
    }) | ConvertTo-Json -Depth 4
}
function Check-Sentinel {
    foreach($s in $sentinels){if((Get-Content -LiteralPath $s -Raw) -ne $marker){throw "User file changed: $s"}}
}
function Run-Setup([string]$version,[string]$stage) {
    $exe=Join-Path $root "installer\Output\GasProjectCalculator-Setup-$version.exe"
    $args=@('/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART',"/DIR=`"$install`"",'/TASKS=desktopicon',"/LOG=`"$logPrefix-$stage.log`"")
    Write-Output "COMMAND CWD=$root EXE=$exe ARGS=$args"
    $p=Start-Process -FilePath $exe -ArgumentList $args -WindowStyle Hidden -PassThru -Wait
    Write-Output "$stage exit=$($p.ExitCode)"
    if($p.ExitCode -ne 0){throw "Setup $stage failed"}
    $props=Get-ItemProperty -LiteralPath $key
    if($props.InstallLocation.TrimEnd('\') -ne $install -or $props.DisplayVersion -ne $version){throw 'Unexpected installed registration'}
    $shell=New-Object -ComObject WScript.Shell
    foreach($link in $links){if($shell.CreateShortcut($link).TargetPath -ne (Join-Path $install 'GasProjectCalculator.exe')){throw "Shortcut mismatch: $link"}}
    Write-Output "Registered version=$($props.DisplayVersion) path=$($props.InstallLocation); both shortcuts point to isolated exe"
}
if(Test-Path -LiteralPath $work){throw 'Fresh cycle directory required; refusing to overwrite backup'}
New-Item -ItemType Directory -Path $backup -Force | Out-Null
$before=Snapshot
$before | Set-Content "$backup\user-install.json"
& reg.exe export $reg "$backup\uninstall.reg" /y
if($LASTEXITCODE){throw 'Cannot back up registry'}
$beforeReg=(Get-FileHash "$backup\uninstall.reg").Hash
$beforeLocation=(Get-ItemProperty -LiteralPath $key).InstallLocation
$linkState=@()
for($i=0;$i -lt $links.Count;$i++){
    $exists=Test-Path -LiteralPath $links[$i]
    if($exists){Copy-Item -LiteralPath $links[$i] -Destination "$backup\$i.lnk"}
    $linkState+=@{path=$links[$i];exists=$exists;hash=$(if($exists){(Get-FileHash -LiteralPath $links[$i]).Hash}else{$null})}
}
$linkState | ConvertTo-Json | Set-Content "$backup\links.json"
$protected=@(Get-Process -Id 13248,12888,23152 | Select-Object Id,StartTime)
$protected | ConvertTo-Json | Set-Content "$backup\processes.json"
try {
    Run-Setup '1.1.0' 'install-old'
    $marker="VP-02 preserved user content `r`n logical MD-03 A2"
    $sentinels=@((Join-Path $install 'user-notes.txt'),(Join-Path $install '_internal\user-data\custom.txt'))
    New-Item -ItemType Directory -Path (Split-Path $sentinels[1]) | Out-Null
    foreach($s in $sentinels){[IO.File]::WriteAllText($s,$marker)}
    Run-Setup '1.2.0' 'upgrade'
    Check-Sentinel
    Write-Output 'UPGRADE user sentinels preserved'
    $payloadBefore=Get-FileHash (Join-Path $install 'GasProjectCalculator.exe')
    Run-Setup '1.2.0' 'reinstall'
    Check-Sentinel
    if((Get-FileHash (Join-Path $install 'GasProjectCalculator.exe')).Hash -ne $payloadBefore.Hash){throw 'Reinstall changed payload'}
    Write-Output 'REINSTALL payload hash and user sentinels preserved'
    $uninstall=Join-Path $install 'unins000.exe'
    $args=@('/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART',"/LOG=`"$logPrefix-uninstall.log`"")
    Write-Output "COMMAND CWD=$root EXE=$uninstall ARGS=$args"
    $p=Start-Process -FilePath $uninstall -ArgumentList $args -WindowStyle Hidden -PassThru -Wait
    Write-Output "uninstall exit=$($p.ExitCode)"
    if($p.ExitCode){throw 'Uninstall failed'}
    Check-Sentinel
    if(Test-Path (Join-Path $install 'GasProjectCalculator.exe')){throw 'Executable remains after uninstall'}
    if(Test-Path -LiteralPath $key){throw 'Isolated uninstall registration remains'}
    foreach($link in $links){if(Test-Path -LiteralPath $link){throw 'Isolated shortcut remains'}}
    Write-Output 'UNINSTALL removed program/registration/shortcuts, preserved both user files'
} finally {
    if(Test-Path -LiteralPath $key){
        $location=(Get-ItemProperty -LiteralPath $key).InstallLocation
        if($location.TrimEnd('\') -eq $install){Remove-Item -LiteralPath $key -Recurse}
        elseif($location -ne $beforeLocation){throw "Unexpected registry owner: $location"}
    }
    & reg.exe import "$backup\uninstall.reg"
    if($LASTEXITCODE){throw 'Registry restore failed'}
    for($i=0;$i -lt $links.Count;$i++){
        if($linkState[$i].exists){Copy-Item -LiteralPath "$backup\$i.lnk" -Destination $links[$i] -Force}
        elseif(Test-Path -LiteralPath $links[$i]){
            $shell=New-Object -ComObject WScript.Shell
            if($shell.CreateShortcut($links[$i]).TargetPath -ne (Join-Path $install 'GasProjectCalculator.exe')){throw 'Unexpected shortcut owner'}
            Remove-Item -LiteralPath $links[$i]
        }
        if($linkState[$i].exists -and (Get-FileHash -LiteralPath $links[$i]).Hash -ne $linkState[$i].hash){throw 'Shortcut restore hash mismatch'}
    }
    & reg.exe export $reg "$backup\restored.reg" /y
    if((Get-FileHash "$backup\restored.reg").Hash -ne $beforeReg){throw 'Registry restore export mismatch'}
    $after=Snapshot
    $after | Set-Content "$backup\user-install-after.json"
    if($before -ne $after){throw 'User installation changed'}
    foreach($p in $protected){if((Get-Process -Id $p.Id).StartTime -ne $p.StartTime){throw 'Protected process replaced'}}
    Write-Output 'RESTORED: exact HKCU export, exact shortcut hashes, all 106 user files and protected process start times unchanged'
}
Write-Output 'CYCLE_COMPLETE'
