import pygame
import datetime

from Globals.FlightData.FlightDataManager import FlightDataManager
from Globals.FlightData.ZoomGoal import ZoomGoal
from Globals.FlightData.FlightDataManager import FlightDataManager
from Globals.FlightData.ZoomGoal import ZoomGoal

from Views.MainView import RenderFlightInterface
from Views.StartView import *

from ViewController.DrawManager import DrawManager
from ViewController.Rocket.RocketFlightState import RocketFlightState


from Methods.PackageInstaller import InstallAllPackages
from Methods.ConfigurePlanets import ConfigurePlanets
from Methods.GameMethods import ProcessHotKeyEvents, CenterScreenOnPlanet, PlanetIsInScreen, AutomaticZoomOnRocket
from Methods.RocketConfig import LoadRocket


now = datetime.datetime.now()

def main():
    global CLOCK
    # TODO set intial FlightDataManger values in Constants
    time_passed = datetime.timedelta(seconds=0)
    run = True
    zoomReferencePlanet = False
    pause = False
    show_distance = False
    mouse_x = 0
    mouse_y = 0
    draw_line = True
    manager = pg.UIManager((WIDTH,HEIGHT))
    planets = ConfigurePlanets()
    rocket = LoadRocket(planets)

    while run:
        CLOCK.tick(60)
        
        WINDOW.fill(COLOR_UNIVERSE)

        for event in pygame.event.get():
            event, rocket, planets = ProcessHotKeyEvents(event, rocket, planets)
        if DATA.getZoomGoal == ZoomGoal.nearestPlanet:
            CenterScreenOnPlanet(rocket.nearestPlanet)
        else:
            if DATA.getZoomGoal() == ZoomGoal.rocket:
                AutomaticZoomOnRocket(rocket) 
        for planet in planets:
            #if not pause:
            #    planet.update_position(planets, rocket)
            # Ohne Radius verschwinden die Balken bugs im Screen

            if PlanetIsInScreen(planet,):
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