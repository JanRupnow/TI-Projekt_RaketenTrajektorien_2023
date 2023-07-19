import math
import numpy as np

from Globals.Constants import *

from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketState import RocketState

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

        self.r_x = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.r_z = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.v_x = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.v_z = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.currentStep = 0
        self.currentCalculationStep = 0

        self.r_x[0] = x
        self.r_z[0] = y

    def Attraction(self, other, i):
        other_x, other_y = other.r_x[i], other.r_z[i]
        distance_x = other_x - self.r_x[i]
        distance_y = other_y - self.r_z[i]
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def ResetPlanetsArrayToSyncWithRocket(self):
        self.r_x[0:NUM_OF_PREDICTIONS] = self.r_x[self.currentStep:self.currentStep+NUM_OF_PREDICTIONS]
        self.r_z[0:NUM_OF_PREDICTIONS] = self.r_z[self.currentStep:self.currentStep+NUM_OF_PREDICTIONS]
        self.v_x[0:NUM_OF_PREDICTIONS] = self.v_x[self.currentStep:self.currentStep+NUM_OF_PREDICTIONS]
        self.v_z[0:NUM_OF_PREDICTIONS] = self.v_z[self.currentStep:self.currentStep+NUM_OF_PREDICTIONS]
        self.currentStep = 0
        self.currentCalculationStep = NUM_OF_PREDICTIONS-1

    def ResetArray(self):
        self.r_x[1:NUM_OF_PREDICTIONS+1] = self.r_x[NUM_OF_PREDICTIONS:]
        self.r_z[1:NUM_OF_PREDICTIONS+1] = self.r_z[NUM_OF_PREDICTIONS:]
        self.v_x[1:NUM_OF_PREDICTIONS+1] = self.v_x[NUM_OF_PREDICTIONS:]
        self.v_z[1:NUM_OF_PREDICTIONS+1] = self.v_z[NUM_OF_PREDICTIONS:]
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
        self.v_x[i+1] = self.v_x[i] + total_fx / self.mass * self.timestep
        self.v_z[i+1] = self.v_z[i] + total_fy / self.mass * self.timestep
        self.r_x[i+1] = self.r_x[i] + self.v_x[i+1] * self.timestep
        self.r_z[i+1] = self.r_z[i] + self.v_z[i+1] * self.timestep

        self.UpdateDistanceToRocket(rocket)

        if not pause:
            self.currentCalculationStep += 1

    def UpdateDistanceToRocket(self, rocket : Rocket):
        self.distanceToRocket = math.sqrt((self.r_x[self.currentStep]-rocket.r_x[rocket.currentStep])**2+(self.r_z[self.currentStep]-rocket.r_z[rocket.currentStep])**2)

    def PredictNext(self, planets : list[__init__], pause):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.Attraction(planet, self.currentCalculationStep)
            total_fx += fx
            total_fy += fy
        self.v_x[self.currentCalculationStep+1] = self.v_x[self.currentCalculationStep] + total_fx / self.mass * self.timestep
        self.v_z[self.currentCalculationStep+1] = self.v_z[self.currentCalculationStep] + total_fy / self.mass * self.timestep
        self.r_x[self.currentCalculationStep+1] = self.r_x[self.currentCalculationStep] + self.v_x[self.currentCalculationStep+1] * self.timestep
        self.r_z[self.currentCalculationStep+1] = self.r_z[self.currentCalculationStep] + self.v_z[self.currentCalculationStep+1] * self.timestep

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
            rocket.state = RocketState.landed
            rocket.thrust = 0
            rocket.CalculateEntryAngle()
            rocket.ClearArray()
            self.UpdateDistanceToRocket(rocket)
            return True
        run = False
        return False, run
