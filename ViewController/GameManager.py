
from Globals.Constants import DATA

from Methods.GameMethods import center_screen_on_planet, planet_is_in_screen, automatic_zoom_on_rocket

from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.ZoomGoal import ZoomGoal
from Globals.Constants import NUM_OF_PREDICTIONS

from ViewController.Rocket.RocketFlightState import RocketFlightState
from ViewController.DrawManager import DrawManager 
from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket

class GameManager:
    @staticmethod
    def calculate_next_iteration(rocket : Rocket, planets : list[Planet]):
        if DATA.get_flight_change_state() == FlightChangeState.paused:
            return
        
        ### Planet
        
        if planets[0].currentStep == 0:
            for planet in planets:
                    planet.currentCalculationStep = planet.currentStep
            # calculate whole orbit
            for i in range(NUM_OF_PREDICTIONS):
                for planet in planets:
                    planet.predict_next(planets)
            # calculate 1 step
            else:
                for planet in planets:
                    planet.predict_next(planets)
        for planet in planets:
                planet.currentStep += 1
        if planets[0].currentStep >= NUM_OF_PREDICTIONS:
                for planet in planets:
                    planet.reset_array()

        if DATA.get_flight_change_state == FlightChangeState.powerChanged:

            DATA.set_flight_change_state = FlightChangeState.unchanged
            return
        if DATA.get_flight_change_state == FlightChangeState.timeStepChanged:
            DATA.set_flight_change_state = FlightChangeState.unchanged
            return
        if DATA.get_flight_change_state == FlightChangeState.unchanged:
    @staticmethod
    def display_iteration(rocket : Rocket, planets : list[Planet]):

        DrawManager.draw_rocket(rocket)
        DrawManager.draw_rocket_prediction(rocket)

        for planet in planets:
            if planet_is_in_screen(planet):
                DrawManager.draw_planet(planet)
            if DATA.get_draw_orbit():
                DrawManager.draw_planet_orbit(planet)
            if DATA.getShowDistance():
                DrawManager.display_planet_distances(planet)

        if DATA.get_zoom_goal() == ZoomGoal.nearestPlanet:
            center_screen_on_planet(rocket.nearestPlanet)
        elif DATA.get_zoom_goal() == ZoomGoal.rocket:
                automatic_zoom_on_rocket(rocket)
