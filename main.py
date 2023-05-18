import pygame
from objects.planet import *
from variables.konstanten import *
from objects.rocket import *
from methods.game_methods import *
import datetime
from DtoProcessEvent import DTOProcessEvent
from methods.planets import *
from views.main_view import *

WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)
pygame.display.set_caption("Solar System Simulation")


now = datetime.datetime.now()


def main():
    time_passed = datetime.timedelta(seconds=0)
    global scale, timestep, now, img0, move_x, move_y
    run = True
    pause = False
    show_distance = False
    clock = pygame.time.Clock()
    mouse_x = 0
    mouse_y = 0
    draw_line = True

    # Metric from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

    
    planets = getInitialPlanets()
    
    earth = next(filter(lambda x: x.name == "Erde", planets),None)
    sun = next(filter(lambda x: x.name == "Sonne", planets),None)


    rocket = Rocket(45,0,0,10000,earth,2,(255,255,255), sun)
    while run:
        clock.tick(60)
        WINDOW.fill(COLOR_UNIVERSE)
        
        for event in pygame.event.get():

            dtoProcessEvent = processKeyEvent(
                event,
                DTOProcessEvent(run, scale, move_x, move_y, mouse_x, mouse_y, show_distance, draw_line, timestep, pause),
                rocket,
                planets
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


        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        window_w, window_h = pygame.display.get_surface().get_size()
        distance = 10
        if keys[pygame.K_LEFT] or mouse_x == 0:
            move_x += distance
        if keys[pygame.K_RIGHT] or mouse_x == window_w - 1:
            move_x -= distance
        if keys[pygame.K_UP] or mouse_y == 0:
            move_y += distance
        if keys[pygame.K_DOWN] or mouse_y == window_h - 1:
            move_y -= distance
    

        move_x, move_y = automaticZoomOnRocket(rocket, scale, move_x, move_y)
        # Rocket
        rocket.draw(WINDOW,move_x,move_y, planets, pause, scale, WIDTH, HEIGHT)
        if rocket.rocketstarted:
            for planet in planets:
                #if not pause:
                #    planet.update_position(planets, rocket)
                # Ohne Radius verschwinden die Balken bugs im Screen

                if isInScreen(scale, planet, move_x, move_y, HEIGHT, WIDTH):
                    if show_distance :
                        planet.draw(WINDOW, 1, move_x, move_y, draw_line,scale, WIDTH, HEIGHT, pause, rocket)
                    else:
                        planet.draw(WINDOW, 0, move_x, move_y, draw_line,scale, WIDTH, HEIGHT, pause, rocket)
                else: 
                    planet.drawlineonly(WINDOW, move_x, move_y, draw_line, scale, WIDTH, HEIGHT, pause, rocket, show_distance)

        time_passed = renderTextView(WINDOW, rocket, now, FONT_1, pause, clock, time_passed, timestep)
        
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()