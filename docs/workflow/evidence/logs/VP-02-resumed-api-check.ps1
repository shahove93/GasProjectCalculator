$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }
$root = 'D:\Antigravity\GasProjectCalculator'
$work = 'C:\Users\user\AppData\Local\Temp\opencode\vp-02-resume'
$logDir = Join-Path $root 'docs\workflow\evidence\logs'
$port = (Get-Content "$work\port.json" -Raw | ConvertFrom-Json).port
$base = "http://127.0.0.1:$port"

function Invoke-Post([string]$path, $payload) {
    $json = $payload | ConvertTo-Json -Depth 10 -Compress
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
    try {
        $resp = Invoke-WebRequest -Method Post -Uri "$base$path" -ContentType 'application/json; charset=utf-8' -Body $bytes -UseBasicParsing
        $text = [System.Text.Encoding]::UTF8.GetString($resp.RawContentStream.ToArray())
        return [pscustomobject]@{ path = $path; request = $payload; status = [int]$resp.StatusCode; response = ($text | ConvertFrom-Json); raw = $text }
    } catch {
        $status = 0
        $text = ''
        $ex = $_.Exception
        if ($ex.Response -and $ex.Response.StatusCode) {
            $status = [int]$ex.Response.StatusCode
        }
        if ($_.ErrorDetails -and $_.ErrorDetails.Message) {
            $text = $_.ErrorDetails.Message
        } elseif ($ex.Response) {
            try {
                $stream = $ex.Response.GetResponseStream()
                $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
                $text = $reader.ReadToEnd()
            } catch { }
        }
        return [pscustomobject]@{ path = $path; request = $payload; status = $status; response = $null; raw = $text }
    }
}

