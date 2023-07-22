
import datetime

from Globals.Constants import HEIGHT, WIDTH, DATA
import Globals.Hotkeys as keys

from Views.HotkeyView import *

from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.ZoomGoal import ZoomGoal

from ViewController.Planet import Planet

from Methods.SupportMethods import *

def AddClockTime():
    DATA.setTimePassed(DATA.getTimePassed()+ datetime.timedelta(seconds=DATA.getTimeStep))

def AutomaticZoomOnRocket(rocket : Rocket):
    DATA.setMoveX(-rocket.position_X[rocket.currentStep] * DATA.getScale())
    DATA.setMoveY(-rocket.position_Y[rocket.currentStep] * DATA.getScale())

def AutomaticZoomOnRocketOnce(rocket : Rocket):
    DATA.setMoveX(-rocket.position_X[rocket.currentStep] * DATA.getScale())
    DATA.setMoveY(-rocket.position_Y[rocket.currentStep] * DATA.getScale())

def CenterScreenOnPlanet(planet : Planet):
    DATA.setMoveX(-planet.position_X[planet.currentStep] * DATA.getScale())
    DATA.setMoveY(-planet.position_Y[planet.currentStep] * DATA.getScale())

def ScaleRelative(factor):
    DATA.setScale(STARTSCALE* factor)

def MousePositionShiftScreen():
    DATA.setMoveX(DATA.getMoveX()-(DATA.getMouseX()-WIDTH/2)/2)
    DATA.setMoveY(DATA.getMoveY()-(DATA.getMouseY()-HEIGHT/2)/2)

def ShiftTimeStep(shiftUp):
    index = min(AllTimeSteps.index(DATA.getTimeStep()) + 1, len(AllTimeSteps) - 1) if shiftUp else max(AllTimeSteps.index(DATA.getTimeStep()) - 1, 0)
    DATA.setTimeStep(AllTimeSteps[index])
    DATA.setFlightChangeState(FlightChangeState.timeStepChanged)
    


def PlanetIsInScreen(planet : Planet):
    inScreen = planet.position_Y[planet.currentStep]*DATA.getScale()+planet.radius*DATA.getScale() > -DATA.getMoveY()-HEIGHT/2
    inScreen = inScreen and planet.position_Y[planet.currentStep]*DATA.getScale()-planet.radius*DATA.getScale() < -DATA.getMoveY()+HEIGHT/2
    inScreen = inScreen and planet.position_X[planet.currentStep]*DATA.getScale()+planet.radius*DATA.getScale() > -DATA.getMoveX()-WIDTH/2
    return inScreen and planet.position_X[planet.currentStep]*DATA.getScale()-planet.radius*DATA.getScale() < -DATA.getMoveX()+WIDTH/2


