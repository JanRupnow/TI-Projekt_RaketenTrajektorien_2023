
import datetime

from Globals.Constants import *
import Globals.Hotkeys as keys

from Views.HotkeyView import *

from ViewController.DtoProcessEvent import DTOProcessEvent
from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketState import RocketState
from ViewController.Planet import Planet

from Methods.SupportMethods import *

def AddClockTime(pause, time_passed, timestep):
    if not pause:
        time_passed += datetime.timedelta(seconds=timestep)
    return time_passed

def AutomaticZoomOnRocket(rocket : Rocket, scale, move_x, move_y):
    if rocket.zoomOnRocket:
        move_x, move_y = -rocket.r_x[rocket.currentStep] * scale, -rocket.r_z[rocket.currentStep] * scale
    return move_x, move_y

def AutomaticZoomOnRocketOnce(rocket : Rocket, scale, move_x, move_y):
    move_x, move_y = -rocket.r_x[rocket.currentStep] * scale, -rocket.r_z[rocket.currentStep] * scale
    return move_x, move_y

def CenterScreenOnPlanet(planet : Planet, scale, move_x, move_y):
     move_x, move_y = -planet.r_x[planet.currentStep] * scale, -planet.r_z[planet.currentStep] * scale
     return move_x, move_y

def ScaleRelative(factor, startscale):
    return startscale* factor

def MousePositionShiftScreen(mouse_x, mouse_y, move_x, move_y):
    move_x-=(mouse_x-WIDTH/2)/2
    move_y-=(mouse_y-HEIGHT/2)/2
    return move_x, move_y

def ShiftTimeStep(shiftUp, rocket : Rocket, planets : list[Planet], timestep):
    index = min(AllTimeSteps.index(timestep) + 1, len(AllTimeSteps) - 1) if shiftUp else max(AllTimeSteps.index(timestep) - 1, 0)
    
    timestep = AllTimeSteps[index]
    rocket.timestep = timestep
    rocket.timestepChanged = True
    for planet in planets:
        planet.timestep = timestep
    return timestep


def PlanetIsInScreen(scale, planet : Planet, move_x, move_y, height, width):
    inScreen = planet.r_z[planet.currentStep]*scale+planet.radius*scale > -move_y-height/2
    inScreen = inScreen and planet.r_z[planet.currentStep]*scale-planet.radius*scale < -move_y+height/2
    inScreen = inScreen and planet.r_x[planet.currentStep]*scale+planet.radius*scale > -move_x-width/2
    return inScreen and planet.r_x[planet.currentStep]*scale-planet.radius*scale < -move_x+width/2


