from setuptools import setup
from glob import glob
from datetime import datetime

module_name = "project"
name = "Project"
version = ""
main_file = "main.py"

# Overrides the above
exec(open("info.py").read())


APP = [f'{module_name}/{main_file}']
DATA_FILES = [
    ('resources', glob(module_name + '/resources/*.png') + glob(module_name + '/resources/*.rtf') + glob(module_name + '/resources/*.txt')),
]
OPTIONS = {
    'iconfile': module_name + '/resources/icon.icns',
    'extra_scripts': 'info.py',
    'includes': {'PySide6.QtCore', 'PySide6.QtUiTools', 'PySide6.QtGui', 'PySide6.QtWidgets', 'certifi', 'cffi', 'pem'},
    'excludes': {'tkinter'},
    'qt_plugins': [
        'platforms/libqcocoa.dylib',
        'platforms/libqminimal.dylib',
        'platforms/libqoffscreen.dylib',
        'styles/libqmacstyle.dylib'
    ],
    'plist': {
        'CFBundleName': name,
        'CFBundleShortVersionString': version,
        'CFBundleIdentifier': f'pl.{module_name}.{name}',
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
