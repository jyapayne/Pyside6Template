from setuptools import setup
from glob import glob
from datetime import datetime
from package_alias import package

info = package.info

name = info.name
version = info.version
bundle_identifier = info.bundle_identifier
module_name = info.module_name

APP = [f'pyinstaller.py']
DATA_FILES = [
    ('resources', glob(module_name + '/resources/*')),
]
OPTIONS = {
    'arch': 'universal2',
    'optimize': 2,
    'iconfile': module_name + '/resources/icon.icns',
    'includes': {'PySide6.QtCore', 'PySide6.QtUiTools', 'PySide6.QtGui', 'PySide6.QtWidgets', 'certifi', },
    'excludes': {'tkinter', "unittest"},
    'qt_plugins': [
        'platforms/libqcocoa.dylib',
        'platforms/libqminimal.dylib',
        'platforms/libqoffscreen.dylib',
        'styles/libqmacstyle.dylib'
    ],
    'argv_emulation': True,
    'plist': {
        'CFBundleName': name,
        'CFBundleShortVersionString': version,
        'CFBundleIdentifier': bundle_identifier,
        'LSMinimumSystemVersion': '10.12.0',
        'NSHumanReadableCopyright': f'Copyright © {datetime.now().year} {name} All Rights Reserved',
    }
}

setup(
    app=APP,
    name=name,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
