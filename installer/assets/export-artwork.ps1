# Convert the accepted local VP-01 artwork into Inno's native bitmap format.
# No downloads, render engine or additional packages are needed.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
foreach ($name in @('sidebar', 'header')) {
    $source = Join-Path $projectRoot "frontend/assets/installer-$name.png"
    $destination = Join-Path $PSScriptRoot "wizard-$name.bmp"
    $image = [System.Drawing.Image]::FromFile($source)
    $bitmap = [System.Drawing.Bitmap]::new($image.Width, $image.Height, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    try {
        $graphics.Clear([System.Drawing.Color]::White)
        $graphics.DrawImageUnscaled($image, 0, 0)
        $bitmap.Save($destination, [System.Drawing.Imaging.ImageFormat]::Bmp)
        Write-Output "$destination ($($image.Width)x$($image.Height), 24-bit BMP)"
    } finally {
        $graphics.Dispose()
        $bitmap.Dispose()
        $image.Dispose()
    }
}
