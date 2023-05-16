import math
import numpy as np
from planet import *
from konstanten import *
from rocket import *
from main import *
import datetime


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

def scaleRelative(factor):
    global STARTSCALE
    return STARTSCALE* factor

def mousePositionShiftScreen(mouse_x, mouse_y, move_x, move_y):
    global HEIGHT, WIDTH
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
