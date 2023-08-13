import json
import subprocess
import sys


def install_requirements():
    try:
        subprocess.run(['pip', 'install', 'pipenv'])
        subprocess.run(['pipenv', 'install', '--ignore-pipfile', '-r', 'requirements.txt'])
    except Exception as e:
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
