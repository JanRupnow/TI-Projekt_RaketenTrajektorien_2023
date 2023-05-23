from objects.planet import Planet
from variables.konstanten import *
import datetime
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel
from sunpy.coordinates import get_body_heliographic_stonyhurst
import astropy.units as u
import pygame
from objects.planet import *
import math

pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h




##api für planeten koodinaten
now = datetime.datetime.now()
obstime = Time(now)
planet_coord = [get_body_heliographic_stonyhurst(
    this_planet, time=obstime, include_velocity=True) for this_planet in planetNameArray]
for planet in planet_coord:
    print(planet)

# Metric from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

def getInitialPlanets():
    sun = Planet(0, 0, 695 * 10 ** 6, COLOR_SUN, 1.98892 * 10 ** 30,planetNameArray[0], 0)
    sun.sun = True

    mercury = Planet(-0.387 * AU, 0, 2439 * 10 ** 3, COLOR_MERCURY, 3.30 * 10 ** 23,planetNameArray[1], 47.36 * 1000)

    venus = Planet(-0.723 * AU, 0, 6052 * 10 ** 3, COLOR_VENUS, 4.8685 * 10 ** 24,planetNameArray[2], 35.02 * 1000)

    earth = Planet(-1 * AU, 0, 6378 * 10 ** 3, COLOR_EARTH, 5.9722 * 10 ** 24,planetNameArray[3], 29.783 * 1000)

    moon = Planet(-1*AU-378_000_000,0,1750*10**3,(220,220,220),73*10**21,planetNameArray[4], 1.022*1000)

    mars = Planet(-1.524 * AU, 0, 3394  * 10 ** 3, COLOR_MARS, 6.39 * 10 ** 23,planetNameArray[5], 24.077 * 1000)

    jupiter = Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 27,planetNameArray[6], 13.06 * 1000)

    saturn = Planet(-9.573 * AU, 0, 60268  * 10 ** 3, COLOR_SATURN, 5.683 * 10 ** 26,planetNameArray[7], 9.68 * 1000)

    uranus = Planet(-19.165 * AU, 0, 25559  * 10 ** 3, COLOR_URANUS, 8.681 * 10 ** 25,planetNameArray[8], 6.80 * 1000)

    neptune = Planet(-30.178 * AU, 0, 24764  * 10 ** 3, COLOR_NEPTUNE, 1.024 * 10 ** 26,planetNameArray[9], 5.43 * 1000)

    planetlist = [neptune, uranus, saturn, jupiter, mars, moon, earth, venus, mercury, sun]
    for planet_name, this_coord in zip(planetNameArray, planet_coord):
        planet = next(filter(lambda x: x.name == planet_name, planetlist),None)
        # Set Start Coordinates 
        planet.r_x[0] = this_coord.radius.value*(np.cos(this_coord.lon.to("rad")))*AU
        planet.r_z[0] = this_coord.radius.value*(np.sin(this_coord.lon.to("rad")))*AU

        θ = math.atan2(planet.r_z[0], planet.r_x[0])
        if planet.name != "Moon":
            planet.v_x[0] = -planet.meanVelocity * np.sin(θ)
            planet.v_z[0] = planet.meanVelocity * np.cos(θ)
        print(f"{planet.name}: r: {planet.r_x[0]}{planet.r_z[0]},v: {planet.v_x[0]} {planet.v_z[0]}")
        # Convert AU per day to m/s
        #velocity = np.multiply(get_body_barycentric_posvel(planet_name, Time(datetime.datetime.now()))[1].xyz.value,(-AU/86400))
        # Set Start Velocity
        #print(f"{planet.name}: {velocity}")
        #planet.v_x[0] = velocity[2]
        #planet.v_z[0] = velocity[0]
        #print(f"{planet.name}: {planet.v_x[0]} {planet.v_z[0]}")

    moon = next(filter(lambda x: x.name == "Moon", planetlist))
    earth = next(filter(lambda x: x.name == "Earth", planetlist))
    θ = math.atan2(moon.r_x[0]-earth.r_x[0], moon.r_z[0]-earth.r_z[0])
    moon.v_x[0] = earth.v_x[0] - moon.meanVelocity * np.sin(θ)
    moon.v_z[0] = earth.v_z[0] + moon.meanVelocity * np.cos(θ)
        
    return [neptune, uranus, saturn, jupiter, mars, moon, earth, venus, mercury, sun]