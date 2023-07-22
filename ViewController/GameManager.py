
from Globals.Constants import DATA

from Methods.GameMethods import CenterScreenOnPlanet, PlanetIsInScreen, AutomaticZoomOnRocket

from Globals.FlightData.FlightChangeState import FlightChangeState
from Globals.FlightData.ZoomGoal import ZoomGoal

from ViewController.Rocket.RocketFlightState import RocketFlightState
from ViewController.DrawManager import DrawManager 
from ViewController.Planet import Planet
from ViewController.Rocket.Rocket import Rocket

class GameManager():
    @staticmethod
    def CalculateNextIteration(rocket : Rocket, planets : list[Planet]):
        
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
            AutomaticZoomOnRocket(rocket)
            pygame.draw.lines(WINDOW, rocket.color, False, np.array((rocket.position_X[rocket.currentStep:rocket.currentCalculationStep]*DATA.getScale()+DATA.getMoveX()+WIDTH/2, rocket.position_Y[rocket.currentStep:rocket.currentCalculationStep]*DATA.getScale()+DATA.getMoveY()+ HEIGHT/2)).T, 1)
            
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

            if rocket.nearestPlanet.CheckCollision():
                if not rocket.flightState == RocketFlightState.landed:
                    rocket.nearestPlanet.CheckLanding(rocket)
                    rocket.UpdatePlanetsInRangeList(planets)
                    rocket.UpdateNearestPlanet(planets)

        rocket.CalculateLandedValues()
    @staticmethod
    def DisplayIteration(rocket : Rocket, planets : list[Planet]):

        DrawManager.DrawRocket(rocket)
        DrawManager.DrawRocketPrediction(rocket)

        for planet in planets:
            if PlanetIsInScreen(planet):
                DrawManager.DrawPlanet(planet)
            if DATA.getDrawOrbit():
                DrawManager.DrawPlanetOrbit(planet)
            if DATA.getShowDistance():
                DrawManager.DisplayPlanetDistances(planet)

        if DATA.getZoomGoal() == ZoomGoal.nearestPlanet:
            CenterScreenOnPlanet(rocket.nearestPlanet)
        elif DATA.getZoomGoal() == ZoomGoal.rocket:
                AutomaticZoomOnRocket(rocket) 
