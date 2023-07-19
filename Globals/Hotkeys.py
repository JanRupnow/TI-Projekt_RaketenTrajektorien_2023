import json

from Methods.JsonMethods import *


try: 
    jsonFile = open("./Globals/HotkeysConfig/CurrentHotkeys.json")
    hotkeysJson = json.load(jsonFile)

    listHotKeys = []

    ### Rocket Controls

    H_rocketBoostForward = GetH_rocketBoostForward(hotkeysJson)
    listHotKeys.append(H_rocketBoostForward)
    H_rocketBoostLeft = GetH_rocketBoostLeft(hotkeysJson)
    listHotKeys.append(H_rocketBoostLeft)
    H_rocketBoostRight = GetH_rocketBoostRight(hotkeysJson)
    listHotKeys.append(H_rocketBoostRight)
    H_lowerRocketBoost = GetH_lowerRocketBoost(hotkeysJson)
    listHotKeys.append(H_lowerRocketBoost)

    ### Rocket Zooms
    H_zoomRocketStart = GetH_zoomRocketStart(hotkeysJson)
    listHotKeys.append(H_zoomRocketStart)
    H_zoomRocketPlanet = GetH_zoomRocketPlanet(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanet)
    H_zoomRocketPlanetSystem = GetH_zoomRocketPlanetSystem(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanetSystem)
    H_zoomAutoOnRocket = GetH_zoomAutoOnRocket(hotkeysJson)
    listHotKeys.append(H_zoomAutoOnRocket)
    H_zoomAutoOnReferencePlanet = GetH_zoomAutoOnReferencePlanet(hotkeysJson)
    listHotKeys.append(H_zoomAutoOnReferencePlanet)

    ### Centering 
    H_centerOnSun = GetH_centerOnSun(hotkeysJson)
    listHotKeys.append(H_centerOnSun)
    H_centerOnRocket = GetH_centerOnRocket(hotkeysJson)
    listHotKeys.append(H_centerOnRocket)

    ### Time Manipulation
    H_shiftTimeStepUp = GetH_shiftTimeStepUp(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepUp)
    H_shiftTimeStepDown = GetH_shiftTimeStepDown(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepDown)

    ### Generals
    H_drawLine = GetH_drawLine(hotkeysJson)
    listHotKeys.append(H_drawLine)
    H_showDistance = GetH_showDistance(hotkeysJson)
    listHotKeys.append(H_showDistance)
    H_pauseSimulation = GetH_pauseSimulation(hotkeysJson)
    listHotKeys.append(H_pauseSimulation)

    ### Navigation
    H_displayHotKeys = GetH_displayHotKeys(hotkeysJson)
    listHotKeys.append(H_displayHotKeys)
    H_leaveSimulation = GetH_leaveSimulation(hotkeysJson)
    listHotKeys.append(H_leaveSimulation)
    H_openSettings = GetH_openSettings(hotkeysJson)
    listHotKeys.append(H_openSettings)
    H_closeWindow =  GetH_closeWindow(hotkeysJson)
    listHotKeys.append(H_closeWindow)
    H_moveScreenUp = GetH_moveScreenUp(hotkeysJson)
    listHotKeys.append(H_moveScreenUp)
    H_moveScreenDown = GetH_moveScreenDown(hotkeysJson)
    listHotKeys.append(H_moveScreenDown)
    H_moveScreenRight = GetH_moveScreenRight(hotkeysJson)
    listHotKeys.append(H_moveScreenRight)
    H_moveScreenLeft = GetH_moveScreenLeft(hotkeysJson)
    listHotKeys.append(H_moveScreenLeft)

