from enum import Enum


class FlightChangeState(Enum):
    unchanged = 0,
    paused = 1,
    timeStepChanged = 2,  # time and power cant be changed at the same time for a calculation
    powerChanged = 3,  # since we use elifs for the hotkey changes
