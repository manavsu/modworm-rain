# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['rain.py'],
    pathex=[],
    binaries=[],
    datas=[('LICENSE.txt', '.'), ('README.md', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='rain',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True, # Strip symbols from the binary, harder to debug smaller size
    upx=True,
    console=True,
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
    strip=True, # Strip symbols from the binary, harder to debug smaller size
    upx=True,
    upx_exclude=[],
    name='rain',
)
