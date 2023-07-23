import json
import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def install_all_packages():
    json_file = open("./Globals/General.json", "r+")

    hotkeys_json = json.load(json_file)
    if not hotkeys_json["downloaded"]:
        package_list = ["numpy", "pygame", "pygame_gui", "datetime", "astropy", "sunpy", "json"]
        for package in package_list:
            install(package)
        # Overwriting package status
        new_json = {"downloaded": True}
        json_file.seek(0)
        json_file.truncate()
        json.dump(new_json, json_file, indent=4, ensure_ascii=False)
        json_file.close()
