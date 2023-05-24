from variables.konstanten import *
def static_View():
    pygame.display.set_caption("Solar System Simulation")
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