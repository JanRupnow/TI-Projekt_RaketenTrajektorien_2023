import numpy as np
import math
from pygame import Surface
from Globals.Constants import *
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.FlightDataManager import DATA
from Methods.GameMethods import line_is_in_screen, add_clock_time

from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState


class DrawManager:
    rocket_initialImage: Surface = None
    rocket_currentImage: Surface = None
    rocket_notRotatedImage: Surface = None

    @staticmethod
    def draw_planet(planet: Planet):

        DrawManager.draw_planet_orbit(planet)
        pygame.draw.circle(WINDOW, planet.color, (
            planet.position_X[planet.currentStep] * DATA.scale + DATA.move_x + WIDTH / 2,
            planet.position_Y[planet.currentStep] * DATA.scale + DATA.move_y + HEIGHT / 2),
                           max(planet.scaleR * DATA.scale, 2))

    @classmethod
    def set_rocket_image(cls, image: Surface, radius) -> None:
        cls.rocket_initialImage = image
        cls.rocket_currentImage = pygame.transform.scale_by(image, min(0.1 * radius, 1))
        cls.rocket_notRotatedImage = cls.rocket_currentImage

    @classmethod
    def set_rocket_scale(cls, rocket: Rocket, scale) -> None:
        rocket.set_scale(scale)
        if MIN_ROCKET_RADIUS < rocket.radius < MAX_ROCKET_RADIUS:
            cls.rocket_notRotatedImage = pygame.transform.scale_by(
                cls.rocket_initialImage,
                max(min(0.1 * rocket.radius, 1), 0.1))

    @staticmethod
    def draw_planet_orbit(planet: Planet):

        line_in_screen = line_is_in_screen(np.array((planet.position_X[
                                                     planet.currentStep:planet.currentCalculationStep] * DATA.scale,
                                                     planet.position_Y[
                                                     planet.currentStep:planet.currentCalculationStep] * DATA.scale)).T)
        # size > 3 because (2,3) are 2 coordinates for 1 point, you need 2 points to connect a line ((x,y),(x2,y2))
        if line_in_screen.size > 3:
            pygame.draw.lines(WINDOW, planet.color, False, line_in_screen, 1)

    @staticmethod
    def display_planet_distances(planet: Planet):

        distance_text = pygame.font.SysFont("Trebuchet MS", 16).render(
            f"{planet.name}:{str(round(planet.distanceToRocket * 1.057 * 10 ** -16, 8))} light years", True,
            COLOR_WHITE)
        WINDOW.blit(distance_text, (planet.position_X[
                                        planet.currentStep] * DATA.scale + WIDTH / 2 - distance_text.get_width() / 2 + DATA.move_x,
                                    planet.position_Y[
                                        planet.currentStep] * DATA.scale + HEIGHT / 2 + distance_text.get_height() / 2 - 20 + DATA.move_y))

    @staticmethod
    def draw_rocket_prediction(rocket: Rocket):

        line_in_screen = line_is_in_screen(np.array((rocket.position_X[
                                                     rocket.currentStep:rocket.currentCalculationStep] * DATA.scale,
                                                     rocket.position_Y[
                                                     rocket.currentStep:rocket.currentCalculationStep] * DATA.scale)).T)
        # size > 3 because (2,3) are 2 coordinates for 1 point, you need 2 points to connect a line ((x,y),(x2,y2))
        if line_in_screen.size > 3:
            pygame.draw.lines(WINDOW, rocket.color, False, line_in_screen, 1)

    @classmethod
    def draw_rocket(cls, rocket: Rocket):

        if rocket.radius < MIN_ROCKET_RADIUS:
            pygame.draw.circle(WINDOW, rocket.color, (
                rocket.position_X[rocket.currentStep] * DATA.scale + DATA.move_x + WIDTH / 2,
                rocket.position_Y[rocket.currentStep] * DATA.scale + DATA.move_y + HEIGHT / 2),
                               MIN_ROCKET_RADIUS)
            return
        if rocket.flightState == RocketFlightState.flying:
            cls.rocket_currentImage = pygame.transform.rotate(cls.rocket_notRotatedImage, math.atan2(
                rocket.position_Y[rocket.currentStep] - rocket.nearestPlanet.position_Y[rocket.currentStep],
                rocket.position_X[rocket.currentStep] - rocket.nearestPlanet.position_X[rocket.currentStep]) * (
                                                                  -180) / np.pi - 90)
        else:
            cls.rocket_currentImage = pygame.transform.rotate(cls.rocket_notRotatedImage,
                                                              math.atan2(
                                                                  rocket.velocity_Y[rocket.currentStep],
                                                                  rocket.velocity_X[rocket.currentStep])
                                                              * (-180) / np.pi - 90)

        # img = pygame.transform.rotozoom(img0, math.atan2(self.position_Y[self.currentStep], self.position_X[self.currentStep]), max(0.05, self.radius))
        WINDOW.blit(cls.rocket_currentImage, (rocket.position_X[
                                                  rocket.currentStep] * DATA.scale
                                              + DATA.move_x + WIDTH / 2 - cls.rocket_currentImage.get_width() / 2,
                                              rocket.position_Y[
                                                  rocket.currentStep] * DATA.scale
                                              + DATA.move_y + HEIGHT / 2 - cls.rocket_currentImage.get_height() / 2
                                              ))

    @staticmethod
    def render_flight_interface(rocket: Rocket, now, planets):

        if DATA.flight_change_state != FlightChangeState.paused:
            add_clock_time()

        display_bar(rocket, now)

        if DATA.advanced_interface:
            # Advanced flight details
            fps_text = FONT_1.render("FPS: " + str(int(CLOCK.get_fps())), True, COLOR_WHITE)
            WINDOW.blit(fps_text, (WIDTH * 0.025, HEIGHT * 0.13))

            # TODO implement Pressure
            # TODO implement Current Weight

            rocket_max_q = FONT_1.render(f'MaxQ: %', True, COLOR_WHITE)
            WINDOW.blit(rocket_max_q, (WIDTH * 0.75, HEIGHT * 0.12))
            rocket_state = FONT_1.render(f'Rocket current: {rocket.currentStep}', True, COLOR_WHITE)
            WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.16))
            rocket_state = FONT_1.render(f'Rocket calculation: {rocket.currentCalculationStep}', True, COLOR_WHITE)
            WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.20))
            rocket_state = FONT_1.render(f'Planet current: {planets[0].currentStep}', True, COLOR_WHITE)
            WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.24))
            rocket_state = FONT_1.render(f'Planet calculation: {planets[0].currentCalculationStep}', True, COLOR_WHITE)
            WINDOW.blit(rocket_state, (WIDTH * 0.75, HEIGHT * 0.28))

            # Planet colors and names
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

        distance = np.sqrt(
            (rocket.position_X[rocket.currentStep] - rocket.nearestPlanet.position_X[
                rocket.nearestPlanet.currentStep]) ** 2
            + (rocket.position_Y[rocket.currentStep] - rocket.nearestPlanet.position_Y[
                rocket.nearestPlanet.currentStep]) ** 2)
        speed = round(
            rocket.get_current_relative_velocity()) if distance < rocket.nearestPlanet.radius * 5 else round(
            rocket.get_absolute_velocity())

        rocket_velocity = FONT_1.render(f'Rocket Speed: {speed}km/h', True, COLOR_WHITE)
        WINDOW.blit(rocket_velocity, (WIDTH * 0.75, HEIGHT * 0.8))
        thrust_text = FONT_1.render(f'Thrust: {rocket.thrust}m/s^2', True, COLOR_WHITE)
        WINDOW.blit(thrust_text, (WIDTH * 0.75, HEIGHT * 0.84))
        fuel_bar()


