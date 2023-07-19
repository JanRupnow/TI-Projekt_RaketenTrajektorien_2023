import pygame
import datetime

from Methods.PackageInstaller import InstallAllPackages

from Views.MainView import RenderFlightInterface
from Views.StartView import *

from ViewController.DtoProcessEvent import DTOProcessEvent
from ViewController.DrawManager import DrawManager

from Methods.InitialisePlanets import ConfigurePlanets
from Methods.GameMethods import ProcessHotKeyEvents, CenterScreenOnPlanet, PlanetIsInScreen, AutomaticZoomOnRocket
from Methods.RocketConfig import LoadRocket


now = datetime.datetime.now()


def main():
    time_passed = datetime.timedelta(seconds=0)
    global scale, timestep, now, move_x, move_y, clock
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
        clock.tick(60)
        
        WINDOW.fill(COLOR_UNIVERSE)

        for event in pygame.event.get():

            dtoProcessEvent = ProcessHotKeyEvents(
                event,
                DTOProcessEvent(run, scale, move_x, move_y, mouse_x, mouse_y, show_distance, draw_line, timestep, pause, zoomReferencePlanet),
                rocket,
                planets,
            )

            run = dtoProcessEvent.run
            scale = dtoProcessEvent.scale
            move_x = dtoProcessEvent.move_x
            move_y = dtoProcessEvent.move_y
            mouse_x = dtoProcessEvent.mouse_x
            mouse_y = dtoProcessEvent.mouse_y
            show_distance = dtoProcessEvent.show_distance
            draw_line = dtoProcessEvent.draw_line
            timestep = dtoProcessEvent.timestep
            pause = dtoProcessEvent.pause
            zoomReferencePlanet = dtoProcessEvent.zoomReferencePlanet

        if  zoomReferencePlanet:
            move_x, move_y = CenterScreenOnPlanet(rocket.nearestPlanet, scale, move_x, move_y)
        else:
            move_x, move_y = AutomaticZoomOnRocket(rocket, scale, move_x, move_y) 
        for planet in planets:
            #if not pause:
            #    planet.update_position(planets, rocket)
            # Ohne Radius verschwinden die Balken bugs im Screen

            if PlanetIsInScreen(scale, planet, move_x, move_y, HEIGHT, WIDTH):
                DrawManager.PlanetDraw(planet, WINDOW, show_distance, move_x, move_y, draw_line, scale, WIDTH, HEIGHT)
            else: 
                DrawManager.PlanetDrawLineOnly(planet, WINDOW, move_x, move_y, draw_line, scale, WIDTH, HEIGHT, show_distance)

        time_passed = RenderFlightInterface(WINDOW, rocket, now, FONT_1, pause, clock, time_passed, timestep, manager)
        if rocket.nearestPlanet.CheckCollision():
            if not rocket.landed:
                rocket.nearestPlanet.CheckLanding(rocket, run)
        DrawManager.RocketDraw(rocket, WINDOW,move_x,move_y, planets, pause, scale, WIDTH, HEIGHT)
        if not rocket.landed:
            rocket.UpdatePlanetsInRangeList(planets)
            rocket.UpdateNearestPlanet(planets)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    InstallAllPackages()
    ShowStartUI()
    main()