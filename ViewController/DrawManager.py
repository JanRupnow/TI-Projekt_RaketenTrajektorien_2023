import pygame 
import numpy as np 
import math

from Globals.Constants import MIN_ROCKET_RADIUS, COLOR_WHITE, WIDTH, HEIGHT, WINDOW, DATA

from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket
from ViewController.Rocket.RocketFlightState import RocketFlightState

class DrawManager():

    @staticmethod
    def DrawPlanet(planet : Planet):
 
        DrawManager.DrawPlanetOrbit(planet)
        pygame.draw.circle(WINDOW, planet.color, (planet.position_X[planet.currentStep]*DATA.getScale()+DATA.getMoveX()+WIDTH/2, planet.position_Y[planet.currentStep]*DATA.getScale()+DATA.getMoveY()+ HEIGHT/2), max(planet.scaleR * DATA.getScale(), 2))
       
    @staticmethod
    def DrawPlanetOrbit(planet : Planet):

        lineInScreen = planet.LineIsInScreen(np.array((planet.position_X[planet.currentStep:planet.currentCalculationStep]*DATA.getScale(), planet.position_Y[planet.currentStep:planet.currentCalculationStep]*DATA.getScale())).T)
        # size > 3 because (2,3) are 2 coordinates for 1 point and you need 2 points to connect a line ((x,y),(x2,y2))
        if lineInScreen.size > 3:
            pygame.draw.lines(WINDOW, planet.color, False, lineInScreen, 1)

    @staticmethod        
    def DisplayPlanetDistances(planet : Planet):

        distance_text = pygame.font.SysFont("Trebuchet MS", 16).render(f"{planet.name}:{str(round(planet.distanceToRocket * 1.057 * 10 ** -16, 8))} light years", True,
                                    COLOR_WHITE)
        WINDOW.blit(distance_text, (planet.position_X[planet.currentStep]*DATA.getScale()+ WIDTH/2 - distance_text.get_width() / 2 + DATA.getMoveX(),
                                planet.position_Y[planet.currentStep]*DATA.getScale()+ HEIGHT/2 + distance_text.get_height() / 2 - 20 + DATA.getMoveY()))

    @staticmethod
    def DrawRocketPrediction(rocket : Rocket):

        pygame.draw.lines(WINDOW, rocket.color, False, np.array((rocket.position_X[rocket.currentStep:rocket.currentCalculationStep]*DATA.getScale()+DATA.getMoveX()+WIDTH/2, rocket.position_Y[rocket.currentStep:rocket.currentCalculationStep]*DATA.getScale()+DATA.getMoveY()+ HEIGHT/2)).T, 1)
    
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