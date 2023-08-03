import json
import subprocess
import sys


def install_requirements():
    try:
        with open("requirements.txt", 'r') as file:
            for line in file:
                package = line.strip()
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"Please install the requirements.txt manually.\n You have to install these following packages:")
        with open("requirements.txt", 'r') as file:
            for line in file:
                package = line.strip()
                print(package)
        print(f"You have to search for 'cmd' in your Windows search")
        print(f"Command: pip install 'package_name'=='desired_version'")
        print(f"Example: pip install numpy==1.23.5")
        sys.exit()


def package_installer():
    json_file = open("./Globals/General.json", "r+")

    hotkeys_json = json.load(json_file)
    if not hotkeys_json["downloaded"]:
        install_requirements()
        # Overwriting package status
        new_json = {"downloaded": True}
        json_file.seek(0)
        json_file.truncate()
        json.dump(new_json, json_file, indent=4, ensure_ascii=False)
        json_file.close()

