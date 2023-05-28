import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('numpy')
install('pygame')
install('pygame_gui')
install('datetime')
install('astropy')
install('sunpy')
