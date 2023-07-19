import pygame
import datetime

from Methods.PackageInstaller import InstallAllPackages

from Views.MainView import RenderFlightInterface
from Views.StartView import *

from ViewController.DtoProcessEvent import DTOProcessEvent
from ViewController.DrawManager import DrawManager

from Methods.ConfigurePlanets import ConfigurePlanets
from Methods.GameMethods import ProcessHotKeyEvents, CenterScreenOnPlanet, PlanetIsInScreen, AutomaticZoomOnRocket
from Methods.RocketConfig import LoadRocket


now = datetime.datetime.now()
o

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

            if PlanetIsInScreen(Scale, planet, MoveX, MoveY, HEIGHT, WIDTH):
                DrawManager.PlanetDraw(planet, WINDOW, show_distance, MoveX, MoveY, draw_line, Scale, WIDTH, HEIGHT)
            else: 
                DrawManager.PlanetDrawLineOnly(planet, WINDOW, MoveX, MoveY, draw_line, Scale, WIDTH, HEIGHT, show_distance)

        time_passed = RenderFlightInterface(WINDOW, rocket, now, FONT_1, pause, Clock, time_passed, TimeStep, manager)
        if rocket.nearestPlanet.CheckCollision():
            if not rocket.landed:
                rocket.nearestPlanet.CheckLanding(rocket, run)
        DrawManager.RocketDraw(rocket, WINDOW,MoveX,MoveY, planets, pause, Scale, WIDTH, HEIGHT)
        if not rocket.landed:
            rocket.UpdatePlanetsInRangeList(planets)
            rocket.UpdateNearestPlanet(planets)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    InstallAllPackages()
    ShowStartUI()
    main()