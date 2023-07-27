from enum import Enum


class FlightChangeState(Enum):
    unchanged = 0,
    paused = 1,
    timeStepChanged = 2,  # time and power cant be changed at the same time for a calculation
    powerChanged = 3,
    pausedAndPowerChanged = 4,
    pausedAndTimeStepChanged = 5,# since we use elifs for the hotkey changes

    def __str__(self):
        if self == FlightChangeState.unchanged:
            return "normal"
        elif self == FlightChangeState.paused:
            return "paused"
        elif self == FlightChangeState.timeStepChanged:
            return "timestep shifted"
        elif self == FlightChangeState.powerChanged:
            return "powerChanged"
        elif self == FlightChangeState.pausedAndPowerChanged:
            return "paused and power changed"
        elif self == FlightChangeState.pausedAndTimeStepChanged:
            return "paused and timestep shift"
        else:
            return "unknown"