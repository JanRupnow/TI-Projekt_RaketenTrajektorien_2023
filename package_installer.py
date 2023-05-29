import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

package_list = ["numpy", "pygame", "pygame_gui", "datetime", "astropy", "sunpy"]

for package in package_list:
    install(package)