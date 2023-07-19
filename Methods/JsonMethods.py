from Methods.SupportMethods import *

def UpdateKeyInJson(json, hotkey):
    for category in json.keys():
        for key in json[category].keys():
            if hotkey[1] == json[category][key]["text"]:
                json[category][key]["key"] = hotkey[0]
    return json

def UpdateKeyInJsonRocket(json, identifier, value):
    for category in json.keys():
        try:
            for key in json[category].keys():
                # didn't need to catch because this method should only update values
                # which are in the form of the if clause
                try:
                    if identifier == RemoveSpaces(json[category][key]["text"]+"_input") or identifier == RemoveSpaces(json[category][key]["text"]+"_dropdown"):
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
def GetH_rocketBoostForward(hotkeysJson):
    return [
        hotkeysJson["RocketControls"]["H_rocketBoostForward"]["key"],
        hotkeysJson["RocketControls"]["H_rocketBoostForward"]["text"]
    ]
def GetH_rocketBoostLeft(hotkeysJson):
    return [
        hotkeysJson["RocketControls"]["H_rocketBoostLeft"]["key"],
        hotkeysJson["RocketControls"]["H_rocketBoostLeft"]["text"]
    ]
def GetH_rocketBoostRight(hotkeysJson):
    return [
        hotkeysJson["RocketControls"]["H_rocketBoostRight"]["key"],
        hotkeysJson["RocketControls"]["H_rocketBoostRight"]["text"]
    ]
def GetH_lowerRocketBoost(hotkeysJson):
    return [
        hotkeysJson["RocketControls"]["H_lowerRocketBoost"]["key"],
        hotkeysJson["RocketControls"]["H_lowerRocketBoost"]["text"]
    ]

# Rocket Zooms
def GetH_zoomRocketStart(hotkeysJson):
    return [
        hotkeysJson["RocketZooms"]["H_zoomRocketStart"]["key"],
        hotkeysJson["RocketZooms"]["H_zoomRocketStart"]["text"]
    ]
def GetH_zoomRocketPlanet(hotkeysJson):
    return [
        hotkeysJson["RocketZooms"]["H_zoomRocketPlanet"]["key"],
        hotkeysJson["RocketZooms"]["H_zoomRocketPlanet"]["text"]
    ]
def GetH_zoomRocketPlanetSystem(hotkeysJson):
    return [
        hotkeysJson["RocketZooms"]["H_zoomRocketPlanetSystem"]["key"],
        hotkeysJson["RocketZooms"]["H_zoomRocketPlanetSystem"]["text"]
    ]
def GetH_zoomAutoOnRocket(hotkeysJson):
    return [
        hotkeysJson["RocketZooms"]["H_zoomAutoOnRocket"]["key"],
        hotkeysJson["RocketZooms"]["H_zoomAutoOnRocket"]["text"]
    ]
def GetH_zoomAutoOnReferencePlanet(hotkeysJson):
    return [
        hotkeysJson["RocketZooms"]["H_zoomAutoOnReferencePlanet"]["key"],
        hotkeysJson["RocketZooms"]["H_zoomAutoOnReferencePlanet"]["text"]
    ]

# Centering
def GetH_centerOnSun(hotkeysJson):
    return [
        hotkeysJson["Centering"]["H_centerOnSun"]["key"],
        hotkeysJson["Centering"]["H_centerOnSun"]["text"]
    ]
def GetH_centerOnRocket(hotkeysJson):
    return [
        hotkeysJson["Centering"]["H_centerOnRocket"]["key"],
        hotkeysJson["Centering"]["H_centerOnRocket"]["text"]
    ]

# Time Manipulation
def GetH_shiftTimeStepUp(hotkeysJson):
    return [
        hotkeysJson["TimeManipulation"]["H_shiftTimeStepUp"]["key"],
        hotkeysJson["TimeManipulation"]["H_shiftTimeStepUp"]["text"]
    ]
def GetH_shiftTimeStepDown(hotkeysJson):
    return [
        hotkeysJson["TimeManipulation"]["H_shiftTimeStepDown"]["key"],
        hotkeysJson["TimeManipulation"]["H_shiftTimeStepDown"]["text"]
    ]

# Generals
def GetH_drawLine(hotkeysJson):
    return [
        hotkeysJson["Generals"]["H_drawLine"]["key"],
        hotkeysJson["Generals"]["H_drawLine"]["text"]
    ]
def GetH_showDistance(hotkeysJson):
    return [
        hotkeysJson["Generals"]["H_showDistance"]["key"],
        hotkeysJson["Generals"]["H_showDistance"]["text"]
    ]
def GetH_pauseSimulation(hotkeysJson):
    return [
        hotkeysJson["Generals"]["H_pauseSimulation"]["key"],
        hotkeysJson["Generals"]["H_pauseSimulation"]["text"]
    ]

# Navigation
def GetH_displayHotKeys(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_displayHotKeys"]["key"],
        hotkeysJson["Navigation"]["H_displayHotKeys"]["text"]
    ]
def GetH_leaveSimulation(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_leaveSimulation"]["key"],
        hotkeysJson["Navigation"]["H_leaveSimulation"]["text"]
    ]
def GetH_openSettings(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_openSettings"]["key"],
        hotkeysJson["Navigation"]["H_openSettings"]["text"]
    ]
def GetH_closeWindow(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_closeWindow"]["key"],
        hotkeysJson["Navigation"]["H_closeWindow"]["text"]
    ]
def GetH_moveScreenUp(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_moveScreenUp"]["key"],
        hotkeysJson["Navigation"]["H_moveScreenUp"]["text"]
    ]
def GetH_moveScreenDown(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_moveScreenDown"]["key"],
        hotkeysJson["Navigation"]["H_moveScreenDown"]["text"]
    ]
def GetH_moveScreenRight(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_moveScreenRight"]["key"],
        hotkeysJson["Navigation"]["H_moveScreenRight"]["text"]
    ]
def GetH_moveScreenLeft(hotkeysJson):
    return [
        hotkeysJson["Navigation"]["H_moveScreenLeft"]["key"],
        hotkeysJson["Navigation"]["H_moveScreenLeft"]["text"]
    ]