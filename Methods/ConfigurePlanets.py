import math
import json

import numpy as np
from sunpy.coordinates import get_body_heliographic_stonyhurst
from Globals.Constants import *
from Methods.ViewMethods import get_start_day, get_start_month, get_start_year, check_date_is_legal
from ViewController.Planet import Planet


def get_start_time() -> datetime.datetime:
    jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json")
    config = json.load(jsonfile)
    time_year = config["StartTime"]["Year"]["value"]
    time_month = config["StartTime"]["Month"]["value"]
    time_day = config["StartTime"]["Day"]["value"]
    return datetime.datetime(time_year, time_month, time_day, 0, 0, 0)


def configure_planets() -> list[Planet]:
    time_year = get_start_year()
    time_month = get_start_month()
    time_day = get_start_day()
    check_date_is_legal(time_day, time_month, time_year)
    simulation_time = f"{time_year}-{time_month}-{time_day}"
    planet_coord = [get_body_heliographic_stonyhurst(
        this_planet, time=simulation_time, include_velocity=False) for this_planet in planetNameArray]

    # Metrics from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

    sun = Planet(0, 0, 695 * 10 ** 6, COLOR_SUN, 1.98892 * 10 ** 30, planetNameArray[0], 0)
    # sun.sun = True

    mercury = Planet(-0.387 * AU, 0, 2439 * 10 ** 3, COLOR_MERCURY, 3.30 * 10 ** 23, planetNameArray[1], 47.36 * 1000)

    venus = Planet(-0.723 * AU, 0, 6052 * 10 ** 3, COLOR_VENUS, 4.8685 * 10 ** 24, planetNameArray[2], 35.02 * 1000)

    earth = Planet(-1 * AU, 0, 6378 * 10 ** 3, COLOR_EARTH, 5.9722 * 10 ** 24, planetNameArray[3], 29.783 * 1000)

    moon = Planet(-1 * AU - 378_000_000, 0, 1750 * 10 ** 3, COLOR_MOON, 73.0 * 10 ** 21, planetNameArray[4], 1.022 * 1000)

    mars = Planet(-1.524 * AU, 0, 3394 * 10 ** 3, COLOR_MARS, 6.39 * 10 ** 23, planetNameArray[5], 24.077 * 1000)

    jupiter = Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 27, planetNameArray[6], 13.06 * 1000)

    saturn = Planet(-9.573 * AU, 0, 60268 * 10 ** 3, COLOR_SATURN, 5.683 * 10 ** 26, planetNameArray[7], 9.68 * 1000)

    uranus = Planet(-19.165 * AU, 0, 25559 * 10 ** 3, COLOR_URANUS, 8.681 * 10 ** 25, planetNameArray[8], 6.80 * 1000)

    neptune = Planet(-30.178 * AU, 0, 24764 * 10 ** 3, COLOR_NEPTUNE, 1.024 * 10 ** 26, planetNameArray[9], 5.43 * 1000)

    planet_list = [neptune, uranus, saturn, jupiter, mars, moon, earth, venus, mercury, sun]
    for planet_name, this_coord in zip(planetNameArray, planet_coord):
        planet = next(filter(lambda x: x.name == planet_name, planet_list), None)
        # Set Start Coordinates 
        planet.position_X[0] = this_coord.radius.value * (np.cos(this_coord.lon.to("rad"))) * AU
        planet.position_Y[0] = this_coord.radius.value * (np.sin(this_coord.lon.to("rad"))) * AU

        # Calculate Angle relative to the sun
        angle = math.atan2(planet.position_Y[0], planet.position_X[0])
        # Calculate positional velocity from mean velocity
        if planet.name != "Moon":
            planet.velocity_X[0] = -planet.meanVelocity * np.sin(angle)
            planet.velocity_Y[0] = planet.meanVelocity * np.cos(angle)

    moon = next(filter(lambda x: x.name == "Moon", planet_list))
    earth = next(filter(lambda x: x.name == "Earth", planet_list))
    angle = math.atan2(moon.position_X[0] - earth.position_X[0], moon.position_Y[0] - earth.position_Y[0])
    moon.velocity_X[0] = earth.velocity_X[0] - moon.meanVelocity * np.sin(angle)
    moon.velocity_Y[0] = earth.velocity_Y[0] + moon.meanVelocity * np.cos(angle)

    return [neptune, uranus, saturn, jupiter, mars, moon, earth, venus, mercury, sun]
