import datetime

from Globals.Constants import STARTSCALE, AllTimeSteps
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.ZoomGoal import ZoomGoal


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class FlightDataManager(metaclass=SingletonMeta):
    def __init__(self):
        self.flightChangeState = FlightChangeState.unchanged
        self.showDistance = False
        self.run = True
        self.scale = STARTSCALE
        self.drawOrbit = True
        self.moveX = 0
        self.moveY = 0
        self.mouseX = 0
        self.mouseY = 0
        self.timestep = AllTimeSteps[0]
        self.zoom_goal = ZoomGoal.rocket
        self.time_passed = datetime.timedelta(seconds=0)

    def set_flight_change_state(self, value: FlightChangeState):
        self.flightChangeState = value

    def get_flight_change_state(self):
        return self.flightChangeState

    def set_show_distance(self, value: bool):
        self.showDistance = value

    def get_show_distance(self):
        return self.showDistance

    def set_run(self, value: bool):
        self.run = value

    def get_run(self):
        return self.run

    def set_scale(self, value: float):
        self.scale = value

    def get_scale(self):
        return self.scale

    def set_move_x(self, value: int):
        self.moveX = value

    def get_move_x(self):
        return self.moveX

    def set_move_y(self, value: int):
        self.moveY = value

    def get_move_y(self):
        return self.moveY

    def set_mouse_x(self, value: float):
        self.mouseX = value

    def get_mouse_x(self):
        return self.mouseX

    def set_mouse_y(self, value: float):
        self.mouseY = value

    def get_mouse_y(self):
        return self.mouseY

    def set_draw_orbit(self, value: bool):
        self.drawOrbit = value

    def get_draw_orbit(self):
        return self.drawOrbit

    def set_time_step(self, value: float):
        self.timestep = value

    def get_time_step(self):
        return self.timestep

    def set_zoom_goal(self, value: ZoomGoal):
        self.zoom_goal = value

    def get_zoom_goal(self):
        return self.zoom_goal

    def set_time_passed(self, value: datetime):
        self.time_passed = value

    def get_time_passed(self):
        return self.time_passed


DATA = FlightDataManager()