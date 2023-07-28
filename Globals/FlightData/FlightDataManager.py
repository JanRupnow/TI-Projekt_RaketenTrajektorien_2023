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
        self._flight_change_state = FlightChangeState.unchanged
        self._show_distance = False
        self._run = True
        self._scale = STARTSCALE
        self._draw_orbit = True
        self._move_x = 0
        self._move_y = 0
        self._mouse_x = 0
        self._mouse_y = 0
        self._time_step = AllTimeSteps[0]
        self._zoom_goal = ZoomGoal.rocket
        self._time_passed = datetime.timedelta(seconds=0)
        self._advanced_interface = True

    

    @property
    def flight_change_state(self):
        return self._flight_change_state

    @flight_change_state.setter
    def flight_change_state(self, value: FlightChangeState):
        self._flight_change_state = value

    @property
    def show_distance(self):
        return self._show_distance
    
    @show_distance.setter
    def show_distance(self, value: bool):
        self._show_distance = value

    @property
    def run(self):
        return self._run
    
    @run.setter
    def run(self, value: bool):
        self._run = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value

    @property
    def move_x(self):
        return self._move_x

    @move_x.setter
    def move_x(self, value: int):
        self._move_x = value

    @property
    def move_y(self):
        return self._move_y
        
    @move_y.setter
    def move_y(self, value: int):
        self._move_y = value

    @property
    def mouse_x(self):
        return self._mouse_x

    @mouse_x.setter
    def mouse_x(self, value: float):
        self._mouse_x = value

    @property
    def mouse_y(self):
        return self._mouse_y
    
    @mouse_y.setter
    def mouse_y(self, value: float):
        self._mouse_y = value

    @property
    def draw_orbit(self):
        return self._draw_orbit
    
    @draw_orbit.setter
    def draw_orbit(self, value: bool):
        self._draw_orbit = value

    @property
    def time_step(self):
        return self._time_step
    
    @time_step.setter
    def time_step(self, value: float):
        if min(AllTimeSteps) < value < max(AllTimeSteps):
            self._time_step = value
        else:
            raise ValueError("Invalid time step value. The value should be within the range of AllTimeSteps.")

    @property
    def zoom_goal(self):
        return self._zoom_goal
    
    @zoom_goal.setter
    def zoom_goal(self, value: ZoomGoal):
        self._zoom_goal = value

    @property
    def time_passed(self):
        return self._time_passed

    @time_passed.setter
    def time_passed(self, value: datetime):
        self._time_passed = value

    @property
    def advanced_interface(self):
        return self._advanced_interface

    @advanced_interface.setter
    def advanced_interface(self, value: bool):
        self._advanced_interface = value


DATA = FlightDataManager()
