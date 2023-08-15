import pygame

from Globals.Constants import WINDOW, WIDTH, HEIGHT
from Views.StartView import get_selected_rocket


def loading_screen():
    show_gui = True
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    # Screen is shown for 2 seconds
    duration = 2000

    space_loading_img = pygame.image.load("Images/Space.jpg").convert_alpha()
    space_loading_img = pygame.transform.scale(space_loading_img, (WIDTH, HEIGHT))

    rocket_loading_img = pygame.image.load(f"Images/Rocket{get_selected_rocket() + 1}.png").convert_alpha()
    rocket_loading_img = pygame.transform.scale(rocket_loading_img, (WIDTH * 0.25, HEIGHT * 0.5))
    rocket_loading_img = pygame.transform.rotate(rocket_loading_img, 300)
    title_font = pygame.font.SysFont("Trebuchet MS", 56, True)
    title_text = title_font.render("Spaceflight Simulator", True, (0, 150, 150))
    loading_font = pygame.font.SysFont("Display", 72, True)
    loading_text = loading_font.render("Loading...", True, (0, 150, 150))
    while show_gui:

        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time

        WINDOW.fill((0, 0, 0))
        # Space Image
        WINDOW.blit(space_loading_img, (0, 0))
        # Rocket Image
        WINDOW.blit(rocket_loading_img, (WIDTH * 0.325, HEIGHT * 0.3))
        # Fake Loading Bar
        pygame.draw.rect(WINDOW, (128, 128, 128), pygame.Rect(WIDTH * 0.2, HEIGHT * 0.85, WIDTH * 0.6, HEIGHT * 0.075),
                         1)
        pygame.draw.rect(WINDOW, (255, 255, 255),
                         pygame.Rect(WIDTH * 0.2, HEIGHT * 0.85, WIDTH * 0.6 * (min(elapsed_time, duration * 0.95)
                                                                                / duration), HEIGHT * 0.075))
        # Caption
        WINDOW.blit(title_text, (WIDTH * 0.33, HEIGHT * 0.1))
        # Loading Text
        WINDOW.blit(loading_text, (WIDTH * 0.75, HEIGHT * 0.75))

        if elapsed_time >= duration:
            show_gui = False

        pygame.display.update()

        clock.tick(60)
