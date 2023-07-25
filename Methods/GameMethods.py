from Globals.FlightData.ZoomGoal import ZoomGoal
from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState
from Views.HotkeyView import *

from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.FlightDataManager import DATA


def add_clock_time():
    DATA.set_time_passed(DATA.get_time_passed() + datetime.timedelta(seconds=DATA.get_time_step))


def automatic_zoom_on_rocket(rocket: Rocket):
    DATA.set_move_x(-rocket.position_X[rocket.currentStep] * DATA.get_scale())
    DATA.set_move_y(-rocket.position_Y[rocket.currentStep] * DATA.get_scale())


def automatic_zoom_on_rocket_once(rocket: Rocket):
    DATA.set_move_x(-rocket.position_X[rocket.currentStep] * DATA.get_scale())
    DATA.set_move_y(-rocket.position_Y[rocket.currentStep] * DATA.get_scale())


def center_screen_on_planet(planet: Planet):
    DATA.set_move_x(-planet.position_X[planet.currentStep] * DATA.get_scale())
    DATA.set_move_y(-planet.position_Y[planet.currentStep] * DATA.get_scale())


def scale_relative(factor):
    DATA.set_scale(STARTSCALE * factor)


def mouse_position_shift_screen():
    DATA.set_move_x(DATA.get_move_x() - (DATA.get_mouse_x() - WIDTH / 2) / 2)
    DATA.set_move_y(DATA.get_move_y() - (DATA.get_mouse_y() - HEIGHT / 2) / 2)


def shift_time_step(shift_up):
    index = min(AllTimeSteps.index(DATA.get_time_step()) + 1, len(AllTimeSteps) - 1) if shift_up else max(
        AllTimeSteps.index(DATA.get_time_step()) - 1, 0)
    DATA.set_time_step(AllTimeSteps[index])
    DATA.set_flight_change_state(FlightChangeState.timeStepChanged)


def planet_is_in_screen(planet: Planet):
    in_screen = planet.position_Y[
                   planet.currentStep] * DATA.get_scale() + planet.radius * DATA.get_scale() > -DATA.get_move_y() - HEIGHT / 2
    in_screen = in_screen and planet.position_Y[
        planet.currentStep] * DATA.get_scale() - planet.radius * DATA.get_scale() < -DATA.get_move_y() + HEIGHT / 2
    in_screen = in_screen and planet.position_X[
        planet.currentStep] * DATA.get_scale() + planet.radius * DATA.get_scale() > -DATA.get_move_x() - WIDTH / 2
    return in_screen and planet.position_X[
        planet.currentStep] * DATA.get_scale() - planet.radius * DATA.get_scale() < -DATA.get_move_x() + WIDTH / 2


