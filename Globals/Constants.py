import datetime
import json
import pygame

pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)
COLOR_WHITE = (255, 255, 255)
COLOR_UNIVERSE = (36, 36, 36)
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (173, 168, 165)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MOON = (220, 220, 220)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (216, 202, 157)
COLOR_SATURN = (191, 189, 175)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)
# Solarsystem Variablen
AU = 149.6e6 * 1000  # Astronomical unit
G = 6.67428e-11  # Gravitational constant
STARTSCALE = 200 / AU
# Generelle Variablen
AirResistance = 0.0162  # Luftwiderstandsbeiwert                     #  - Verwendung zur Einstellung des Schubs
Gravity = 9.81  # [m/s^2]
p_0 = 1.225  # Luftdichte auf Meereshöhe [kg/m^3]
h_s = 8400  # Skalenhöhe [m]
planetNameArray = ["Sun", "Mercury", "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
# Zeit-Variablen
StartTime = 0  # [s]                # [s]
CalculationSteps = 100000
EndTime = CalculationSteps * 5
# dt=(Endzeit-Startzeit)/Rechenschritte
CurrentStep = 0
CurrentCalculationStep = 0
AllTimeSteps = [1 / 60, 5 / 60, 10 / 60, 25 / 60, 100 / 60, 500 / 60, 1000 / 60, 2500 / 60, 10000 / 60, 25000 / 60,
                100000 / 60]
jsonfile = open("./Globals/RocketConfig/CurrentRocketConfig.json")
config = json.load(jsonfile)
time_year = config["StartTime"]["Year"]["value"]
time_month = config["StartTime"]["Month"]["value"]
time_day = config["StartTime"]["Day"]["value"]
Now = datetime.datetime(time_year, time_month, time_day, 0, 0, 0)
MoveX = 0
MoveY = 0
MIN_ROCKET_RADIUS = 2
NUM_OF_PREDICTIONS = 1000
# muss größer als NUM_OF_PREDICTIONS sein
LEN_OF_PREDICTIONS_ARRAY = NUM_OF_PREDICTIONS * 2
pygame.init()
CLOCK = pygame.time.Clock()
WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h