except:
    ### Error or Empty while Reading triggers copy from standard to current
    jsonFile = open("./Globals/HotkeysConfig/StandardHotkeys.json")

    hotkeysJson = json.load(jsonFile)

    with open("./Globals/HotkeysConfig/CurrentHotkeys.json", "w") as outfile:
        json.dump(hotkeysJson, outfile, indent=4, ensure_ascii=False)

    listHotKeys = []

    ### Rocket Controls

    H_rocketBoostForward = GetH_rocketBoostForward(hotkeysJson)
    listHotKeys.append(H_rocketBoostForward)
    H_rocketBoostLeft = GetH_rocketBoostLeft(hotkeysJson)
    listHotKeys.append(H_rocketBoostLeft)
    H_rocketBoostRight = GetH_rocketBoostRight(hotkeysJson)
    listHotKeys.append(H_rocketBoostRight)
    H_lowerRocketBoost = GetH_lowerRocketBoost(hotkeysJson)
    listHotKeys.append(H_lowerRocketBoost)

    ### Rocket Zooms
    H_zoomRocketStart = GetH_zoomRocketStart(hotkeysJson)
    listHotKeys.append(H_zoomRocketStart)
    H_zoomRocketPlanet = GetH_zoomRocketPlanet(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanet)
    H_zoomRocketPlanetSystem = GetH_zoomRocketPlanetSystem(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanetSystem)
    H_zoomAutoOnRocket = GetH_zoomAutoOnRocket(hotkeysJson)
    listHotKeys.append(H_zoomAutoOnRocket)
    H_zoomAutoOnReferencePlanet = GetH_zoomAutoOnReferencePlanet(hotkeysJson)
    listHotKeys.append(H_zoomAutoOnReferencePlanet)

    ### Centering 
    H_centerOnSun = GetH_centerOnSun(hotkeysJson)
    listHotKeys.append(H_centerOnSun)
    H_centerOnRocket = GetH_centerOnRocket(hotkeysJson)
    listHotKeys.append(H_centerOnRocket)

    ### Time Manipulation
    H_shiftTimeStepUp = GetH_shiftTimeStepUp(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepUp)
    H_shiftTimeStepDown = GetH_shiftTimeStepDown(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepDown)

    ### Generals
    H_drawLine = GetH_drawLine(hotkeysJson)
    listHotKeys.append(H_drawLine)
    H_showDistance = GetH_showDistance(hotkeysJson)
    listHotKeys.append(H_showDistance)
    H_pauseSimulation = GetH_pauseSimulation(hotkeysJson)
    listHotKeys.append(H_pauseSimulation)

    ### Navigation
    H_displayHotKeys = GetH_displayHotKeys(hotkeysJson)
    listHotKeys.append(H_displayHotKeys)
    H_leaveSimulation = GetH_leaveSimulation(hotkeysJson)
    listHotKeys.append(H_leaveSimulation)
    H_openSettings = GetH_openSettings(hotkeysJson)
    listHotKeys.append(H_openSettings)
    H_closeWindow =  GetH_closeWindow(hotkeysJson)
    listHotKeys.append(H_closeWindow)
    H_moveScreenUp = GetH_moveScreenUp(hotkeysJson)
    listHotKeys.append(H_moveScreenUp)
    H_moveScreenDown = GetH_moveScreenDown(hotkeysJson)
    listHotKeys.append(H_moveScreenDown)
    H_moveScreenRight = GetH_moveScreenRight(hotkeysJson)
    listHotKeys.append(H_moveScreenRight)
    H_moveScreenLeft = GetH_moveScreenLeft(hotkeysJson)
    listHotKeys.append(H_moveScreenLeft)


jsonFile.close()


