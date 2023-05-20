from methods.support_methods import *

def updateKeyInJson(json, hotkey):
    for category in json.keys():
        for key in json[category].keys():
            if hotkey[1] == json[category][key]["text"]:
                json[category][key]["key"] = hotkey[0]
    return json

def updateKeyInJsonRocket(json, identifier, value):
    for category in json.keys():
        try:
            for key in json[category].keys():
                # didn't need to catch because this method should only update values
                # which are in the form of the if clause
                try:
                    if identifier == removeSpaces(json[category][key]["text"]+"_input") or identifier == removeSpaces(json[category][key]["text"]+"_dropdown"):
                        if value.isdigit():
                            json[category][key]["value"] = int(value)
                        else:
                            json[category][key]["value"] = value
                except:
                    pass
        except:
            pass
    return json

# Rocket Controls
def getH_rocketBoostForward(hotkeysJson):
    return [
        hotkeysJson["RocketControls"]["H_rocketBoostForward"]["key"],
        hotkeysJson["RocketControls"]["H_rocketBoostForward"]["text"]
    ]
def getH_rocketBoostLeft(hotkeysJson):
    return [
        hotkeysJson["RocketControls"]["H_rocketBoostLeft"]["key"],
        hotkeysJson["RocketControls"]["H_rocketBoostLeft"]["text"]
    ]
def getH_rocketBoostRight(hotkeysJson):
    return [
        hotkeysJson["RocketControls"]["H_rocketBoostRight"]["key"],
        hotkeysJson["RocketControls"]["H_rocketBoostRight"]["text"]
    ]
def getH_lowerRocketBoost(hotkeysJson):
    return [
        hotkeysJson["RocketControls"]["H_lowerRocketBoost"]["key"],
        hotkeysJson["RocketControls"]["H_lowerRocketBoost"]["text"]
    ]

# Rocket Zooms
def getH_zoomRocketStart(hotkeysJson):
    return [
        hotkeysJson["RocketZooms"]["H_zoomRocketStart"]["key"],
        hotkeysJson["RocketZooms"]["H_zoomRocketStart"]["text"]
    ]
def getH_zoomRocketPlanet(hotkeysJson):
    return [
        hotkeysJson["RocketZooms"]["H_zoomRocketPlanet"]["key"],
        hotkeysJson["RocketZooms"]["H_zoomRocketPlanet"]["text"]
    ]
def getH_zoomRocketPlanetSystem(hotkeysJson):
    return [
        hotkeysJson["RocketZooms"]["H_zoomRocketPlanetSystem"]["key"],
        hotkeysJson["RocketZooms"]["H_zoomRocketPlanetSystem"]["text"]
    ]
def getH_zoomAutoOnRocket(hotkeysJson):
    return [
        hotkeysJson["RocketZooms"]["H_zoomAutoOnRocket"]["key"],
        hotkeysJson["RocketZooms"]["H_zoomAutoOnRocket"]["text"]
    ]

# Centering
def getH_centerOnSun(hotkeysJson):
    return [
        hotkeysJson["Centering"]["H_centerOnSun"]["key"],
        hotkeysJson["Centering"]["H_centerOnSun"]["text"]
    ]
def getH_centerOnRocket(hotkeysJson):
    return [
        hotkeysJson["Centering"]["H_centerOnRocket"]["key"],
        hotkeysJson["Centering"]["H_centerOnRocket"]["text"]
    ]

# Time Manipulation
def getH_shiftTimeStepUp(hotkeysJson):
    return [
        hotkeysJson["TimeManipulation"]["H_shiftTimeStepUp"]["key"],
        hotkeysJson["TimeManipulation"]["H_shiftTimeStepUp"]["text"]
    ]
def getH_shiftTimeStepDown(hotkeysJson):
    return [
        hotkeysJson["TimeManipulation"]["H_shiftTimeStepDown"]["key"],
        hotkeysJson["TimeManipulation"]["H_shiftTimeStepDown"]["text"]
    ]

# Generals
def getH_drawLine(hotkeysJson):
    return [
        hotkeysJson["Generals"]["H_drawLine"]["key"],
        hotkeysJson["Generals"]["H_drawLine"]["text"]
    ]
def getH_showDistance(hotkeysJson):
    return [
        hotkeysJson["Generals"]["H_showDistance"]["key"],
        hotkeysJson["Generals"]["H_showDistance"]["text"]
    ]
def getH_pauseSimulation(hotkeysJson):
    return [
        hotkeysJson["Generals"]["H_pauseSimulation"]["key"],
        hotkeysJson["Generals"]["H_pauseSimulation"]["text"]
    ]

# Navigation
def getH_displayHotKeys(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_displayHotKeys"]["key"],
        hotkeysJson["Navigation"]["H_displayHotKeys"]["text"]
    ]
def getH_leaveSimulation(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_leaveSimulation"]["key"],
        hotkeysJson["Navigation"]["H_leaveSimulation"]["text"]
    ]
def getH_openSettings(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_openSettings"]["key"],
        hotkeysJson["Navigation"]["H_openSettings"]["text"]
    ]
def getH_closeWindow(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_closeWindow"]["key"],
        hotkeysJson["Navigation"]["H_closeWindow"]["text"]
    ]