import sys
import os
from glob import glob

info_name = 'info'
info_file = glob(os.path.join('*', f'{info_name}.py'))[0]
package_name = info_file.split(os.path.sep)[0]

package = __import__(f"{package_name}", fromlist=["main", "info"])
if package_name not in sys.modules:
    sys.modules[package_name] = package