def resetOverwriteCurrent():
    global listHotKeys, H_rocketBoostForward, H_rocketBoostLeft, H_rocketBoostRight, H_lowerRocketBoost, H_zoomRocketStart, H_zoomRocketPlanet, H_zoomRocketPlanetSystem, H_zoomAutoOnRocket, H_centerOnSun, H_centerOnRocket, H_shiftTimeStepUp, H_centerOnRocket, H_shiftTimeStepUp, H_shiftTimeStepDown, H_drawLine, H_showDistance, H_pauseSimulation, H_displayHotKeys, H_leaveSimulation, H_openSettings, H_closeWindow
    jsonFile = open("./Globals/HotkeysConfig/StandardHotkeys.json")
    hotkeysJson = json.load(jsonFile)

    with open("./Globals/HotkeysConfig/CurrentHotkeys.json", "w") as outfile:
        json.dump(hotkeysJson, outfile, indent=4, ensure_ascii=False)

    listHotKeys = []
    jsonFile = open("./Globals/HotkeysConfig/CurrentHotkeys.json")
    hotkeysJson = json.load(jsonFile)
    ### Rocket Controls

    H_rocketBoostForward = GetH_rocketBoostForward(hotkeysJson)
    listHotKeys.append(H_rocketBoostForward)
    H_rocketBoostLeft = GetH_rocketBoostLeft(hotkeysJson)
    listHotKeys.append(H_rocketBoostLeft)
    H_rocketBoostRight = GetH_rocketBoostRight(hotkeysJson)
    listHotKeys.append(H_rocketBoostRight)
    H_lowerRocketBoost = GetH_lowerRocketBoost(hotkeysJson)
    listHotKeys.append(H_lowerRocketBoost)

    ### Rocket Zooms
    H_zoomRocketStart = GetH_zoomRocketStart(hotkeysJson)
    listHotKeys.append(H_zoomRocketStart)
    H_zoomRocketPlanet = GetH_zoomRocketPlanet(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanet)
    H_zoomRocketPlanetSystem = GetH_zoomRocketPlanetSystem(hotkeysJson)
    listHotKeys.append(H_zoomRocketPlanetSystem)
    H_zoomAutoOnRocket = GetH_zoomAutoOnRocket(hotkeysJson)
    listHotKeys.append(H_zoomAutoOnRocket)
    H_zoomAutoOnReferencePlanet = GetH_zoomAutoOnReferencePlanet(hotkeysJson)
    listHotKeys.append(H_zoomAutoOnReferencePlanet)

    ### Centering 
    H_centerOnSun = GetH_centerOnSun(hotkeysJson)
    listHotKeys.append(H_centerOnSun)
    H_centerOnRocket = GetH_centerOnRocket(hotkeysJson)
    listHotKeys.append(H_centerOnRocket)

    ### Time Manipulation
    H_shiftTimeStepUp = GetH_shiftTimeStepUp(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepUp)
    H_shiftTimeStepDown = GetH_shiftTimeStepDown(hotkeysJson)
    listHotKeys.append(H_shiftTimeStepDown)

    ### Generals
    H_drawLine = GetH_drawLine(hotkeysJson)
    listHotKeys.append(H_drawLine)
    H_showDistance = GetH_showDistance(hotkeysJson)
    listHotKeys.append(H_showDistance)
    H_pauseSimulation = GetH_pauseSimulation(hotkeysJson)
    listHotKeys.append(H_pauseSimulation)

    ### Navigation
    H_displayHotKeys = GetH_displayHotKeys(hotkeysJson)
    listHotKeys.append(H_displayHotKeys)
    H_leaveSimulation = GetH_leaveSimulation(hotkeysJson)
    listHotKeys.append(H_leaveSimulation)
    H_openSettings = GetH_openSettings(hotkeysJson)
    listHotKeys.append(H_openSettings)
    H_closeWindow =  GetH_closeWindow(hotkeysJson)
    listHotKeys.append(H_closeWindow)
    H_moveScreenUp = GetH_moveScreenUp(hotkeysJson)
    listHotKeys.append(H_moveScreenUp)
    H_moveScreenDown = GetH_moveScreenDown(hotkeysJson)
    listHotKeys.append(H_moveScreenDown)
    H_moveScreenRight = GetH_moveScreenRight(hotkeysJson)
    listHotKeys.append(H_moveScreenRight)
    H_moveScreenLeft = GetH_moveScreenLeft(hotkeysJson)
    listHotKeys.append(H_moveScreenLeft)


    jsonFile.close()

