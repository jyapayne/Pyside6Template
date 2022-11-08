import sys
from py2app.util import codesign_adhoc

APPDIR = sys.argv[1]

codesign_adhoc(APPDIR)