$mixedInputs = @(
    @{ name='D1'; up_to_25=4; from_32_to_40=0; diameter_57=4; expected=75600 },
    @{ name='D2'; up_to_25=2; from_32_to_40=4; diameter_57=3; expected=79275 },
    @{ name='D3'; up_to_25=0; from_32_to_40=5; diameter_57=2; expected=71400 },
    @{ name='D4'; up_to_25=3; from_32_to_40=1; diameter_57=1; expected=63000 },
    @{ name='D5'; up_to_25=8; from_32_to_40=0; diameter_57=0; expected=70875 }
)
$results = [ordered]@{}
$summary = @()
foreach ($c in $mixedInputs) {
    $payload = [ordered]@{
        customer_type = 'частное лицо'
        is_district = $false
        pipe_lengths = [ordered]@{ up_to_25=$c.up_to_25; from_32_to_40=$c.from_32_to_40; diameter_57=$c.diameter_57 }
        drilling_holes = 0
        sakz_sets = 0
        has_panel = $false
    }
    $r = Invoke-Post '/calculate/gsv' $payload
    $results[$c.name] = $r
    $summary += ("{0}: input={1}/{2}/{3} status={4} total={5} expected={6} total_length={7} breakdown={8} keys={9}" -f `
        $c.name, $c.up_to_25, $c.from_32_to_40, $c.diameter_57, $r.status, $r.response.total, $c.expected, $r.response.total_length, ($r.response.pipe_breakdown | ConvertTo-Json -Depth 5 -Compress), (($r.response.PSObject.Properties.Name) -join ','))
    if ([int]$r.response.total -ne $c.expected) { throw "$($c.name) total mismatch: $($r.response.total) != $($c.expected)" }
}

# Combined example: GSN 10 m without options 75 600 with district VAT; GSV 4/0/4 without other options 82 950 with district VAT.
$combinedPayload = [ordered]@{
    customer_type = 'частное лицо'
    is_district = $true
    gsn = [ordered]@{ length=10; angles=0; hdd=$false; excavator_hours=0; hydraulic_hammer=$false; has_grpsh=$false }
    gsv = [ordered]@{ pipe_lengths=[ordered]@{ up_to_25=4; from_32_to_40=0; diameter_57=4 }; drilling_holes=0; sakz_sets=0; has_panel=$false }
}
$combined = Invoke-Post '/calculate/combined' $combinedPayload
$results['combined'] = $combined
$summary += ("combined: status={0} gsn.total={1} gsv.total={2} subtotal={3} vat={4} total={5} expected_total=158550" -f $combined.status, $combined.response.gsn.total, $combined.response.gsv.total, $combined.response.subtotal, $combined.response.vat, $combined.response.total)
if ([int]$combined.response.total -ne 158550 -or [int]$combined.response.subtotal -ne 151000 -or [int]$combined.response.vat -ne 7550) { throw 'combined benchmark mismatch' }

# Mixed with options: D1 + SAKZ 1 + panel + district -> 97 000 + VAT 4 850 = 101 850.
$optionsPayload = [ordered]@{
    customer_type = 'частное лицо'
    is_district = $true
    pipe_lengths = [ordered]@{ up_to_25=4; from_32_to_40=0; diameter_57=4 }
    drilling_holes = 0
    sakz_sets = 1
    has_panel = $true
}
$options = Invoke-Post '/calculate/gsv' $optionsPayload
$results['mixed_options'] = $options
$summary += ("mixed_options: status={0} subtotal={1} vat={2} total={3} expected=101850" -f $options.status, $options.response.subtotal, $options.response.vat, $options.response.total)
if ([int]$options.response.total -ne 101850) { throw 'mixed options benchmark mismatch' }

# Legacy GSV form must still work and keep the old response shape (no total_length / pipe_breakdown).
$legacyPayload = [ordered]@{
    customer_type = 'частное лицо'
    length = 8
    diameter = 25
    drilling_holes = 2
    sakz_sets = 1
    has_panel = $true
    is_district = $true
}
$legacy = Invoke-Post '/calculate/gsv' $legacyPayload
$results['legacy_gsv'] = $legacy
$legacyKeys = ($legacy.response.PSObject.Properties.Name) -join ','
$summary += ("legacy_gsv: status={0} total={1} expected=105525 keys={2} has_total_length={3} has_pipe_breakdown={4}" -f $legacy.status, $legacy.response.total, $legacyKeys, ($legacyKeys -match 'total_length'), ($legacyKeys -match 'pipe_breakdown'))
if ([int]$legacy.response.total -ne 105525) { throw 'legacy GSV total mismatch' }
if ($legacyKeys -match 'total_length' -or $legacyKeys -match 'pipe_breakdown') { throw 'legacy response contains mixed-only keys' }

# Mixed form conflict: pipe_lengths plus length/diameter must be rejected with 422.
$conflictPayload = [ordered]@{
    customer_type = 'частное лицо'
    is_district = $false
    pipe_lengths = [ordered]@{ up_to_25=4; from_32_to_40=0; diameter_57=4 }
    length = 4
    diameter = 25
    drilling_holes = 0
    sakz_sets = 0
    has_panel = $false
}
$conflict = Invoke-Post '/calculate/gsv' $conflictPayload
$results['mixed_422_conflict'] = $conflict
$summary += ("mixed_422_conflict: status={0} raw={1}" -f $conflict.status, $conflict.raw)
if ($conflict.status -ne 422) { throw "expected 422 for mixed form, got $($conflict.status)" }

# Panel without SAKZ must be rejected with 422.
$panelPayload = [ordered]@{
    customer_type = 'частное лицо'
    is_district = $false
    pipe_lengths = [ordered]@{ up_to_25=4; from_32_to_40=0; diameter_57=4 }
    drilling_holes = 0
    sakz_sets = 0
    has_panel = $true
}
$panel = Invoke-Post '/calculate/gsv' $panelPayload
$results['panel_without_sakz_422'] = $panel
$summary += ("panel_without_sakz_422: status={0} raw={1}" -f $panel.status, $panel.raw)
if ($panel.status -ne 422) { throw "expected 422 for panel without SAKZ, got $($panel.status)" }

# GSN regression: the MD-02 accepted example (10 m, city, no options) = 68 250;
# and the legacy RD-03 example = 131 250.
$gsnSimplePayload = [ordered]@{
    customer_type = 'частное лицо'
    length = 10
    angles = 0
    hdd = $false
    excavator_hours = 0
    hydraulic_hammer = $false
    is_district = $false
    has_grpsh = $false
}
$gsnSimple = Invoke-Post '/calculate' $gsnSimplePayload
$results['gsn_simple'] = $gsnSimple
$summary += ("gsn_simple: status={0} total={1} expected=68250" -f $gsnSimple.status, $gsnSimple.response.total)
if ([int]$gsnSimple.response.total -ne 68250) { throw 'GSN simple regression mismatch' }

$gsnLegacyPayload = [ordered]@{
    customer_type = 'юридическое лицо'
    length = 14
    angles = 2
    hdd = $false
    excavator_hours = 4
    hydraulic_hammer = $false
    is_district = $true
    has_grpsh = $false
}
$gsnLegacy = Invoke-Post '/calculate' $gsnLegacyPayload
$results['gsn_legacy'] = $gsnLegacy
$summary += ("gsn_legacy: status={0} total={1} expected=131250" -f $gsnLegacy.status, $gsnLegacy.response.total)
if ([int]$gsnLegacy.response.total -ne 131250) { throw 'GSN legacy regression mismatch' }

$jsonPath = Join-Path $logDir 'VP-02-resumed-api.json'
($results | ConvertTo-Json -Depth 20) | Set-Content -LiteralPath $jsonPath -Encoding utf8
$summaryPath = Join-Path $logDir 'VP-02-resumed-api-summary.txt'
@("Timestamp: $(Get-Date -Format o)", "Base URL: $base", "") + $summary | Set-Content -LiteralPath $summaryPath -Encoding utf8
$summary | Set-Content -LiteralPath (Join-Path $work 'api-summary.txt') -Encoding utf8
$summary
Write-Output 'API_BENCHMARKS_OK'


