from package_alias import package_name, package

with open("pyinstaller.py", "w+") as f:
    f.writelines([
        f"from {package_name} import {package.info.main_module}\n",
        f"{package.info.main_module}.main()"
    ])
