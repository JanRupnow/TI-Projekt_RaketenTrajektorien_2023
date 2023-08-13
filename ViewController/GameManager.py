import sys

import numpy as np
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
    def __init__(self, data_df: pd.DataFrame):
        self.data_df = data_df

    def calculate_next_iteration(self, rocket: Rocket, planets: list[Planet]):

        rocket_takeoff = rocket.currentCalculationStep == 0 and rocket.currentStep == 0
        planet_takeoff = planets[0].currentCalculationStep == 0 and planets[0].currentStep == 0

        if planet_takeoff:
            self.new_calculations_for_planet(planets)
            return

        if rocket_takeoff and rocket.flightState == RocketFlightState.flying:
            [planet.reset_planets_array_to_sync_with_rocket() for planet in planets]

            self.new_calculations_for_planet(planets)
            rocket.calculate_new_calculation_of_predictions()
            rocket.currentStep += 1

        if DATA.flight_change_state == FlightChangeState.pausedAndPowerChanged:
            rocket.calculate_new_calculation_of_predictions()
            DATA.flight_change_state = FlightChangeState.paused
            return
        if DATA.flight_change_state == FlightChangeState.pausedAndTimeStepChanged:
            self.new_calculations_for_planet(planets)
            rocket.calculate_new_calculation_of_predictions()

        if DATA.flight_change_state == FlightChangeState.paused:
            return

        # Landed Rocket
        if rocket.flightState == RocketFlightState.landed:

            if DATA.flight_change_state == FlightChangeState.timeStepChanged:
                self.new_calculations_for_planet(planets)

            if DATA.flight_change_state == FlightChangeState.unchanged:
                self.calculate_next_step_for_planets(planets, rocket)

            rocket.stick_to_planet()

        # Flying Rocket
        if rocket.flightState == RocketFlightState.flying:
            # Save Rocket indepent variables
            if DATA.flight_change_state == FlightChangeState.timeStepChanged:
                # Calculate new orbits
                self.new_calculations_for_planet(planets)
                rocket.calculate_new_calculation_of_predictions()
                rocket.currentStep += 1

            if DATA.flight_change_state == FlightChangeState.powerChanged:
                [planet.__setattr__('currentStep', planet.currentStep + 1) for planet in planets]
                [planet.calculate_next_step(planets) for planet in planets]
                # If only power changed adjust the rocket prediction
                rocket.calculate_new_calculation_of_predictions()
                rocket.currentStep += 1

            if DATA.flight_change_state == FlightChangeState.unchanged:
                self.calculate_next_step_for_planets(planets, rocket)
                rocket.calculate_one_prediction()
                rocket.currentStep += 1

            rocket.update_planets_in_range_list(planets)
            rocket.update_nearest_planet(planets)
            if rocket.nearestPlanet.check_collision():
                rocket.nearestPlanet.check_landing(rocket)
                if rocket.flavor == RocketFlightState.crashed:
                    self.crash_fill_dataframe()
                    sys.exit(0)
            DATA_ARRAY[rocket.currentStep] = [(simulation_start_time + DATA.time_passed).strftime('%Y-%m-%d %H:%M:%S'),
                                              rocket.thrust,
                                              rocket.angle,
                                              1,
                                              rocket.fuelmass]
        # Only One condition since current steps should be synced after every calculation step
        if rocket.currentStep >= NUM_OF_PREDICTIONS:
            self.fill_dataframe(rocket)
            rocket.reset_array()
            [planet.reset_array() for planet in planets]

        DATA.flight_change_state = FlightChangeState.unchanged

        # Reset Planets arrays if rocket didnt start
        if planets[0].currentStep >= NUM_OF_PREDICTIONS:
            [planet.reset_array() for planet in planets]

    def new_calculations_for_planet(self, planets: list[Planet]):
        [planet.__setattr__('currentCalculationStep', planet.currentStep) for planet in planets]

        for i in range(NUM_OF_PREDICTIONS):
            [planet.calculate_next_step(planets) for planet in planets]
        if DATA.flight_change_state not in {FlightChangeState.paused, FlightChangeState.pausedAndPowerChanged,
                                            FlightChangeState.pausedAndTimeStepChanged}:
            [planet.__setattr__('currentStep', planet.currentStep + 1) for planet in planets]

    def calculate_next_step_for_planets(self, planets: list[Planet], rocket: Rocket):
        [(planet.predict_step(planet.currentCalculationStep, planets, rocket),
          planet.__setattr__('currentStep', planet.currentStep + 1)) for planet in planets]

    def display_iteration(self, rocket: Rocket, planets: list[Planet]):

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
        rows_to_append = []
        for idx, row in enumerate(DATA_ARRAY):
            if row[0] == 0:
                continue
            new_row = pd.DataFrame({"Time": row[0],
                       "Position_X": rocket.position_X[idx],
                       "Position_Y": rocket.position_Y[idx],
                       "Velocity_X": rocket.velocity_X[idx],
                       "Velocity_Y": rocket.velocity_X[idx],
                       "Power": row[1],
                       "Angle": row[2],
                       "Force": row[3],
                       "Rocket_Fuel": row[4]}, index=[0])
            rows_to_append.append(new_row)

        rows_to_append = np.reshape(rows_to_append, (rocket.currentStep-1, 9))
        new_data_df = pd.DataFrame(rows_to_append, columns=DF_COLUMNS)

        self.data_df = pd.concat([self.data_df, new_data_df], ignore_index=True)

        if self.data_df.shape[0] >= 2000:
            self.store_dataframe()

    def crash_fill_dataframe(self, rocket: Rocket):
        rows_to_append = []
        for idx, row in enumerate(DATA_ARRAY):
            if row[0] == 0:
                continue
            new_row = pd.DataFrame({"Time": row[0],
                       "Position_X": rocket.position_X[idx],
                       "Position_Y": rocket.position_Y[idx],
                       "Velocity_X": rocket.velocity_X[idx],
                       "Velocity_Y": rocket.velocity_X[idx],
                       "Power": row[1],
                       "Angle": row[2],
                       "Force": row[3],
                       "Rocket_Fuel": row[4]}, index=[0])
            rows_to_append.append(new_row)

        rows_to_append = np.reshape(rows_to_append, (rocket.currentStep-1, 9))
        new_data_df = pd.DataFrame(rows_to_append, columns=DF_COLUMNS)

        self.data_df = pd.concat([self.data_df, new_data_df], ignore_index=True)
        self.store_dataframe()

    def store_dataframe(self):
        self.data_df.to_csv(f"{FILE_NAME}", mode="a", header=False, index=False)
        self.data_df = pd.DataFrame(columns=DF_COLUMNS)
