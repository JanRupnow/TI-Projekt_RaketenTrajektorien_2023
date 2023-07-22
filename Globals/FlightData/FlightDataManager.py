from abc import ABC, abstractmethod

import datetime
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.ZoomGoal import ZoomGoal

class FlightDataManager(ABC):

    _instance = None

    @classmethod
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
 
    @abstractmethod
    def setFlightChangeState(self, value: FlightChangeState):
        self.flightChangeState = value 
    @abstractmethod 
    def getFlightChangeState(self):
        return self.flightChangeState 

    @abstractmethod
    def setCalculationState(self, value: bool):
        self.showDistance = value  
    @abstractmethod    
    def getCalculationStatehowDistance(self):
        return self.showDistance 
    
    @abstractmethod
    def setRun(self, value: bool):
        self.run = value  
    @abstractmethod
    def getRun(self):
        return self.run  
    
    @abstractmethod
    def setScale(self, value: float):
        self.scale = value 
    @abstractmethod 
    def getScale(self):
        return self.scale
       
    @abstractmethod
    def setMoveX(self, value: int):
        self.moveX = value  
    @abstractmethod    
    def getMoveX(self):
        return self.moveX 
    
    @abstractmethod
    def setMoveY(self, value: int):
        self.moveY = value  
    @abstractmethod    
    def getMoveY(self):
        return self.moveY 
    
    @abstractmethod
    def setMouseX(self, value: float):
        self.mouseX = value  
    @abstractmethod    
    def getMouseX(self):
        return self.mouseX
    
    @abstractmethod
    def setMouseY(self, value: float):
        self.mouseY = value  
    @abstractmethod    
    def getMouseY(self):
        return self.mouseY 
    
    @abstractmethod
    def setShowDistance(self, value: bool):
        self.showDistance = value  
    @abstractmethod    
    def getShowDistance(self):
        return self.showDistance 
    
    @abstractmethod
    def setDrawOrbit(self, value: bool):
        self.drawOrbit = value  
    @abstractmethod    
    def getDrawOrbit(self):
        return self.drawOrbit 
    
    @abstractmethod
    def setTimeStep(self, value: float):
        self.timeStep = value  
    @abstractmethod    
    def getTimeStep(self):
        return self.timeStep 
    
    @abstractmethod
    def setSimulationPause(self, value: bool):
        self.simulationIsPaused = value  
    @abstractmethod    
    def getSimulationPause(self):
        return self.simulationIsPaused 
    
    @abstractmethod
    def setZoomGoal(self, value: ZoomGoal):
        self.zoomGoal = value  
    @abstractmethod    
    def getZoomGoal(self):
        return self.zoomGoal
    
    @abstractmethod
    def setTimePassed(self, value: datetime):
        self.timePassed = value  
    @abstractmethod    
    def getTimePassed(self):
        return self.timePassed
    