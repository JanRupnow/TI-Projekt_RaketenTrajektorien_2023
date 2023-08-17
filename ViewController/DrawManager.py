import math
from pygame import Surface

from Globals.Constants import *
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.FlightDataManager import DATA
from Globals.FlightData.ZoomGoal import ZoomGoal
from Methods.ConfigurePlanets import get_start_time

from Methods.GameMethods import convert_to_line_in_screen, add_clock_time, center_screen_on_planet, \
    automatic_zoom_on_rocket, planet_is_in_screen

from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState


class DrawManager:
    rocket_initialImage: Surface = None
    rocket_currentImage: Surface = None
    rocket_notRotatedImage: Surface = None
    sun_surface = FONT_1.render("- Sun", True, COLOR_SUN)
    mercury_surface = FONT_1.render("- Mercury", True, COLOR_MERCURY)
    venus_surface = FONT_1.render("- Venus", True, COLOR_VENUS)
    earth_surface = FONT_1.render("- Earth", True, COLOR_EARTH)
    mars_surface = FONT_1.render("- Mars", True, COLOR_MARS)
    jupiter_surface = FONT_1.render("- Jupiter", True, COLOR_JUPITER)
    saturn_surface = FONT_1.render("- Saturn", True, COLOR_SATURN)
    uranus_surface = FONT_1.render("- Uranus", True, COLOR_URANUS)
    neptune_surface = FONT_1.render("- Neptune", True, COLOR_NEPTUNE)

    state_text = FONT_1.render("State", True, COLOR_WHITE)
    simulation_start_time_text = FONT_1.render("Simulation Time:", True, COLOR_WHITE)
    rocket_weight_text = FONT_1.render("Weight (t):", True, COLOR_WHITE)
    time_step_text = FONT_1.render("Step >>", True, COLOR_WHITE)
    zoom_text = FONT_1.render("Zoom", True, COLOR_WHITE)
    velocity_text = FONT_1.render("Velocity", True, COLOR_WHITE)
    time_passed_text = FONT_1.render("Time passed (Simulation):", True, COLOR_WHITE)
    altitude_text = FONT_1.render("Altitude", True, COLOR_WHITE)

    def display_iteration(self, rocket: Rocket, planets: list[Planet]):

        if DATA.zoom_goal == ZoomGoal.nearestPlanet:
            center_screen_on_planet(rocket.nearestPlanet)
        elif DATA.zoom_goal == ZoomGoal.rocket:
            automatic_zoom_on_rocket(rocket)

        if rocket.flightState == RocketFlightState.flying:
            self.draw_rocket(rocket)
            self.draw_rocket_prediction(rocket)
        else:
            self.draw_rocket(rocket)
        for planet in planets:
            if planet_is_in_screen(planet):
                self.draw_planet(planet)
            if DATA.draw_orbit:
                self.draw_planet_orbit(planet)
            if DATA.show_distance:
                self.display_planet_distances(planet)
        self.render_flight_interface(rocket, planets)

    def draw_planet(self, planet: Planet) -> None:
        self.draw_planet_orbit(planet)
        pygame.draw.circle(WINDOW, planet.color, (
            planet.position_X[planet.currentStep] * DATA.scale + DATA.move_x + WIDTH / 2,
            planet.position_Y[planet.currentStep] * DATA.scale + DATA.move_y + HEIGHT / 2),
                           max(planet.scaleR * DATA.scale, 2))

    def set_rocket_image(self, image: Surface, radius) -> None:
        self.rocket_initialImage = image
        self.rocket_currentImage = pygame.transform.scale_by(image, min(0.1 * radius, 1))
        self.rocket_notRotatedImage = self.rocket_currentImage

    def set_rocket_scale(self, rocket: Rocket, scale) -> None:
        rocket.set_scale(scale)
        if MIN_ROCKET_RADIUS < rocket.radius < MAX_ROCKET_RADIUS:
            self.rocket_notRotatedImage = pygame.transform.scale_by(
                self.rocket_initialImage,
                max(min(0.1 * rocket.radius, 1), 0.1))

    def draw_planet_orbit(self, planet: Planet) -> None:

        line_in_screen = convert_to_line_in_screen(np.array((planet.position_X[
                                                             planet.currentStep:planet.currentCalculationStep] * DATA.scale,
                                                             planet.position_Y[
                                                             planet.currentStep:planet.currentCalculationStep] * DATA.scale)).T)
        # size > 3 because (2,3) are 2 coordinates for 1 point, you need 2 points to connect a line ((x,y),(x2,y2))
        if line_in_screen.size > 3:
            pygame.draw.lines(WINDOW, planet.color, False, line_in_screen, 1)

    def display_planet_distances(self, planet: Planet) -> None:

        distance_text = pygame.font.SysFont("Trebuchet MS", 16).render(
            f"{planet.name}:{str(round(planet.distanceToRocket * 1.057 * 10 ** -16, 8))} light years", True,
            COLOR_WHITE)
        WINDOW.blit(distance_text, (planet.position_X[
                                        planet.currentStep] * DATA.scale + WIDTH / 2 - distance_text.get_width() / 2 + DATA.move_x,
                                    planet.position_Y[
                                        planet.currentStep] * DATA.scale + HEIGHT / 2 + distance_text.get_height() / 2 - 20 + DATA.move_y))

    def draw_rocket_prediction(self, rocket: Rocket) -> None:

        line_in_screen = convert_to_line_in_screen(np.array((rocket.position_X[
                                                             rocket.currentStep:rocket.currentCalculationStep] * DATA.scale,
                                                             rocket.position_Y[
                                                             rocket.currentStep:rocket.currentCalculationStep] * DATA.scale)).T)
        # size > 3 because (2,3) are 2 coordinates for 1 point, you need 2 points to connect a line ((x,y),(x2,y2))
        if line_in_screen.size > 3:
            pygame.draw.lines(WINDOW, rocket.color, False, line_in_screen, 1)

    def draw_rocket(self, rocket: Rocket) -> None:

        if rocket.radius < MIN_ROCKET_RADIUS:
            pygame.draw.circle(WINDOW, rocket.color, (
                rocket.position_X[rocket.currentStep] * DATA.scale + DATA.move_x + WIDTH / 2,
                rocket.position_Y[rocket.currentStep] * DATA.scale + DATA.move_y + HEIGHT / 2),
                               MIN_ROCKET_RADIUS)
            return
        if rocket.flightState == RocketFlightState.flying:
            self.rocket_currentImage = pygame.transform.rotate(self.rocket_notRotatedImage, math.atan2(
                rocket.velocity_Y[rocket.currentStep] - rocket.startplanet.velocity_Y[rocket.currentStep],
                rocket.velocity_X[rocket.currentStep] - rocket.startplanet.velocity_X[rocket.currentStep]) * (
                                                                   -180) / np.pi - 90 - rocket.angle)
        elif rocket.flightState == RocketFlightState.landed:
            self.rocket_currentImage = pygame.transform.rotate(self.rocket_notRotatedImage,
                                                               rocket.planetAngle * (-180) / np.pi - 180)
        else:
            self.rocket_currentImage = pygame.transform.rotate(self.rocket_notRotatedImage,
                                                               math.atan2(
                                                                   rocket.velocity_Y[rocket.currentStep],
                                                                   rocket.velocity_X[rocket.currentStep])
                                                               * (-180) / np.pi - 90)

        # img = pygame.transform.rotozoom(img0, math.atan2(self.position_Y[self.currentStep], self.position_X[self.currentStep]), max(0.05, self.radius))
        WINDOW.blit(self.rocket_currentImage, (rocket.position_X[
                                                   rocket.currentStep] * DATA.scale
                                               + DATA.move_x + WIDTH / 2 - self.rocket_currentImage.get_width() / 2,
                                               rocket.position_Y[
                                                   rocket.currentStep] * DATA.scale
                                               + DATA.move_y + HEIGHT / 2 - self.rocket_currentImage.get_height() / 2
                                               ))

    def display_bar(self, rocket: Rocket) -> None:
        # Complete bar
        pygame.draw.rect(WINDOW, (50, 50, 50), (0, 0, WIDTH * 1, HEIGHT * 0.1))

        # Current Time
        pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.03, HEIGHT * 0.015, WIDTH * 0.15, HEIGHT * 0.04))

        WINDOW.blit(self.simulation_start_time_text, (WIDTH * 0.04, HEIGHT * 0.02))

        pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.03, HEIGHT * 0.05, WIDTH * 0.15, HEIGHT * 0.04))

        text_actual_time = FONT_1.render(
            f'{(get_start_time() + DATA.time_passed).strftime("%d/%m/%Y, %H:%M:%S")}',
            True, COLOR_WHITE)
        WINDOW.blit(text_actual_time, (WIDTH * 0.04, HEIGHT * 0.055))

        # Weight
        pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.2, HEIGHT * 0.015, WIDTH * 0.1, HEIGHT * 0.04))

        WINDOW.blit(self.rocket_weight_text, (WIDTH * 0.21, HEIGHT * 0.02))

        pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.2, HEIGHT * 0.05, WIDTH * 0.1, HEIGHT * 0.04))

        text_weight = FONT_1.render(
            f'{rocket.current_mass:,.0f}', True, COLOR_WHITE)
        WINDOW.blit(text_weight, (WIDTH * 0.21, HEIGHT * 0.055))

        # State
        pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.37, HEIGHT * 0.015, WIDTH * 0.07, HEIGHT * 0.04))

        WINDOW.blit(self.state_text, (WIDTH * 0.39, HEIGHT * 0.02))

        pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.37, HEIGHT * 0.05, WIDTH * 0.07, HEIGHT * 0.04))

        rocket_state = FONT_1.render(f'{rocket.flightState}', True, COLOR_WHITE)
        WINDOW.blit(rocket_state, (WIDTH * 0.385, HEIGHT * 0.055))
        # Timestep
        pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.45, HEIGHT * 0.015, WIDTH * 0.07, HEIGHT * 0.04))

        WINDOW.blit(self.time_step_text, (WIDTH * 0.465, HEIGHT * 0.02))

        pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.45, HEIGHT * 0.05, WIDTH * 0.07, HEIGHT * 0.04))

        time_step_value = FONT_1.render(f'{int(DATA.time_step * 60)}x', True, COLOR_WHITE)
        WINDOW.blit(time_step_value, (WIDTH * 0.465, HEIGHT * 0.055))

        # Zoom
        pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.53, HEIGHT * 0.015, WIDTH * 0.08, HEIGHT * 0.04))

        WINDOW.blit(self.zoom_text, (WIDTH * 0.55, HEIGHT * 0.02))

        pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.53, HEIGHT * 0.05, WIDTH * 0.08, HEIGHT * 0.04))

        zoom_value = FONT_1.render(f'{DATA.zoom_goal}', True, COLOR_WHITE)
        WINDOW.blit(zoom_value, (WIDTH * 0.532, HEIGHT * 0.055))

        # Current Speed
        pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.62, HEIGHT * 0.015, WIDTH * 0.07, HEIGHT * 0.04))

        WINDOW.blit(self.velocity_text, (WIDTH * 0.63, HEIGHT * 0.02))

        pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.62, HEIGHT * 0.05, WIDTH * 0.07, HEIGHT * 0.04))

        speed = round(
            rocket.get_current_relative_velocity()) if rocket.nearestPlanet.distanceToRocket < rocket.nearestPlanet.radius * 5 else round(
            rocket.get_absolute_velocity())

        rocket_velocity = FONT_1.render(f'{speed:,.0f} km/h', True,
                                        ((0, 160, 0) if speed < CRASH_VELOCITY else (160, 0, 0)))
        WINDOW.blit(rocket_velocity, (WIDTH * 0.625, HEIGHT * 0.055))

        # Time Passed
        total_seconds = DATA.time_passed.total_seconds()
        years, remainder = divmod(total_seconds, 31_536_000)  # 31,536,000 seconds in a year (approximate)
        days, remainder = divmod(remainder, 86_400)  # 86,400 seconds in a day
        hours, remainder = divmod(remainder, 3_600)  # 3,600 seconds in an hour
        minutes, seconds = divmod(remainder, 60)  # 60 seconds in a minute

        pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.7, HEIGHT * 0.015, WIDTH * 0.19, HEIGHT * 0.04))

        WINDOW.blit(self.time_passed_text, (WIDTH * 0.71, HEIGHT * 0.02))

        pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.7, HEIGHT * 0.05, WIDTH * 0.19, HEIGHT * 0.04))

        time_passed_value = FONT_1.render(
            f'{int(years)} {"year" if int(years) <= 1 else "years"}, {int(days)} {"day" if int(days) <= 1 else "days"}, {int(hours):02}:{int(minutes):02}:{int(seconds):02}' if years > 0 else
            f'{int(days)} {"day" if int(days) <= 1 else "days"}, {int(hours):02}:{int(minutes):02}:{int(seconds):02}',
            True, COLOR_WHITE)
        WINDOW.blit(time_passed_value, (WIDTH * 0.71, HEIGHT * 0.055))

        if rocket.flightState == RocketFlightState.flying and \
                rocket.nearestPlanet.distanceToRocket - rocket.nearestPlanet.radius < 3 / 2 * rocket.nearestPlanet.radius:
            pygame.draw.rect(WINDOW, (100, 100, 100), (WIDTH * 0.915, HEIGHT * 0.015, WIDTH * 0.07, HEIGHT * 0.04))

            WINDOW.blit(self.altitude_text, (WIDTH * 0.925, HEIGHT * 0.02))

            pygame.draw.rect(WINDOW, (20, 20, 20), (WIDTH * 0.915, HEIGHT * 0.05, WIDTH * 0.07, HEIGHT * 0.04))

            altitude_value = FONT_1.render(
                f'{round((rocket.nearestPlanet.distanceToRocket - rocket.nearestPlanet.radius) / 1000, 0)} km',
                True, COLOR_WHITE)
            WINDOW.blit(altitude_value, (WIDTH * 0.925, HEIGHT * 0.055))

    def fuel_bar(self, rocket: Rocket) -> None:
        percentage = rocket.fuelmass / rocket.startfuelmass
        pygame.draw.rect(WINDOW, (255 * (1 - percentage), 255 * percentage, 0),
                         (WIDTH * 0.925, HEIGHT * 0.95 - HEIGHT * 0.15 * percentage, WIDTH * 0.05,
                          HEIGHT * 0.15 * percentage))
        pygame.draw.rect(WINDOW, (150, 150, 150),
                         (WIDTH * 0.925, HEIGHT * 0.8, WIDTH * 0.05, HEIGHT * 0.15 * (1 - percentage)))
        rocket_fuel = FONT_1.render(f'Fuel: {int(percentage * 100)}%', True, COLOR_WHITE)
        WINDOW.blit(rocket_fuel, (WIDTH * 0.925, HEIGHT * 0.95))

    def angle_arc(self, rocket: Rocket) -> None:
        radius = 125
        center_x, center_y = WIDTH * 0.8, HEIGHT * 0.95
        line_length = radius
        pygame.draw.arc(WINDOW, (180, 180, 180), (center_x - radius, center_y - radius, radius * 2, radius * 2),
                        2 * math.pi, math.pi)
        x90 = center_x + radius * math.cos(0)
        y90 = center_y - radius * math.sin(0)
        x45 = center_x + line_length * math.cos(3 * math.pi / 4)
        y45 = center_y - line_length * math.sin(3 * math.pi / 4)
        x0 = center_x + radius * math.cos(math.pi / 2)
        y0 = center_y - radius * math.sin(math.pi / 2)
        x45_neg = center_x + line_length * math.cos(math.pi / 4)
        y45_neg = center_y - line_length * math.sin(math.pi / 4)
        x90_neg = center_x + radius * math.cos(math.pi)
        y90_neg = center_y - radius * math.sin(math.pi)
        pygame.draw.line(WINDOW, (180, 180, 180), (center_x, center_y), (x90, y90), 2)
        pygame.draw.line(WINDOW, (180, 180, 180), (center_x, center_y), (x45, y45), 2)
        pygame.draw.line(WINDOW, (180, 180, 180), (center_x, center_y), (x0, y0), 2)
        pygame.draw.line(WINDOW, (180, 180, 180), (center_x, center_y), (x45_neg, y45_neg), 2)
        pygame.draw.line(WINDOW, (180, 180, 180), (center_x, center_y), (x90_neg, y90_neg), 2)
        # Draw the needle based on the given angle
        angle_rad = math.radians(-rocket.angle + 90)
        min_size = line_length / 3
        x_needle = center_x + (min_size + ((line_length - min_size) / 10 * rocket.thrust)) * math.cos(angle_rad)
        y_needle = center_y - (min_size + ((line_length - min_size) / 10 * rocket.thrust)) * math.sin(angle_rad)
        pygame.draw.line(WINDOW, ((rocket.thrust / 10 * 255), ((10 - rocket.thrust) / 10 * 255), 0),
                         (center_x, center_y),
                         (x_needle,
                          y_needle),
                         5)

        rocket_power = FONT_1.render(f'Power: {rocket.thrust * 10}%', True, COLOR_WHITE)
        WINDOW.blit(rocket_power, (WIDTH * 0.77, HEIGHT * 0.96))

    def render_flight_interface(self, rocket: Rocket, planets: list[Planet]) -> None:
        if DATA.flight_change_state != FlightChangeState.paused:
            add_clock_time()

        self.display_bar(rocket)

        if DATA.advanced_interface:
            # Advanced flight details
            fps_text = FONT_1.render("FPS: " + str(int(CLOCK.get_fps())), True, COLOR_WHITE)
            WINDOW.blit(fps_text, (WIDTH * 0.025, HEIGHT * 0.13))

            # TODO implement Pressure

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
            WINDOW.blit(self.sun_surface, (15, 285))
            WINDOW.blit(self.mercury_surface, (15, 315))
            WINDOW.blit(self.venus_surface, (15, 345))
            WINDOW.blit(self.earth_surface, (15, 375))
            WINDOW.blit(self.mars_surface, (15, 405))
            WINDOW.blit(self.jupiter_surface, (15, 435))
            WINDOW.blit(self.saturn_surface, (15, 465))
            WINDOW.blit(self.uranus_surface, (15, 495))
            WINDOW.blit(self.neptune_surface, (15, 525))

        self.fuel_bar(rocket)
        self.angle_arc(rocket)