def display_bar(rocket: Rocket, now):
    # Complete bar
    pygame.draw.rect(WINDOW, (50, 50, 50), (0, 0, WIDTH * 1, HEIGHT * 0.1))

    # Current Time

    pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.03, HEIGHT * 0.015, WIDTH * 0.15, HEIGHT * 0.04))

    year_text = FONT_1.render("Simulation Time:", True, COLOR_WHITE)
    WINDOW.blit(year_text, (WIDTH * 0.04, HEIGHT * 0.02))

    pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.03, HEIGHT * 0.05, WIDTH * 0.15, HEIGHT * 0.04))

    text_actual_time = FONT_1.render(
        f'{(now + DATA.time_passed).strftime("%d/%m/%Y, %H:%M:%S")}',
        True, COLOR_WHITE)
    WINDOW.blit(text_actual_time, (WIDTH * 0.04, HEIGHT * 0.055))

    # Generals
    # State
    pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.37, HEIGHT * 0.015, WIDTH * 0.07, HEIGHT * 0.04))

    year_text = FONT_1.render("State", True, COLOR_WHITE)
    WINDOW.blit(year_text, (WIDTH * 0.39, HEIGHT * 0.02))

    pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.37, HEIGHT * 0.05, WIDTH * 0.07, HEIGHT * 0.04))

    rocket_state = FONT_1.render(f'{rocket.flightState}', True, COLOR_WHITE)
    WINDOW.blit(rocket_state, (WIDTH * 0.385, HEIGHT * 0.055))
    # Timestep
    pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.45, HEIGHT * 0.015, WIDTH * 0.07, HEIGHT * 0.04))

    year_text = FONT_1.render("Step >>", True, COLOR_WHITE)
    WINDOW.blit(year_text, (WIDTH * 0.465, HEIGHT * 0.02))

    pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.45, HEIGHT * 0.05, WIDTH * 0.07, HEIGHT * 0.04))

    rocket_state = FONT_1.render(f'{int(DATA.time_step * 60)}x', True, COLOR_WHITE)
    WINDOW.blit(rocket_state, (WIDTH * 0.465, HEIGHT * 0.055))

    # Zoom
    pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.53, HEIGHT * 0.015, WIDTH * 0.07, HEIGHT * 0.04))

    year_text = FONT_1.render("Zoom", True, COLOR_WHITE)
    WINDOW.blit(year_text, (WIDTH * 0.55, HEIGHT * 0.02))

    pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.53, HEIGHT * 0.05, WIDTH * 0.07, HEIGHT * 0.04))

    rocket_state = FONT_1.render(f'{DATA.zoom_goal}', True, COLOR_WHITE)
    WINDOW.blit(rocket_state, (WIDTH * 0.545, HEIGHT * 0.055))

    # Time Passed
    total_seconds = DATA.time_passed.total_seconds()
    years, remainder = divmod(total_seconds, 31_536_000)  # 31,536,000 seconds in a year (approximate)
    days, remainder = divmod(remainder, 86_400)  # 86,400 seconds in a day
    hours, remainder = divmod(remainder, 3_600)  # 3,600 seconds in an hour
    minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute

    pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.8, HEIGHT * 0.015, WIDTH * 0.19, HEIGHT * 0.04))

    year_text = FONT_1.render("Time passed (Simulation):", True, COLOR_WHITE)
    WINDOW.blit(year_text, (WIDTH * 0.81, HEIGHT * 0.02))

    pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.8, HEIGHT * 0.05, WIDTH * 0.19, HEIGHT * 0.04))

    text_actual_time = FONT_1.render(
        f'{int(years)} {"year" if int(years) <= 1 else "years"}, {int(days)} {"day" if int(days) <= 1 else "days"}, {int(hours):02}:{int(minutes):02}:{int(seconds):02}' if years > 0 else
        f'{int(days)} {"day" if int(days) <= 1 else "days"}, {int(hours):02}:{int(minutes):02}:{int(seconds):02}',
        True, COLOR_WHITE)
    WINDOW.blit(text_actual_time, (WIDTH * 0.81, HEIGHT * 0.055))

    if rocket.flightState == RocketFlightState.flying and \
            rocket.nearestPlanet.distanceToRocket - rocket.nearestPlanet.radius < 3 / 2 * rocket.nearestPlanet.radius:
        pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.915, HEIGHT * 0.015, WIDTH * 0.07, HEIGHT * 0.04))

        year_text = FONT_1.render("Altitude", True, COLOR_WHITE)
        WINDOW.blit(year_text, (WIDTH * 0.93, HEIGHT * 0.02))

        pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.915, HEIGHT * 0.05, WIDTH * 0.07, HEIGHT * 0.04))

        rocket_velocity = FONT_1.render(
            f'{round((rocket.nearestPlanet.distanceToRocket - rocket.nearestPlanet.radius) / 1000, 0)} km',
            True, COLOR_WHITE)
        WINDOW.blit(rocket_velocity, (WIDTH * 0.93, HEIGHT * 0.055))


def fuel_bar():
    # percentage = rocket.fuelmass / rocket.startfuelmass
    percentage = 0.75
    pygame.draw.rect(WINDOW, (255 * (1 - percentage), 255 * percentage, 0),
                     (WIDTH * 0.925, HEIGHT * 0.8, WIDTH * 0.05, HEIGHT * 0.15))
    pygame.draw.rect(WINDOW, (150, 150, 150),
                     (WIDTH * 0.925, HEIGHT * 0.8, WIDTH * 0.05, HEIGHT * 0.15 * (1 - percentage)))
    rocket_fuel = FONT_1.render(f'Fuel: {int(percentage * 100)}%', True, COLOR_WHITE)
    WINDOW.blit(rocket_fuel, (WIDTH * 0.94, HEIGHT * 0.95))
