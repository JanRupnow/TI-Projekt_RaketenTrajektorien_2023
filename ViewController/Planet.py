import math

import numpy as np

from Globals.Constants import *
from ViewController.Rocket.RocketFlightState import RocketFlightState
from numba.experimental import jitclass
from numba import int32, float32, float64, typeof


@jitclass([
    ("radius", float64),
    ("color", typeof((1, 1, 1))),
    ("mass", float64),
    ("name", typeof("test")),
    ("distanceToRocket", float64),
    ("scaleR", float32),
    ("time_step", float32),
    ("meanVelocity", float64),
    ("position_X", float64[:]),
    ("position_Y", float64[:]),
    ("velocity_X", float64[:]),
    ("velocity_Y", float64[:]),
    ("currentStep", int32),
    ("currentCalculationStep", int32)])
class Planet:

    def __init__(self, x, y, radius, color, mass, name, velocity):
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name
        self.distanceToRocket = 2 * radius
        # drawing radius used only for displaying not calculating!!!
        self.scaleR = radius
        self.meanVelocity = velocity
        self.time_step = 1 / 60
        self.position_X = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.position_Y = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.velocity_X = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.velocity_Y = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.currentStep = 0
        self.currentCalculationStep = 0

        self.position_X[0] = x
        self.position_Y[0] = y

    def attraction(self, other, i):
        otherposition_x, other_y = other.position_X[i], other.position_Y[i]  # double
        distance_x = otherposition_x - self.position_X[i]  # double
        distance_y = other_y - self.position_Y[i]  # double
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)  # double
        force = G * self.mass * other.mass / distance ** 2  # double
        # force = G * (self.mass * self.mass_factor) * (other.mass * other.mass_factor) / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def reset_planets_array_to_sync_with_rocket(self):
        self.position_X[0:NUM_OF_PREDICTIONS] = self.position_X[self.currentStep:self.currentStep + NUM_OF_PREDICTIONS]
        self.position_Y[0:NUM_OF_PREDICTIONS] = self.position_Y[self.currentStep:self.currentStep + NUM_OF_PREDICTIONS]
        self.velocity_X[0:NUM_OF_PREDICTIONS] = self.velocity_X[self.currentStep:self.currentStep + NUM_OF_PREDICTIONS]
        self.velocity_Y[0:NUM_OF_PREDICTIONS] = self.velocity_Y[self.currentStep:self.currentStep + NUM_OF_PREDICTIONS]
        self.currentStep = 0
        self.currentCalculationStep = NUM_OF_PREDICTIONS - 1

    def reset_array(self):
        self.position_X[1:NUM_OF_PREDICTIONS + 1] = self.position_X[NUM_OF_PREDICTIONS:]
        self.position_Y[1:NUM_OF_PREDICTIONS + 1] = self.position_Y[NUM_OF_PREDICTIONS:]
        self.velocity_X[1:NUM_OF_PREDICTIONS + 1] = self.velocity_X[NUM_OF_PREDICTIONS:]
        self.velocity_Y[1:NUM_OF_PREDICTIONS + 1] = self.velocity_Y[NUM_OF_PREDICTIONS:]
        self.currentStep = 1
        self.currentCalculationStep = NUM_OF_PREDICTIONS

    def set_scale(self, scale):
        self.scaleR *= scale

    def predict_step(self, i, planets: list[__init__], rocket):
        self.currentCalculationStep = i
        total_fx = total_fy = 0
        for planet in planets:
            if self.name == planet.name:
                continue
            fx, fy = self.attraction(planet, i)
            total_fx += fx
            total_fy += fy
        self.velocity_X[i + 1] = self.velocity_X[i] + total_fx / self.mass * self.time_step
        self.velocity_Y[i + 1] = self.velocity_Y[i] + total_fy / self.mass * self.time_step
        self.position_X[i + 1] = self.position_X[i] + self.velocity_X[i + 1] * self.time_step
        self.position_Y[i + 1] = self.position_Y[i] + self.velocity_Y[i + 1] * self.time_step

        self.update_distance_to_rocket(rocket)

        self.currentCalculationStep += 1

    def update_distance_to_rocket(self, rocket):
        self.distanceToRocket = math.sqrt(
            (self.position_X[self.currentStep] - rocket.position_X[rocket.currentStep]) ** 2 + (
                    self.position_Y[self.currentStep] - rocket.position_Y[rocket.currentStep]) ** 2)

    def calculate_next_step(self, planets: list[__init__]):
        total_fx = total_fy = 0
        for planet in planets:
            if self.name == planet.name:
                continue
            fx, fy = self.attraction(planet, self.currentCalculationStep)
            total_fx += fx
            total_fy += fy
        self.velocity_X[self.currentCalculationStep + 1] = self.velocity_X[
                                                               self.currentCalculationStep] + total_fx / self.mass * self.time_step
        self.velocity_Y[self.currentCalculationStep + 1] = self.velocity_Y[
                                                               self.currentCalculationStep] + total_fy / self.mass * self.time_step
        self.position_X[self.currentCalculationStep + 1] = self.position_X[self.currentCalculationStep] + \
                                                           self.velocity_X[
                                                               self.currentCalculationStep + 1] * self.time_step
        self.position_Y[self.currentCalculationStep + 1] = self.position_Y[self.currentCalculationStep] + \
                                                           self.velocity_Y[
                                                               self.currentCalculationStep + 1] * self.time_step
        self.currentCalculationStep += 1

    def check_collision(self):
        if self.distanceToRocket <= self.radius * 95 / 100:
            return True
        return False

    def check_landing(self, rocket):
        if not self.currentStep % math.ceil(100 / self.time_step) == 0:
            return
        # Safe landing
        if self.distanceToRocket <= self.radius * 95 / 100 and rocket.get_current_relative_velocity() < 1000000000:
            rocket.flightState = RocketFlightState.landed
            rocket.thrust = 0
            rocket.calculate_entry_angle()
            rocket.clear_array()
            self.update_distance_to_rocket(rocket)
            return
        # Crashing
        if self.distanceToRocket >= self.radius * 95 / 100 and rocket.get_current_relative_velocity() > 1000000000:
            rocket.flightState = RocketFlightState.landed
            rocket.clear_array()
