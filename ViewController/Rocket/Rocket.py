import math

import numpy as np

from Globals.Constants import *
from ViewController.Planet import Planet
from ViewController.Rocket.RocketFlightState import RocketFlightState

from numba.experimental import jitclass
from numba import int32, float32, float64, typeof, types


@jitclass([
    ("currentStep", int32),
    ("currentCalculationStep", int32),
    ("mass", float32),
    ("fuelmass", float64),
    ("PlanetsInRangeList", types.List(typeof(
        Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 21, planetNameArray[6], 13.06 * 1000)))),
    ("nearestPlanet", typeof(
        Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 21, planetNameArray[6], 13.06 * 1000))),
    ("planetAngle", float32),
    ("position_X", float64[:]),
    ("position_Y", float64[:]),
    ("velocity_X", float64[:]),
    ("velocity_Y", float64[:]),
    ("time_step", float64),
    ("c", float64),
    ("radius", float64),
    ("thrust", int32),
    ("angle", float32),
    ("flightState", typeof(RocketFlightState.flying)),
    ("color", typeof((1, 1, 1))),
    ("startplanet", typeof(
        Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 21, planetNameArray[6], 13.06 * 1000))),
    ("sun", typeof(
        Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 21, planetNameArray[6], 13.06 * 1000))),
    ("entryAngle", float32)])
