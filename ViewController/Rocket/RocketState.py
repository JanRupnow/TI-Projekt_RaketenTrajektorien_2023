from enum import Enum

class RocketState(Enum):
    notStarted = 0,
    flying = 1,
    landed = 2,
    crashed = 3,