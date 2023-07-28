from enum import Enum


class RocketFlightState(Enum):
    landed = 0,
    flying = 1,
    crashed = 2,

    def __str__(self):
        if self == RocketFlightState.landed:
            return "landed"
        elif self == RocketFlightState.flying:
            return "flying"
        elif self == RocketFlightState.crashed:
            return "crashed"
        else:
            return "unknown"
