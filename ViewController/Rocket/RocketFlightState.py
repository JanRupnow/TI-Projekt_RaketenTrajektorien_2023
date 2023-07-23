from enum import Enum


class RocketFlightState(Enum):
    landed = 0,
    flying = 1,
    crashed = 2,
