import pygame
from objects.planet import *
import variables.konstanten as keys
from objects.rocket import *
from methods.game_methods import *
import datetime
from objects.DtoProcessEvent import DTOProcessEvent
from methods.initialise_planets import *
from views.main_view import *
from views.start_view import *
from methods.rocket_config import *
import time

FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)
pygame.display.set_caption("Solar System Simulation")


now = datetime.datetime.now()


def main():
    time_passed = datetime.timedelta(seconds=0)
    global scale, timestep, now, img0, move_x, move_y, clock
    run = True
    pause = False
    show_distance = False
    mouse_x = 0
    mouse_y = 0
    draw_line = True

    
    planets = getInitialPlanets()

    rocket = loadRocket(planets)
    #rocket = Rocket(45,0,10000,earth,2,(255,255,255), sun)
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
        

        move_x, move_y = automaticZoomOnRocket(rocket, scale, move_x, move_y)
        # Rocket
        rocket.draw(WINDOW,move_x,move_y, planets, pause, scale, WIDTH, HEIGHT)
        #if rocket.rocketstarted:
        startPlanetdraw = time.time()
        for planet in planets:
            #if not pause:
            #    planet.update_position(planets, rocket)
            # Ohne Radius verschwinden die Balken bugs im Screen

            if planetIsInScreen(scale, planet, move_x, move_y, HEIGHT, WIDTH):
                if show_distance :
                    planet.draw(WINDOW, 1, move_x, move_y, draw_line,scale, WIDTH, HEIGHT, pause, rocket)
                else:
                    planet.draw(WINDOW, 0, move_x, move_y, draw_line,scale, WIDTH, HEIGHT, pause, rocket)
            else: 
                planet.drawlineonly(WINDOW, move_x, move_y, draw_line, scale, WIDTH, HEIGHT, pause, rocket, show_distance)

        time_passed = renderTextView(WINDOW, rocket, now, FONT_1, pause, clock, time_passed, timestep)
        endPlanetdraw = time.time()
        print(f"Planetdraw time: {startPlanetdraw-endPlanetdraw}")
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    # shows the start ui until start is clicked
    showStartUI()
    main()