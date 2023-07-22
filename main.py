import pygame
import datetime

from Globals.FlightData.ZoomGoal import ZoomGoal
from Globals.Constants import DATA

from Views.MainView import RenderFlightInterface
from Views.StartView import *

from ViewController.DrawManager import DrawManager
from ViewController.Rocket.RocketFlightState import RocketFlightState


from Methods.PackageInstaller import InstallAllPackages
from Methods.ConfigurePlanets import ConfigurePlanets
from Methods.GameMethods import ProcessHotKeyEvents, CenterScreenOnPlanet, PlanetIsInScreen, AutomaticZoomOnRocket
from Methods.RocketConfig import LoadRocket




def main():

    now = datetime.datetime.now()
    global CLOCK
    
    ConfigureStartValues()
    planets = ConfigurePlanets()
    rocket = LoadRocket(planets)

    while DATA.getRun():
        CLOCK.tick(60)
        
        WINDOW.fill(COLOR_UNIVERSE)

        for event in pygame.event.get():
            event, rocket = ProcessHotKeyEvents(event, rocket, planets)

        if DATA.getZoomGoal() == ZoomGoal.nearestPlanet:
            CenterScreenOnPlanet(rocket.nearestPlanet)
        elif DATA.getZoomGoal() == ZoomGoal.rocket:
                AutomaticZoomOnRocket(rocket) 

        for planet in planets:
            if PlanetIsInScreen(planet):
                DrawManager.PlanetDraw(planet)
            else: 
                DrawManager.PlanetDrawLineOnly(planet)

        RenderFlightInterface(rocket, now)
        if rocket.nearestPlanet.CheckCollision():
            if not rocket.flightState == RocketFlightState.landed:
                rocket.nearestPlanet.CheckLanding(rocket)

        DrawManager.RocketDraw(rocket, planets)
        if not rocket.flightState == RocketFlightState.landed:
            rocket.UpdatePlanetsInRangeList(planets)
            rocket.UpdateNearestPlanet(planets)
        pygame.display.update()
        
    pygame.quit()


if __name__ == "__main__":
    InstallAllPackages()
    ShowStartUI()
    main()