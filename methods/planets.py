from objects.planet import Planet
from variables.konstanten import *

# Metric from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

def getInitialPlanets():
    sun = Planet(0, 0, 695 * 10 ** 6, COLOR_SUN, 1.98892 * 10 ** 30,"Sonne")
    sun.sun = True

    mercury = Planet(-0.387 * AU, 0, 2439 * 10 ** 3, COLOR_MERCURY, 3.30 * 10 ** 23,"Merkur")
    mercury.v_z[0] = 47.4 * 1000

    venus = Planet(-0.723 * AU, 0, 6052 * 10 ** 3, COLOR_VENUS, 4.8685 * 10 ** 24,"Venus")
    venus.v_z[0] = 35.02 * 1000

    earth = Planet(-1 * AU, 0, 6378 * 10 ** 3, COLOR_EARTH, 5.9722 * 10 ** 24,"Erde")
    earth.v_z[0] = 29.783 * 1000

    mars = Planet(-1.524 * AU, 0, 3394  * 10 ** 3, COLOR_MARS, 6.39 * 10 ** 23,"Mars")
    mars.v_z[0] = 24.077 * 1000

    jupiter = Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 27,"Jupiter")
    jupiter.v_z[0] = 13.06 * 1000

    saturn = Planet(-9.573 * AU, 0, 60268  * 10 ** 3, COLOR_SATURN, 5.683 * 10 ** 26,"Saturn")
    saturn.v_z[0] = 9.68 * 1000

    uranus = Planet(-19.165 * AU, 0, 25559  * 10 ** 3, COLOR_URANUS, 8.681 * 10 ** 25,"Uranus")
    uranus.v_z[0] = 6.80 * 1000

    neptune = Planet(-30.178 * AU, 0, 24764  * 10 ** 3, COLOR_NEPTUNE, 1.024 * 10 ** 26,"Neptun")
    neptune.v_z[0] = 5.43 * 1000

    moon = Planet(-1*AU-378_000_000,0,1750*10**3,(220,220,220),73*10**21,"Mond")
    moon.v_z[0] = earth.v_z[0]+1.022*1000

    return [moon,neptune, uranus, saturn, jupiter, mars,earth, venus, mercury, sun]