import pygame 
import numpy as np 
import math
from abc import abstractmethod

from Methods.GameMethods import AutomaticZoomOnRocket

from Globals.Constants import NUM_OF_PREDICTIONS, MIN_ROCKET_RADIUS

from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket

class DrawManager():

    @abstractmethod
    def PlanetDraw(planet : Planet, window, show, move_x, move_y, draw_line, scale, width, height):

        # Orbit 
        DrawManager.PlanetDrawLineOnly(planet, window, move_x, move_y, draw_line, scale, width, height, show)
        # Planet
        pygame.draw.circle(window, planet.color, (planet.r_x[planet.currentStep]*scale+move_x+width/2, planet.r_z[planet.currentStep]*scale+move_y+ height/2), max(planet.scaleR * scale, 2))

    @abstractmethod
    def PlanetDrawLineOnly(planet : Planet, window, move_x, move_y, draw_line, scale, width, height, show):

        if show:
            DrawManager.PlanetDisplayDistances(planet, scale, width ,height, window, move_x, move_y)
        if not draw_line:
            return
        line = planet.LineIsInScreen(np.array((planet.r_x[planet.currentStep:planet.currentCalculationStep]*scale, planet.r_z[planet.currentStep:planet.currentCalculationStep]*scale)).T, move_x, move_y, height, width)
        # size > 3 because (2,3) are 2 coordinates for 1 point and you need 2 points to connect a line ((x,y),(x2,y2))
        if line.size > 3:
            pygame.draw.lines(window, planet.color, False, line, 1)

    @abstractmethod         
    def PlanetDisplayDistances(planet : Planet, scale, width, height, window, move_x, move_y):

        distance_text = pygame.font.SysFont("Trebuchet MS", 16).render(planet.name+ ": "+str(round(planet.distanceToRocket * 1.057 * 10 ** -16, 8))+ "light years", True,
                                    (255,255,255))
        window.blit(distance_text, (planet.r_x[planet.currentStep]*scale+ width/2 - distance_text.get_width() / 2 + move_x,
                                planet.r_z[planet.currentStep]*scale+ height/2 + distance_text.get_height() / 2 - 20 + move_y))
        
    @abstractmethod
    def RocketDraw(rocket : Rocket, window, move_x, move_y, planets : list[Planet], paused, scale, width, height):
        if not rocket.rocketstarted or rocket.landed:
            #self.drawAndValueBeforeStarting(window, scale, width, height, move_x, move_y)
            DrawManager.RocketDrawIfNotStarted(rocket, paused, planets, window, scale, width, height, move_x, move_y)
            return
        if not paused:
            if rocket.powerchanged or rocket.currentStep==0 or rocket.timestepChanged:
                firstTime = rocket.currentCalculationStep == 0
                if firstTime:
                    for planet in planets:
                        planet.ResetPlanetsArrayToSyncWithRocket()
                rocket.currentCalculationStep = rocket.currentStep
                rocket.CalculateNewCalculationOfPredictions(firstTime, planets, paused)
                if not (firstTime or rocket.timestepChanged):
                    for planet in planets:
                        planet.PredictStep(rocket.currentCalculationStep-1, planets, paused, rocket)

                rocket.powerchanged = False
                rocket.timestepChanged = False

            else:
                rocket.CalculateOnePrediction(planets, paused)
        # move_x and move_y verschieben je nach bewegung des Bildschirm
        if rocket.currentCalculationStep > 2:
            move_x, move_y = AutomaticZoomOnRocket(rocket, scale, move_x, move_y)
            pygame.draw.lines(window, rocket.color, False, np.array((rocket.r_x[rocket.currentStep:rocket.currentCalculationStep]*scale+move_x+width/2, rocket.r_z[rocket.currentStep:rocket.currentCalculationStep]*scale+move_y+ height/2)).T, 1)
            
            DrawManager.DrawRocket(rocket, window, width, height, move_x, move_y, scale)
        if paused:
            return
        rocket.currentStep += 1
        for planet in planets:
            planet.currentStep += 1

        if rocket.currentStep >= (NUM_OF_PREDICTIONS):
            rocket.ResetArray()
            for planet in planets:
                planet.ResetArray()

    @abstractmethod
    def RocketDrawIfNotStarted(rocket : Rocket, paused, planets, window, scale, width, height, move_x, move_y):
        if not paused:
            if planets[0].currentStep == 0 or rocket.timestepChanged:
                for planet in planets:
                    planet.aktuellerrechenschritt = planet.currentStep
                for i in range(NUM_OF_PREDICTIONS):
                    for planet in planets:
                        planet.PredictNext(planets, paused)

                if rocket.timestepChanged:
                    rocket.timestepChanged = False

            else:
                for planet in planets:
                    planet.PredictNext(planets, paused)

            for planet in planets:
                planet.currentStep += 1

            if planets[0].currentStep >= NUM_OF_PREDICTIONS:
                for planet in planets:
                    planet.ResetArray()

        DrawManager.RocketDrawAndValueBeforeStarting(rocket, planet, window, scale, width, height, move_x, move_y)

    @abstractmethod
    def RocketDrawAndValueBeforeStarting(rocket : Rocket, planet : Planet ,window, scale, width, height, move_x, move_y):
        rocket.planet = rocket.nearestPlanet if rocket.landed else rocket.startplanet
        rocket.angle = rocket.entryAngle if rocket.landed else rocket.startingAngle
        rocket.r_x[0] = planet.r_x[planet.currentStep] + planet.radius * np.cos(rocket.angle * np.pi / 180)  
        rocket.r_z[0] = planet.r_z[planet.currentStep] + planet.radius * np.sin(rocket.angle * np.pi / 180)
        rocket.v_x[0] = planet.v_x[planet.currentStep]
        rocket.v_z[0] = planet.v_z[planet.currentStep]

        move_x, move_y = AutomaticZoomOnRocket(rocket, scale, move_x, move_y)
        DrawManager.DrawRocket(rocket, window, width, height, move_x, move_y, scale)

    @abstractmethod
    def DrawRocket(rocket : Rocket, window, width, height, move_x, move_y, scale):

        if rocket.radius < MIN_ROCKET_RADIUS:
            pygame.draw.circle(window, rocket.color, (rocket.r_x[rocket.currentStep]*scale+move_x+width/2, rocket.r_z[rocket.currentStep]*scale+move_y+height/2), MIN_ROCKET_RADIUS)
            return
        if rocket.landed or not rocket.rocketstarted:
            rocket.img = pygame.transform.rotate(rocket.notRotatedImg, math.atan2(rocket.r_z[rocket.currentStep] - rocket.nearestPlanet.r_z[rocket.currentStep], 
                                                                              rocket.r_x[rocket.currentStep] - rocket.nearestPlanet.r_x[rocket.currentStep]) * (-180) /np.pi - 90)
        else:
            rocket.img = pygame.transform.rotate(rocket.notRotatedImg, math.atan2(rocket.v_z[rocket.currentStep], rocket.v_x[rocket.currentStep]) * (-180) /np.pi - 90)
        #img = pygame.transform.rotozoom(img0, math.atan2(self.v_z[self.currentStep], self.v_x[self.currentStep]), max(0.05, self.radius))
        window.blit(rocket.img, (rocket.r_x[rocket.currentStep]*scale+move_x+width/2 -rocket.img.get_width()/2 , rocket.r_z[rocket.currentStep]*scale+move_y+height/2 - rocket.img.get_height()/2))