def ProcessHotKeyEvents(event, rocket : Rocket, planets : list[Planet]):
    KeyPressed = pygame.key.get_pressed()
    #mouse_x, mouse_y = pygame.mouse.get_pos()
    DATA.setMouseX(pygame.mouse.get_pos()[0])
    DATA.setMouseY(pygame.mouse.get_pos()[1])
    distance = 10

    if  KeyPressed[keys.H_moveScreenLeft[0]] or DATA.getMouseX() == 0:
        DATA.setMoveX(DATA.getMoveX()+distance)
    elif KeyPressed[keys.H_moveScreenRight[0]] or DATA.getMouseX() == WIDTH - 1:
        DATA.setMoveX(DATA.getMoveX()-distance)
    elif KeyPressed[keys.H_moveScreenUp[0]] or DATA.getMouseY() == 0:
        DATA.setMoveY(DATA.getMoveY()+distance)
    elif KeyPressed[keys.H_moveScreenDown[0]] or DATA.getMouseY() == HEIGHT - 1:
        DATA.setMoveY(DATA.getMoveY()-distance)

    elif ( not event.type == pygame.KEYDOWN ) and KeyPressed[keys.H_rocketBoostForward[0]] and rocket.thrust<10 and (rocket.flightState == RocketFlightState.flying or not DATA.getSimulationPause()):
        rocket.thrust += 1
        DATA.setFlightChangeState(FlightChangeState.powerChanged)
        rocket.flightState = RocketFlightState.flying
    elif ( not event.type == pygame.KEYDOWN ) and KeyPressed[keys.H_rocketBoostLeft[0]] and rocket.angle>-45:
        rocket.angle -= 1
        DATA.setFlightChangeState(FlightChangeState.powerChanged)
    elif ( not event.type == pygame.KEYDOWN ) and KeyPressed[keys.H_rocketBoostRight[0]]  and rocket.angle<45:
        rocket.angle += 1
        DATA.setFlightChangeState(FlightChangeState.powerChanged)
    elif ( not event.type == pygame.KEYDOWN ) and KeyPressed[keys.H_lowerRocketBoost[0]] and rocket.thrust>0:
        rocket.thrust -= 1
        DATA.setFlightChangeState(FlightChangeState.powerChanged)
        
    elif event.type == pygame.QUIT or CheckKeyDown(event, keys.H_leaveSimulation[0]) or CheckKeyDown(event, keys.H_closeWindow[0]):
        DATA.setRun(False)
    elif CheckKeyDown(event, keys.H_zoomRocketStart[0]):
        DATA.setScale(ScaleRelative(100000))
        rocket.SetScale(100000)
        AutomaticZoomOnRocketOnce(rocket)
    #Zoom Startorbit
    elif CheckKeyDown(event, keys.H_zoomRocketPlanet[0]):
        DATA.setScale(ScaleRelative(10))
        rocket.SetScale(10)
        AutomaticZoomOnRocketOnce(rocket)
    #Zoom Universum
    elif CheckKeyDown(event, keys.H_zoomRocketPlanetSystem[0]):
        DATA.setScale(ScaleRelative(1))
        rocket.SetScale(1)
        AutomaticZoomOnRocketOnce(rocket)

    elif CheckKeyDown(event, keys.H_zoomAutoOnReferencePlanet[0]) and not DATA.getZoomGoal() == ZoomGoal.rocket:
        if(DATA.getZoomGoal() == ZoomGoal.nearestPlanet):
            DATA.setZoomGoal(ZoomGoal.none)
        elif(DATA.getZoomGoal() == ZoomGoal.none):
            DATA.setZoomGoal(ZoomGoal.nearestPlanet)
    elif CheckKeyDown(event, keys.H_zoomAutoOnRocket[0]) and not DATA.getZoomGoal() == ZoomGoal.nearestPlanet:
        if(DATA.getZoomGoal() == ZoomGoal.rocket):
            DATA.setZoomGoal(ZoomGoal.none)
        elif(DATA.getZoomGoal() == ZoomGoal.none):
            DATA.setZoomGoal(ZoomGoal.rocket)
    elif CheckKeyDown(event, keys.H_pauseSimulation[0]):
        if(DATA.getFlightChangeState == FlightChangeState.paused):
            DATA.setFlightChangeState(FlightChangeState.unchanged)
        if(DATA.getFlightChangeState == FlightChangeState.unchanged):
            DATA.setFlightChangeState(FlightChangeState.paused)
    elif CheckKeyDown(event, keys.H_showDistance[0]):
        DATA.setShowDistance(not DATA.getShowDistance())
    elif CheckKeyDown(event, keys.H_centerOnSun[0]):
        sun = next(filter(lambda x: x.name == "Sun", planets),None)
        CenterScreenOnPlanet(sun)
    elif CheckKeyDown(event, keys.H_centerOnRocket[0]):
        AutomaticZoomOnRocketOnce(rocket)
    elif CheckKeyDown(event, keys.H_drawLine[0]):
        DATA.setDrawOrbit(not DATA.getDrawOrbit())
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
        MousePositionShiftScreen()
        DATA.setScale(DATA.getScale() * 0.75)
        rocket.SetScale(0.75)

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
        MousePositionShiftScreen()
        DATA.setScale(DATA.getScale() * 1.25)
        rocket.SetScale(1.25)

    elif CheckKeyDown(event, keys.H_shiftTimeStepUp[0]):
        ShiftTimeStep(True, rocket, planets)
    elif CheckKeyDown(event, keys.H_shiftTimeStepDown[0]): 
        ShiftTimeStep(False, rocket, planets)
    elif CheckKeyDown(event, keys.H_openSettings[0]):
        ShowSettingsUI()
    return event, rocket, planets 