class Rocket:
    def __init__(self, start_angle: float, fuel: float, mass: float, startplanet: Planet, radius: float, color: tuple,
                 sun: Planet):
        self.currentStep: int = CurrentStep
        self.currentCalculationStep: int = CurrentCalculationStep
        self.mass: float = mass
        self.fuelmass: float = fuel
        # TODO angle refactor
        self.startplanet: Planet = startplanet
        self.PlanetsInRangeList: list[Planet] = [startplanet]
        self.nearestPlanet: Planet = startplanet
        self.planetAngle: float = start_angle
        self.position_X: np.array = np.zeros(LEN_OF_PREDICTIONS_ARRAY)  # x-Position [m]
        self.position_Y: np.array = np.zeros(LEN_OF_PREDICTIONS_ARRAY)  # z-Position [m]
        self.velocity_X: np.array = np.zeros(LEN_OF_PREDICTIONS_ARRAY)  # x-Velocity [m/s]
        self.velocity_Y: np.array = np.zeros(LEN_OF_PREDICTIONS_ARRAY)  # z-Velocity [m/s]
        self.time_step: float = 1 / 60
        self.c: float = AirResistance / self.mass
        self.radius: float = radius
        self.thrust: int = 0  # aktuell nicht genutzt
        self.angle: float = 0
        self.flightState: RocketFlightState = RocketFlightState.landed
        self.color: tuple = color
        self.velocity_X[0]: np.array = self.nearestPlanet.velocity_X[0]
        self.velocity_Y[0]: np.array = self.nearestPlanet.velocity_Y[0]
        # Berechnung der Startposition der Rakete abhängig vom Startplaneten ohne Skalierung
        self.position_X[0] = startplanet.position_X[self.currentStep] + startplanet.radius * np.cos(
            self.planetAngle * np.pi / 180)
        self.position_Y[0] = startplanet.position_Y[self.currentStep] + startplanet.radius * np.sin(
            self.planetAngle * np.pi / 180)
        self.sun: Planet = sun
        self.entryAngle: float = 0

    """
    # Methode für die x-Komponente
    def f2(self, v, i: int, distance_to_sun: float):
        x = 0
        for planet in self.PlanetsInRangeList:
            r = self.get_distance_to_planet(planet, i)
            # r0 = np.sqrt( (self.position_X[i] - self.nearestPlanet.position_X[i])**2 + (self.position_Y[i] - self.nearestPlanet.position_Y[i])**2)
            x += (-(G * planet.mass / r ** 2) - (
                    AirResistance * self.get_relative_velocity(i) ** 2 * np.sign(self.velocity_X[i]) * p_0 * np.exp(
                -abs((r - planet.radius)) / h_s)) / (2 * self.mass)) * (
                         (self.position_X[i] - planet.position_X[i]) / r)  # Extrakraft x einbauen

        # distanceToSun = np.sqrt( (self.position_X[i] - self.sun.position_X[i])**2 + (self.position_Y[i] - self.sun.position_Y[i])**2)
        x -= (G * self.sun.mass / distance_to_sun ** 2) * (
                    (self.position_X[i] - self.sun.position_X[i]) / distance_to_sun)
        # y=-(G*m_E/(position_X**2 + position_Y**2)**1.5) * position_X - c*x**2*np.sign(x)
        if self.thrust != 0:
            x += math.cos(
                math.atan2(self.velocity_Y[i], self.velocity_X[i]) + self.angle * np.pi / 180) * self.thrust * 10
        return x

    # Methode für die z-Komponente
    def f1(self, v, i: int, distance_to_sun: float):
        z = 0
        for planet in self.PlanetsInRangeList:
            r = self.get_distance_to_planet(planet, i)
            # r0 = np.sqrt( (self.position_X[i] - self.nearestPlanet.position_X[i])**2 + (self.position_Y[i] - self.nearestPlanet.position_Y[i])**2)
            z += (-(G * planet.mass / r ** 2) - (
                    AirResistance * self.get_relative_velocity(i) ** 2 * np.sign(self.velocity_Y[i]) * p_0 * np.exp(
                -abs((r - planet.radius)) / h_s)) / (2 * self.mass)) * (
                         (self.position_Y[i] - planet.position_Y[i]) / r)
            test = self.get_relative_velocity(i)
        # distanceToSun = np.sqrt( (self.position_X[i] - self.sun.position_X[i])**2 + (self.position_Y[i] - self.sun.position_Y[i])**2)
        z -= (G * self.sun.mass / distance_to_sun ** 2) * (
                (self.position_Y[i] - self.sun.position_Y[i]) / distance_to_sun)
        # TODO muss die Geschwindigkeit relativ zum Planet sein?
        #  Eigentlich ja oder? (Luftwiderstand) (wie kann man das besser machen? planetenabhängig?)

        if self.thrust != 0:
            z += math.sin(
                math.atan2(self.velocity_Y[i], self.velocity_X[i]) + self.angle * np.pi / 180) * self.thrust * 10
        return z
    """

    def f(self, v_x: float, v_y: float, i: int, distance_to_sun: float) -> None:
        x = 0
        y = 0
        for planet in self.PlanetsInRangeList:
            r = np.sqrt((self.position_X[i] - planet.position_X[i]) ** 2
                        + (self.position_Y[i] - planet.position_Y[i]) ** 2)

            abs_a = (G * planet.mass / r ** 2)

            # Luftwiderstand nur auf der Erde berechnen und nur bis 100km Höhe
            if planet.name == "Earth" and r < 100_000:
                abs_a += ((AirResistance * (v_x ** 2 + v_y ** 2) * np.sign(self.velocity_Y[i]) *
                           p_0 * np.exp(-abs((r - planet.radius)) / h_s))
                          / (2 * self.mass))

            sign_x = np.sign(self.position_X[i] - planet.position_X[i])
            sign_y = np.sign(self.position_Y[i] - planet.position_Y[i])

            x += sign_x * abs_a * ((self.position_X[i] - planet.position_X[i]) / r)
            y += sign_y * abs_a * ((self.position_Y[i] - planet.position_Y[i]) / r)

        x -= (G * self.sun.mass / distance_to_sun ** 2) * (
                (self.position_X[i] - self.sun.position_X[i]) / distance_to_sun)
        y -= (G * self.sun.mass / distance_to_sun ** 2) * (
                (self.position_Y[i] - self.sun.position_Y[i]) / distance_to_sun)

        if self.thrust != 0:
            x += math.cos(math.atan2(self.velocity_Y[i],
                                     self.velocity_X[i])
                          + self.angle * np.pi / 180) * self.thrust * 10

            y += math.sin(math.atan2(self.velocity_Y[i],
                                     self.velocity_X[i])
                          + self.angle * np.pi / 180) * self.thrust * 10

        return x, y

    # Berechnung nach Runge-Kutta Verfahren
    def calculate_next_step(self, i: int) -> None:

        distance_to_sun = np.sqrt((self.position_X[i] - self.sun.position_X[i]) ** 2
                                  + (self.position_Y[i] - self.sun.position_Y[i]) ** 2)

        k1_x, k1_y = self.f(self.velocity_X[i] - self.startplanet.velocity_X[i],
                            (self.velocity_Y[i] - self.startplanet.velocity_Y[i]),
                            i, distance_to_sun)
        k2_x, k2_y = self.f((self.velocity_X[i] - self.startplanet.velocity_X[i]) + k1_x * self.time_step / 2,
                            (self.velocity_Y[i] - self.startplanet.velocity_Y[i]) + k1_y * self.time_step / 2,
                            i, distance_to_sun)
        k3_x, k3_y = self.f((self.velocity_X[i] - self.startplanet.velocity_X[i]) + k2_x * self.time_step / 2,
                            (self.velocity_Y[i] - self.startplanet.velocity_Y[i]) + k2_y * self.time_step / 2,
                            i, distance_to_sun)
        k4_x, k4_y = self.f((self.velocity_X[i] - self.startplanet.velocity_X[i]) + k3_x * self.time_step / 2,
                            (self.velocity_Y[i] - self.startplanet.velocity_Y[i]) + k3_y * self.time_step / 2,
                            i, distance_to_sun)

        k_x = (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
        k_y = (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6

        self.velocity_X[i + 1] = self.velocity_X[i] + k_x * self.time_step
        self.position_X[i + 1] = self.position_X[i] + self.velocity_X[i] * self.time_step

        self.velocity_Y[i + 1] = self.velocity_Y[i] + k_y * self.time_step
        self.position_Y[i + 1] = self.position_Y[i] + self.velocity_Y[i] * self.time_step

    def set_scale(self, scale: float) -> None:
        self.radius *= scale

    # def get_current_distance_to_next_planet(self):
    #     return np.sqrt((self.position_X[self.currentCalculationStep] - self.nearestPlanet.position_X[
    #         self.currentCalculationStep]) ** 2 +
    #                    (self.position_Y[self.currentCalculationStep] - self.nearestPlanet.position_Y[
    #                        self.currentCalculationStep]) ** 2)

    # def get_relative_velocity(self, i: int):
    #     if self.flightState == RocketFlightState.flying:
    #         return np.sqrt((self.velocity_X[i] - self.nearestPlanet.velocity_X[i]) ** 2
    #                        + (self.velocity_Y[i] - self.nearestPlanet.velocity_Y[i]) ** 2)
    #     return 0

    def get_current_relative_velocity(self) -> float:
        if self.flightState == RocketFlightState.flying:
            return np.sqrt(
                (self.velocity_X[self.currentStep] - self.nearestPlanet.velocity_X[self.nearestPlanet.currentStep]) ** 2
                + (self.velocity_Y[self.currentStep] - self.nearestPlanet.velocity_Y[
                    self.nearestPlanet.currentStep]) ** 2)
        return 0

    # in m/s
    def get_absolute_velocity(self) -> float:
        if self.flightState == RocketFlightState.flying:
            return np.sqrt(self.velocity_X[self.currentStep] ** 2 + self.velocity_Y[self.currentStep] ** 2)
        return 0.0

    def reset_array(self) -> None:
        self.position_X[1:NUM_OF_PREDICTIONS + 1] = self.position_X[NUM_OF_PREDICTIONS:]
        self.position_Y[1:NUM_OF_PREDICTIONS + 1] = self.position_Y[NUM_OF_PREDICTIONS:]
        self.velocity_X[1:NUM_OF_PREDICTIONS + 1] = self.velocity_X[NUM_OF_PREDICTIONS:]
        self.velocity_Y[1:NUM_OF_PREDICTIONS + 1] = self.velocity_Y[NUM_OF_PREDICTIONS:]
        self.currentStep = 1
        self.currentCalculationStep = NUM_OF_PREDICTIONS

    def calculate_entry_angle(self) -> None:
        self.planetAngle = math.atan2(
            self.position_Y[self.currentStep] - self.nearestPlanet.position_Y[self.nearestPlanet.currentStep],
            self.position_X[self.currentStep] - self.nearestPlanet.position_X[self.nearestPlanet.currentStep]) * (
                                   180 / np.pi)

    def calculate_new_calculation_of_predictions(self) -> None:
        self.currentCalculationStep = self.currentStep
        for i in range(NUM_OF_PREDICTIONS):
            # for planet in planets:
            #    planet.predict_step(self.currentCalculationStep, planets, self)
            self.calculate_next_step(self.currentCalculationStep)
            self.currentCalculationStep += 1

    def calculate_one_prediction(self) -> None:
        # for planet in planets:
        #    planet.predict_step(self.currentCalculationStep, planets, self)
        self.calculate_next_step(self.currentCalculationStep)
        self.currentCalculationStep += 1

    def clear_array(self) -> None:
        self.position_X = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.position_Y = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.velocity_X = np.zeros(LEN_OF_PREDICTIONS_ARRAY)
        self.velocity_Y = np.zeros(LEN_OF_PREDICTIONS_ARRAY)

        self.currentStep = 0
        self.currentCalculationStep = 0

        self.position_X[0] = self.nearestPlanet.position_X[
                                 self.nearestPlanet.currentStep] + self.nearestPlanet.radius * np.cos(
            self.planetAngle * np.pi / 180)
        self.position_Y[0] = self.nearestPlanet.position_Y[
                                 self.nearestPlanet.currentStep] + self.nearestPlanet.radius * np.sin(
            self.planetAngle * np.pi / 180)
        self.velocity_X[0] = self.nearestPlanet.position_X[self.nearestPlanet.currentStep]
        self.velocity_Y[0] = self.nearestPlanet.position_Y[self.nearestPlanet.currentStep]

    def update_planets_in_range_list(self, planets: list[Planet]) -> None:
        if not self.currentStep % math.ceil(100 / self.time_step) == 0:
            return
        self.PlanetsInRangeList = []
        for planet in planets:
            if planet.name != "Sun" and self.get_distance_to_planet(planet,
                                                                    self.currentCalculationStep) < planet.radius * 100:
                self.PlanetsInRangeList.append(planet)

    def update_nearest_planet(self, planets: list[Planet]) -> None:
        if not self.currentStep % math.ceil(100 / self.time_step) == 0:
            return
        self.nearestPlanet = min(planets, key=lambda x: self.get_distance_to_planet(x, self.currentStep))

    def get_distance_to_planet(self, planet: Planet, step: int) -> float:
        return np.sqrt((self.position_X[step] - planet.position_X[step]) ** 2
                       + (self.position_Y[step] - planet.position_Y[step]) ** 2)

    def calculate_landed_values(self) -> None:
        self.position_X[0] = self.position_X[self.currentStep] + self.radius * np.cos(self.angle * np.pi / 180)
        self.position_Y[0] = self.position_Y[self.currentStep] + self.radius * np.sin(
            self.angle * np.pi / 180)  # macht kein Sinn hier
        self.velocity_X[0] = self.velocity_X[self.currentStep]
        self.velocity_Y[0] = self.velocity_Y[self.currentStep]

    def stick_to_planet(self) -> None:
        self.position_X[0] = self.nearestPlanet.position_X[
                                 self.nearestPlanet.currentStep] + self.nearestPlanet.radius * np.cos(
            self.planetAngle * np.pi / 180)
        self.position_Y[0] = self.nearestPlanet.position_Y[
                                 self.nearestPlanet.currentStep] + self.nearestPlanet.radius * np.sin(
            self.planetAngle * np.pi / 180)
        self.velocity_X[0] = self.nearestPlanet.velocity_X[self.nearestPlanet.currentStep]
        self.velocity_Y[0] = self.nearestPlanet.velocity_Y[self.nearestPlanet.currentStep]
