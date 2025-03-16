# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_dynamic_libs, copy_metadata, collect_data_files, collect_submodules
import os

block_cipher = None

added_files = [
    *copy_metadata('pytest'),
    *copy_metadata('pytest_html'),
    *copy_metadata('pluggy'),
    *collect_data_files('_pytest'),
    *copy_metadata('pytest_metadata'),
    *collect_data_files('pytest_html'),
    *copy_metadata('pytest_html'),
    *collect_data_files('jinja2'),
    *collect_data_files('pluggy', include_py_files=True),
    *copy_metadata('pytest_tagging'),
]

hidden_imports = [
    'pytest',
    '_pytest',
    'pluggy',
    'jinja2',
    'jinja2.ext',
    *collect_submodules('pytest_metadata'),
    *collect_submodules('pytest_html'),
    *collect_submodules('pytest_tagging'),
    *collect_submodules('toolkit'),
    *collect_submodules('tests'),
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
