import json
from methods.json_methods import *


try: 
    jsonFile = open("./variables/hotkeys_config/current_hotkeys.json")
    hotkeysJson = json.load(jsonFile)

    listHotKeys = []

    ### Rocket Controls

    H_rocketBoostForward = getH_rocketBoostForward(hotkeysJson)
    listHotKeys.append(H_rocketBoostForward)
    H_rocketBoostLeft = getH_rocketBoostLeft(hotkeysJson)
    listHotKeys.append(H_rocketBoostLeft)
    H_rocketBoostRight = getH_rocketBoostRight(hotkeysJson)
    listHotKeys.append(H_rocketBoostRight)
    H_lowerRocketBoost = getH_lowerRocketBoost(hotkeysJson)
    listHotKeys.append(H_lowerRocketBoost)

    ### Rocket Zooms
    H_zoomRocketStart = getH_zoomRocketStart(hotkeysJson)
    listHotKeys.append(H_zoomRocketStart)
    H_zoomRocketPlanet = getH_zoomRocketPlanet(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanet)
    H_zoomRocketPlanetSystem = getH_zoomRocketPlanetSystem(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanetSystem)
    H_zoomAutoOnRocket = getH_zoomAutoOnRocket(hotkeysJson)
    listHotKeys.append(H_zoomAutoOnRocket)

    ### Centering 
    H_centerOnSun = getH_centerOnSun(hotkeysJson)
    listHotKeys.append(H_centerOnSun)
    H_centerOnRocket = getH_centerOnRocket(hotkeysJson)
    listHotKeys.append(H_centerOnRocket)

    ### Time Manipulation
    H_shiftTimeStepUp = getH_shiftTimeStepUp(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepUp)
    H_shiftTimeStepDown = getH_shiftTimeStepDown(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepDown)

    ### Generals
    H_drawLine = getH_drawLine(hotkeysJson)
    listHotKeys.append(H_drawLine)
    H_showDistance = getH_showDistance(hotkeysJson)
    listHotKeys.append(H_showDistance)
    H_pauseSimulation = getH_pauseSimulation(hotkeysJson)
    listHotKeys.append(H_pauseSimulation)

    ### Navigation
    H_displayHotKeys = getH_displayHotKeys(hotkeysJson)
    listHotKeys.append(H_displayHotKeys)
    H_leaveSimulation = getH_leaveSimulation(hotkeysJson)
    listHotKeys.append(H_leaveSimulation)
    H_openSettings = getH_openSettings(hotkeysJson)
    listHotKeys.append(H_openSettings)
    H_closeWindow =  getH_closeWindow(hotkeysJson)
    listHotKeys.append(H_closeWindow)
    H_moveScreenUp = getH_moveScreenUp(hotkeysJson)
    listHotKeys.append(H_moveScreenUp)
    H_moveScreenDown = getH_moveScreenDown(hotkeysJson)
    listHotKeys.append(H_moveScreenDown)
    H_moveScreenRight = getH_moveScreenRight(hotkeysJson)
    listHotKeys.append(H_moveScreenRight)
    H_moveScreenLeft = getH_moveScreenLeft(hotkeysJson)
    listHotKeys.append(H_moveScreenLeft)

except:
    ### Error or Empty while Reading triggers copy from standard to current
    jsonFile = open("./variables/hotkeys_config/standard_hotkeys.json")

    hotkeysJson = json.load(jsonFile)

    with open("./variables/hotkeys_config/current_hotkeys.json", "w") as outfile:
        json.dump(hotkeysJson, outfile, indent=4, ensure_ascii=False)

    listHotKeys = []

    ### Rocket Controls

    H_rocketBoostForward = getH_rocketBoostForward(hotkeysJson)
    listHotKeys.append(H_rocketBoostForward)
    H_rocketBoostLeft = getH_rocketBoostLeft(hotkeysJson)
    listHotKeys.append(H_rocketBoostLeft)
    H_rocketBoostRight = getH_rocketBoostRight(hotkeysJson)
    listHotKeys.append(H_rocketBoostRight)
    H_lowerRocketBoost = getH_lowerRocketBoost(hotkeysJson)
    listHotKeys.append(H_lowerRocketBoost)

    ### Rocket Zooms
    H_zoomRocketStart = getH_zoomRocketStart(hotkeysJson)
    listHotKeys.append(H_zoomRocketStart)
    H_zoomRocketPlanet = getH_zoomRocketPlanet(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanet)
    H_zoomRocketPlanetSystem = getH_zoomRocketPlanetSystem(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanetSystem)
    H_zoomAutoOnRocket = getH_zoomAutoOnRocket(hotkeysJson)
    listHotKeys.append(H_zoomAutoOnRocket)

    ### Centering 
    H_centerOnSun = getH_centerOnSun(hotkeysJson)
    listHotKeys.append(H_centerOnSun)
    H_centerOnRocket = getH_centerOnRocket(hotkeysJson)
    listHotKeys.append(H_centerOnRocket)

    ### Time Manipulation
    H_shiftTimeStepUp = getH_shiftTimeStepUp(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepUp)
    H_shiftTimeStepDown = getH_shiftTimeStepDown(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepDown)

    ### Generals
    H_drawLine = getH_drawLine(hotkeysJson)
    listHotKeys.append(H_drawLine)
    H_showDistance = getH_showDistance(hotkeysJson)
    listHotKeys.append(H_showDistance)
    H_pauseSimulation = getH_pauseSimulation(hotkeysJson)
    listHotKeys.append(H_pauseSimulation)

    ### Navigation
    H_displayHotKeys = getH_displayHotKeys(hotkeysJson)
    listHotKeys.append(H_displayHotKeys)
    H_leaveSimulation = getH_leaveSimulation(hotkeysJson)
    listHotKeys.append(H_leaveSimulation)
    H_openSettings = getH_openSettings(hotkeysJson)
    listHotKeys.append(H_openSettings)
    H_closeWindow =  getH_closeWindow(hotkeysJson)
    listHotKeys.append(H_closeWindow)
    H_moveScreenUp = getH_moveScreenUp(hotkeysJson)
    listHotKeys.append(H_moveScreenUp)
    H_moveScreenDown = getH_moveScreenDown(hotkeysJson)
    listHotKeys.append(H_moveScreenDown)
    H_moveScreenRight = getH_moveScreenRight(hotkeysJson)
    listHotKeys.append(H_moveScreenRight)
    H_moveScreenLeft = getH_moveScreenLeft(hotkeysJson)
    listHotKeys.append(H_moveScreenLeft)


