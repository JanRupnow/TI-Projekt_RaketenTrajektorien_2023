import subprocess
import sys
import json

def Install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def InstallAllPackages():
    jsonFile = open("./Globals/General.json", "r+")
    
    hotkeysJson = json.load(jsonFile)
    if (not hotkeysJson["downloaded"]):
        package_list = ["numpy", "pygame", "pygame_gui", "datetime", "astropy", "sunpy", "json"]
        for package in package_list:
            Install(package)
        # Overwriting package status
        newJson = {"downloaded": True}
        jsonFile.seek(0)
        jsonFile.truncate()
        json.dump(newJson, jsonFile, indent=4, ensure_ascii=False)
        jsonFile.close()