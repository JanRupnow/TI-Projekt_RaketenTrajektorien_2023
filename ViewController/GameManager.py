import pandas as pd

from Methods.GameMethods import center_screen_on_planet, planet_is_in_screen, automatic_zoom_on_rocket

from Globals.Constants import simulation_start_time, DATA_ARRAY, DF_COLUMNS, FILE_NAME
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.ZoomGoal import ZoomGoal
from Globals.FlightData.FlightDataManager import DATA
from Globals.Constants import NUM_OF_PREDICTIONS

from ViewController.Rocket.RocketFlightState import RocketFlightState
from ViewController.DrawManager import DrawManager, render_flight_interface
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
            [planet.reset_planets_array_to_sync_with_rocket() for planet in planets]

            GameManager.new_calculations_for_planet(planets)
            rocket.calculate_new_calculation_of_predictions()
            rocket.currentStep += 1

        if DATA.flight_change_state == FlightChangeState.pausedAndPowerChanged:
            rocket.calculate_new_calculation_of_predictions()
            DATA.flight_change_state = FlightChangeState.paused
            return
        if DATA.flight_change_state == FlightChangeState.pausedAndTimeStepChanged:
            GameManager.new_calculations_for_planet(planets)
            rocket.calculate_new_calculation_of_predictions()

        if DATA.flight_change_state == FlightChangeState.paused:
            return

        # Landed Rocket
        if rocket.flightState == RocketFlightState.landed:

            if DATA.flight_change_state == FlightChangeState.timeStepChanged:
                GameManager.new_calculations_for_planet(planets)

            if DATA.flight_change_state == FlightChangeState.unchanged:
                GameManager.calculate_next_step_for_planets(planets, rocket)

            rocket.stick_to_planet()

        # Flying Rocket
        if rocket.flightState == RocketFlightState.flying:
            # Save Rocket indepent variables
            if DATA.flight_change_state == FlightChangeState.timeStepChanged:
                # Calculate new orbits
                GameManager.new_calculations_for_planet(planets)
                rocket.calculate_new_calculation_of_predictions()
                rocket.currentStep += 1

            if DATA.flight_change_state == FlightChangeState.powerChanged:
                [planet.__setattr__('currentStep', planet.currentStep + 1) for planet in planets]
                [planet.calculate_next_step(planets) for planet in planets]
                # If only power changed adjust the rocket prediction
                rocket.calculate_new_calculation_of_predictions()
                rocket.currentStep += 1

            if DATA.flight_change_state == FlightChangeState.unchanged:
                GameManager.calculate_next_step_for_planets(planets, rocket)
                rocket.calculate_one_prediction()
                rocket.currentStep += 1

            rocket.update_planets_in_range_list(planets)
            rocket.update_nearest_planet(planets)
            if rocket.nearestPlanet.check_collision():
                # TODO GameManager.fill_dataframe()
                rocket.nearestPlanet.check_landing(rocket)

            #TODO store the variables to Numpy Array
        # Only One condition since current steps should be synced after every calculation step
        if rocket.currentStep >= NUM_OF_PREDICTIONS:
            # TODO GameManager.fill_dataframe()
            rocket.reset_array()
            [planet.reset_array() for planet in planets]

        DATA.flight_change_state = FlightChangeState.unchanged

        # Reset Planets arrays if rocket didnt start
        if planets[0].currentStep >= NUM_OF_PREDICTIONS:
            [planet.reset_array() for planet in planets]

        # TODO implement checking crashing

    @staticmethod
    def new_calculations_for_planet(planets: list[Planet]):
        [planet.__setattr__('currentCalculationStep', planet.currentStep) for planet in planets]

        for i in range(NUM_OF_PREDICTIONS):
            [planet.calculate_next_step(planets) for planet in planets]
        if DATA.flight_change_state not in {FlightChangeState.paused, FlightChangeState.pausedAndPowerChanged,
                                            FlightChangeState.pausedAndTimeStepChanged}:
            [planet.__setattr__('currentStep', planet.currentStep + 1) for planet in planets]

    @staticmethod
    def calculate_next_step_for_planets(planets: list[Planet], rocket: Rocket):
        [(planet.predict_step(planet.currentCalculationStep, planets, rocket),
          planet.__setattr__('currentStep', planet.currentStep + 1)) for planet in planets]

    @staticmethod
    def display_iteration(rocket: Rocket, planets: list[Planet]):

        if DATA.zoom_goal == ZoomGoal.nearestPlanet:
            center_screen_on_planet(rocket.nearestPlanet)
        elif DATA.zoom_goal == ZoomGoal.rocket:
            automatic_zoom_on_rocket(rocket)

        if rocket.flightState == RocketFlightState.flying:
            DrawManager.draw_rocket(rocket)
            DrawManager.draw_rocket_prediction(rocket)
        else:
            DrawManager.draw_rocket(rocket)
        for planet in planets:
            if planet_is_in_screen(planet):
                DrawManager.draw_planet(planet)
            if DATA.draw_orbit:
                DrawManager.draw_planet_orbit(planet)
            if DATA.show_distance:
                DrawManager.display_planet_distances(planet)
        render_flight_interface(rocket, simulation_start_time, planets)

    def fill_dataframe(self, rocket: Rocket):
        global DATA_df
        for idx, row in enumerate(DATA_ARRAY):
            new_row = {"Time": row[0],
                       "Position_X": rocket.position_X[idx + 1],
                       "Position_Y": rocket.position_Y[idx + 1],
                       "Velocity_X": rocket.Velocity_X[idx + 1],
                       "Velocity_Y": rocket.Velocity_X[idx + 1],
                       "Power": row[1],
                       "Angle": row[2],
                       "Force": row[3],
                       "Rocket_Fuel": row[4]}
            DATA_df = DATA_df.append(new_row, ignore_index=True)

            if DATA_df.shape[0] >= 8000:
                self.store_dataframe()

        # Just an Example to store data into the np arrays

    # DATA_ARRAY[rocket.currentStep] = [simulation_start_time + DATA.time_passed,
    #                                           rocket.power,
    #                                           rocket.angle,
    #                                           rocket.force,
    #                                           rocket.fuelmass]
    def store_dataframe(self):
        global DATA_df
        DATA_df.to_csv(f"Globals/FlightData/Flights/{FILE_NAME}", mode="a", header=False, index=False)
        DATA_df = pd.DataFrame(columns=DF_COLUMNS)
