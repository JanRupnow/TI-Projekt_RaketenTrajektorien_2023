from enum import Enum

class RocketChangeState(Enum):
    unchanged = 0,
    timeStepChanged = 1, # time and power cant be changed at the same time for a calculation
    powerChanged = 2, # since we use elifs for the hotkey changes