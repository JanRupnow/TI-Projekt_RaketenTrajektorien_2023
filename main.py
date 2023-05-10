import pygame
import math
import numpy as np
from planet import *
from konstanten import *
from rocket import *
import datetime
pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)
pygame.display.set_caption("Solar System Simulation")


now = datetime.datetime.now()


def main():
    time_passed = datetime.timedelta(seconds=0)
    global SCALE, TIMESTEP, now
    run = True
    pause = False
    show_distance = False
    clock = pygame.time.Clock()
    move_x = 0
    move_y = 0
    draw_line = True

    # Metric from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

    sun = Planet(0, 0, 695 * 10 ** 6, COLOR_SUN, 1.98892 * 10 ** 30,"Sonne")
    sun.sun = True

    mercury = Planet(-0.387 * AU, 0, 2439 * 10 ** 3, COLOR_MERCURY, 3.30 * 10 ** 23,"Merkur")
    mercury.y_vel = 47.4 * 1000

    venus = Planet(-0.723 * AU, 0, 6052 * 10 ** 3, COLOR_VENUS, 4.8685 * 10 ** 24,"Venus")
    venus.y_vel = 35.02 * 1000

    earth = Planet(-1 * AU, 0, 6378 * 10 ** 3, COLOR_EARTH, 5.9722 * 10 ** 24,"Erde")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * AU, 0, 3394  * 10 ** 3, COLOR_MARS, 6.39 * 10 ** 23,"Mars")
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 27,"Jupiter")
    jupiter.y_vel = 13.06 * 1000

    saturn = Planet(-9.573 * AU, 0, 60268  * 10 ** 3, COLOR_SATURN, 5.683 * 10 ** 26,"Saturn")
    saturn.y_vel = 9.68 * 1000

    uranus = Planet(-19.165 * AU, 0, 25559  * 10 ** 3, COLOR_URANUS, 8.681 * 10 ** 25,"Uranus")
    uranus.y_vel = 6.80 * 1000

    neptune = Planet(-30.178 * AU, 0, 24764  * 10 ** 3, COLOR_NEPTUNE, 1.024 * 10 ** 26,"Neptun")
    neptune.y_vel = 5.43 * 1000

    moon = Planet(-1*AU-378_000_000,0,1750*10**3,(220,220,220),73*10**21,"Mond")
    moon.y_vel = earth.y_vel+1.022*1000
    planets = [moon,neptune, uranus, saturn, jupiter, mars,earth, venus, mercury, sun,]
    

    rocket = Rocket(45,0,0,10000,earth,5,(255,255,255))
    while run:
        clock.tick(60)
        WINDOW.fill(COLOR_UNIVERSE)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             (event.key == pygame.K_x or event.key == pygame.K_ESCAPE)):
                run = False
            # Raketenboost Oben
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w and rocket.z_schub<10:
                rocket.z_schub += 1
                rocket.powerchanged = True
                rocket.rocketstarted = True
            # Raketenboost Links   
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and rocket.x_schub>-10:
                rocket.x_schub -= 1
                rocket.powerchanged = True
                rocket.rocketstarted = True
            # Raketenboost Unten
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and rocket.z_schub>-10:
                rocket.z_schub -= 1
                rocket.powerchanged = True
                rocket.rocketstarted = True
            # Raketenboost Rechts
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and rocket.x_schub<10:
                rocket.x_schub += 1
                rocket.powerchanged = True
                rocket.rocketstarted = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                show_distance = not show_distance
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                move_x, move_y = -sun.x * SCALE, -sun.y * SCALE
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                move_x, move_y = -rocket.r_x[rocket.aktuellerschritt] * SCALE, -rocket.r_z[rocket.aktuellerschritt] * SCALE    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                draw_line = not draw_line
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                mouseX, mouseY = pygame.mouse.get_pos()
                move_x-=(mouse_x-WIDTH/2)/2
                move_y-=(mouse_y-HEIGHT/2)/2
                SCALE *= 0.75
                rocket.update_scale(0.75)
                for planet in planets:
                    planet.update_scale(0.75)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                mouseX, mouseY = pygame.mouse.get_pos()
                move_x-=(mouse_x-WIDTH/2)/2
                move_y-=(mouse_y-HEIGHT/2)/2
                SCALE *= 1.25
                rocket.update_scale(1.25)
                for planet in planets:
                    planet.update_scale(1.25)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                index = min(alleZeitschritte.index(TIMESTEP)+1, len(alleZeitschritte)-1)
                TIMESTEP = alleZeitschritte[index]
                rocket.timestep = TIMESTEP
                rocket.timestepChanged = True
                for planet in planets:
                    planet.timestep = rocket.timestep = TIMESTEP
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                try: 
                    index = max(alleZeitschritte.index(TIMESTEP)-1, 0)
                catch
                TIMESTEP = alleZeitschritte[index]
                rocket.timestep = TIMESTEP
                rocket.timestepChanged = True
                for planet in planets:
                    planet.timestep = rocket.timestep = TIMESTEP

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
        
        ### Rocket           
        for planet in planets:
            if not pause:
                planet.update_position(planets, rocket)
            # Ohne Radius verschwinden die Balken bugs im Screen
            if not (planet.y*SCALE+planet.radius*SCALE < -move_y-HEIGHT/2 or planet.y*SCALE-planet.radius*SCALE > -move_y+HEIGHT/2 or planet.x*SCALE+planet.radius*SCALE < -move_x-WIDTH/2 or planet.x*SCALE-planet.radius*SCALE > -move_x+WIDTH/2):
                if show_distance :
                    planet.draw(WINDOW, 1, move_x, move_y, draw_line,SCALE, WIDTH, HEIGHT)
                else:
                    planet.draw(WINDOW, 0, move_x, move_y, draw_line,SCALE, WIDTH, HEIGHT)
            else: 
                planet.drawlineonly(WINDOW, move_x, move_y, draw_line, SCALE, WIDTH, HEIGHT)
        rocket.draw(WINDOW,move_x,move_y, planets, pause, SCALE, WIDTH, HEIGHT)
        fps_text = FONT_1.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
        WINDOW.blit(fps_text, (15, 15))
        text_surface = FONT_1.render("Press X or ESC to exit", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 45))
        text_surface = FONT_1.render("Press P to turn on/off distance", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 75))
        text_surface = FONT_1.render("Press U to turn on/off drawing orbit lines", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 105))
        text_surface = FONT_1.render("Use mouse or arrow keys to move around", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 135))
        text_surface = FONT_1.render("Press C to center to the Sun or B to Center to the rocket", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 165))
        text_surface = FONT_1.render("Press Space to pause/unpause", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 195))
        text_surface = FONT_1.render("Use scroll-wheel to zoom", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 225))
        text_surface = FONT_1.render("Use I to reduce and O to increase the time step", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 255))
        sun_surface = FONT_1.render("- Sun", True, COLOR_SUN)
        WINDOW.blit(sun_surface, (15, 285))
        mercury_surface = FONT_1.render("- Mercury", True, COLOR_MERCURY)
        WINDOW.blit(mercury_surface, (15, 315))
        venus_surface = FONT_1.render("- Venus", True, COLOR_VENUS)
        WINDOW.blit(venus_surface, (15, 345))
        earth_surface = FONT_1.render("- Earth", True, COLOR_EARTH)
        WINDOW.blit(earth_surface, (15, 375))
        mars_surface = FONT_1.render("- Mars", True, COLOR_MARS)
        WINDOW.blit(mars_surface, (15, 405))
        jupiter_surface = FONT_1.render("- Jupiter", True, COLOR_JUPITER)
        WINDOW.blit(jupiter_surface, (15, 435))
        saturn_surface = FONT_1.render("- Saturn", True, COLOR_SATURN)
        WINDOW.blit(saturn_surface, (15, 465))
        uranus_surface = FONT_1.render("- Uranus", True, COLOR_URANUS)
        WINDOW.blit(uranus_surface, (15, 495))
        neptune_surface = FONT_1.render("- Neptune", True, COLOR_NEPTUNE)
        WINDOW.blit(neptune_surface, (15, 525))

        time_passed += datetime.timedelta(seconds=TIMESTEP)
        text_surface = FONT_1.render(f"Time step: {TIMESTEP}x", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (1500, 15))
        text_actual_time = FONT_1.render(f'Current time: {(now+time_passed).strftime("%d/%m/%Y, %H:%M:%S")}', True, COLOR_WHITE)
        WINDOW.blit(text_actual_time, (1500, 45))
        text_time_passed = FONT_1.render(f'Passed time: {time_passed}', True, COLOR_WHITE)
        WINDOW.blit(text_time_passed, (1500, 75))

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()