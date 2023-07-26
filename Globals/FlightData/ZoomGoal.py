from enum import Enum


class ZoomGoal(Enum):
    none = 0,
    nearestPlanet = 1,
    rocket = 2,

    def __str__(self):
        if self == ZoomGoal.none:
            return "Off"
        elif self == ZoomGoal.nearestPlanet:
            return "Nearest Planet"
        elif self == ZoomGoal.rocket:
            return "Rocket"
        else:
            return "unknown"
