import numpy as np

from Globals.Constants import *

from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState

from Methods.GameMethods import add_clock_time


def render_flight_interface(rocket: Rocket, now):
    fps_text = FONT_1.render("FPS: " + str(int(CLOCK.get_fps())), True, COLOR_WHITE)
    # TODO Show current information of zoom
    WINDOW.blit(fps_text, (WIDTH * 0.03, HEIGHT * 0.03))
    if DATA.get_flight_change_state() != FlightChangeState.paused:
        DATA.set_time_passed(add_clock_time())
    text_surface = FONT_1.render(f"Time step: {int(DATA.get_time_step() * 60)}x", True, COLOR_WHITE)
    WINDOW.blit(text_surface, (WIDTH * 0.8, HEIGHT * 0.03))
    text_actual_time = FONT_1.render(f'Current time: {(now + DATA.get_time_passed()).strftime("%d/%m/%Y, %H:%M:%S")}',
                                     True, COLOR_WHITE)
    WINDOW.blit(text_actual_time, (WIDTH * 0.8, HEIGHT * 0.06))
    text_time_passed = FONT_1.render(f'Passed time: {DATA.get_time_passed()}', True, COLOR_WHITE)
    WINDOW.blit(text_time_passed, (WIDTH * 0.8, HEIGHT * 0.09))

    distance = np.sqrt(
        (rocket.position_X[rocket.currentStep] - rocket.nearestPlanet.position_X[rocket.nearestPlanet.currentStep]) ** 2
        + (rocket.position_Y[rocket.currentStep] - rocket.nearestPlanet.position_Y[
            rocket.nearestPlanet.currentStep]) ** 2)
    speed = round(rocket.get_current_relative_velocity()) if distance < rocket.nearestPlanet.radius * 5 else round(
        rocket.get_absolute_velocity())
    rocket_velocity = FONT_1.render(f'Rocket Speed: {speed}km/h', True, COLOR_WHITE)
    WINDOW.blit(rocket_velocity, (WIDTH * 0.8, HEIGHT * 0.12))
    if not rocket.flightState == RocketFlightState.flying:
        rocket_velocity = FONT_1.render(f'Altitude: {0} km (Rocket has not started)', True, COLOR_WHITE)
    elif rocket.nearestPlanet.distanceToRocket - rocket.nearestPlanet.radius < 3 / 2 * rocket.nearestPlanet.radius:
        rocket_velocity = FONT_1.render(
            f'Altitude: {round((rocket.nearestPlanet.distanceToRocket - rocket.nearestPlanet.radius) / 1000, 0)} km',
            True, COLOR_WHITE)
    else:
        rocket_velocity = FONT_1.render(f'Altitude: not available in space', True, COLOR_WHITE)
    WINDOW.blit(rocket_velocity, (WIDTH * 0.8, HEIGHT * 0.15))
    rocket_fuel = FONT_1.render(f'Rocket Fuel: %', True, COLOR_WHITE)
    WINDOW.blit(rocket_fuel, (WIDTH * 0.8, HEIGHT * 0.18))
    rocket_max_q = FONT_1.render(f'MaxQ: %', True, COLOR_WHITE)
    WINDOW.blit(rocket_max_q, (WIDTH * 0.8, HEIGHT * 0.21))

    thrust_text = FONT_1.render(f'Thrust: {rocket.thrust}m/s^2', True, COLOR_WHITE)
    WINDOW.blit(thrust_text, (WIDTH * 0.8, HEIGHT * 0.8))
    angle_text = FONT_1.render(f'Angle: {rocket.angle}°', True, COLOR_WHITE)
    WINDOW.blit(angle_text, (WIDTH * 0.8, HEIGHT * 0.85))

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
