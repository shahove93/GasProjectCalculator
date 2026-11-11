# Verify the installed GasProjectCalculator runtime: no Python prerequisite,
# native window, loopback-only backend, occupied-port handling, all three
# calculation modes, window-close shutdown, and the understandable error path.
#
# Usage (from the repository root, after installer\verify-install.ps1):
#   powershell -ExecutionPolicy Bypass -File installer\verify-runtime.ps1 `
#       -WorkDir C:\Users\user\AppData\Local\Temp\opencode\wi02-runtime

[CmdletBinding()]
param(
    [string]$InstallDir = (Join-Path $env:LOCALAPPDATA 'Programs\GasProjectCalculator'),
    [string]$WorkDir = (Join-Path $env:TEMP 'opencode-wi02-runtime')
)

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }

$exe = Join-Path $InstallDir 'GasProjectCalculator.exe'
if (-not (Test-Path -LiteralPath $exe)) {
    throw "Installed executable not found: $exe. Run installer\verify-install.ps1 first."
}
$workDirFull = [System.IO.Path]::GetFullPath($WorkDir)
Remove-Item -LiteralPath $workDirFull -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $workDirFull | Out-Null
$portFile = Join-Path $workDirFull 'port.json'
$logFile = Join-Path $workDirFull 'desktop.log'
$errorPortFile = Join-Path $workDirFull 'error-port.json'
$errorLogFile = Join-Path $workDirFull 'error-desktop.log'
$occupiedPort = 8123

