import numpy as np

from Globals.Constants import FILE_NAME
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.FlightDataManager import DATA
from Globals.Constants import NUM_OF_PREDICTIONS

from Methods.ConfigurePlanets import get_start_time

from ViewController.Rocket.RocketFlightState import RocketFlightState
from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket


class GameManager:
    def __init__(self):
        self.data_df = np.empty((0, 9), dtype="object")
        self.rows_to_append = np.empty((NUM_OF_PREDICTIONS, 9), dtype="object")
        self.data_array = np.zeros((NUM_OF_PREDICTIONS + 1, 5), dtype="object")

    def calculate_next_iteration(self, rocket: Rocket, planets: list[Planet]):
        if rocket.currentStep > NUM_OF_PREDICTIONS - 5:
            print(f"start: {rocket.currentStep}")

        rocket_takeoff = rocket.currentCalculationStep == 0 and rocket.currentStep == 0
        planet_takeoff = planets[0].currentCalculationStep == 0 and planets[0].currentStep == 0

        if planet_takeoff:
            self.new_calculations_for_planet(planets)
            return

        if rocket_takeoff and rocket.flightState == RocketFlightState.flying:
            [planet.reset_planets_array_to_sync_with_rocket() for planet in planets]

            self.new_calculations_for_planet(planets)
            rocket.calculate_new_calculation_of_predictions()
            rocket.updateRocketMass()
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
                rocket.updateRocketMass()
                rocket.currentStep += 1

            if DATA.flight_change_state == FlightChangeState.powerChanged:
                [planet.__setattr__('currentStep', planet.currentStep + 1) for planet in planets]
                [planet.calculate_next_step(planets) for planet in planets]
                # If only power changed adjust the rocket prediction
                rocket.calculate_new_calculation_of_predictions()
                rocket.updateRocketMass()
                rocket.currentStep += 1

            if DATA.flight_change_state == FlightChangeState.unchanged:
                self.calculate_next_step_for_planets(planets, rocket)
                rocket.calculate_one_prediction()
                rocket.updateRocketMass()
                rocket.currentStep += 1

            rocket.update_planets_in_range_list(planets)
            rocket.update_nearest_planet(planets)
            if rocket.nearestPlanet.check_collision():
                if rocket.nearestPlanet.check_landing(rocket):
                    rocket.flightState = RocketFlightState.landed
                    rocket.thrust = 0
                    self.fill_dataframe(rocket)
                    rocket.calculate_entry_angle()
                    rocket.clear_array()
                    rocket.nearestPlanet.update_distance_to_rocket(rocket)
                else:
                    rocket.flightState = RocketFlightState.crashed
                    self.fill_dataframe(rocket)
            if rocket.currentStep > NUM_OF_PREDICTIONS-5:
                print(f"end: {rocket.currentStep}")
            self.data_array[rocket.currentStep] = [(get_start_time() + DATA.time_passed).timestamp(),
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

        if rocket.flightState == RocketFlightState.crashed:
            DATA.run = False

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

    def fill_dataframe(self, rocket: Rocket):
        print(self.data_array[2:][~np.all(self.data_array[2:] == 0, axis=1)].shape)
        print(rocket.position_X.reshape(-1, 1)[2:rocket.currentStep].shape)
        print(rocket.position_Y.reshape(-1, 1)[2:rocket.currentStep].shape)
        print(rocket.velocity_X.reshape(-1, 1)[2:rocket.currentStep].shape)
        print(rocket.velocity_Y.reshape(-1, 1)[2:rocket.currentStep].shape)
        whole_data = np.hstack((self.data_array[2:][~np.all(self.data_array[2:] == 0, axis=1)],
                                rocket.position_X.reshape(-1, 1)[2:rocket.currentStep],
                                rocket.position_Y.reshape(-1, 1)[2:rocket.currentStep],
                                rocket.velocity_X.reshape(-1, 1)[2:rocket.currentStep],
                                rocket.velocity_Y.reshape(-1, 1)[2:rocket.currentStep]))
        self.data_df = np.vstack((self.data_df, whole_data))
        self.data_array = np.zeros((NUM_OF_PREDICTIONS + 1, 5))
        if rocket.flightState in {RocketFlightState.crashed, RocketFlightState.landed}:
            self.store_dataframe()

    def store_dataframe(self):
        with open(FILE_NAME, mode="a") as file:
            for row in self.data_df:
                file.write(','.join(map(str, row)) + '\n')
