from Globals.Constants import Now

from Methods.GameMethods import center_screen_on_planet, planet_is_in_screen, automatic_zoom_on_rocket

from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.ZoomGoal import ZoomGoal
from Globals.FlightData.FlightDataManager import DATA
from Globals.Constants import NUM_OF_PREDICTIONS

from ViewController.Rocket.RocketFlightState import RocketFlightState
from ViewController.DrawManager import DrawManager
from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket


class GameManager:
    @staticmethod
    def calculate_next_iteration(rocket: Rocket, planets: list[Planet]):

        rocket_takeoff = rocket.currentCalculationStep == 0 and rocket.currentStep == 0
        planet_takeoff = planets[0].currentCalculationStep == 0 and planets[0].currentStep == 0

        if planet_takeoff:
            GameManager.new_calculations_for_planet(planets)
            return

        if rocket_takeoff and rocket.flightState == RocketFlightState.flying:
            for planet in planets:
                planet.reset_planets_array_to_sync_with_rocket()
            GameManager.new_calculations_for_planet(planets)
            rocket.calculate_new_calculation_of_predictions(planets)
            rocket.currentStep += 1

        if DATA.get_flight_change_state() == FlightChangeState.pausedAndPowerChanged:
            rocket.calculate_new_calculation_of_predictions(planets)
            DATA.set_flight_change_state(FlightChangeState.paused)
            return
        if DATA.get_flight_change_state() == FlightChangeState.pausedAndTimeStepChanged:
            GameManager.new_calculations_for_planet(planets)
            rocket.calculate_new_calculation_of_predictions(planets)
            DATA.set_flight_change_state(FlightChangeState.paused)
            return
        if DATA.get_flight_change_state() == FlightChangeState.paused:
            return

        # Landed Rocket
        if rocket.flightState == RocketFlightState.landed:

            if DATA.get_flight_change_state() == FlightChangeState.timeStepChanged:

                for planet in planets:
                    planet.currentCalculationStep = planet.currentStep
                for i in range(NUM_OF_PREDICTIONS):
                    for planet in planets:
                        planet.calculate_next_step(planets)
                        planet.currentStep += 1

            if DATA.get_flight_change_state() == FlightChangeState.unchanged:

                GameManager.calculate_next_step_for_planets(planets, rocket)

            rocket.stick_to_planet()

        # Flying Rocket
        if rocket.flightState == RocketFlightState.flying:

            if DATA.get_flight_change_state() == FlightChangeState.timeStepChanged:

                # Calculate new orbits
                rocket.calculate_new_calculation_of_predictions(planets)
                rocket.currentStep += 1

            if DATA.get_flight_change_state() == FlightChangeState.powerChanged:

                for planet in planets:
                    planet.calculate_next_step(planets)
                    planet.currentStep += 1
                # If only power changed adjust the rocket prediction
                rocket.calculate_new_calculation_of_predictions(planets)
                rocket.currentStep += 1

            if DATA.get_flight_change_state() == FlightChangeState.unchanged:

                rocket.calculate_one_prediction(planets)
                rocket.currentStep += 1

        # Only One condition since current steps should be synced after every calculation step
        if rocket.currentStep >= NUM_OF_PREDICTIONS:
            rocket.reset_array()
            for planet in planets:
                planet.reset_array()

        DATA.set_flight_change_state(FlightChangeState.unchanged)

        # Reset Planets arrays if rocket didnt start
        if planets[0].currentStep >= NUM_OF_PREDICTIONS:
            for planet in planets:
                planet.reset_array()

    @staticmethod
    def display_iteration(rocket: Rocket, planets: list[Planet]):

        if DATA.get_zoom_goal() == ZoomGoal.nearestPlanet:
            center_screen_on_planet(rocket.nearestPlanet)
        elif DATA.get_zoom_goal() == ZoomGoal.rocket:
            automatic_zoom_on_rocket(rocket)

        if rocket.flightState == RocketFlightState.flying:
            DrawManager.draw_rocket(rocket)
            DrawManager.draw_rocket_prediction(rocket)
        else:
            DrawManager.draw_rocket(rocket)
        for planet in planets:
            if planet_is_in_screen(planet):
                DrawManager.draw_planet(planet)
            if DATA.get_draw_orbit():
                DrawManager.draw_planet_orbit(planet)
            if DATA.get_show_distance():
                DrawManager.display_planet_distances(planet)

        DrawManager.render_flight_interface(rocket, Now, planets)