Write-Output "=== WI-02 installed runtime verification ==="
Write-Output "Timestamp: $(Get-Date -Format o)"
Write-Output "Installed exe: $exe"
Write-Output ("Installed exe SHA256: " + (Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash)
Write-Output "Work directory: $workDirFull"

# I5: PE subsystem 2 == WINDOWS_GUI (no console window).
$bytes = [System.IO.File]::ReadAllBytes($exe)
$peOffset = [BitConverter]::ToInt32($bytes, 0x3C)
$subsystem = [BitConverter]::ToUInt16($bytes, $peOffset + 0x5C)
$subsystemName = switch ($subsystem) {
    2 { 'WINDOWS_GUI (no console)' }
    3 { 'WINDOWS_CUI (console)' }
    default { "unknown($subsystem)" }
}
Write-Output "PE subsystem: $subsystem $subsystemName"
if ($subsystem -ne 2) {
    throw "Installed executable is not a windowed build (subsystem $subsystem)"
}

# Precompile the Win32 helper before the PATH is stripped.
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class Wi02Win32 {
    [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    [DllImport("user32.dll", SetLastError = true)]
    public static extern bool PostMessage(IntPtr hWnd, uint Msg, IntPtr wParam, IntPtr lParam);
}
"@

function Wait-PortFile([string]$path, [int]$timeoutSeconds) {
    $deadline = (Get-Date).AddSeconds($timeoutSeconds)
    while (-not (Test-Path -LiteralPath $path)) {
        if ((Get-Date) -gt $deadline) { throw "Port file was not written within ${timeoutSeconds}s: $path" }
        Start-Sleep -Milliseconds 200
    }
    return Get-Content -LiteralPath $path -Raw
}

function Invoke-JsonPost([string]$base, [string]$path, [string]$body) {
    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($body)
    $response = Invoke-WebRequest -Method Post -Uri "$base$path" -ContentType 'application/json; charset=utf-8' -Body $bodyBytes -UseBasicParsing
    # Decode the raw response bytes as UTF-8 so Cyrillic values survive PowerShell 5.1.
    $text = [System.Text.Encoding]::UTF8.GetString($response.RawContentStream.ToArray())
    Write-Output "HTTP $($response.StatusCode) raw response: $text"
    return ($text | ConvertFrom-Json)
}

$savedPath = $env:PATH
$occupiedListener = $null
try {
    # I5: strip Python from PATH; the installed exe must still launch.
    $env:PATH = 'C:\Windows\System32;C:\Windows'
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
    Write-Output ""
    Write-Output "=== I5: Python-free PATH ==="
    Write-Output "PATH=$env:PATH"
    Write-Output ("python command after PATH strip: " + $(if ($pythonCommand) { $pythonCommand.Source } else { '<not found>' }))
    if ($pythonCommand) {
        throw "python is still resolvable after PATH strip"
    }

    # I8: hold an unrelated listener on the preferred port.
    $occupiedListener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Parse('127.0.0.1'), $occupiedPort)
    $occupiedListener.Start()
    Write-Output ""
    Write-Output "=== I8: occupied-port scenario ==="
    Write-Output "Holding a test listener on 127.0.0.1:$occupiedPort"
    Get-NetTCPConnection -State Listen -LocalPort $occupiedPort -ErrorAction SilentlyContinue |
        Format-Table LocalAddress,LocalPort,OwningProcess -AutoSize | Out-String | Write-Output

    $argumentLine = "--preferred-port $occupiedPort --port-file `"$portFile`" --auto-close-seconds 40 --log-file `"$logFile`""
    Write-Output ""
    Write-Output "Launch: & `"$exe`" $argumentLine"
    $process = Start-Process -FilePath $exe -ArgumentList $argumentLine -PassThru
    Write-Output "Started PID=$($process.Id)"

    # I6: the port file is written only after the backend answers 200.
    $portRaw = Wait-PortFile $portFile 30
    $portInfo = $portRaw | ConvertFrom-Json
    Write-Output "Port file: $portRaw"
    $port = [int]$portInfo.port
    if ($portInfo.status -ne 'ready') { throw "Backend did not report ready: $portRaw" }
    if ($port -eq $occupiedPort) { throw "Backend did not skip the occupied port $occupiedPort" }
    Write-Output "Backend selected port $port after skipping occupied $occupiedPort"

    # I8: loopback-only listener.
    Write-Output ""
    Write-Output "=== I8: backend listener addresses ==="
    $listeners = Get-NetTCPConnection -State Listen -OwningProcess $process.Id -ErrorAction SilentlyContinue
    $listeners | Format-Table LocalAddress,LocalPort,OwningProcess -AutoSize | Out-String | Write-Output
    if (-not $listeners) { throw "No listener found for installed process $($process.Id)" }
    $nonLoopback = $listeners | Where-Object { $_.LocalAddress -ne '127.0.0.1' }
    if ($nonLoopback) { throw "Non-loopback listener detected: $($nonLoopback | Out-String)" }

    # I6: native window appears after readiness.
    Write-Output ""
    Write-Output "=== I6: native window after backend readiness ==="
    $processInfo = Get-Process -Id $process.Id
    Write-Output "Process name: $($processInfo.ProcessName)"
    Write-Output "MainWindowHandle immediately: $($processInfo.MainWindowHandle)"
    $deadline = (Get-Date).AddSeconds(20)
    while ($processInfo.MainWindowHandle -eq 0 -and (Get-Date) -lt $deadline) {
        Start-Sleep -Milliseconds 300
        $processInfo.Refresh()
    }
    if ($processInfo.MainWindowHandle -eq 0) { throw "Native window did not appear" }
    $windowSeen = Get-Date
    Write-Output "MainWindowHandle: $($processInfo.MainWindowHandle)"
    Write-Output "MainWindowTitle: $($processInfo.MainWindowTitle)"
    $portFileTime = (Get-Item -LiteralPath $portFile).LastWriteTime
    Write-Output "Port file written: $($portFileTime.ToString('o'))"
    Write-Output "Window observed:   $($windowSeen.ToString('o'))"
    if ($windowSeen -lt $portFileTime) { throw "Window was observed before the backend readiness port file" }

    # I7: all three modes against the installed backend.
    $base = "http://127.0.0.1:$port"
    Write-Output ""
    Write-Output "=== I7: GET / ==="
    $rootResponse = Invoke-WebRequest -Uri "$base/" -UseBasicParsing
    Write-Output "HTTP $($rootResponse.StatusCode) content-type=$($rootResponse.Headers['Content-Type']) length=$($rootResponse.Content.Length)"
    Write-Output ("Contains title marker: " + ($rootResponse.Content -match 'GasProjectCalculator'))

    Write-Output ""
    Write-Output "=== I7: POST /calculate (GSN) ==="
    $gsnBody = '{"customer_type":"\u044e\u0440\u0438\u0434\u0438\u0447\u0435\u0441\u043a\u043e\u0435 \u043b\u0438\u0446\u043e","length":14,"angles":2,"hdd":false,"excavator_hours":4,"hydraulic_hammer":false,"is_district":true,"has_grpsh":false}'
    Write-Output "Request body: $gsnBody"
    $gsn = Invoke-JsonPost $base '/calculate' $gsnBody
    Write-Output ("Response: " + ($gsn | ConvertTo-Json -Compress))
    Write-Output "GSN subtotal=$($gsn.subtotal) vat=$($gsn.vat) total=$($gsn.total)"

    Write-Output ""
    Write-Output "=== I7: POST /calculate/gsv ==="
    $gsvBody = '{"customer_type":"\u0447\u0430\u0441\u0442\u043d\u043e\u0435 \u043b\u0438\u0446\u043e","length":8,"diameter":25,"drilling_holes":2,"sakz_sets":1,"has_panel":true,"is_district":true}'
    Write-Output "Request body: $gsvBody"
    $gsv = Invoke-JsonPost $base '/calculate/gsv' $gsvBody
    Write-Output ("Response: " + ($gsv | ConvertTo-Json -Compress))
    Write-Output "GSV subtotal=$($gsv.subtotal) vat=$($gsv.vat) total=$($gsv.total)"

    Write-Output ""
    Write-Output "=== I7: POST /calculate/combined ==="
    $combinedBody = '{"customer_type":"\u0447\u0430\u0441\u0442\u043d\u043e\u0435 \u043b\u0438\u0446\u043e","is_district":true,"gsn":{"length":10,"angles":0,"hdd":false,"excavator_hours":0,"hydraulic_hammer":false,"has_grpsh":false},"gsv":{"length":5,"diameter":25,"drilling_holes":0,"sakz_sets":0,"has_panel":false}}'
    Write-Output "Request body: $combinedBody"
    $combined = Invoke-JsonPost $base '/calculate/combined' $combinedBody
    Write-Output ("Response: " + ($combined | ConvertTo-Json -Depth 5 -Compress))
    Write-Output "Combined subtotal=$($combined.subtotal) vat=$($combined.vat) total=$($combined.total)"

    # I9: the auto-close hook destroys the window; the process and backend must exit.
    Write-Output ""
    Write-Output "=== I9: closing the window stops the application and backend ==="
    $process.WaitForExit(90000) | Out-Null
    Write-Output "Process HasExited: $($process.HasExited)"
    Write-Output "Process ExitCode: $($process.ExitCode)"
    $stillRunning = Get-Process -Id $process.Id -ErrorAction SilentlyContinue
    Write-Output ("Process still present: " + $(if ($stillRunning) { 'YES' } else { 'no' }))
    $remaining = Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue
    Write-Output ("Listeners on port ${port} after exit: " + $(if ($remaining) { ($remaining | Out-String) } else { '<none>' }))
    if ($stillRunning) { throw "Installed process did not exit after window close" }
    if ($remaining) { throw "Backend port $port is still listening after window close" }
    Write-Output "Child processes of installed PID (should be none):"
    Get-CimInstance Win32_Process -Filter "ParentProcessId=$($process.Id)" -ErrorAction SilentlyContinue |
        Select-Object ProcessId,Name,CommandLine | Format-Table -AutoSize | Out-String | Write-Output

    Write-Output ""
    Write-Output "=== Desktop log (I6/I7/I9) ==="
    Get-Content -LiteralPath $logFile -Encoding UTF8 | Write-Output

    # I10: understandable launch failure with the native dialog.
    Write-Output ""
    Write-Output "=== I10: launch failure path ==="
    $errorArgumentLine = "--simulate-startup-failure --port-file `"$errorPortFile`" --log-file `"$errorLogFile`""
    Write-Output "Launch: & `"$exe`" $errorArgumentLine"
    $errorProcess = Start-Process -FilePath $exe -ArgumentList $errorArgumentLine -PassThru
    Write-Output "Started PID=$($errorProcess.Id)"
    $deadline = (Get-Date).AddSeconds(20)
    $dialogHandle = [IntPtr]::Zero
    while ($dialogHandle -eq [IntPtr]::Zero -and (Get-Date) -lt $deadline) {
        Start-Sleep -Milliseconds 200
        # The message box class is #32770; passing $null for the class name from
        # PowerShell marshals as an empty string, so query the class explicitly.
        $dialogHandle = [Wi02Win32]::FindWindow('#32770', 'GasProjectCalculator')
    }
    Write-Output "Error dialog handle: $dialogHandle"
    if ($dialogHandle -eq [IntPtr]::Zero) {
        Stop-Process -Id $errorProcess.Id -Force -ErrorAction SilentlyContinue
        throw "Native launch-failure dialog was not observed"
    }
    # WM_CLOSE == 0x0010
    [Wi02Win32]::PostMessage($dialogHandle, 0x0010, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null
    $errorProcess.WaitForExit(15000) | Out-Null
    if (-not $errorProcess.HasExited) {
        Stop-Process -Id $errorProcess.Id -Force -ErrorAction SilentlyContinue
        throw "Launch-failure process did not exit after closing the dialog"
    }
    Write-Output "Error process exit code: $($errorProcess.ExitCode)"
    Write-Output "Error port file:"
    if (Test-Path -LiteralPath $errorPortFile) { Get-Content -LiteralPath $errorPortFile -Raw | Write-Output }
    Write-Output "Error desktop log:"
    Get-Content -LiteralPath $errorLogFile -Encoding UTF8 | Write-Output
    if ($errorProcess.ExitCode -ne 1) {
        throw "Launch-failure process should exit 1, got $($errorProcess.ExitCode)"
    }
    $errorPortInfo = Get-Content -LiteralPath $errorPortFile -Raw | ConvertFrom-Json
    if ($errorPortInfo.status -ne 'failed') {
        throw "Error port file did not report a failed status"
    }
} finally {
    if ($occupiedListener) {
        try { $occupiedListener.Stop() } catch { }
    }
    $env:PATH = $savedPath
}

Write-Output "=== Installed runtime verification complete ==="