def process_hot_key_events(event, rocket: Rocket, planets: list[Planet]):
    key_pressed = pygame.key.get_pressed()
    # mouse_x, mouse_y = pygame.mouse.get_pos()
    DATA.set_mouse_x(pygame.mouse.get_pos()[0])
    DATA.set_mouse_y(pygame.mouse.get_pos()[1])
    distance = 10

    if key_pressed[Keys.H_moveScreenLeft[0]] or DATA.get_mouse_x() == 0:
        DATA.set_move_x(DATA.get_move_x() + distance)
    elif key_pressed[Keys.H_moveScreenRight[0]] or DATA.get_mouse_x() == WIDTH - 1:
        DATA.set_move_x(DATA.get_move_x() - distance)
    elif key_pressed[Keys.H_moveScreenUp[0]] or DATA.get_mouse_y() == 0:
        DATA.set_move_y(DATA.get_move_y() + distance)
    elif key_pressed[Keys.H_moveScreenDown[0]] or DATA.get_mouse_y() == HEIGHT - 1:
        DATA.set_move_y(DATA.get_move_y() - distance)

    elif (not event.type == pygame.KEYDOWN) and \
            key_pressed[Keys.h_rocket_boost_forward[0]] and rocket.thrust < 10 \
            and not DATA.get_flight_change_state() != FlightChangeState.paused:
        rocket.thrust += 1
        DATA.set_flight_change_state(FlightChangeState.powerChanged)
        if rocket.flightState == RocketFlightState.landed:
            rocket.flightState = RocketFlightState.flying
    elif (not event.type == pygame.KEYDOWN) and key_pressed[Keys.h_rocket_boost_left[0]] and rocket.angle > -45 and rocket.flightState == RocketFlightState.flying:
        rocket.angle -= 1
        DATA.set_flight_change_state(FlightChangeState.powerChanged)
    elif (not event.type == pygame.KEYDOWN) and key_pressed[Keys.h_rocket_boost_right[0]] and rocket.angle < 45 and rocket.flightState == RocketFlightState.flying:
        rocket.angle += 1
        DATA.set_flight_change_state(FlightChangeState.powerChanged)
    elif (not event.type == pygame.KEYDOWN) and key_pressed[Keys.h_lower_rocket_boost[0]] and rocket.thrust > 0 and rocket.flightState == RocketFlightState.flying:
        rocket.thrust -= 1
        DATA.set_flight_change_state(FlightChangeState.powerChanged)

    elif event.type == pygame.QUIT or check_key_down(event, Keys.h_leave_simulation[0]) or check_key_down(event,
                                                                                                          Keys.h_close_window[
                                                                                                             0]):
        DATA.set_run(False)
    elif check_key_down(event, Keys.h_zoom_rocket_start[0]):
        DATA.set_scale(scale_relative(100000))
        rocket.set_scale(100000)
        automatic_zoom_on_rocket_once(rocket)
    # Zoom Startorbit
    elif check_key_down(event, Keys.h_zoom_rocket_planet[0]):
        DATA.set_scale(scale_relative(10))
        rocket.set_scale(10)
        automatic_zoom_on_rocket_once(rocket)
    # Zoom Universum
    elif check_key_down(event, Keys.h_zoom_rocket_planet_system[0]):
        DATA.set_scale(scale_relative(1))
        rocket.set_scale(1)
        automatic_zoom_on_rocket_once(rocket)

    elif check_key_down(event, Keys.H_zoomAutoOnReferencePlanet[0]) and DATA.get_zoom_goal() != ZoomGoal.rocket:
        if DATA.get_zoom_goal() == ZoomGoal.nearestPlanet:
            DATA.set_zoom_goal(ZoomGoal.none)
        elif DATA.get_zoom_goal() == ZoomGoal.none:
            DATA.set_zoom_goal(ZoomGoal.nearestPlanet)
    elif check_key_down(event, Keys.h_zoom_auto_on_rocket[0]) and DATA.get_zoom_goal() != ZoomGoal.nearestPlanet:
        if DATA.get_zoom_goal() == ZoomGoal.rocket:
            DATA.set_zoom_goal(ZoomGoal.none)
        elif DATA.get_zoom_goal() == ZoomGoal.none:
            DATA.set_zoom_goal(ZoomGoal.rocket)
    elif check_key_down(event, Keys.h_pause_simulation[0]):
        if DATA.get_flight_change_state == FlightChangeState.paused:
            DATA.set_flight_change_state(FlightChangeState.unchanged)
        if DATA.get_flight_change_state == FlightChangeState.unchanged:
            DATA.set_flight_change_state(FlightChangeState.paused)
    elif check_key_down(event, Keys.h_show_distance[0]):
        DATA.set_show_distance(not DATA.getShowDistance())
    elif check_key_down(event, Keys.h_center_on_sun[0]):
        sun = next(filter(lambda x: x.name == "Sun", planets), None)
        center_screen_on_planet(sun)
    elif check_key_down(event, Keys.h_center_on_rocket[0]):
        automatic_zoom_on_rocket_once(rocket)
    elif check_key_down(event, Keys.h_draw_line[0]):
        DATA.set_draw_orbit(not DATA.get_draw_orbit())
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
        mouse_position_shift_screen()
        DATA.set_scale(DATA.get_scale() * 0.75)
        rocket.set_scale(0.75)

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
        mouse_position_shift_screen()
        DATA.set_scale(DATA.get_scale() * 1.25)
        rocket.set_scale(1.25)

    elif check_key_down(event, Keys.h_shift_time_step_up[0]):
        shift_time_step(True)
    elif check_key_down(event, Keys.h_shift_time_step_down[0]):
        shift_time_step(False)
    elif check_key_down(event, Keys.h_open_settings[0]):
        show_settings_ui()
    return event, rocket


def line_is_in_screen(line):
    line_in_screen = line[(line[:, 0] < -DATA.get_move_x() + WIDTH / 2) & (line[:, 0] > -DATA.get_move_x() - WIDTH / 2)]
    line_in_screen = line_in_screen[
        (line_in_screen[:, 1] > -DATA.get_move_y() - HEIGHT / 2) & (line_in_screen[:, 1] < -DATA.get_move_y() + HEIGHT / 2)]
    line_in_screen[:, 0] = line_in_screen[:, 0] + DATA.get_move_x() + WIDTH / 2
    line_in_screen[:, 1] = line_in_screen[:, 1] + DATA.get_move_y() + HEIGHT / 2
    return line_in_screen
