from variables.konstanten import * 
from methods.game_methods import addClockTime

def renderTextView(WINDOW, rocket, now, FONT_1, pause, clock, time_passed, timestep):

    fps_text = FONT_1.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
    ### Menü implementieren zur Übersicht der Tasten
    WINDOW.blit(fps_text, (15, 15))

    time_passed = addClockTime(pause, time_passed, timestep)

    text_surface = FONT_1.render(f"Time step: {timestep}x", True, COLOR_WHITE)
    WINDOW.blit(text_surface, (1500, 15))
    text_actual_time = FONT_1.render(f'Current time: {(now+time_passed).strftime("%d/%m/%Y, %H:%M:%S")}', True, COLOR_WHITE)
    WINDOW.blit(text_actual_time, (1500, 45))
    text_time_passed = FONT_1.render(f'Passed time: {time_passed}', True, COLOR_WHITE)
    WINDOW.blit(text_time_passed, (1500, 75))
    rocket_velocity = FONT_1.render(f'Rocket Speed: {round(rocket.getCurrentRelativeVelocity()*3.6)}km/h', True, COLOR_WHITE)
    WINDOW.blit(rocket_velocity, (1500, 105))
    rocket_fuel = FONT_1.render(f'Rocket Fuel: %', True, COLOR_WHITE)
    WINDOW.blit(rocket_fuel, (1500, 135))
    rocket_maxQ = FONT_1.render(f'MaxQ: %', True, COLOR_WHITE)
    WINDOW.blit(rocket_maxQ, (1500, 165))

    thrust_text = FONT_1.render(f'Thrust: {rocket.thrust}m/s^2', True, COLOR_WHITE)
    WINDOW.blit(thrust_text, (1500, 970))
    angle_text = FONT_1.render(f'Angle: {rocket.angle}°', True, COLOR_WHITE)
    WINDOW.blit(angle_text, (1500, 1000))

    return time_passed