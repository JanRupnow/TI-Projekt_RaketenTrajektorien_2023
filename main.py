import pygame
import datetime

from Methods.PackageInstaller import InstallAllPackages

from Views.MainView import RenderFlightInterface
from Views.StartView import *

from ViewController.DtoProcessEvent import DTOProcessEvent
from ViewController.DrawManager import DrawManager
from ViewController.Rocket.RocketFlightState import RocketFlightState

from Methods.ConfigurePlanets import ConfigurePlanets
from Methods.GameMethods import ProcessHotKeyEvents, CenterScreenOnPlanet, PlanetIsInScreen, AutomaticZoomOnRocket
from Methods.RocketConfig import LoadRocket


now = datetime.datetime.now()

def main():
    time_passed = datetime.timedelta(seconds=0)

    global Scale, TimeStep, now, MoveX, MoveY, Clock
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
        Clock.tick(60)
        
        WINDOW.fill(COLOR_UNIVERSE)

        for event in pygame.event.get():

            dtoProcessEvent = ProcessHotKeyEvents(
                event,
                DTOProcessEvent(run, Scale, MoveX, MoveY, mouse_x, mouse_y, show_distance, draw_line, TimeStep, pause, zoomReferencePlanet),
                rocket,
                planets,
            )

            run = dtoProcessEvent.run
            Scale = dtoProcessEvent.scale
            MoveX = dtoProcessEvent.move_x
            MoveY = dtoProcessEvent.move_y
            mouse_x = dtoProcessEvent.mouse_x
            mouse_y = dtoProcessEvent.mouse_y
            show_distance = dtoProcessEvent.show_distance
            draw_line = dtoProcessEvent.draw_line
            TimeStep = dtoProcessEvent.timestep
            pause = dtoProcessEvent.pause
            zoomReferencePlanet = dtoProcessEvent.zoomReferencePlanet

        if  zoomReferencePlanet:
            MoveX, MoveY = CenterScreenOnPlanet(rocket.nearestPlanet, Scale, MoveX, MoveY)
        else:
            MoveX, MoveY = AutomaticZoomOnRocket(rocket, Scale, MoveX, MoveY) 
        for planet in planets:
            #if not pause:
            #    planet.update_position(planets, rocket)
            # Ohne Radius verschwinden die Balken bugs im Screen

            if PlanetIsInScreen(Scale, planet, MoveX, MoveY):
                DrawManager.PlanetDraw(planet, show_distance, MoveX, MoveY, draw_line, Scale)
            else: 
                DrawManager.PlanetDrawLineOnly(planet, MoveX, MoveY, draw_line, Scale, show_distance)

        time_passed = RenderFlightInterface(rocket, now, pause, Clock, time_passed, TimeStep)
        if rocket.nearestPlanet.CheckCollision():
            if not rocket.flightState == RocketFlightState.landed:
                rocket.nearestPlanet.CheckLanding(rocket, run)
        DrawManager.RocketDraw(rocket, MoveX, MoveY, planets, pause, Scale)
        if not rocket.flightState == RocketFlightState.landed:
            rocket.UpdatePlanetsInRangeList(planets)
            rocket.UpdateNearestPlanet(planets)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    InstallAllPackages()
    ShowStartUI()
    main()