jsonFile.close()


def resetOverwriteCurrent():
    global listHotKeys, H_rocketBoostForward, H_rocketBoostLeft, H_rocketBoostRight, H_lowerRocketBoost, H_zoomRocketStart, H_zoomRocketPlanet, H_zoomRocketPlanetSystem, H_zoomAutoOnRocket, H_centerOnSun, H_centerOnRocket, H_shiftTimeStepUp, H_centerOnRocket, H_shiftTimeStepUp, H_shiftTimeStepDown, H_drawLine, H_showDistance, H_pauseSimulation, H_displayHotKeys, H_leaveSimulation, H_openSettings, H_closeWindow
    jsonFile = open("./variables/hotkeys_config/standard_hotkeys.json")
    hotkeysJson = json.load(jsonFile)

    with open("./variables/hotkeys_config/current_hotkeys.json", "w") as outfile:
        json.dump(hotkeysJson, outfile, indent=4, ensure_ascii=False)

    listHotKeys = []
    jsonFile = open("./variables/hotkeys_config/current_hotkeys.json")
    hotkeysJson = json.load(jsonFile)
    ### Rocket Controls

    H_rocketBoostForward = getH_rocketBoostForward(hotkeysJson)
    listHotKeys.append(H_rocketBoostForward)
    H_rocketBoostLeft = getH_rocketBoostLeft(hotkeysJson)
    listHotKeys.append(H_rocketBoostLeft)
    H_rocketBoostRight = getH_rocketBoostRight(hotkeysJson)
    listHotKeys.append(H_rocketBoostRight)
    H_lowerRocketBoost = getH_lowerRocketBoost(hotkeysJson)
    listHotKeys.append(H_lowerRocketBoost)

    ### Rocket Zooms
    H_zoomRocketStart = getH_zoomRocketStart(hotkeysJson)
    listHotKeys.append(H_zoomRocketStart)
    H_zoomRocketPlanet = getH_zoomRocketPlanet(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanet)
    H_zoomRocketPlanetSystem = getH_zoomRocketPlanetSystem(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanetSystem)
    H_zoomAutoOnRocket = getH_zoomAutoOnRocket(hotkeysJson)
    listHotKeys.append(H_zoomAutoOnRocket)

    ### Centering 
    H_centerOnSun = getH_centerOnSun(hotkeysJson)
    listHotKeys.append(H_centerOnSun)
    H_centerOnRocket = getH_centerOnRocket(hotkeysJson)
    listHotKeys.append(H_centerOnRocket)

    ### Time Manipulation
    H_shiftTimeStepUp = getH_shiftTimeStepUp(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepUp)
    H_shiftTimeStepDown = getH_shiftTimeStepDown(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepDown)

    ### Generals
    H_drawLine = getH_drawLine(hotkeysJson)
    listHotKeys.append(H_drawLine)
    H_showDistance = getH_showDistance(hotkeysJson)
    listHotKeys.append(H_showDistance)
    H_pauseSimulation = getH_pauseSimulation(hotkeysJson)
    listHotKeys.append(H_pauseSimulation)

    ### Navigation
    H_displayHotKeys = getH_displayHotKeys(hotkeysJson)
    listHotKeys.append(H_displayHotKeys)
    H_leaveSimulation = getH_leaveSimulation(hotkeysJson)
    listHotKeys.append(H_leaveSimulation)
    H_openSettings = getH_openSettings(hotkeysJson)
    listHotKeys.append(H_openSettings)
    H_closeWindow =  getH_closeWindow(hotkeysJson)
    listHotKeys.append(H_closeWindow)
    H_moveScreenUp = getH_moveScreenUp(hotkeysJson)
    listHotKeys.append(H_moveScreenUp)
    H_moveScreenDown = getH_moveScreenDown(hotkeysJson)
    listHotKeys.append(H_moveScreenDown)
    H_moveScreenRight = getH_moveScreenRight(hotkeysJson)
    listHotKeys.append(H_moveScreenRight)
    H_moveScreenLeft = getH_moveScreenLeft(hotkeysJson)
    listHotKeys.append(H_moveScreenLeft)


    jsonFile.close()

