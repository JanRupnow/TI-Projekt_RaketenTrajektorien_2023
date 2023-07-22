from abc import ABC, abstractmethod, ABCMeta

import datetime
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
    def setFlightChangeState(self, value: FlightChangeState):
        self.flightChangeState = value  
    def getFlightChangeState(self):
        return self.flightChangeState 

    def setShowDistance(self, value: bool):
        self.showDistance = value     
    def getshowDistance(self):
        return self.showDistance 
    
    def setRun(self, value: bool):
        self.run = value  
    def getRun(self):
        return self.run  
    
    def setScale(self, value: float):
        self.scale = value 
    def getScale(self):
        return self.scale
       
    def setMoveX(self, value: int):
        self.moveX = value    
    def getMoveX(self):
        return self.moveX 
    
    def setMoveY(self, value: int):
        self.moveY = value   
    def getMoveY(self):
        return self.moveY 
    
    def setMouseX(self, value: float):
        self.mouseX = value   
    def getMouseX(self):
        return self.mouseX
    
    def setMouseY(self, value: float):
        self.mouseY = value   
    def getMouseY(self):
        return self.mouseY 
    
    def setShowDistance(self, value: bool):
        self.showDistance = value
    def getShowDistance(self):
        return self.showDistance 
    
    def setDrawOrbit(self, value: bool):
        self.drawOrbit = value    
    def getDrawOrbit(self):
        return self.drawOrbit 
    
    def setTimeStep(self, value: float):
        self.timeStep = value   
    def getTimeStep(self):
        return self.timeStep 
    
    def setSimulationPause(self, value: bool):
        self.simulationIsPaused = value      
    def getSimulationPause(self):
        return self.simulationIsPaused 
    
    def setZoomGoal(self, value: ZoomGoal):
        self.zoomGoal = value   
    def getZoomGoal(self):
        return self.zoomGoal
    
    def setTimePassed(self, value: datetime):
        self.timePassed = value      
    def getTimePassed(self):
        return self.timePassed