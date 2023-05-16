import numpy as np

COLOR_WHITE = (255, 255, 255)
COLOR_UNIVERSE = (36, 36, 36)
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (173, 168, 165)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (216, 202, 157)
COLOR_SATURN = (191, 189, 175)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)
### Solarsystem Variablen 
AU = 149.6e6 * 1000  # Astronomical unit
G = 6.67428e-11  # Gravitational constant
SCALE = 200 / AU
StartScale = SCALE
### Generelle Variablen
Luftwiederstand = 0.0162        # Luftwiderstandsbeiwert                     #  - Verwendung zur Einstellung des Schubs
FallBeschleunigung = 9.81       # [m/s^2]
p_0 = 1.225 # Luftdichte auf Meereshöhe [kg/m^3]
h_s = 8400  # Skalenhöhe [m]

### Zeit-Variablen
Startzeit = 0                   # [s]                # [s]
Rechenschritte = 100000
Endzeit = Rechenschritte*5
#dt=(Endzeit-Startzeit)/Rechenschritte
TIMESTEP = 100
AktuellerSchritt = 0
AktuellerRechenschritt = 0
alleZeitschritte = [1, 5, 10, 25, 100, 500, 1000, 2500, 10000, 25000, 100000]


MIN_ROCKET_RADIUS = 2
