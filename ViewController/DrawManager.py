import pygame 
import numpy as np 
import math
from abc import abstractmethod

from Methods.GameMethods import AutomaticZoomOnRocket

from Globals.Constants import NUM_OF_PREDICTIONS, MIN_ROCKET_RADIUS, COLOR_WHITE, WIDTH, HEIGHT, WINDOW, DATA

from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState
from Globals.FlightData.FlightChangeState import FlightChangeState

class DrawManager():

    @staticmethod
    def PlanetDraw(planet : Planet):

        # Orbit 
        DrawManager.PlanetDrawLineOnly(planet)
        # Planet
        pygame.draw.circle(WINDOW, planet.color, (planet.position_X[planet.currentStep]*DATA.getScale()+DATA.getMoveX()+WIDTH/2, planet.position_Y[planet.currentStep]*DATA.getScale()+move_y+ HEIGHT/2), max(planet.scaleR * DATA.getScale(), 2))

    @staticmethod
    def PlanetDrawLineOnly(planet : Planet):

        if DATA.getShowDistance():
            DrawManager.PlanetDisplayDistances(planet)
        if not DATA.getDrawOrbit():
            return
        line = planet.LineIsInScreen(np.array((planet.position_X[planet.currentStep:planet.currentCalculationStep]*DATA.getScale(), planet.position_Y[planet.currentStep:planet.currentCalculationStep]*DATA.getScale())).T, DATA.getMoveX(), DATA.getMoveY(), HEIGHT, WIDTH)
        # size > 3 because (2,3) are 2 coordinates for 1 point and you need 2 points to connect a line ((x,y),(x2,y2))
        if line.size > 3:
            pygame.draw.lines(WINDOW, planet.color, False, line, 1)

    @staticmethod        
    def PlanetDisplayDistances(planet : Planet):

        distance_text = pygame.font.SysFont("Trebuchet MS", 16).render(f"{planet.name}:{str(round(planet.distanceToRocket * 1.057 * 10 ** -16, 8))} light years", True,
                                    COLOR_WHITE)
        WINDOW.blit(distance_text, (planet.position_X[planet.currentStep]*DATA.getScale()+ WIDTH/2 - distance_text.get_width() / 2 + DATA.getMoveX(),
                                planet.position_Y[planet.currentStep]*DATA.getScale()+ HEIGHT/2 + distance_text.get_height() / 2 - 20 + DATA.getMoveY()))
        
    @staticmethod
    def RocketDraw(rocket : Rocket, planets : list[Planet]):

        if not rocket.flightState == RocketFlightState.flying:

            DrawManager.RocketDrawIfNotStarted(rocket, planets)
            return
        if not DATA.getSimulationPause():
            if DATA.getFlightChangeState() != FlightChangeState.unchanged or rocket.currentStep==0:
                firstTime = rocket.currentCalculationStep == 0

                if firstTime:
                    for planet in planets:
                        planet.ResetPlanetsArrayToSyncWithRocket()

                rocket.currentCalculationStep = rocket.currentStep
                rocket.CalculateNewCalculationOfPredictions(firstTime, planets)

                if not (firstTime or DATA.getFlightChangeState() == FlightChangeState.timeStepChanged):
                    for planet in planets:
                        planet.PredictStep(rocket.currentCalculationStep-1, planets, rocket)

                DATA.setFlightChangeState(FlightChangeState.unchanged)
            else:
                rocket.CalculateOnePrediction(planets)
        if rocket.currentCalculationStep > 2:
            # move_x and move_y verschieben je nach bewegung des Bildschirm
            move_x, move_y = AutomaticZoomOnRocket(rocket)
            pygame.draw.lines(WINDOW, rocket.color, False, np.array((rocket.position_X[rocket.currentStep:rocket.currentCalculationStep]*DATA.getScale()+move_x+WIDTH/2, rocket.position_Y[rocket.currentStep:rocket.currentCalculationStep]*DATA.getScale()+move_y+ HEIGHT/2)).T, 1)
            
            DrawManager.DrawRocket(rocket)
        if DATA.getSimulationPause:
            return
        rocket.currentStep += 1
        for planet in planets:
            planet.currentStep += 1

        if rocket.currentStep >= (NUM_OF_PREDICTIONS):
            rocket.ResetArray()
            for planet in planets:
                planet.ResetArray()

    @staticmethod
    def RocketDrawIfNotStarted(rocket : Rocket, planets):
        if not DATA.getSimulationPause():
            if planets[0].currentStep == 0 or DATA.getFlightChangeState == FlightChangeState.timeStepChanged:
                for planet in planets:
                    planet.aktuellerrechenschritt = planet.currentStep
                for i in range(NUM_OF_PREDICTIONS):
                    for planet in planets:
                        planet.PredictNext(planets)

                if DATA.getFlightChangeState == FlightChangeState.timeStepChanged:
                    DATA.setFlightChangeState(FlightChangeState.unchanged)

            else:
                for planet in planets:
                    planet.PredictNext(planets)

            for planet in planets:
                planet.currentStep += 1

            if planets[0].currentStep >= NUM_OF_PREDICTIONS:
                for planet in planets:
                    planet.ResetArray()

        DrawManager.RocketDrawAndValueBeforeStarting(rocket, planet)

    @staticmethod
    def RocketDrawAndValueBeforeStarting(rocket : Rocket, planet : Planet,):
        rocket.planet = rocket.nearestPlanet if rocket.flightState == RocketFlightState.landed else rocket.startplanet
        rocket.angle = rocket.entryAngle if rocket.flightState == RocketFlightState.landed else rocket.startingAngle
        rocket.position_X[0] = planet.position_X[planet.currentStep] + planet.radius * np.cos(rocket.angle * np.pi / 180)  
        rocket.position_Y[0] = planet.position_Y[planet.currentStep] + planet.radius * np.sin(rocket.angle * np.pi / 180)
        rocket.velocity_X[0] = planet.velocity_X[planet.currentStep]
        rocket.velocity_Y[0] = planet.velocity_Y[planet.currentStep]

        AutomaticZoomOnRocket(rocket)
        DrawManager.DrawRocket(rocket)

    @staticmethod
    def DrawRocket(rocket : Rocket):

        if rocket.radius < MIN_ROCKET_RADIUS:
            pygame.draw.circle(WINDOW, rocket.color, (rocket.position_X[rocket.currentStep]*DATA.getScale()+DATA.getMoveX()+WIDTH/2, rocket.position_Y[rocket.currentStep]*DATA.getScale()+DATA.getMoveY()+HEIGHT/2), MIN_ROCKET_RADIUS)
            return
        if rocket.flightState == RocketFlightState.flying:
            rocket.img = pygame.transform.rotate(rocket.notRotatedImg, math.atan2(rocket.position_Y[rocket.currentStep] - rocket.nearestPlanet.position_Y[rocket.currentStep], 
                                                                              rocket.position_X[rocket.currentStep] - rocket.nearestPlanet.position_X[rocket.currentStep]) * (-180) /np.pi - 90)
        else:
            rocket.img = pygame.transform.rotate(rocket.notRotatedImg, math.atan2(rocket.velocity_Y[rocket.currentStep], rocket.velocity_X[rocket.currentStep]) * (-180) /np.pi - 90)
        #img = pygame.transform.rotozoom(img0, math.atan2(self.position_Y[self.currentStep], self.position_X[self.currentStep]), max(0.05, self.radius))
        WINDOW.blit(rocket.img, (rocket.position_X[rocket.currentStep]*DATA.getScale()+DATA.getMoveX()+WIDTH/2 -rocket.img.get_width()/2 , rocket.position_Y[rocket.currentStep]*DATA.getScale()+DATA.getMoveY()+HEIGHT/2 - rocket.img.get_height()/2))