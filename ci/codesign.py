# -*- coding: utf-8 -*-
import os
import shutil
import sys
from pathlib import Path
from typing import Generator, List, Optional

from macholib.MachO import MachO

import contextlib
import fcntl
import os
import subprocess
import sys
import time

from macholib.util import is_platform_file

def _dosign(*path):
    with reset_blocking_status():
        subprocess.check_call(
            (
                "codesign",
                "--deep",
                "--force",
                "-s",
                "-",
                "--preserve-metadata=identifier,entitlements,flags,runtime",
                "-f",
                "-vvvv",
            )
            + path,
        )

def _macho_find(path):
    for basename, _dirs, files in os.walk(path):
        for fn in files:
            path = os.path.join(basename, fn)
            if is_platform_file(path):
                yield path

def codesign_adhoc(bundle):
    """
    (Re)sign a bundle

    Signing should be done "depth-first", sign
    libraries before signing the libraries/executables
    linking to them.

    The current implementation is a crude hack,
    but is better than nothing. Signing properly requires
    performing a topological sort using dependencies.

    "codesign" will resign the entire bundle, but only
    if partial signatures are valid.
    """
    # try:
    #    _dosign(bundle)
    #    return
    # except subprocess.CalledProcessError:
    #    pass

    platfiles = list(_macho_find(bundle))
    print("sign", platfiles)
    while platfiles:
        failed = []
        for file in platfiles:
            failed = []
            try:
                _dosign(file)
            except subprocess.CalledProcessError:
                failed.append(file)
        if failed == platfiles:
            raise RuntimeError("Cannot sign bundle %r" % (bundle,))
        platfiles = failed

    for _ in range(5):
        try:
            _dosign(bundle)
            break
        except subprocess.CalledProcessError:
            time.sleep(1)
            continue


@contextlib.contextmanager
def reset_blocking_status():
    """
    Contextmanager that resets the non-blocking status of
    the std* streams as necessary. Used with all calls of
    xcode tools, mostly because ibtool tends to set the
    std* streams to non-blocking.
    """
    orig_nonblocking = [
        fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_NONBLOCK for fd in (0, 1, 2)
    ]

    try:
        yield

    finally:
        for fd, is_nonblocking in zip((0, 1, 2), orig_nonblocking):
            cur = fcntl.fcntl(fd, fcntl.F_GETFL)
            if is_nonblocking:
                reset = cur | os.O_NONBLOCK
            else:
                reset = cur & ~os.O_NONBLOCK

            if cur != reset:
                print("Resetting blocking status of %s" % (fd,))
                fcntl.fcntl(fd, fcntl.F_SETFL, reset)

def create_symlink(folder: Path) -> None:
    """Create the appropriate symlink in the MacOS folder
    pointing to the Resources folder.
    """
    sibbling = Path(str(folder).replace("MacOS", ""))

    # PyQt5/Qt/qml/QtQml/Models.2
    root = str(sibbling).partition("Contents")[2].lstrip("/")
    # ../../../../
    backward = "../" * (root.count("/") + 1)
    # ../../../../Resources/PyQt5/Qt/qml/QtQml/Models.2
    good_path = f"{backward}Resources/{root}"

    folder.symlink_to(good_path)


def fix_dll(dll: Path) -> None:
    """Fix the DLL lookup paths to use relative ones for Qt dependencies.
    Inspiration: PyInstaller/depend/dylib.py:mac_set_relative_dylib_deps()
    Currently one header is pointing to (we are in the Resources folder):
        @loader_path/../../../../QtCore (it is referencing to the old MacOS folder)
    It will be converted to:
        @loader_path/../../../../../../MacOS/QtCore
    """

    def match_func(pth: str) -> Optional[str]:
        """Callback function for MachO.rewriteLoadCommands() that is
        called on every lookup path setted in the DLL headers.
        By returning None for system libraries, it changes nothing.
        Else we return a relative path pointing to the good file
        in the MacOS folder.
        """
        basename = os.path.basename(pth)
        if not basename.startswith("Qt"):
            return None
        return f"@loader_path{good_path}/{basename}"

    # Resources/PyQt5/Qt/qml/QtQuick/Controls.2/Fusion
    root = str(dll.parent).partition("Contents")[2][1:]
    # /../../../../../../..
    backward = "/.." * (root.count("/") + 1)
    # /../../../../../../../MacOS
    good_path = f"{backward}/MacOS"

    # Rewrite Mach headers with corrected @loader_path
    mach_dll = MachO(dll)
    mach_dll.rewriteLoadCommands(match_func)
    with open(mach_dll.filename, "rb+") as f:
        for header in mach_dll.headers:
            f.seek(0)
            mach_dll.write(f)
        f.seek(0, 2)
        f.flush()


def find_problematic_folders(folder: Path) -> Generator[Path, None, None]:
    """Recursively yields problematic folders (containing a dot in their name)."""
    for path in folder.iterdir():
        print(path)
        if not path.is_dir() or path.is_symlink():
            # Skip simlinks as they are allowed (even with a dot)
            continue
        if "." in path.name:
            yield path
        else:
            yield from find_problematic_folders(path)


def move_contents_to_resources(folder: Path) -> Generator[Path, None, None]:
    """Recursively move any non symlink file from a problematic folder
    to the sibbling one in Resources.
    """
    for path in folder.iterdir():
        if path.is_symlink():
            continue
        if path.name == "qml":
            yield from move_contents_to_resources(path)
        else:
            sibbling = Path(str(path).replace("MacOS", "Resources"))
            sibbling.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(path, sibbling)
            yield sibbling


def main(args: List[str]):
    """
    Fix the application to allow codesign (NXDRIVE-1301).
    Take one or more .app as arguments: "Nuxeo Drive.app".
    To overall process will:
        - move problematic folders from MacOS to Resources
        - fix the DLLs lookup paths
        - create the appropriate symbolic link
    """
    for app in args:
        name = os.path.basename(app)
        print(f">>> [{name}] Fixing Qt folder names")
        path = Path(app) / "Contents" / "MacOS"
        for folder in find_problematic_folders(path):
            for file in move_contents_to_resources(folder):
                try:
                    fix_dll(file)
                except (ValueError, IsADirectoryError):
                    continue
            shutil.rmtree(folder)
            create_symlink(folder)
            print(f" !! Fixed {folder}")
        codesign_adhoc(app)
        print(f">>> [{name}] Application fixed.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
