from enum import Enum

class RocketFlightState(Enum):
    notStarted = 0,
    flying = 1,
    landed = 2,
    crashed = 3,