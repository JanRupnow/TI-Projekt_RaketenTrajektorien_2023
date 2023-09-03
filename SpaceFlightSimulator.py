from ViewController.DrawManager import DrawManager
from ViewController.GameManager import GameManager
from Views.LoadingView import loading_screen
from Views.StartView import *

from Globals.FlightData.FlightDataManager import DATA

from Methods.PackageInstaller import package_installer
from Methods.ConfigurePlanets import configure_planets
from Methods.GameMethods import process_hot_key_events
from Methods.RocketConfig import load_rocket


def main():
    #package_installer()
    #isnt required anymore

    game_manager = GameManager()
    draw_manager = DrawManager()

    show_start_ui()

    planets = configure_planets()
    rocket = load_rocket(planets, draw_manager)

    game_manager.set_rocket_and_planets(rocket, planets)
    draw_manager.set_rocket_and_planets(rocket, planets)

    loading_screen()

    while DATA.run:
        CLOCK.tick(60)
        WINDOW.fill(COLOR_UNIVERSE)

        for event in pygame.event.get():
            event, rocket, planets = process_hot_key_events(event, rocket, planets, draw_manager)

        game_manager.calculate_next_iteration()
        draw_manager.display_iteration()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
