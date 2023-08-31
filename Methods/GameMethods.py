import pygame

from Views.HotkeyView import *

from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState

from Globals.FlightData.ZoomGoal import ZoomGoal
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.FlightDataManager import DATA


def add_clock_time():
    DATA.time_passed += datetime.timedelta(seconds=DATA.time_step)


def automatic_zoom_on_rocket(rocket: Rocket):
    DATA.move_x = -rocket.position_X[rocket.currentStep] * DATA.scale
    DATA.move_y = -rocket.position_Y[rocket.currentStep] * DATA.scale


def automatic_zoom_on_rocket_once(rocket: Rocket):
    DATA.move_x = -rocket.position_X[rocket.currentStep] * DATA.scale
    DATA.move_y = -rocket.position_Y[rocket.currentStep] * DATA.scale


def center_screen_on_planet(planet: Planet):
    DATA.move_x = -planet.position_X[planet.currentStep] * DATA.scale
    DATA.move_y = -planet.position_Y[planet.currentStep] * DATA.scale


def scale_relative(factor):
    DATA.scale = STARTSCALE * factor


def mouse_position_shift_screen():
    DATA.move_x -= (DATA.mouse_x - WIDTH / 2) / 2
    DATA.move_y -= (DATA.mouse_y - HEIGHT / 2) / 2


def shift_time_step(shift_up, planets: list[Planet], rocket: Rocket):
    index = min(AllTimeSteps.index(DATA.time_step) + 1, len(AllTimeSteps) - 1) if shift_up else max(
        AllTimeSteps.index(DATA.time_step) - 1, 0)
    DATA.time_step = AllTimeSteps[index]
    for planet in planets:
        planet.time_step = AllTimeSteps[index]
    rocket.time_step = AllTimeSteps[index]
    if DATA.flight_change_state == FlightChangeState.paused:
        DATA.flight_change_state = FlightChangeState.pausedAndTimeStepChanged
    else:
        DATA.flight_change_state = FlightChangeState.timeStepChanged


def planet_is_in_screen(planet: Planet) -> bool:
    in_screen = planet.position_Y[
                   planet.currentStep] * DATA.scale + planet.radius * DATA.scale > -DATA.move_y - HEIGHT / 2
    in_screen = in_screen and planet.position_Y[
        planet.currentStep] * DATA.scale - planet.radius * DATA.scale < -DATA.move_y + HEIGHT / 2
    in_screen = in_screen and planet.position_X[
        planet.currentStep] * DATA.scale + planet.radius * DATA.scale > -DATA.move_x - WIDTH / 2
    return in_screen and planet.position_X[
        planet.currentStep] * DATA.scale - planet.radius * DATA.scale < -DATA.move_x + WIDTH / 2


