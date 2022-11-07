#! /bin/bash

set -x
set -e

BUILD_DIR=".debpkg"
mkdir -p "$BUILD_DIR"

# store repo root as variable
REPO_ROOT=$(readlink -f $(dirname $(dirname "$0")))
OLD_CWD=$(readlink -f .)

export VER="$(cat $REPO_ROOT/info.py | grep -w version | awk -F'"' '$0=$2')"
export PROJ_NAME="$(cat $REPO_ROOT/info.py | grep -w name | awk -F'"' '$0=$2')"
export PROJ_MOD="$(cat $REPO_ROOT/info.py | grep -w module_name | awk -F'"' '$0=$2')"
export MAIN_FILE="$(cat $REPO_ROOT/info.py | grep -w main_file | awk -F'"' '$0=$2')"
export BUNDLE_ID="$(cat $REPO_ROOT/info.py | grep -w bundle_identifier | awk -F'"' '$0=$2')"
export PROJECT_LICENSE="$(cat $REPO_ROOT/info.py | grep -w project_license | awk -F'"' '$0=$2')"
export SCREENSHOT="$(cat $REPO_ROOT/info.py | grep -w screenshot | awk -F'"' '$0=$2')"
export METADATA_LICENSE="$(cat $REPO_ROOT/info.py | grep -w metadata_license | awk -F'"' '$0=$2')"
export DESCRIPTION="$(cat $REPO_ROOT/info.py | grep -w description | awk -F'"' '$0=$2')"
export HOMEPAGE="$(cat $REPO_ROOT/info.py | grep -w homepage | awk -F'"' '$0=$2')"
export SUMMARY="$(cat $REPO_ROOT/info.py | grep -w summary | awk -F'"' '$0=$2')"
export CATEGORIES="$(cat $REPO_ROOT/info.py | grep -w categories | awk -F'"' '$0=$2')"
export MIMETYPE="$(cat $REPO_ROOT/info.py | grep -w mimetype | awk -F'"' '$0=$2')"
export KEYWORDS="$(cat $REPO_ROOT/info.py | grep -w keywords | awk -F'"' '$0=$2')"
export APP_TYPE="$(cat $REPO_ROOT/info.py | grep -w application_type | awk -F'"' '$0=$2')"
export MAIN_MOD="$(cat $REPO_ROOT/info.py | grep -w main_module | awk -F'"' '$0=$2')"
export EMAIL="$(cat $REPO_ROOT/info.py | grep -w email | awk -F'"' '$0=$2')"

pushd "$BUILD_DIR"

# move and rename .desktop file
cat > $PROJ_MOD.desktop <(envsubst < $REPO_ROOT/ci/projectemplate.desktop)


mkdir -p $PROJ_MOD/usr/bin

chmod +x $REPO_ROOT/$PROJ_MOD-bin
cp $REPO_ROOT/$PROJ_MOD-bin $PROJ_MOD/usr/bin/$PROJ_MOD

mkdir -p $PROJ_MOD/usr/share/applications
mkdir -p $PROJ_MOD/usr/lib/$PROJ_MOD
chmod +x $PROJ_MOD/usr/bin/$PROJ_MOD
cp $PROJ_MOD.desktop $PROJ_MOD/usr/share/applications
chmod +x $PROJ_MOD/usr/share/applications/$PROJ_MOD.desktop
mkdir -p $PROJ_MOD/DEBIAN
