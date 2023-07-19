import numpy as np

from Globals.Constants import * 

from ViewController.Rocket.Rocket import Rocket

from Methods.GameMethods import AddClockTime

def RenderFlightInterface(WINDOW, rocket : Rocket, now, FONT_1, pause, clock, time_passed, timestep, manager):

    fps_text = FONT_1.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
    ### Menü implementieren zur Übersicht der Tasten
    WINDOW.blit(fps_text, (WIDTH*0.03, HEIGHT*0.03))

    time_passed = AddClockTime(pause, time_passed, timestep)
    #angle_slider = pg.elements.UIHorizontalSlider(pygame.Rect((WIDTH*0.8,HEIGHT*0.6),(WIDTH*0.15,HEIGHT*0.05)),start_value = 0,value_range=[-45,45],manager=manager,visible=1,click_increment=1,object_id="angle_slider")                               
    text_surface = FONT_1.render(f"Time step: {int(timestep*60)}x", True, COLOR_WHITE)
    WINDOW.blit(text_surface, (WIDTH*0.8, HEIGHT*0.03))
    text_actual_time = FONT_1.render(f'Current time: {(now+time_passed).strftime("%d/%m/%Y, %H:%M:%S")}', True, COLOR_WHITE)
    WINDOW.blit(text_actual_time, (WIDTH*0.8, HEIGHT*0.06))
    text_time_passed = FONT_1.render(f'Passed time: {time_passed}', True, COLOR_WHITE)
    WINDOW.blit(text_time_passed, (WIDTH*0.8, HEIGHT*0.09))

    distance = np.sqrt( (rocket.r_x[rocket.currentStep] - rocket.nearestPlanet.r_x[rocket.nearestPlanet.currentStep])**2 
                        + (rocket.r_z[rocket.currentStep] - rocket.nearestPlanet.r_z[rocket.nearestPlanet.currentStep])**2)
    speed = round(rocket.GetCurrentRelativeVelocity()) if distance < rocket.nearestPlanet.radius*5 else round(rocket.GetAbsoluteVelocity())
    rocket_velocity = FONT_1.render(f'Rocket Speed: {speed}km/h', True, COLOR_WHITE)
    WINDOW.blit(rocket_velocity, (WIDTH*0.8, HEIGHT*0.12))
    if (not rocket.rocketstarted) or rocket.landed:
        rocket_velocity = FONT_1.render(f'Altitude: {0} km (Rocket has not started)',True, COLOR_WHITE)
    elif rocket.nearestPlanet.distanceToRocket-rocket.nearestPlanet.radius < 3/2* rocket.nearestPlanet.radius:
        rocket_velocity = FONT_1.render(f'Altitude: {round((rocket.nearestPlanet.distanceToRocket-rocket.nearestPlanet.radius)/1000,0)} km', True, COLOR_WHITE)
    else:
        rocket_velocity = FONT_1.render(f'Altitude: not available in space', True, COLOR_WHITE)
    WINDOW.blit(rocket_velocity, (WIDTH*0.8, HEIGHT*0.15))
    rocket_fuel = FONT_1.render(f'Rocket Fuel: %', True, COLOR_WHITE)
    WINDOW.blit(rocket_fuel, (WIDTH*0.8, HEIGHT*0.18)) 
    rocket_maxQ = FONT_1.render(f'MaxQ: %', True, COLOR_WHITE)
    WINDOW.blit(rocket_maxQ, (WIDTH*0.8, HEIGHT*0.21))

    thrust_text = FONT_1.render(f'Thrust: {rocket.thrust}m/s^2', True, COLOR_WHITE)
    WINDOW.blit(thrust_text, (WIDTH*0.8, HEIGHT*0.8))
    angle_text = FONT_1.render(f'Angle: {rocket.angle}°', True, COLOR_WHITE)
    WINDOW.blit(angle_text, (WIDTH*0.8, HEIGHT*0.85))

   # manager.process_events(event)

    return time_passed