def process_hot_key_events(event: pygame.event, rocket: Rocket, planets: list[Planet], draw_manager) -> (pygame.event, Rocket, list[Planet]):
    from ViewController.DrawManager import DrawManager

    key_pressed = pygame.key.get_pressed()
    # mouse_x, mouse_y = pygame.mouse.get_pos()
    DATA.mouse_x = pygame.mouse.get_pos()[0]
    DATA.mouse_y = pygame.mouse.get_pos()[1]
    distance = 10
    if key_pressed[Keys.H_moveScreenLeft[0]] or DATA.mouse_x < 5 and DATA.zoom_goal == ZoomGoal.none:
        DATA.move_x += distance
    elif key_pressed[Keys.H_moveScreenRight[0]] or DATA.mouse_x > WIDTH - 5 and DATA.zoom_goal == ZoomGoal.none:
        DATA.move_x -= distance
    elif key_pressed[Keys.H_moveScreenUp[0]] or DATA.mouse_y < 5 and DATA.zoom_goal == ZoomGoal.none:
        DATA.move_y += distance
    elif key_pressed[Keys.H_moveScreenDown[0]] or DATA.mouse_y > HEIGHT - 5 and DATA.zoom_goal == ZoomGoal.none:
        DATA.move_y -= distance

    elif (not event.type == pygame.KEYDOWN) and \
            key_pressed[Keys.h_rocket_boost_forward[0]] and rocket.thrust < 10:
        rocket.thrust += 1 and not DATA.flight_change_state == FlightChangeState.pausedAndPowerChanged
        if DATA.flight_change_state == FlightChangeState.paused:
            DATA.flight_change_state = FlightChangeState.pausedAndPowerChanged
        else:
            DATA.flight_change_state = FlightChangeState.powerChanged
        if rocket.flightState == RocketFlightState.landed:
            rocket.flightState = RocketFlightState.flying
    elif (not event.type == pygame.KEYDOWN) and key_pressed[Keys.h_rocket_boost_left[0]] and rocket.angle > -45 \
            and rocket.flightState == RocketFlightState.flying \
            and not DATA.flight_change_state == FlightChangeState.pausedAndPowerChanged:
        rocket.angle -= 1
        if DATA.flight_change_state == FlightChangeState.paused:
            DATA.flight_change_state = FlightChangeState.pausedAndPowerChanged
        else:
            DATA.flight_change_state = FlightChangeState.powerChanged
    elif (not event.type == pygame.KEYDOWN) and key_pressed[Keys.h_rocket_boost_right[0]] and rocket.angle < 45 \
            and rocket.flightState == RocketFlightState.flying \
            and not DATA.flight_change_state == FlightChangeState.pausedAndPowerChanged:
        rocket.angle += 1
        if DATA.flight_change_state == FlightChangeState.paused:
            DATA.flight_change_state = FlightChangeState.pausedAndPowerChanged
        else:
            DATA.flight_change_state = FlightChangeState.powerChanged
    elif (not event.type == pygame.KEYDOWN) and key_pressed[Keys.h_lower_rocket_boost[0]] and rocket.thrust > 0 and \
            rocket.flightState == RocketFlightState.flying \
            and not DATA.flight_change_state == FlightChangeState.pausedAndPowerChanged:
        rocket.thrust -= 1
        if DATA.flight_change_state == FlightChangeState.paused:
            DATA.flight_change_state = FlightChangeState.pausedAndPowerChanged
        else:
            DATA.flight_change_state = FlightChangeState.powerChanged

    elif event.type == pygame.QUIT or check_key_down(event, Keys.h_leave_simulation[0]) or check_key_down(event,
                                                                                                          Keys.h_close_window[
                                                                                                             0]):
        DATA.run = False
    elif check_key_down(event, Keys.h_zoom_rocket_start[0]):
        scale_relative(100000)
        draw_manager.set_rocket_scale(rocket, 100000)
        automatic_zoom_on_rocket_once(rocket)
    # Zoom Startorbit
    elif check_key_down(event, Keys.h_zoom_rocket_planet[0]):
        scale_relative(10)
        draw_manager.set_rocket_scale(rocket, 10)
        automatic_zoom_on_rocket_once(rocket)
    # Zoom Universum
    elif check_key_down(event, Keys.h_zoom_rocket_planet_system[0]):
        scale_relative(1)
        draw_manager.set_rocket_scale(rocket, 1)
        automatic_zoom_on_rocket_once(rocket)

    elif check_key_down(event, Keys.H_zoomAutoOnReferencePlanet[0]) and DATA.zoom_goal != ZoomGoal.rocket:
        if DATA.zoom_goal == ZoomGoal.nearestPlanet:
            DATA.zoom_goal = ZoomGoal.none
        elif DATA.zoom_goal == ZoomGoal.none:
            DATA.zoom_goal = ZoomGoal.nearestPlanet
    elif check_key_down(event, Keys.h_zoom_auto_on_rocket[0]) and DATA.zoom_goal != ZoomGoal.nearestPlanet:
        if DATA.zoom_goal == ZoomGoal.rocket:
            DATA.zoom_goal = ZoomGoal.none
        elif DATA.zoom_goal == ZoomGoal.none:
            DATA.zoom_goal = ZoomGoal.rocket
    elif check_key_down(event, Keys.h_pause_simulation[0]) and (FlightChangeState.paused or FlightChangeState.unchanged):
        if DATA.flight_change_state == FlightChangeState.paused:
            DATA.flight_change_state = FlightChangeState.unchanged
        elif DATA.flight_change_state == FlightChangeState.unchanged:
            DATA.flight_change_state = FlightChangeState.paused
    elif check_key_down(event, Keys.h_show_distance[0]):
        DATA.show_distance = not DATA.show_distance
    elif check_key_down(event, Keys.h_center_on_sun[0]):
        sun = next(filter(lambda x: x.name == "Sun", planets), None)
        center_screen_on_planet(sun)
    elif check_key_down(event, Keys.h_center_on_rocket[0]):
        automatic_zoom_on_rocket_once(rocket)
    elif check_key_down(event, Keys.h_draw_line[0]):
        DATA.draw_orbit = not DATA.draw_orbit
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
        mouse_position_shift_screen()
        DATA.scale *= 0.75
        draw_manager.set_rocket_scale(0.75)

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
        mouse_position_shift_screen()
        DATA.scale *= 1.25
        draw_manager.set_rocket_scale(1.25)

    elif check_key_down(event, Keys.h_shift_time_step_up[0]) and not DATA.flight_change_state == FlightChangeState.pausedAndTimeStepChanged:
        shift_time_step(True, planets, rocket)
    elif check_key_down(event, Keys.h_shift_time_step_down[0]) and not DATA.flight_change_state == FlightChangeState.pausedAndTimeStepChanged:
        shift_time_step(False, planets, rocket)
    elif check_key_down(event, Keys.h_open_settings[0]):
        show_settings_ui()

    elif check_key_down(event, Keys.h_switch_interface[0]):
        DATA.advanced_interface = not DATA.advanced_interface
    return event, rocket, planets


def convert_to_line_in_screen(line) -> np.array:
    line_in_screen = line
    line_in_screen[:, 0] = line_in_screen[:, 0] + DATA.move_x + WIDTH / 2
    line_in_screen[:, 1] = line_in_screen[:, 1] + DATA.move_y + HEIGHT / 2
    line_in_screen = line_in_screen[(line_in_screen[:, 0] < WIDTH) & (line_in_screen[:, 0] > 0)]
    line_in_screen = line_in_screen[(line_in_screen[:, 1] < HEIGHT) & (line_in_screen[:, 1] > 0)]
    return line_in_screen