def ProcessHotKeyEvents(event, dto: DTOProcessEvent, rocket : Rocket, planets : list[Planet]):
    KeyPressed = pygame.key.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    window_w, window_h = pygame.display.get_surface().get_size()
    distance = 10
    if  KeyPressed[keys.H_moveScreenLeft[0]] or mouse_x == 0:
        dto.move_x += distance
    elif KeyPressed[keys.H_moveScreenRight[0]] or mouse_x == window_w - 1:
        dto.move_x -= distance
    elif KeyPressed[keys.H_moveScreenUp[0]] or mouse_y == 0:
        dto.move_y += distance
    elif KeyPressed[keys.H_moveScreenDown[0]] or mouse_y == window_h - 1:
        dto.move_y -= distance
    elif ( not event.type == pygame.KEYDOWN ) and KeyPressed[keys.H_rocketBoostForward[0]] and rocket.thrust<10 and (rocket.state == RocketState.flying or not dto.pause):
        rocket.thrust += 1
        rocket.powerchanged = True
        rocket.state = RocketState.flying
    elif ( not event.type == pygame.KEYDOWN ) and KeyPressed[keys.H_rocketBoostLeft[0]] and rocket.angle>-45:
        rocket.angle -= 1
        rocket.powerchanged = True
    elif ( not event.type == pygame.KEYDOWN ) and KeyPressed[keys.H_rocketBoostRight[0]]  and rocket.angle<45:
        rocket.angle += 1
        rocket.powerchanged = True
    elif ( not event.type == pygame.KEYDOWN ) and KeyPressed[keys.H_lowerRocketBoost[0]] and rocket.thrust>0:
        rocket.thrust -= 1
        rocket.powerchanged = True
    elif event.type == pygame.QUIT or CheckKeyDown(event, keys.H_leaveSimulation[0]) or CheckKeyDown(event, keys.H_closeWindow[0]):
        dto.run = False
    #    rocket.powerchanged = True
    elif CheckKeyDown(event, keys.H_zoomRocketStart[0]):
        dto.scale = ScaleRelative(100000, STARTSCALE)
        rocket.SetScale(100000)
        dto.move_x, dto.move_y = AutomaticZoomOnRocketOnce(rocket, dto.scale, dto.move_x, dto.move_y)
    #Zoom Startorbit
    elif CheckKeyDown(event, keys.H_zoomRocketPlanet[0]):
        dto.scale = ScaleRelative(10, STARTSCALE)
        rocket.SetScale(10)
        dto.move_x, dto.move_y = AutomaticZoomOnRocketOnce(rocket, dto.scale, dto.move_x, dto.move_y)
    #Zoom Universum
    elif CheckKeyDown(event, keys.H_zoomRocketPlanetSystem[0]):
        dto.scale = ScaleRelative(1, STARTSCALE)
        rocket.SetScale(1)
        dto.move_x, dto.move_y = AutomaticZoomOnRocketOnce(rocket, dto.scale, dto.move_x, dto.move_y)

    elif CheckKeyDown(event, keys.H_zoomAutoOnReferencePlanet[0]) and not rocket.zoomOnRocket:
        dto.zoomReferencePlanet = not dto.zoomReferencePlanet
    elif CheckKeyDown(event, keys.H_zoomAutoOnRocket[0]) and not dto.zoomReferencePlanet:
        rocket.zoomOnRocket = not rocket.zoomOnRocket
    elif CheckKeyDown(event, keys.H_pauseSimulation[0]):
        dto.pause = not dto.pause
    elif CheckKeyDown(event, keys.H_showDistance[0]):
        dto.show_distance = not dto.show_distance
    elif CheckKeyDown(event, keys.H_centerOnSun[0]):
        sun = next(filter(lambda x: x.name == "Sun", planets),None)
        dto.move_x, dto.move_y = CenterScreenOnPlanet(sun, dto.scale, dto.move_x, dto.move_y)
    elif CheckKeyDown(event, keys.H_centerOnRocket[0]):
        dto.move_x, dto.move_y = AutomaticZoomOnRocketOnce(rocket, dto.scale, dto.move_x, dto.move_y)
    elif CheckKeyDown(event, keys.H_drawLine[0]):
        dto.draw_line = not dto.draw_line
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
        dto.mouse_x, dto.mouse_y = pygame.mouse.get_pos()
        dto.move_x, dto.move_y = MousePositionShiftScreen(dto.mouse_x, dto.mouse_y, dto.move_x, dto.move_y)
        dto.scale *= 0.75
        rocket.SetScale(0.75)

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
        dto.mouse_x, dto.mouse_y = pygame.mouse.get_pos()
        dto.move_x, dto.move_y = MousePositionShiftScreen(dto.mouse_x, dto.mouse_y, dto.move_x, dto.move_y)
        dto.scale *= 1.25
        rocket.SetScale(1.25)

    elif CheckKeyDown(event, keys.H_shiftTimeStepUp[0]):
        dto.timestep = ShiftTimeStep(True, rocket, planets, dto.timestep)
    elif CheckKeyDown(event, keys.H_shiftTimeStepDown[0]): 
        dto.timestep = ShiftTimeStep(False, rocket, planets, dto.timestep)
    elif CheckKeyDown(event, keys.H_openSettings[0]):
        ShowSettingsUI()
    return dto