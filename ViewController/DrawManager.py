import numpy as np
import math

from datetime import datetime, timedelta
from Globals.Constants import *
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.FlightDataManager import DATA
from Methods.GameMethods import line_is_in_screen, add_clock_time

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
                                                     planet.position_Y[
                                                     planet.currentStep:planet.currentCalculationStep] * DATA.get_scale())).T)
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

        line_in_screen = line_is_in_screen(np.array((rocket.position_X[
                                                     rocket.currentStep:rocket.currentCalculationStep] * DATA.get_scale(),
                                                     rocket.position_Y[
                                                     rocket.currentStep:rocket.currentCalculationStep] * DATA.get_scale())).T)
        # size > 3 because (2,3) are 2 coordinates for 1 point, you need 2 points to connect a line ((x,y),(x2,y2))
        if line_in_screen.size > 3:
            pygame.draw.lines(WINDOW, rocket.color, False, line_in_screen, 1)

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

    @staticmethod
    def render_flight_interface(rocket: Rocket, now, planets):
        fps_text = FONT_1.render("FPS: " + str(int(CLOCK.get_fps())), True, COLOR_WHITE)
        WINDOW.blit(fps_text, (WIDTH * 0.03, HEIGHT * 0.03))
        if DATA.get_flight_change_state() != FlightChangeState.paused:
            add_clock_time()
        text_surface = FONT_1.render(f"Time step: {int(DATA.get_time_step() * 60)}x", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (WIDTH * 0.75, HEIGHT * 0.04))
        text_actual_time = FONT_1.render(
            f'Current time: {(now + DATA.get_time_passed()).strftime("%d/%m/%Y, %H:%M:%S")}',
            True, COLOR_WHITE)
        WINDOW.blit(text_actual_time, (WIDTH * 0.75, HEIGHT * 0.08))
        text_time_passed = FONT_1.render(f'Passed time: {DATA.get_time_passed()}', True, COLOR_WHITE)
        WINDOW.blit(text_time_passed, (WIDTH * 0.75, HEIGHT * 0.12))

        # TODO hotkey to set detailed interface or basic interface
        distance = np.sqrt(
            (rocket.position_X[rocket.currentStep] - rocket.nearestPlanet.position_X[
                rocket.nearestPlanet.currentStep]) ** 2
            + (rocket.position_Y[rocket.currentStep] - rocket.nearestPlanet.position_Y[
                rocket.nearestPlanet.currentStep]) ** 2)
        speed = round(rocket.get_current_relative_velocity()) if distance < rocket.nearestPlanet.radius * 5 else round(
            rocket.get_absolute_velocity())
        rocket_velocity = FONT_1.render(f'Rocket Speed: {speed}km/h', True, COLOR_WHITE)
        WINDOW.blit(rocket_velocity, (WIDTH * 0.75, HEIGHT * 0.16))
        if not rocket.flightState == RocketFlightState.flying:
            rocket_velocity = FONT_1.render(f'Altitude: {0} km (Rocket has not started)', True, COLOR_WHITE)
        elif rocket.nearestPlanet.distanceToRocket - rocket.nearestPlanet.radius < 3 / 2 * rocket.nearestPlanet.radius:
            rocket_velocity = FONT_1.render(
                f'Altitude: {round((rocket.nearestPlanet.distanceToRocket - rocket.nearestPlanet.radius) / 1000, 0)} km',
                True, COLOR_WHITE)
        else:
            rocket_velocity = FONT_1.render(f'Altitude: not available in space', True, COLOR_WHITE)
        WINDOW.blit(rocket_velocity, (WIDTH * 0.75, HEIGHT * 0.20))
        rocket_fuel = FONT_1.render(f'Rocket Fuel: %', True, COLOR_WHITE)
        WINDOW.blit(rocket_fuel, (WIDTH * 0.75, HEIGHT * 0.24))
        rocket_max_q = FONT_1.render(f'MaxQ: %', True, COLOR_WHITE)
        WINDOW.blit(rocket_max_q, (WIDTH * 0.75, HEIGHT * 0.28))
        zoom_text = FONT_1.render(f'Automatic Zoom: {DATA.get_zoom_goal()}', True, COLOR_WHITE)
        WINDOW.blit(zoom_text, (WIDTH * 0.75, HEIGHT * 0.32))
        rocket_state = FONT_1.render(f'Rocket: {rocket.flightState}', True, COLOR_WHITE)
        WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.36))
        rocket_state = FONT_1.render(f'Rocket current: {rocket.currentStep}', True, COLOR_WHITE)
        WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.40))
        rocket_state = FONT_1.render(f'Rocket calculation: {rocket.currentCalculationStep}', True, COLOR_WHITE)
        WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.44))
        rocket_state = FONT_1.render(f'Planet current: {planets[0].currentStep}', True, COLOR_WHITE)
        WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.48))
        rocket_state = FONT_1.render(f'Planet calculation: {planets[0].currentCalculationStep}', True, COLOR_WHITE)
        WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.52))
        rocket_state = FONT_1.render(f'Flight State: {DATA.get_flight_change_state()}', True, COLOR_WHITE)
        WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.56))

        thrust_text = FONT_1.render(f'Thrust: {rocket.thrust}m/s^2', True, COLOR_WHITE)
        WINDOW.blit(thrust_text, (WIDTH * 0.75, HEIGHT * 0.8))

        sun_surface = FONT_1.render("- Sun", True, COLOR_SUN)
        WINDOW.blit(sun_surface, (15, 285))
        mercury_surface = FONT_1.render("- Mercury", True, COLOR_MERCURY)
        WINDOW.blit(mercury_surface, (15, 315))
        venus_surface = FONT_1.render("- Venus", True, COLOR_VENUS)
        WINDOW.blit(venus_surface, (15, 345))
        earth_surface = FONT_1.render("- Earth", True, COLOR_EARTH)
        WINDOW.blit(earth_surface, (15, 375))
        mars_surface = FONT_1.render("- Mars", True, COLOR_MARS)
        WINDOW.blit(mars_surface, (15, 405))
        jupiter_surface = FONT_1.render("- Jupiter", True, COLOR_JUPITER)
        WINDOW.blit(jupiter_surface, (15, 435))
        saturn_surface = FONT_1.render("- Saturn", True, COLOR_SATURN)
        WINDOW.blit(saturn_surface, (15, 465))
        uranus_surface = FONT_1.render("- Uranus", True, COLOR_URANUS)
        WINDOW.blit(uranus_surface, (15, 495))
        neptune_surface = FONT_1.render("- Neptune", True, COLOR_NEPTUNE)
        WINDOW.blit(neptune_surface, (15, 525))
