import pygame
import numpy as np
import math

from Globals.Constants import MIN_ROCKET_RADIUS, COLOR_WHITE, WIDTH, HEIGHT, WINDOW, DATA
from Methods.GameMethods import line_is_in_screen

from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState


class DrawManager:

    @staticmethod
    def draw_planet(planet: Planet):

        DrawManager.draw_planet_orbit(planet)
        pygame.draw.circle(WINDOW, planet.color, (
            planet.position_X[planet.currentStep] * DATA.get_scale() + DATA.get_move_x() + WIDTH / 2,
            planet.position_Y[planet.currentStep] * DATA.get_scale() + DATA.get_move_y() + HEIGHT / 2),
                           max(planet.scaleR * DATA.get_scale(), 2))

    @staticmethod
    def draw_planet_orbit(planet: Planet):

        line_in_screen = line_is_in_screen(np.array((planet.position_X[
                        planet.currentStep:planet.currentCalculationStep] * DATA.get_scale(),
                        planet.position_Y[planet.currentStep:planet.currentCalculationStep] * DATA.get_scale())).T)
        # size > 3 because (2,3) are 2 coordinates for 1 point, you need 2 points to connect a line ((x,y),(x2,y2))
        if line_in_screen.size > 3:
            pygame.draw.lines(WINDOW, planet.color, False, line_in_screen, 1)

    @staticmethod
    def display_planet_distances(planet: Planet):

        distance_text = pygame.font.SysFont("Trebuchet MS", 16).render(
            f"{planet.name}:{str(round(planet.distanceToRocket * 1.057 * 10 ** -16, 8))} light years", True,
            COLOR_WHITE)
        WINDOW.blit(distance_text, (planet.position_X[
                                        planet.currentStep] * DATA.get_scale() + WIDTH / 2 - distance_text.get_width() / 2 + DATA.get_move_x(),
                                    planet.position_Y[
                                        planet.currentStep] * DATA.get_scale() + HEIGHT / 2 + distance_text.get_height() / 2 - 20 + DATA.get_move_y()))

    @staticmethod
    def draw_rocket_prediction(rocket: Rocket):

        pygame.draw.lines(WINDOW, rocket.color, False, np.array((rocket.position_X[
                                                                 rocket.currentStep:rocket.currentCalculationStep] * DATA.get_scale() + DATA.get_move_x() + WIDTH / 2,
                                                                 rocket.position_Y[
                                                                 rocket.currentStep:rocket.currentCalculationStep] * DATA.get_scale() + DATA.get_move_y() + HEIGHT / 2)).T,
                          1)

    @staticmethod
    def draw_rocket(rocket: Rocket):

        if rocket.radius < MIN_ROCKET_RADIUS:
            pygame.draw.circle(WINDOW, rocket.color, (
                rocket.position_X[rocket.currentStep] * DATA.get_scale() + DATA.get_move_x() + WIDTH / 2,
                rocket.position_Y[rocket.currentStep] * DATA.get_scale() + DATA.get_move_y() + HEIGHT / 2),
                               MIN_ROCKET_RADIUS)
            return
        if rocket.flightState == RocketFlightState.flying:
            rocket.img = pygame.transform.rotate(rocket.notRotatedImg, math.atan2(
                rocket.position_Y[rocket.currentStep] - rocket.nearestPlanet.position_Y[rocket.currentStep],
                rocket.position_X[rocket.currentStep] - rocket.nearestPlanet.position_X[rocket.currentStep]) * (
                                                     -180) / np.pi - 90)
        else:
            rocket.img = pygame.transform.rotate(rocket.notRotatedImg, math.atan2(rocket.velocity_Y[rocket.currentStep],
                                                                                  rocket.velocity_X[
                                                                                      rocket.currentStep]) * (
                                                     -180) / np.pi - 90)
        # img = pygame.transform.rotozoom(img0, math.atan2(self.position_Y[self.currentStep], self.position_X[self.currentStep]), max(0.05, self.radius))
        WINDOW.blit(rocket.img, (rocket.position_X[
                                     rocket.currentStep] * DATA.get_scale() + DATA.get_move_x() + WIDTH / 2 - rocket.img.get_width() / 2,
                                 rocket.position_Y[
                                     rocket.currentStep] * DATA.get_scale() + DATA.get_move_y() + HEIGHT / 2 - rocket.img.get_height() / 2))
