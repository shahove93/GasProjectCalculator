# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller onedir spec for the GasProjectCalculator desktop application."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

project_root = Path(SPECPATH).resolve().parent
frontend_index = project_root / "frontend" / "index.html"
splash_page = project_root / "frontend" / "splash.html"
frontend_assets = project_root / "frontend" / "assets"
if not frontend_index.is_file():
    raise SystemExit(f"Missing frontend asset: {frontend_index}")
if not splash_page.is_file():
    raise SystemExit(f"Missing splash asset: {splash_page}")

datas = [
    (str(frontend_index), "frontend"),
    (str(splash_page), "frontend"),
]
if frontend_assets.is_dir():
    datas.append((str(frontend_assets), "frontend/assets"))

# uvicorn imports its protocol/lifespan implementations lazily.
hiddenimports = collect_submodules("uvicorn")
hiddenimports += [
    "app.desktop_launcher",
    "app.main",
    "app.calculator",
    "app.gsv_calculator",
    "app.resources",
    # pywebview selects its backend lazily at runtime.
    "webview.platforms.winforms",
    "webview.platforms.edgechromium",
    "webview.platforms.mshtml",
    "webview.state",
    "webview.util",
    "webview.window",
    "webview.http",
    "webview.menu",
    "webview.screen",
    "webview.event",
    "webview.errors",
    "webview.dom",
    # pythonnet / clr loading in a frozen build.
    "clr",
    "clr_loader",
    "pythonnet",
]

a = Analysis(
    [str(project_root / "desktop_app.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["pytest", "_pytest"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="GasProjectCalculator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="GasProjectCalculator",
)
