import math
import numpy as np
from objects.planet import *
from variables.konstanten import *
from objects.rocket import *
import variables.hotkeys as keys
import datetime
from methods.support_methods import *
from views.hotkey_view import *
from DtoProcessEvent import DTOProcessEvent


def addClockTime(pause, time_passed, timestep):
    if not pause:
        time_passed += datetime.timedelta(seconds=timestep)
    return time_passed

def automaticZoomOnRocket(rocket, scale, move_x, move_y):
    if rocket.zoomOnRocket:
        move_x, move_y = -rocket.r_x[rocket.aktuellerschritt] * scale, -rocket.r_z[rocket.aktuellerschritt] * scale
    return move_x, move_y

def automaticZoomOnRocketOnce(rocket, scale, move_x, move_y):
    move_x, move_y = -rocket.r_x[rocket.aktuellerschritt] * scale, -rocket.r_z[rocket.aktuellerschritt] * scale
    return move_x, move_y

def centerScreenOnPlanet(planet, scale, move_x, move_y):
     move_x, move_y = -planet.r_x[planet.aktuellerschritt] * scale, -planet.r_z[planet.aktuellerschritt] * scale
     return move_x, move_y

def scaleRelative(factor, startscale):
    return startscale* factor

def mousePositionShiftScreen(mouse_x, mouse_y, move_x, move_y):
    move_x-=(mouse_x-WIDTH/2)/2
    move_y-=(mouse_y-HEIGHT/2)/2
    return move_x, move_y

def shiftTimeStep(shiftUp, rocket, planets, timestep):
    if shiftUp:
        index = min(alleZeitschritte.index(timestep) + 1, len(alleZeitschritte) - 1)
    else:
        index = max(alleZeitschritte.index(timestep) - 1, 0)
        
    timestep = alleZeitschritte[index]
    rocket.timestep = timestep
    rocket.timestepChanged = True
    for planet in planets:
        planet.timestep = rocket.timestep = timestep
    return timestep


def isInScreen(scale, planet, move_x, move_y, height, width):
    inScreen = planet.r_z[planet.aktuellerschritt]*scale+planet.radius*scale > -move_y-height/2
    inScreen = inScreen or planet.r_z[planet.aktuellerschritt]*scale-planet.radius*scale < -move_y+height/2
    inScreen = inScreen or planet.r_z[planet.aktuellerschritt]*scale+planet.radius*scale > -move_x-width/2
    return inScreen or planet.r_x[planet.aktuellerschritt]*scale-planet.radius*scale < -move_x+width/2

def processKeyEvent(event, dto: DTOProcessEvent, rocket: Rocket, planets):

    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                    (event.key == pygame.K_x or event.key == pygame.K_ESCAPE)):
        dto.run = False
    # Raketenboost erhöhen
    elif checkKeyDown(event, keys.H_rocketBoostForward[0]) and rocket.thrust<10 and (rocket.rocketstarted or  not dto.pause):
        rocket.thrust += 1
        rocket.powerchanged = True
        rocket.rocketstarted = True
    # Raketenboost Links   
    elif checkKeyDown(event, keys.H_rocketBoostLeft[0]) and rocket.angle>-45:
        rocket.angle -= 1
        rocket.powerchanged = True
    # Raketenboost verrigern
    elif checkKeyDown(event, keys.H_lowerRocketBoost[0]) and rocket.thrust>0:
        rocket.thrust -= 1
        rocket.powerchanged = True
    # Raketenboost Rechts
    elif checkKeyDown(event, keys.H_rocketBoostRight[0]) and rocket.angle<45:
        rocket.angle += 1
        rocket.powerchanged = True

    elif checkKeyDown(event, keys.H_zoomRocketStart[0]):
        dto.scale = scaleRelative(200, STARTSCALE)
        rocket.update_scale(200)
        dto.move_x, dto.move_y = automaticZoomOnRocketOnce(rocket, dto.scale, dto.move_x, dto.move_y)
    #Zoom Startorbit
    elif checkKeyDown(event, keys.H_zoomRocketPlanet[0]):
        dto.scale = scaleRelative(5, STARTSCALE)
        rocket.update_scale(5)
        dto.move_x, dto.move_y = automaticZoomOnRocketOnce(rocket, dto.scale, dto.move_x, dto.move_y)
    #Zoom Universum
    elif checkKeyDown(event, keys.H_zoomRocketPlanetSystem[0]):
        dto.scale = scaleRelative(1, STARTSCALE)
        rocket.update_scale(1)
        dto.move_x, dto.move_y = automaticZoomOnRocketOnce(rocket, dto.scale, dto.move_x, dto.move_y)

    elif checkKeyDown(event, keys.H_zoomAutoOnRocket[0]):
        rocket.zoomOnRocket = not rocket.zoomOnRocket
    elif checkKeyDown(event, keys.H_pauseSimulation):
        dto.pause = not dto.pause
    elif checkKeyDown(event, keys.H_showDistance[0]):
        dto.show_distance = not dto.show_distance
    elif checkKeyDown(event, keys.H_centerOnSun[0]):
        sun = next(filter(lambda x: x.name == "Sonne", planets),None)
        dto.move_x, dto.move_y = centerScreenOnPlanet(sun, dto.scale, dto.move_x, dto.move_y)
    elif checkKeyDown(event, keys.H_centerOnRocket[0]):
        dto.move_x, dto.move_y = automaticZoomOnRocketOnce(rocket, dto.scale, dto.move_x, dto.move_y)
    elif checkKeyDown(event, keys.H_drawLine[0]):
        dto.draw_line = not dto.draw_line
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
        dto.mouse_y, dto.mouse_x = pygame.mouse.get_pos()
        dto.move_x, dto.move_y = mousePositionShiftScreen(dto.mouse_x, dto.mouse_y, dto.move_x, dto.move_y)
        dto.scale *= 0.75
        rocket.update_scale(0.75)

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
        dto.mouse_x, dto.mouse_y = pygame.mouse.get_pos()
        dto.move_x, dto.move_y = mousePositionShiftScreen(dto.mouse_x, dto.mouse_y, dto.move_x, dto.move_y)
        dto.scale *= 1.25
        rocket.update_scale(1.25)

    elif checkKeyDown(event, keys.H_shiftTimeStepUp[0]):
        dto.timestep = shiftTimeStep(True, rocket, planets, dto.timestep)
    elif checkKeyDown(event, keys.H_shiftTimeStepDown[0]): 
        dto.timestep = shiftTimeStep(False, rocket, planets, dto.timestep)
    elif checkKeyDown(event, keys.H_openSettings[0]):
        showSettingsUI()
    return dto