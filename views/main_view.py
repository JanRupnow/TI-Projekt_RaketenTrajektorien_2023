from variables.konstanten import * 
from methods.game_methods import addClockTime
import numpy as np

def renderTextView(WINDOW, rocket, now, FONT_1, pause, clock, time_passed, timestep):

    fps_text = FONT_1.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
    ### Menü implementieren zur Übersicht der Tasten
    WINDOW.blit(fps_text, (WIDTH*0.03, HEIGHT*0.03))

    time_passed = addClockTime(pause, time_passed, timestep)

    text_surface = FONT_1.render(f"Time step: {timestep}x", True, COLOR_WHITE)
    WINDOW.blit(text_surface, (WIDTH*0.8, HEIGHT*0.03))
    text_actual_time = FONT_1.render(f'Current time: {(now+time_passed).strftime("%d/%m/%Y, %H:%M:%S")}', True, COLOR_WHITE)
    WINDOW.blit(text_actual_time, (WIDTH*0.8, HEIGHT*0.06))
    text_time_passed = FONT_1.render(f'Passed time: {time_passed}', True, COLOR_WHITE)
    WINDOW.blit(text_time_passed, (WIDTH*0.8, HEIGHT*0.09))

    distance = np.sqrt( (rocket.r_x[rocket.aktuellerschritt] - rocket.nearestPlanet.r_x[rocket.nearestPlanet.aktuellerschritt])**2 
                        + (rocket.r_z[rocket.aktuellerschritt] - rocket.nearestPlanet.r_z[rocket.nearestPlanet.aktuellerschritt])**2)
    speed = round(rocket.getCurrentRelativeVelocity()) if distance < rocket.nextPlanet.radius*5 else round(rocket.getAbsoluteVelocity())
    rocket_velocity = FONT_1.render(f'Rocket Speed: {speed}km/h', True, COLOR_WHITE)
    WINDOW.blit(rocket_velocity, (WIDTH*0.8, HEIGHT*0.12))
    rocket_fuel = FONT_1.render(f'Rocket Fuel: %', True, COLOR_WHITE)
    WINDOW.blit(rocket_fuel, (WIDTH*0.8, HEIGHT*0.15)) 
    rocket_maxQ = FONT_1.render(f'MaxQ: %', True, COLOR_WHITE)
    WINDOW.blit(rocket_maxQ, (WIDTH*0.8, HEIGHT*0.18))

    thrust_text = FONT_1.render(f'Thrust: {rocket.thrust}m/s^2', True, COLOR_WHITE)
    WINDOW.blit(thrust_text, (WIDTH*0.8, HEIGHT*0.8))
    angle_text = FONT_1.render(f'Angle: {rocket.angle}°', True, COLOR_WHITE)
    WINDOW.blit(angle_text, (WIDTH*0.8, HEIGHT*0.85))

    return time_passed