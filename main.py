import pygame
import math
import numpy as np
from planet import *
from konstanten import *
from rocket import *
from game_functions import *
import datetime
import sys
pygame.init()
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
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
    move_x = 0
    move_y = 0
    draw_line = True
    zoomrocket = False

    # Metric from: https://nssdc.gsfc.nasa.gov/planetary/factsheet/

    sun = Planet(0, 0, 695 * 10 ** 6, COLOR_SUN, 1.98892 * 10 ** 30,"Sonne")
    sun.sun = True

    mercury = Planet(-0.387 * AU, 0, 2439 * 10 ** 3, COLOR_MERCURY, 3.30 * 10 ** 23,"Merkur")
    mercury.v_z[0] = 47.4 * 1000

    venus = Planet(-0.723 * AU, 0, 6052 * 10 ** 3, COLOR_VENUS, 4.8685 * 10 ** 24,"Venus")
    venus.v_z[0] = 35.02 * 1000

    earth = Planet(-1 * AU, 0, 6378 * 10 ** 3, COLOR_EARTH, 5.9722 * 10 ** 24,"Erde")
    earth.v_z[0] = 29.783 * 1000

    mars = Planet(-1.524 * AU, 0, 3394  * 10 ** 3, COLOR_MARS, 6.39 * 10 ** 23,"Mars")
    mars.v_z[0] = 24.077 * 1000

    jupiter = Planet(-5.204 * AU, 0, 71492 * 10 ** 3, COLOR_JUPITER, 1.898 * 10 ** 27,"Jupiter")
    jupiter.v_z[0] = 13.06 * 1000

    saturn = Planet(-9.573 * AU, 0, 60268  * 10 ** 3, COLOR_SATURN, 5.683 * 10 ** 26,"Saturn")
    saturn.v_z[0] = 9.68 * 1000

    uranus = Planet(-19.165 * AU, 0, 25559  * 10 ** 3, COLOR_URANUS, 8.681 * 10 ** 25,"Uranus")
    uranus.v_z[0] = 6.80 * 1000

    neptune = Planet(-30.178 * AU, 0, 24764  * 10 ** 3, COLOR_NEPTUNE, 1.024 * 10 ** 26,"Neptun")
    neptune.v_z[0] = 5.43 * 1000

    moon = Planet(-1*AU-378_000_000,0,1750*10**3,(220,220,220),73*10**21,"Mond")
    moon.v_z[0] = earth.v_z[0]+1.022*1000
    planets = [moon,neptune, uranus, saturn, jupiter, mars,earth, venus, mercury, sun]
    

    rocket = Rocket(45,0,0,10000,earth,2,(255,255,255), sun)
    while run:
        clock.tick(60)
        WINDOW.fill(COLOR_UNIVERSE)
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             (event.key == pygame.K_x or event.key == pygame.K_ESCAPE)):
                run = False
            # Raketenboost erhöhen
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w and rocket.thrust<10 and not pause:
                rocket.thrust += 1
                rocket.powerchanged = True
                rocket.rocketstarted = True
            # Raketenboost Links   
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a and rocket.angle>-45:
                rocket.angle -= 1
                rocket.powerchanged = True
            # Raketenboost verrigern
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s and rocket.thrust>0:
                rocket.thrust -= 1
                rocket.powerchanged = True
            # Raketenboost Rechts
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d and rocket.angle<45:
                rocket.angle += 1
                rocket.powerchanged = True

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                scale = scaleRelative(200)
                rocket.update_scale(200)
                move_x, move_y = automaticZoomOnRocketOnce(rocket, scale, move_x, move_y)
            #Zoom Startorbit
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                scale = scaleRelative(5)
                rocket.update_scale(5)
                move_x, move_y = automaticZoomOnRocketOnce(rocket, scale, move_x, move_y)
            #Zoom Universum
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                scale = scaleRelative(1)
                rocket.update_scale(1)
                move_x, move_y = automaticZoomOnRocketOnce(rocket, scale, move_x, move_y)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                rocket.zoomOnRocket = not rocket.zoomOnRocket
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                show_distance = not show_distance
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                move_x, move_y = centerScreenOnPlanet(sun, scale, move_x, move_y)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                move_x, move_y = automaticZoomOnRocketOnce(rocket, scale, move_x, move_y)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                draw_line = not draw_line
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                mouse_y, mouse_x = pygame.mouse.get_pos()
                move_x, move_y = mousePositionShiftScreen(mouse_x, mouse_y, move_x, move_y)
                scale *= 0.75
                rocket.update_scale(0.75)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                move_x, move_y = mousePositionShiftScreen(mouse_x, mouse_y, move_x, move_y)
                scale *= 1.25
                rocket.update_scale(1.25)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                timestep = shiftTimeStep(True, rocket, planets, timestep)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_i: 
                timestep = shiftTimeStep(False, rocket, planets, timestep)

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
                if not (planet.r_z[planet.aktuellerschritt]*scale+planet.radius*scale < -move_y-HEIGHT/2 
                        or planet.r_z[planet.aktuellerschritt]*scale-planet.radius*scale > -move_y+HEIGHT/2 
                        or planet.r_z[planet.aktuellerschritt]*scale+planet.radius*scale < -move_x-WIDTH/2 
                        or planet.r_x[planet.aktuellerschritt]*scale-planet.radius*scale > -move_x+WIDTH/2):
                    if show_distance :
                        planet.draw(WINDOW, 1, move_x, move_y, draw_line,scale, WIDTH, HEIGHT, pause)
                    else:
                        planet.draw(WINDOW, 0, move_x, move_y, draw_line,scale, WIDTH, HEIGHT, pause)
                else: 
                    planet.drawlineonly(WINDOW, move_x, move_y, draw_line, scale, WIDTH, HEIGHT, pause)

        fps_text = FONT_1.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
        ### Menü implementieren zur Übersicht der Tasten
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
        text_surface = FONT_1.render("Press F to automatically center the rocket", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 285))
        sun_surface = FONT_1.render("- Sun", True, COLOR_SUN)
        WINDOW.blit(sun_surface, (15, 315))
        mercury_surface = FONT_1.render("- Mercury", True, COLOR_MERCURY)
        WINDOW.blit(mercury_surface, (15, 345))
        venus_surface = FONT_1.render("- Venus", True, COLOR_VENUS)
        WINDOW.blit(venus_surface, (15, 375))
        earth_surface = FONT_1.render("- Earth", True, COLOR_EARTH)
        WINDOW.blit(earth_surface, (15, 405))
        mars_surface = FONT_1.render("- Mars", True, COLOR_MARS)
        WINDOW.blit(mars_surface, (15, 435))
        jupiter_surface = FONT_1.render("- Jupiter", True, COLOR_JUPITER)
        WINDOW.blit(jupiter_surface, (15, 465))
        saturn_surface = FONT_1.render("- Saturn", True, COLOR_SATURN)
        WINDOW.blit(saturn_surface, (15, 495))
        uranus_surface = FONT_1.render("- Uranus", True, COLOR_URANUS)
        WINDOW.blit(uranus_surface, (15, 525))
        neptune_surface = FONT_1.render("- Neptune", True, COLOR_NEPTUNE)
        WINDOW.blit(neptune_surface, (15, 555))
        if not pause:
            time_passed += datetime.timedelta(seconds=timestep)
        text_surface = FONT_1.render(f"Time step: {timestep}x", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (1500, 15))
        text_actual_time = FONT_1.render(f'Current time: {(now+time_passed).strftime("%d/%m/%Y, %H:%M:%S")}', True, COLOR_WHITE)
        WINDOW.blit(text_actual_time, (1500, 45))
        text_time_passed = FONT_1.render(f'Passed time: {time_passed}', True, COLOR_WHITE)
        WINDOW.blit(text_time_passed, (1500, 75))
        rocket_velocity = FONT_1.render(f'Rocket Speed: {round(rocket.getAbsoluteVelocity()*3.6/1000)}km/h', True, COLOR_WHITE)
        WINDOW.blit(rocket_velocity, (1500, 105))
        rocket_fuel = FONT_1.render(f'Rocket Fuel: %', True, COLOR_WHITE)
        WINDOW.blit(rocket_fuel, (1500, 135))
        rocket_maxQ = FONT_1.render(f'MaxQ: %', True, COLOR_WHITE)
        WINDOW.blit(rocket_maxQ, (1500, 165))

        thrust_text = FONT_1.render(f'Thrust: {rocket.thrust}m/s^2', True, COLOR_WHITE)
        WINDOW.blit(thrust_text, (1500, 970))
        angle_text = FONT_1.render(f'Angle: {rocket.angle}°', True, COLOR_WHITE)
        WINDOW.blit(angle_text, (1500, 1000))
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()