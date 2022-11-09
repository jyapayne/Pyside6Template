#! /bin/bash

set -x
set -e

BUILD_DIR=".debpkg"
mkdir -p "$BUILD_DIR"

# store repo root as variable
REPO_ROOT=$(readlink -f $(dirname $(dirname "$0")))
OLD_CWD=$(readlink -f .)
FILE_LOC=$(find $REPO_ROOT -name info.py)

export VER="$(cat $FILE_LOC | grep -w version | awk -F'"' '$0=$2')"
export PROJ_NAME="$(cat $FILE_LOC | grep -w name | awk -F'"' '$0=$2')"
export PROJ_MOD="$(cat $FILE_LOC | grep -w module_name | awk -F'"' '$0=$2')"
export MAIN_FILE="$(cat $FILE_LOC | grep -w main_file | awk -F'"' '$0=$2')"
export BUNDLE_ID="$(cat $FILE_LOC | grep -w bundle_identifier | awk -F'"' '$0=$2')"
export PROJECT_LICENSE="$(cat $FILE_LOC | grep -w project_license | awk -F'"' '$0=$2')"
export SCREENSHOT="$(cat $FILE_LOC | grep -w screenshot | awk -F'"' '$0=$2')"
export METADATA_LICENSE="$(cat $FILE_LOC | grep -w metadata_license | awk -F'"' '$0=$2')"
export DESCRIPTION="$(cat $FILE_LOC | grep -w description | awk -F'"' '$0=$2')"
export HOMEPAGE="$(cat $FILE_LOC | grep -w homepage | awk -F'"' '$0=$2')"
export SUMMARY="$(cat $FILE_LOC | grep -w summary | awk -F'"' '$0=$2')"
export CATEGORIES="$(cat $FILE_LOC | grep -w categories | awk -F'"' '$0=$2')"
export MIMETYPE="$(cat $FILE_LOC | grep -w mimetype | awk -F'"' '$0=$2')"
export KEYWORDS="$(cat $FILE_LOC | grep -w keywords | awk -F'"' '$0=$2')"
export APP_TYPE="$(cat $FILE_LOC | grep -w application_type | awk -F'"' '$0=$2')"
export MAIN_MOD="$(cat $FILE_LOC | grep -w main_module | awk -F'"' '$0=$2')"
export EMAIL="$(cat $FILE_LOC | grep -w email | awk -F'"' '$0=$2')"

pushd "$BUILD_DIR"

# move and rename .desktop file
cat > $PROJ_MOD.desktop <(envsubst < $REPO_ROOT/ci/projectemplate.desktop)


mkdir -p $PROJ_MOD/usr/bin/$PROJ_MOD-bin

chmod +x $REPO_ROOT/$PROJ_MOD/$PROJ_MOD
cp -r $REPO_ROOT/$PROJ_MOD/* $PROJ_MOD/usr/bin/$PROJ_MOD-bin/

cat > $PROJ_MOD/usr/bin/$PROJ_MOD <(envsubst < $REPO_ROOT/ci/bintemplate)
chmod +x $PROJ_MOD/usr/bin/$PROJ_MOD

mkdir -p $PROJ_MOD/usr/share/applications
mkdir -p $PROJ_MOD/usr/lib/$PROJ_MOD

cp $PROJ_MOD.desktop $PROJ_MOD/usr/share/applications
chmod +x $PROJ_MOD/usr/share/applications/$PROJ_MOD.desktop

mkdir -p $PROJ_MOD/DEBIAN
