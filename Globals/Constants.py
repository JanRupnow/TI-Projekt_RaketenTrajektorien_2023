import datetime
import sys

import numpy as np
import pandas as pd

import pygame

pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
TITLE_FONT_1 = pygame.font.SysFont("Trebuchet MS", 30, True)

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
# Start zoom depth
STARTSCALE = 200 / AU

AirResistance = 0.0162  # Luftwiderstandsbeiwert
p_0 = 1.225  # Luftdichte auf Meereshöhe [kg/m^3]
h_s = 8400  # Skalenhöhe [m]

planetNameArray = ["Sun", "Mercury", "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


# Should start with initialized 0
CurrentStep = 0
CurrentCalculationStep = 0


CRASH_VELOCITY = 1_000_000  # m/s
MIN_ROCKET_RADIUS = 2
MAX_ROCKET_RADIUS = 0.1
NUM_OF_PREDICTIONS = 1000
AllTimeSteps = [1 / 60, 5 / 60, 10 / 60, 25 / 60, 100 / 60, 500 / 60, 1000 / 60, 2500 / 60, 10000 / 60, 25000 / 60,
                100000 / 60]
# must be twice the size so the array has room for calculations before resetting to 0:NUM_OF_PREDICTIONS
LEN_OF_PREDICTIONS_ARRAY = NUM_OF_PREDICTIONS * 2

if sys.platform.startswith('win'):
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u'LJ.SFS.v1')

pygame.init()
WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

rocket = pygame.image.load("Images/RocketIcon.png").convert_alpha()
pygame.display.set_icon(rocket)
pygame.display.set_caption("Spaceflight Simulator")
pygame.display.set_allow_screensaver(True)

CLOCK = pygame.time.Clock()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
FILE_NAME = f"Globals/FlightData/Flights/{timestamp}_Flight.csv"
with open(FILE_NAME, "w") as file:
    file.write("Time,Position_X,Position_Y,Velocity_X,Velocity_Y,Power,Angle,Force,Rocket_Fuel,Acceleration_Planets,Acceleration_Sun,Acceleration_Air\n")

DATA_ARRAY = np.zeros((NUM_OF_PREDICTIONS+1, 8), dtype="object")
DF_COLUMNS = ["Time", "Position_X", "Position_Y", "Velocity_X", "Velocity_Y", "Power", "Angle",
                                "Force", "Rocket_Fuel", "Acceleration_Planets", "Acceleration_Sun", "Acceleration_Air"]

DATA_df = pd.DataFrame(columns=DF_COLUMNS)
