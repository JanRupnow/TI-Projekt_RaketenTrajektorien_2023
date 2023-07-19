import numpy as np
import pygame
import math

from Globals.Constants import *

from ViewController.Rocket.RocketState import RocketState


class Rocket:
    def __init__(self, startAngle, fuel, mass, startplanet, radius, color, sun, image):
        self.currentStep = CurrentStep
        self.currentCalculationStep = CurrentCalculationStep
        self.timestep = TimeStep
        self.timestepChanged = False
        self.mass = mass
        self.fuelmass = fuel
        self.startingAngle = startAngle
        self.r_x= np.zeros(LEN_OF_PREDICTIONS_ARRAY)   # x-Position [m]
        self.r_z= np.zeros(LEN_OF_PREDICTIONS_ARRAY)   # z-Position [m]
        self.v_x=np.zeros(LEN_OF_PREDICTIONS_ARRAY)    # x-Geschwindigkeit [m/s]
        self.v_z=np.zeros(LEN_OF_PREDICTIONS_ARRAY)    # z-Geschwindigkeit [m/s]               
        self.c = AirResistance/self.mass
        self.radius = radius
        self.thrust = 0                     # aktuell nicht genutzt     
        self.angle = 0  
        self.state = RocketState.notStarted
        self.powerchanged = False
        self.color = color
        self.startplanet = startplanet
        self.predictions = []
        self.v_x[0] = self.startplanet.v_x[0]
        self.v_z[0] = self.startplanet.v_z[0]
        ## Berechnung der Startposition der Rakete abhängig vom Startplaneten ohne Skalierung
        self.r_x[0]= startplanet.r_x[self.currentStep] + startplanet.radius * np.cos(self.startingAngle * np.pi / 180)  
        self.r_z[0]= startplanet.r_z[self.currentStep] + startplanet.radius * np.sin(self.startingAngle * np.pi / 180)
        self.img = image
        self.img0 = image
        self.notRotatedImg = pygame.transform.scale_by(image, min(0.1*self.radius, 1))
        self.zoomOnRocket = False
        self.sun = sun
        self.entryAngle = 0

        self.PlanetsInRangeList = [self.startplanet]
        self.nearestPlanet = self.startplanet
        #self.imgage = img0
    # Methode für die x-Komponente
    def F2(self, v, i:int, r0, distanceToSun):
        x = 0
        for r in r0:
            #r0 = np.sqrt( (self.r_x[i] - self.nearestPlanet.r_x[i])**2 + (self.r_z[i] - self.nearestPlanet.r_z[i])**2)
            x = ( -(G*self.nearestPlanet.mass/r**2) - (AirResistance*self.GetRelativeVelocity(i)**2*np.sign(self.v_x[i]) * p_0 * np.exp(-abs((r-self.nearestPlanet.radius)) / h_s))/(2 * self.mass) ) * ((self.r_x[i] - self.nearestPlanet.r_x[i])/r) #Extrakraft x einbauen

        #distanceToSun = np.sqrt( (self.r_x[i] - self.sun.r_x[i])**2 + (self.r_z[i] - self.sun.r_z[i])**2)
        x -= (G*self.sun.mass/distanceToSun**2)* ((self.r_x[i] - self.sun.r_x[i])/distanceToSun)
        #y=-(G*m_E/(r_x**2 + r_z**2)**1.5) * r_x - c*x**2*np.sign(x)
        if self.thrust != 0:
            x += math.cos(math.atan2(self.v_z[i], self.v_x[i]) + self.angle*np.pi/180)*self.thrust*10
        return x
    # Methode für die z-Komponente
    def F1(self, v,i:int, r0, distanceToSun):
        z = 0       
        for r in r0:
            #r0 = np.sqrt( (self.r_x[i] - self.nearestPlanet.r_x[i])**2 + (self.r_z[i] - self.nearestPlanet.r_z[i])**2)
            z = ( -(G*self.nearestPlanet.mass/r**2) - (AirResistance*self.GetRelativeVelocity(i)**2*np.sign(self.v_z[i]) * p_0 * np.exp(-abs((r-self.nearestPlanet.radius)) / h_s))/(2 * self.mass) ) * ((self.r_z[i] - self.nearestPlanet.r_z[i])/r)

        #distanceToSun = np.sqrt( (self.r_x[i] - self.sun.r_x[i])**2 + (self.r_z[i] - self.sun.r_z[i])**2)
        z -= (G*self.sun.mass/distanceToSun**2)* ((self.r_z[i] - self.sun.r_z[i])/distanceToSun)
        # TODO muss die Geschwindigkeit relativ zum Planet sein? Eigentlich ja oder? (Luftwiderstand) (wie kann man das besser machen? planetenabhängig?)

        if self.thrust != 0:
            z += math.sin(math.atan2(self.v_z[i], self.v_x[i]) + self.angle*np.pi/180)*self.thrust*10
        return z
    # Berechnung nach Runge-Kutta Verfahren
    def CalculateNextStep(self, i: int):
        
        r0 = []
        for planet in self.PlanetsInRangeList:
           r0.append(np.sqrt( (self.r_x[i] - planet.r_x[i])**2 + (self.r_z[i] - planet.r_z[i])**2))
        distanceToSun = np.sqrt( (self.r_x[i] - self.sun.r_x[i])**2 + (self.r_z[i] - self.sun.r_z[i])**2)

        # z-Komponente
        k1 = self.F1(self.v_z[i],i, r0, distanceToSun)
        k2 = self.F1(self.v_z[i] + k1*self.timestep/2,i, r0, distanceToSun)
        k3 = self.F1(self.v_z[i] + k2*self.timestep/2,i, r0, distanceToSun)
        k4 = self.F1(self.v_z[i] + k3*self.timestep/2,i, r0, distanceToSun)
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        self.v_z[i+1] = self.v_z[i] + k*self.timestep
        self.r_z[i+1] = self.r_z[i] + self.v_z[i]*self.timestep

        # x-Komponente
        k1 = self.F2(self.v_x[i],i, r0, distanceToSun)
        k2 = self.F2(self.v_x[i] + k1*self.timestep/2,i, r0, distanceToSun)
        k3 = self.F2(self.v_x[i] + k2*self.timestep/2,i, r0, distanceToSun)
        k4 = self.F2(self.v_x[i] + k3*self.timestep/2,i, r0, distanceToSun)
        k = (k1 + 2*k2 + 2*k3 + k4)/6
        self.v_x[i+1] = self.v_x[i] + k*self.timestep
        self.r_x[i+1] = self.r_x[i] + self.v_x[i]*self.timestep


    def SetScale(self,scale):
        self.radius *= scale
        if self.radius > MIN_ROCKET_RADIUS and self.radius < 0.1:
            self.notRotatedImg = pygame.transform.scale_by(self.img0, max(min(0.1*self.radius, 1), 0.1))
                
    def GetCurrentDistanceToNextPlanet(self):
        if self.planetNearEnough == False:
            return -1
        return np.sqrt((self.r_x[self.currentCalculationStep] - self.nearestPlanet.r_x[self.currentCalculationStep])**2 + 
                           (self.r_z[self.currentCalculationStep] - self.nearestPlanet.r_z[self.currentCalculationStep])**2)

    def GetRelativeVelocity(self, i):
        if not self.state == RocketState.currentlyFlying:
            return 0
        return np.sqrt( (self.v_x[i] - self.nearestPlanet.v_x[i])**2 
                        + (self.v_z[i] - self.nearestPlanet.v_z[i])**2)
        
    def GetCurrentRelativeVelocity(self):
        if not self.state == RocketState.currentlyFlying:
            return 0
        return np.sqrt( (self.v_x[self.currentStep] - self.nearestPlanet.v_x[self.nearestPlanet.currentStep])**2 
                        + (self.v_z[self.currentStep] - self.nearestPlanet.v_z[self.nearestPlanet.currentStep])**2)


    # in m/s
    def GetAbsoluteVelocity(self):
        if self.state == RocketState.currentlyFlying:
            return np.sqrt(self.v_x[self.currentStep]**2 + self.v_z[self.currentStep]**2)
        return 0
    def ResetArray(self):
        self.r_x[1:NUM_OF_PREDICTIONS+1] = self.r_x[NUM_OF_PREDICTIONS:]
        self.r_z[1:NUM_OF_PREDICTIONS+1] = self.r_z[NUM_OF_PREDICTIONS:]
        self.v_x[1:NUM_OF_PREDICTIONS+1] = self.v_x[NUM_OF_PREDICTIONS:]
        self.v_z[1:NUM_OF_PREDICTIONS+1] = self.v_z[NUM_OF_PREDICTIONS:]
        self.currentStep = 1
        self.currentCalculationStep = NUM_OF_PREDICTIONS

    def CalculateEntryAngle(self):
        self.entryAngle =  math.atan2(self.r_z[self.currentStep] - self.nearestPlanet.r_z[self.nearestPlanet.currentStep],
                          self.r_x[self.currentStep] - self.nearestPlanet.r_x[self.nearestPlanet.currentStep]) * (180 / np.pi)
        
    def CalculateNewCalculationOfPredictions(self, firstTime, planets, paused):
        for i in range(NUM_OF_PREDICTIONS):
            if firstTime or self.timestepChanged:
                for planet in planets:
                    planet.PredictStep(self.currentCalculationStep, planets, paused, self)
            self.CalculateNextStep(self.currentCalculationStep)
            self.currentCalculationStep += 1

    def CalculateOnePrediction(self, planets, paused):
        for planet in planets:
            planet.PredictStep(self.currentCalculationStep, planets, paused, self)
        self.CalculateNextStep(self.currentCalculationStep)
        self.currentCalculationStep += 1
        
    def ClearArray(self):
        self.r_x = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.r_z = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.v_x = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.v_z = np.zeros(LEN_OF_PREDICTIONS_ARRAY)

        self.currentStep = 0
        self.currentCalculationStep = 0

        self.r_x[0] = self.nearestPlanet.r_x[self.nearestPlanet.currentStep] + self.nearestPlanet.radius * np.cos(self.entryAngle * np.pi / 180)  
        self.r_z[0] = self.nearestPlanet.r_z[self.nearestPlanet.currentStep] + self.nearestPlanet.radius * np.sin(self.entryAngle * np.pi / 180)
        self.v_x[0] = self.nearestPlanet.v_x[self.nearestPlanet.currentStep]
        self.v_z[0] = self.nearestPlanet.v_z[self.nearestPlanet.currentStep]

    def UpdatePlanetsInRangeList(self,planets):
        if not self.currentStep % math.ceil(100/self.timestep) == 0:
            return
        self.PlanetsInRangeList = []
        for planet in planets:
            if planet.name != "Sun" and self.GetDistanceToPlanet(planet, self.currentCalculationStep) < planet.radius * 100:
                self.PlanetsInRangeList.append(planet)

    def UpdateNearestPlanet(self,planets):
        if not self.currentStep % math.ceil(100/self.timestep) == 0:
            return
        self.nearestPlanet = min(planets, key=lambda x: self.GetDistanceToPlanet(x, self.currentStep))
    
    def GetDistanceToPlanet(self, planet, step):
        return np.sqrt((self.r_x[step] - planet.r_x[step])**2 
                       + (self.r_z[step] - planet.r_z[step])**2)