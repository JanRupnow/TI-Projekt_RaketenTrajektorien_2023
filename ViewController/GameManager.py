import numpy as np

from Globals.Constants import timestamp
from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.FlightDataManager import DATA
from Globals.Constants import NUM_OF_PREDICTIONS

from Methods.ConfigurePlanets import get_start_time
from ViewController.Manager import Manager

from ViewController.Rocket.RocketFlightState import RocketFlightState

class GameManager(Manager):
    def __init__(self):
        self.data_df = np.zeros((0, 12), dtype="str")
        self.data_array = np.zeros((NUM_OF_PREDICTIONS+1, 8), dtype="str")
        self.flight_number = 1
    def calculate_next_iteration(self):

        rocket_takeoff = self.rocket.currentCalculationStep == 0 and self.rocket.currentStep == 0
        planet_takeoff = self.planets[0].currentCalculationStep == 0 and self.planets[0].currentStep == 0

        if planet_takeoff:
            self.new_calculations_for_planet()
            return

        if rocket_takeoff and self.rocket.flightState == RocketFlightState.flying:
            [planet.reset_planets_array_to_sync_with_rocket() for planet in self.planets]

            self.new_calculations_for_planet()
            self.rocket.calculate_new_calculation_of_predictions()
            self.rocket.updateRocketMass()
            self.rocket.currentStep += 1

        if DATA.flight_change_state == FlightChangeState.pausedAndPowerChanged:
            self.rocket.calculate_new_calculation_of_predictions()
            DATA.flight_change_state = FlightChangeState.paused
            return
        if DATA.flight_change_state == FlightChangeState.pausedAndTimeStepChanged:
            self.new_calculations_for_planet()
            self.rocket.calculate_new_calculation_of_predictions()

        if DATA.flight_change_state == FlightChangeState.paused:
            return

        # Landed Rocket
        if self.rocket.flightState == RocketFlightState.landed:

            if DATA.flight_change_state == FlightChangeState.timeStepChanged:
                self.new_calculations_for_planet()

            if DATA.flight_change_state == FlightChangeState.unchanged:
                self.calculate_next_step_for_planets()

            self.rocket.stick_to_planet()

        # Flying Rocket
        if self.rocket.flightState == RocketFlightState.flying:
            # Save Rocket indepent variables
            if DATA.flight_change_state == FlightChangeState.timeStepChanged:
                # Calculate new orbits
                self.new_calculations_for_planet()
                self.rocket.calculate_new_calculation_of_predictions()
                self.rocket.updateRocketMass()
                self.rocket.currentStep += 1

            if DATA.flight_change_state == FlightChangeState.powerChanged:
                [planet.__setattr__('currentStep', planet.currentStep + 1) for planet in self.planets]
                [planet.calculate_next_step(self.planets) for planet in self.planets]
                # If only power changed adjust the rocket prediction
                self.rocket.calculate_new_calculation_of_predictions()
                self.rocket.updateRocketMass()
                self.rocket.currentStep += 1

            if DATA.flight_change_state == FlightChangeState.unchanged:
                self.calculate_next_step_for_planets()
                self.rocket.calculate_one_prediction()
                self.rocket.updateRocketMass()
                self.rocket.currentStep += 1

            self.rocket.update_planets_in_range_list(self.planets)
            self.rocket.update_nearest_planet(self.planets)
            if self.rocket.nearestPlanet.check_collision():
                if self.rocket.nearestPlanet.check_landing(self.rocket):
                    self.rocket.flightState = RocketFlightState.landed
                    self.rocket.thrust = 0
                    self.fill_dataframe()
                    self.rocket.calculate_entry_angle()
                    self.rocket.clear_array()
                    self.rocket.nearestPlanet.update_distance_to_rocket(self.rocket)
                else:
                    self.rocket.flightState = RocketFlightState.crashed
                    self.fill_dataframe()
            if self.rocket.currentStep > 1 and DATA.save_data:
                (a_planets, a_air, a_sun) = self.rocket.get_current_acceleration_split()
                self.data_array[self.rocket.currentStep] = [(get_start_time() + DATA.time_passed).timestamp(),
                                                       str(self.rocket.thrust),
                                                       str(self.rocket.angle),
                                                       str(1),
                                                       str(self.rocket.fuelmass),
                                                       str(a_planets),
                                                       str(a_air),
                                                       str(a_sun)]
        # Only One condition since current steps should be synced after every calculation step
        if self.rocket.currentStep >= NUM_OF_PREDICTIONS:
            if DATA.save_data:
                self.fill_dataframe()
            self.rocket.reset_array()
            [planet.reset_array() for planet in self.planets]

        DATA.flight_change_state = FlightChangeState.unchanged

        # Reset Planets arrays if rocket didnt start
        if self.planets[0].currentStep >= NUM_OF_PREDICTIONS:
            [planet.reset_array() for planet in self.planets]

        if self.rocket.flightState == RocketFlightState.crashed:
            DATA.run = False

    def new_calculations_for_planet(self):
        [planet.__setattr__('currentCalculationStep', planet.currentStep) for planet in self.planets]

        for i in range(NUM_OF_PREDICTIONS):
            [planet.calculate_next_step(self.planets) for planet in self.planets]
        if DATA.flight_change_state not in {FlightChangeState.paused, FlightChangeState.pausedAndPowerChanged,
                                            FlightChangeState.pausedAndTimeStepChanged}:
            [planet.__setattr__('currentStep', planet.currentStep + 1) for planet in self.planets]

    def calculate_next_step_for_planets(self):
        [(planet.predict_step(planet.currentCalculationStep, self.planets, self.rocket),
          planet.__setattr__('currentStep', planet.currentStep + 1)) for planet in self.planets]

    def fill_dataframe(self):
        data_length = self.data_array[np.any(self.data_array != "", axis=1)].shape[0]
        whole_data = np.hstack((self.data_array[np.any(self.data_array != "", axis=1)],
                                self.rocket.position_X.reshape(-1, 1)[1:data_length+1].astype("str"),
                                self.rocket.position_Y.reshape(-1, 1)[1:data_length+1].astype("str"),
                                self.rocket.velocity_X.reshape(-1, 1)[1:data_length+1].astype("str"),
                                self.rocket.velocity_Y.reshape(-1, 1)[1:data_length+1].astype("str")))
        self.data_df = np.vstack((self.data_df, whole_data))
        self.data_array = np.zeros((NUM_OF_PREDICTIONS+1, 8), dtype="str")
        if self.rocket.flightState in {RocketFlightState.crashed, RocketFlightState.landed}:
            self.store_dataframe()
            self.flight_number += 1
            self.data_df = np.zeros((0, 12), dtype="str")

    def store_dataframe(self):
        with open(f"Globals/FlightData/Flights/{timestamp}_Flight_{self.flight_number}.csv", "w") as file:
            file.write("Time,Position_X,Position_Y,Velocity_X,Velocity_Y,Power,Angle,Force,Rocket_Fuel\n")
        with open(f"Globals/FlightData/Flights/{timestamp}_Flight_{self.flight_number}.csv", mode="a") as file:
            np.savetxt(file, self.data_df, delimiter=',', fmt='%s')