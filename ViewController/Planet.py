import math
import numpy as np

from Globals.Constants import *

from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState

class Planet:

    def __init__(self, x, y, radius, color, mass, name, velocity):
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name
        self.timestep = TimeStep
        self.distanceToRocket = 2* radius
        # drawing radius used only for displaying not calculating!!!
        self.scaleR = radius
        self.meanVelocity = velocity

        self.position_X = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.position_Y = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.velocity_X = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.velocity_Y = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.currentStep = 0
        self.currentCalculationStep = 0

        self.position_X[0] = x
        self.position_Y[0] = y

    def Attraction(self, other, i):
        otheposition_X, other_y = other.position_X[i], other.position_Y[i]
        distance_x = otheposition_X - self.position_X[i]
        distance_y = other_y - self.position_Y[i]
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def ResetPlanetsArrayToSyncWithRocket(self):
        self.position_X[0:NUM_OF_PREDICTIONS] = self.position_X[self.currentStep:self.currentStep+NUM_OF_PREDICTIONS]
        self.position_Y[0:NUM_OF_PREDICTIONS] = self.position_Y[self.currentStep:self.currentStep+NUM_OF_PREDICTIONS]
        self.velocity_X[0:NUM_OF_PREDICTIONS] = self.velocity_X[self.currentStep:self.currentStep+NUM_OF_PREDICTIONS]
        self.velocity_Y[0:NUM_OF_PREDICTIONS] = self.velocity_Y[self.currentStep:self.currentStep+NUM_OF_PREDICTIONS]
        self.currentStep = 0
        self.currentCalculationStep = NUM_OF_PREDICTIONS-1

    def ResetArray(self):
        self.position_X[1:NUM_OF_PREDICTIONS+1] = self.position_X[NUM_OF_PREDICTIONS:]
        self.position_Y[1:NUM_OF_PREDICTIONS+1] = self.position_Y[NUM_OF_PREDICTIONS:]
        self.velocity_X[1:NUM_OF_PREDICTIONS+1] = self.velocity_X[NUM_OF_PREDICTIONS:]
        self.velocity_Y[1:NUM_OF_PREDICTIONS+1] = self.velocity_Y[NUM_OF_PREDICTIONS:]
        self.currentStep = 1
        self.currentCalculationStep = NUM_OF_PREDICTIONS

    def SetScale(self, scale):
        self.scaleR *= scale

    def PredictStep(self, i, planets : list[__init__], pause, rocket : Rocket):
        self.currentCalculationStep = i
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.Attraction(planet, i)
            total_fx += fx
            total_fy += fy
        self.velocity_X[i+1] = self.velocity_X[i] + total_fx / self.mass * self.timestep
        self.velocity_Y[i+1] = self.velocity_Y[i] + total_fy / self.mass * self.timestep
        self.position_X[i+1] = self.position_X[i] + self.velocity_X[i+1] * self.timestep
        self.position_Y[i+1] = self.position_Y[i] + self.velocity_Y[i+1] * self.timestep

        self.UpdateDistanceToRocket(rocket)

        if not pause:
            self.currentCalculationStep += 1

    def UpdateDistanceToRocket(self, rocket : Rocket):
        self.distanceToRocket = math.sqrt((self.position_X[self.currentStep]-rocket.position_X[rocket.currentStep])**2+(self.position_Y[self.currentStep]-rocket.position_Y[rocket.currentStep])**2)

    def PredictNext(self, planets : list[__init__], pause):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.Attraction(planet, self.currentCalculationStep)
            total_fx += fx
            total_fy += fy
        self.velocity_X[self.currentCalculationStep+1] = self.velocity_X[self.currentCalculationStep] + total_fx / self.mass * self.timestep
        self.velocity_Y[self.currentCalculationStep+1] = self.velocity_Y[self.currentCalculationStep] + total_fy / self.mass * self.timestep
        self.position_X[self.currentCalculationStep+1] = self.position_X[self.currentCalculationStep] + self.velocity_X[self.currentCalculationStep+1] * self.timestep
        self.position_Y[self.currentCalculationStep+1] = self.position_Y[self.currentCalculationStep] + self.velocity_Y[self.currentCalculationStep+1] * self.timestep

        if not pause:
            self.currentCalculationStep += 1
        
    def LineIsInScreen(self, line, move_x, move_y, height , width):
        lineInScreen = line[(line[:,0]< -move_x+width/2) & (line[:,0] > -move_x-width/2)]
        lineInScreen = lineInScreen[(lineInScreen[:,1] > -move_y-height/2) & (lineInScreen[:,1] < -move_y+height/2)]
        lineInScreen[:,0] = lineInScreen[:,0]+move_x+width/2
        lineInScreen[:,1] = lineInScreen[:,1]+move_y+ height/2
        return lineInScreen
        
    def CheckCollision(self):
        if self.distanceToRocket <= self.radius*95/100:
            return True
        return False
    
    def CheckLanding(self, rocket : Rocket, run):
        if not self.currentStep % math.ceil(100/self.timestep) == 0:
            return
        if self.distanceToRocket <= self.radius *95/100 and rocket.GetCurrentRelativeVelocity() < 1000000000:
            rocket.flightState = RocketFlightState.landed
            rocket.thrust = 0
            rocket.CalculateEntryAngle()
            rocket.ClearArray()
            self.UpdateDistanceToRocket(rocket)
            return True
        run = False
        return False, run
