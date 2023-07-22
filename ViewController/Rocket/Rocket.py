import numpy as np
import pygame
import math

from Globals.Constants import *
from Globals.FlightData.FlightChangeState import FlightChangeState

from ViewController.Rocket.RocketFlightState import RocketFlightState


class Rocket:
    def __init__(self, startAngle, fuel, mass, startplanet, radius, color, sun, image):
        self.currentStep = CurrentStep
        self.currentCalculationStep = CurrentCalculationStep
        self.mass = mass
        self.fuelmass = fuel
        self.startingAngle = startAngle
        self.position_X= np.zeros(LEN_OF_PREDICTIONS_ARRAY)   # x-Position [m]
        self.position_Y= np.zeros(LEN_OF_PREDICTIONS_ARRAY)   # z-Position [m]
        self.velocity_X=np.zeros(LEN_OF_PREDICTIONS_ARRAY)    # x-Velocity [m/s]
        self.velocity_Y=np.zeros(LEN_OF_PREDICTIONS_ARRAY)    # z-Velocity [m/s]               
        self.c = AirResistance/self.mass
        self.radius = radius
        self.thrust = 0                     # aktuell nicht genutzt     
        self.angle = 0  
        self.flightState = RocketFlightState.notStarted
        self.startplanet = startplanet
        self.predictions = []
        self.color = color
        self.velocity_X[0] = self.startplanet.velocity_X[0]
        self.velocity_Y[0] = self.startplanet.velocity_Y[0]
        ## Berechnung der Startposition der Rakete abhängig vom Startplaneten ohne Skalierung
        self.position_X[0]= startplanet.position_X[self.currentStep] + startplanet.radius * np.cos(self.startingAngle * np.pi / 180)  
        self.position_Y[0]= startplanet.position_Y[self.currentStep] + startplanet.radius * np.sin(self.startingAngle * np.pi / 180)
        self.img = image
        self.img0 = image
        self.notRotatedImg = pygame.transform.scale_by(image, min(0.1*self.radius, 1))
        self.sun = sun
        self.entryAngle = 0

        self.PlanetsInRangeList = [self.startplanet]
        self.nearestPlanet = self.startplanet
        #self.imgage = img0
    # Methode für die x-Komponente
    def F2(self, v, i:int, r0, distanceToSun):
        x = 0
        for r in r0:
            #r0 = np.sqrt( (self.position_X[i] - self.nearestPlanet.position_X[i])**2 + (self.position_Y[i] - self.nearestPlanet.position_Y[i])**2)
            x = ( -(G*self.nearestPlanet.mass/r**2) - (AirResistance*self.GetRelativeVelocity(i)**2*np.sign(self.velocity_X[i]) * p_0 * np.exp(-abs((r-self.nearestPlanet.radius)) / h_s))/(2 * self.mass) ) * ((self.position_X[i] - self.nearestPlanet.position_X[i])/r) #Extrakraft x einbauen

        #distanceToSun = np.sqrt( (self.position_X[i] - self.sun.position_X[i])**2 + (self.position_Y[i] - self.sun.position_Y[i])**2)
        x -= (G*self.sun.mass/distanceToSun**2)* ((self.position_X[i] - self.sun.position_X[i])/distanceToSun)
        #y=-(G*m_E/(position_X**2 + position_Y**2)**1.5) * position_X - c*x**2*np.sign(x)
        if self.thrust != 0:
            x += math.cos(math.atan2(self.velocity_Y[i], self.velocity_X[i]) + self.angle*np.pi/180)*self.thrust*10
        return x
    # Methode für die z-Komponente
    def F1(self, v,i:int, r0, distanceToSun):
        z = 0       
        for r in r0:
            #r0 = np.sqrt( (self.position_X[i] - self.nearestPlanet.position_X[i])**2 + (self.position_Y[i] - self.nearestPlanet.position_Y[i])**2)
            z = ( -(G*self.nearestPlanet.mass/r**2) - (AirResistance*self.GetRelativeVelocity(i)**2*np.sign(self.velocity_Y[i]) * p_0 * np.exp(-abs((r-self.nearestPlanet.radius)) / h_s))/(2 * self.mass) ) * ((self.position_Y[i] - self.nearestPlanet.position_Y[i])/r)

        #distanceToSun = np.sqrt( (self.position_X[i] - self.sun.position_X[i])**2 + (self.position_Y[i] - self.sun.position_Y[i])**2)
        z -= (G*self.sun.mass/distanceToSun**2)* ((self.position_Y[i] - self.sun.position_Y[i])/distanceToSun)
        # TODO muss die Geschwindigkeit relativ zum Planet sein? Eigentlich ja oder? (Luftwiderstand) (wie kann man das besser machen? planetenabhängig?)

        if self.thrust != 0:
            z += math.sin(math.atan2(self.velocity_Y[i], self.velocity_X[i]) + self.angle*np.pi/180)*self.thrust*10
        return z
    # Berechnung nach Runge-Kutta Verfahren
    def CalculateNextStep(self, i: int):
        
        r0 = []
        for planet in self.PlanetsInRangeList:
           r0.append(np.sqrt( (self.position_X[i] - planet.position_X[i])**2 + (self.position_Y[i] - planet.position_Y[i])**2))
        distanceToSun = np.sqrt( (self.position_X[i] - self.sun.position_X[i])**2 + (self.position_Y[i] - self.sun.position_Y[i])**2)

        # z-Komponente
        k1 = self.F1(self.velocity_Y[i],i, r0, distanceToSun)
        k2 = self.F1(self.velocity_Y[i] + k1*DATA.getTimeStep()/2,i, r0, distanceToSun)
        k3 = self.F1(self.velocity_Y[i] + k2*DATA.getTimeStep()/2,i, r0, distanceToSun)
        k4 = self.F1(self.velocity_Y[i] + k3*DATA.getTimeStep()/2,i, r0, distanceToSun)
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        self.velocity_Y[i+1] = self.velocity_Y[i] + k*DATA.getTimeStep()
        self.position_Y[i+1] = self.position_Y[i] + self.velocity_Y[i]*DATA.getTimeStep()

        # x-Komponente
        k1 = self.F2(self.velocity_X[i],i, r0, distanceToSun)
        k2 = self.F2(self.velocity_X[i] + k1*DATA.getTimeStep()/2,i, r0, distanceToSun)
        k3 = self.F2(self.velocity_X[i] + k2*DATA.getTimeStep()/2,i, r0, distanceToSun)
        k4 = self.F2(self.velocity_X[i] + k3*DATA.getTimeStep()/2,i, r0, distanceToSun)
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        self.velocity_X[i+1] = self.velocity_X[i] + k*DATA.getTimeStep()
        self.position_X[i+1] = self.position_X[i] + self.velocity_X[i]*DATA.getTimeStep()


    def SetScale(self,scale):
        self.radius *= scale
        if self.radius > MIN_ROCKET_RADIUS and self.radius < 0.1:
            self.notRotatedImg = pygame.transform.scale_by(self.img0, max(min(0.1*self.radius, 1), 0.1))
                
    def GetCurrentDistanceToNextPlanet(self):
        if self.planetNearEnough == False:
            return -1
        return np.sqrt((self.position_X[self.currentCalculationStep] - self.nearestPlanet.position_X[self.currentCalculationStep])**2 + 
                           (self.position_Y[self.currentCalculationStep] - self.nearestPlanet.position_Y[self.currentCalculationStep])**2)

    def GetRelativeVelocity(self, i):
        if self.flightState == RocketFlightState.flying: 
            return np.sqrt( (self.velocity_X[i] - self.nearestPlanet.position_X[i])**2 
                        + (self.velocity_Y[i] - self.nearestPlanet.position_Y[i])**2)
        return 0
    def GetCurrentRelativeVelocity(self):
        if self.flightState == RocketFlightState.flying:
            return np.sqrt( (self.velocity_X[self.currentStep] - self.nearestPlanet.position_X[self.nearestPlanet.currentStep])**2 
                        + (self.velocity_Y[self.currentStep] - self.nearestPlanet.position_Y[self.nearestPlanet.currentStep])**2)
        return 0

    # in m/s
    def GetAbsoluteVelocity(self):
        if self.flightState == RocketFlightState.flying:
            return np.sqrt(self.velocity_X[self.currentStep]**2 + self.velocity_Y[self.currentStep]**2)
        return 0
    def ResetArray(self):
        self.position_X[1:NUM_OF_PREDICTIONS+1] = self.position_X[NUM_OF_PREDICTIONS:]
        self.position_Y[1:NUM_OF_PREDICTIONS+1] = self.position_Y[NUM_OF_PREDICTIONS:]
        self.velocity_X[1:NUM_OF_PREDICTIONS+1] = self.velocity_X[NUM_OF_PREDICTIONS:]
        self.velocity_Y[1:NUM_OF_PREDICTIONS+1] = self.velocity_Y[NUM_OF_PREDICTIONS:]
        self.currentStep = 1
        self.currentCalculationStep = NUM_OF_PREDICTIONS

    def CalculateEntryAngle(self):
        self.entryAngle =  math.atan2(self.position_Y[self.currentStep] - self.nearestPlanet.position_Y[self.nearestPlanet.currentStep],
                          self.position_X[self.currentStep] - self.nearestPlanet.position_X[self.nearestPlanet.currentStep]) * (180 / np.pi)
        
    def CalculateNewCalculationOfPredictions(self, firstTime, planets):
        for i in range(NUM_OF_PREDICTIONS):
            if firstTime or DATA.getFlightChangeState() == FlightChangeState.timeStepChanged:
                for planet in planets:
                    planet.PredictStep(self.currentCalculationStep, planets, self)
            self.CalculateNextStep(self.currentCalculationStep)
            self.currentCalculationStep += 1

    def CalculateOnePrediction(self, planets):
        for planet in planets:
            planet.PredictStep(self.currentCalculationStep, planets, self)
        self.CalculateNextStep(self.currentCalculationStep)
        self.currentCalculationStep += 1
        
    def ClearArray(self):
        self.position_X = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.position_Y = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.velocity_X = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.velocity_Y = np.zeros(LEN_OF_PREDICTIONS_ARRAY)

        self.currentStep = 0
        self.currentCalculationStep = 0

        self.position_X[0] = self.nearestPlanet.position_X[self.nearestPlanet.currentStep] + self.nearestPlanet.radius * np.cos(self.entryAngle * np.pi / 180)  
        self.position_Y[0] = self.nearestPlanet.position_Y[self.nearestPlanet.currentStep] + self.nearestPlanet.radius * np.sin(self.entryAngle * np.pi / 180)
        self.velocity_X[0] = self.nearestPlanet.position_X[self.nearestPlanet.currentStep]
        self.velocity_Y[0] = self.nearestPlanet.position_Y[self.nearestPlanet.currentStep]

    def UpdatePlanetsInRangeList(self,planets):
        if not self.currentStep % math.ceil(100/DATA.getTimeStep()) == 0:
            return
        self.PlanetsInRangeList = []
        for planet in planets:
            if planet.name != "Sun" and self.GetDistanceToPlanet(planet, self.currentCalculationStep) < planet.radius * 100:
                self.PlanetsInRangeList.append(planet)

    def UpdateNearestPlanet(self,planets):
        if not self.currentStep % math.ceil(100/DATA.getTimeStep()) == 0:
            return
        self.nearestPlanet = min(planets, key=lambda x: self.GetDistanceToPlanet(x, self.currentStep))
    
    def GetDistanceToPlanet(self, planet, step):
        return np.sqrt((self.position_X[step] - planet.position_X[step])**2 
                       + (self.position_Y[step] - planet.position_Y[step])**2)
    
    def CalculateLandedValues(self):
        self.planet = self.nearestPlanet if self.flightState == RocketFlightState.landed else self.startplanet
        self.angle = self.entryAngle if self.flightState == RocketFlightState.landed else self.startingAngle
        self.position_X[0] = self.position_X[self.currentStep] + self.radius * np.cos(self.angle * np.pi / 180)  
        self.position_Y[0] = self.position_Y[self.currentStep] + self.radius * np.sin(self.angle * np.pi / 180)
        self.velocity_X[0] = self.velocity_X[self.currentStep]
        self.velocity_Y[0] = self.velocity_Y[self.currentStep]