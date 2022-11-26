import sys
import os
import platform
import shutil

from glob import glob

pyver = platform.python_version_tuple()[0] + '.' +  platform.python_version_tuple()[1]

# Clean resources
def clean(glob_path: str = "", to_be_kept=None, to_be_deleted=None):
    to_be_kept = to_be_kept or []
    to_be_deleted = to_be_deleted or []

    if to_be_kept and glob_path:
        for f in glob(glob_path):
            if not any({k in f for k in to_be_kept}):
                to_be_deleted.append(f)

    for p in to_be_deleted:
        if os.path.exists(p):
            if os.path.isdir(p):
                shutil.rmtree(p, ignore_errors=True)
            else:
                os.remove(p)


def clean_resources(app_path: str):
    PATH = '{app_path}/Contents/Resources/'

    to_be_kept = []
    to_be_deleted = []

    clean(f'{PATH}/qt*', to_be_deleted=to_be_deleted, to_be_kept=to_be_kept)


def clean_pyside6(app_path: str):
    # Clean PySide6 folder

    PATH = f'{app_path}/Contents/Resources/lib/python{pyver}/PySide6'

    shutil.rmtree(f'{PATH}/examples', ignore_errors=True)
    shutil.rmtree(f'{PATH}/include', ignore_errors=True)
    shutil.rmtree(f'{PATH}/Qt/libexec', ignore_errors=True)

    to_be_kept = ['QtCore', 'QtGui', 'QtWidgets']
    to_be_deleted = []

    for f in glob(f'{PATH}/Qt*'):
        if not any({k in f for k in to_be_kept}):
            to_be_deleted.append(f)

    for a in glob(f'{PATH}/*.app'):
        to_be_deleted.append(a)

    to_be_deleted.remove(f'{PATH}/Qt')
    to_be_deleted.extend([
        f'{PATH}/lupdate',
        f'{PATH}/qmllint',
        f'{PATH}/lrelease',
        f'{PATH}/qmlformat',
        f'{PATH}/qmlls',
    ])
    clean(to_be_deleted=to_be_deleted)


def clean_qt(app_path: str):
    # Clean PySide6/Qt folder

    PATH = f'{app_path}/Contents/Resources/lib/python{pyver}/PySide6/Qt'

    to_be_deleted = [f'{PATH}/qml', f'{PATH}/translations']

    clean(to_be_deleted=to_be_deleted)


def clean_lib(app_path: str):
    # Clean PySide6/Qt/lib folder

    PATH = f'{app_path}/Contents/Resources/lib/python{pyver}/PySide6/Qt/lib'

    to_be_kept = ['QtCore', 'QtDBus', 'QtGui', 'QtWidgets']
    to_be_deleted = [f'{PATH}/metatypes']

    clean(f'{PATH}/Qt*', to_be_kept=to_be_kept, to_be_deleted=to_be_deleted)


def clean_plugins(app_path: str):
    # Clean PySide6/Qt/plugins folder
    PATH = f'{app_path}/Contents/Resources/lib/python{pyver}/PySide6/Qt/plugins'

    to_be_kept = ['platforms', 'styles']
    to_be_deleted = []

    clean(f'{PATH}/*', to_be_kept=to_be_kept, to_be_deleted=to_be_deleted)


def symlink_shiboken(app_path: str):
    # symlink .so from shiboken6 to PySide6 folder
    cwd = os.getcwd()

    FROM = f'{app_path}/Contents/Resources/lib/python{pyver}/shiboken6'
    TO = f'{app_path}/Contents/Resources/lib/python{pyver}/PySide6'

    fn = os.path.basename(glob(f'{FROM}/libshiboken6*.dylib')[0])

    os.chdir(TO)
    os.symlink(f'../shiboken6/{fn}', f'./{fn}')
    os.chdir(cwd)


def main():
    app_path = sys.argv[1]

    clean_resources(app_path)
    clean_pyside6(app_path)
    clean_qt(app_path)
    clean_lib(app_path)
    clean_plugins(app_path)
    symlink_shiboken(app_path)

main()
